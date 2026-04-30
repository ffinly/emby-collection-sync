#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Emby 自动化综合管理工具 (青龙面板专版)
特性：TMDb 榜单自动同步 / 自动抓取榜单简介 / 缺失影片报告 / MoviePilot自动订阅 / 国产影视智能合集聚合 / 豆瓣28大分类 / TMDb原语言海报直入 / 无封面合集自动修复

【功能特性】
1. 榜单同步：自动拉取指定的 TMDb 列表，并在 Emby 创建同名合集。
2. 海报直入：支持策略化抓取海报（榜单第一/库内第一，最新上映/最新入库），注入原生二进制流告别卡死。
3. 查漏补缺：智能比对库内资源，推送缺失影片及 TMDb ID。
4. 自动订阅：支持将缺失的影视一键推送到 MoviePilot 进行自动订阅下载。
5. 国产整理：基于文件路径关键字或 TMDb 产地数据，自动聚合国产影视。
6. 全员收藏：自动将生成的合集加入所有 Emby 用户的“我的收藏”。
7. 封面修复：自动扫描所有无封面的合集，提取其中最早上映的影视海报进行兜底修复。
8. 队列结算：采用异步延时策略，等底层 SQLite 完全落盘后统一结算海报注入，极致性能。

【青龙面板 食用指南】
1. 放置脚本：将本脚本放入青龙面板的 `scripts` 文件夹下。
2. 安装依赖：在青龙面板左侧导航栏 -> 【依赖管理】-> 【Python3】中，添加并安装 `requests` 和 `urllib3`。
3. 消息推送：脚本已原生兼容青龙环境，只需在青龙的【系统设置】->【通知设置】中配好微信/TG/钉钉，即可自动收到精美的整理报告。
4. 定时任务：在青龙【定时任务】新增任务，命令为 `task emby_collection_sync.py`，建议定时规则定为每天执行一次（例：`0 30 8 * * *` 每日8点30分）。
5. 填写配置：请务必在下方的“配置区域”填写好你自己的 Emby 和 TMDB 密钥。国内环境记得开启代理！
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import urllib3
import time
import base64

# 完美兼容青龙面板原生 notify 机制
try:
    from notify import send
except ImportError:
    def send(title, content):
        print(f"\n【模拟通知】标题: {title}\n内容:\n{content}")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 核心配置区域 (使用前请务必修改) =================

# 1. Emby 服务器配置
EMBY_URL = "http://YOUR_EMBY_IP:PORT"  # 替换为你的 Emby 地址，例如 "http://192.168.1.100:8096"
API_KEY = "YOUR_EMBY_API_KEY"          # 替换为你在 Emby 控制台生成的 API 密钥

# 2. TMDb API 配置
TMDB_KEY = "YOUR_TMDB_API_KEY"         # 替换为你的 TMDb API Key (v3)

# 3. MoviePilot 自动订阅配置
MP_ENABLE = False                      # MP 订阅总开关：True 开启，False 关闭
MP_URL = "http://YOUR_MP_IP:PORT"      # 替换为你的 MP 地址，例如 "http://192.168.1.10:3000"
MP_API_TOKEN = "YOUR_MP_API_TOKEN"     # 替换为你的 MP API Token (在 MP 设置 - 基础设置中获取或生成)
# MP 订阅排除列表（分离电影和剧集，防止 TMDb ID 冲突误杀）
MP_EXCLUDE_MOVIE_IDS = []              # 填入不想订阅的电影 TMDb ID
MP_EXCLUDE_SERIES_IDS = []             # 填入不想订阅的剧集 TMDb ID

# 4. 网络代理配置 (国内宿主机直连 TMDb 会超时，需开启代理)
USE_PROXY = False                      # 如果需要走代理，请改为 True
TMDB_PROXY = "http://YOUR_PROXY_IP:PORT" # 替换为你的代理网关，例如 "http://192.168.1.5:6152"
PROXIES = {"http": TMDB_PROXY, "https": TMDB_PROXY} if USE_PROXY else None

# 5. 智能合集关键字配置 
PATH_KEYWORDS = ["国产", "华语", "Chinese"] 
DOMESTIC_KEYWORDS = ["China", "Hong Kong", "Taiwan", "Macao", "中国", "香港", "台湾", "澳门", "CN", "HK", "TW"]
TMDB_DOMESTIC_CODES = ["CN", "HK", "TW"]

# API 请求批处理大小 (默认 50，一般不需要改)
BATCH_SIZE = 50

# 6. 自定义 TMDb 列表同步配置
# mp_subscribe 为该榜单独立订阅策略开关：
#   - True  = 全量订阅（只要库里缺失就发给 MP 订阅）
#   - False = 仅报告不订阅（建议 TV 榜单设为 False，避免狂下几十季剧集）
#   - 整数  = 仅订阅榜单前 N 部（例如填 3，代表只检查榜单前 3 名，缺失则发给 MP）
# notify_missing: 是否在通知中打印具体的缺失片名。设为 False 时，仅在一句话概览中显示缺失数量，防止通知过长。
CUSTOM_LISTS = [
    # === 第一梯队：大众必看与绝对主流（最高频点击，绝对 C 位） ===
    {"name": "IMDb Top 250 Movies", "id": "8647021", "type": "Movie", "mp_subscribe": True, "notify_missing": True},
    {"name": "IMDb Top 250 TV Shows", "id": "8647022", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣电影 Top 250", "id": "8647023", "type": "Movie", "mp_subscribe": True, "notify_missing": True},

    # === 第二梯队：影史权威殿堂（含金量最高，学术与艺术标杆） ===
    {"name": "S&S Directors - Greatest Films", "id": "8649058", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "S&S Critics - Greatest Films", "id": "8649050", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "AFI Top 100 (2007)", "id": "8649041", "type": "Movie", "mp_subscribe": False, "notify_missing": False},

    # === 第三梯队：顶尖电影节与行业风向标（高质量获奖佳作） ===
    {"name": "奥斯卡历届最佳影片", "id": "8648843", "type": "Movie", "mp_subscribe": 1, "notify_missing": True},
    {"name": "戛纳电影节金棕榈奖", "id": "8648844", "type": "Movie", "mp_subscribe": 1, "notify_missing": True},
    {"name": "英国电影学院奖最佳影片", "id": "8648848", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "金球奖最佳剧情片", "id": "8648849", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "金球奖最佳音乐/喜剧片", "id": "8648850", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "独立精神奖最佳长片", "id": "8648851", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "柏林电影节金熊奖", "id": "8648852", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "威尼斯电影节金狮奖", "id": "8648854", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "多伦多电影节人民选择奖", "id": "8648855", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},

    # === 第四梯队：高阶影迷社区（权威与体量之间的完美过渡） ===
    {"name": "Letterboxd's Top 500 Films", "id": "8648802", "type": "Movie", "mp_subscribe": False, "notify_missing": False},

    # === 第五梯队：超大体量考古片库（千部级别，适合日常洗版与核对） ===
    {"name": "TSPDT - 1000 Greatest Films", "id": "8648821", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "1001 Movies You Must See Before You Die", "id": "8649029", "type": "Movie", "mp_subscribe": False, "notify_missing": False},

    # === 第六梯队：实时风向与近期热门（动态变化，适合找新片/新剧） ===
    {"name": "豆瓣 - 一周口碑电影榜", "id": "8648547", "type": "Movie", "mp_subscribe": 3, "notify_missing": True},
    {"name": "豆瓣 - 华语口碑剧集榜", "id": "8648548", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣 - 全球口碑剧集榜", "id": "8648549", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣 - 实时热门电影榜", "id": "8648550", "type": "Movie", "mp_subscribe": 3, "notify_missing": False},
    {"name": "豆瓣 - 实时热门电视榜", "id": "8648551", "type": "Series", "mp_subscribe": False, "notify_missing": False}
]

# 7. 豆瓣 28 大分类列表配置 (独立开关配置)
# 排序规则: 同一分类 -> 近期热门 -> Top 20 -> 高分经典 -> 冷门佳作
DOUBAN_GENRE_LISTS = [
    # 剧情
    {"name": "豆瓣电影 - 剧情 - Top 20", "id": "8647681", "mp_subscribe": False},
    {"name": "豆瓣电影 - 剧情 - 高分经典", "id": "8648565", "mp_subscribe": False},

    # 喜剧
    {"name": "豆瓣电影 - 喜剧 - 近期热门", "id": "8648552", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - Top 20", "id": "8647682", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - 高分经典", "id": "8648566", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - 冷门佳作", "id": "8648595", "mp_subscribe": False},

    # 动作
    {"name": "豆瓣电影 - 动作 - 近期热门", "id": "8648555", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - Top 20", "id": "8647683", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - 高分经典", "id": "8648568", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - 冷门佳作", "id": "8648597", "mp_subscribe": False},

    # 爱情
    {"name": "豆瓣电影 - 爱情 - 近期热门", "id": "8648553", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - Top 20", "id": "8647684", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - 高分经典", "id": "8648567", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - 冷门佳作", "id": "8648596", "mp_subscribe": False},

    # 科幻
    {"name": "豆瓣电影 - 科幻 - 近期热门", "id": "8648556", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - Top 20", "id": "8647685", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - 高分经典", "id": "8648570", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - 冷门佳作", "id": "8648598", "mp_subscribe": False},

    # 动画
    {"name": "豆瓣电影 - 动画 - 近期热门", "id": "8648557", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - Top 20", "id": "8647686", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - 高分经典", "id": "8648571", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - 冷门佳作", "id": "8648599", "mp_subscribe": False},

    # 悬疑
    {"name": "豆瓣电影 - 悬疑 - 近期热门", "id": "8648558", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - Top 20", "id": "8647687", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - 高分经典", "id": "8648572", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - 冷门佳作", "id": "8648600", "mp_subscribe": False},

    # 惊悚
    {"name": "豆瓣电影 - 惊悚 - 近期热门", "id": "8648560", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - Top 20", "id": "8647688", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - 高分经典", "id": "8648574", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - 冷门佳作", "id": "8648602", "mp_subscribe": False},

    # 恐怖
    {"name": "豆瓣电影 - 恐怖 - 近期热门", "id": "8648562", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - Top 20", "id": "8647689", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - 高分经典", "id": "8648581", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - 冷门佳作", "id": "8648607", "mp_subscribe": False},

    # 纪录片
    {"name": "豆瓣电影 - 纪录片 - Top 20", "id": "8647690", "mp_subscribe": False},

    # 短片
    {"name": "豆瓣电影 - 短片 - Top 20", "id": "8647691", "mp_subscribe": False},

    # 情色
    {"name": "豆瓣电影 - 情色 - Top 20", "id": "8647692", "mp_subscribe": False},
    {"name": "豆瓣电影 - 情色 - 高分经典", "id": "8648586", "mp_subscribe": False},
    {"name": "豆瓣电影 - 情色 - 冷门佳作", "id": "8648612", "mp_subscribe": False},

    # 音乐
    {"name": "豆瓣电影 - 音乐 - Top 20", "id": "8647693", "mp_subscribe": False},
    {"name": "豆瓣电影 - 音乐 - 高分经典", "id": "8648578", "mp_subscribe": False},
    {"name": "豆瓣电影 - 音乐 - 冷门佳作", "id": "8648604", "mp_subscribe": False},

    # 歌舞
    {"name": "豆瓣电影 - 歌舞 - Top 20", "id": "8647694", "mp_subscribe": False},
    {"name": "豆瓣电影 - 歌舞 - 高分经典", "id": "8648584", "mp_subscribe": False},
    {"name": "豆瓣电影 - 歌舞 - 冷门佳作", "id": "8648610", "mp_subscribe": False},

    # 家庭
    {"name": "豆瓣电影 - 家庭 - Top 20", "id": "8647695", "mp_subscribe": False},
    {"name": "豆瓣电影 - 家庭 - 高分经典", "id": "8648576", "mp_subscribe": False},

    # 儿童
    {"name": "豆瓣电影 - 儿童 - Top 20", "id": "8647696", "mp_subscribe": False},
    {"name": "豆瓣电影 - 儿童 - 高分经典", "id": "8648577", "mp_subscribe": False},

    # 传记
    {"name": "豆瓣电影 - 传记 - 近期热门", "id": "8648564", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - Top 20", "id": "8647697", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - 高分经典", "id": "8648583", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - 冷门佳作", "id": "8648609", "mp_subscribe": False},

    # 历史
    {"name": "豆瓣电影 - 历史 - Top 20", "id": "8647698", "mp_subscribe": False},
    {"name": "豆瓣电影 - 历史 - 高分经典", "id": "8648579", "mp_subscribe": False},
    {"name": "豆瓣电影 - 历史 - 冷门佳作", "id": "8648605", "mp_subscribe": False},

    # 战争
    {"name": "豆瓣电影 - 战争 - 近期热门", "id": "8648563", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - Top 20", "id": "8647699", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - 高分经典", "id": "8648582", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - 冷门佳作", "id": "8648608", "mp_subscribe": False},

    # 犯罪
    {"name": "豆瓣电影 - 犯罪 - 近期热门", "id": "8648559", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - Top 20", "id": "8647700", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - 高分经典", "id": "8648573", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - 冷门佳作", "id": "8648601", "mp_subscribe": False},

    # 西部
    {"name": "豆瓣电影 - 西部 - Top 20", "id": "8647702", "mp_subscribe": False},
    {"name": "豆瓣电影 - 西部 - 高分经典", "id": "8648588", "mp_subscribe": False},

    # 奇幻
    {"name": "豆瓣电影 - 奇幻 - Top 20", "id": "8647703", "mp_subscribe": False},
    {"name": "豆瓣电影 - 奇幻 - 高分经典", "id": "8648580", "mp_subscribe": False},
    {"name": "豆瓣电影 - 奇幻 - 冷门佳作", "id": "8648606", "mp_subscribe": False},

    # 冒险
    {"name": "豆瓣电影 - 冒险 - 近期热门", "id": "8648561", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - Top 20", "id": "8647704", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - 高分经典", "id": "8648575", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - 冷门佳作", "id": "8648603", "mp_subscribe": False},

    # 灾难
    {"name": "豆瓣电影 - 灾难 - Top 20", "id": "8647705", "mp_subscribe": False},
    {"name": "豆瓣电影 - 灾难 - 高分经典", "id": "8648587", "mp_subscribe": False},
    {"name": "豆瓣电影 - 灾难 - 冷门佳作", "id": "8648613", "mp_subscribe": False},

    # 武侠
    {"name": "豆瓣电影 - 武侠 - Top 20", "id": "8647706", "mp_subscribe": False},
    {"name": "豆瓣电影 - 武侠 - 高分经典", "id": "8648585", "mp_subscribe": False},
    {"name": "豆瓣电影 - 武侠 - 冷门佳作", "id": "8648611", "mp_subscribe": False},

    # 古装
    {"name": "豆瓣电影 - 古装 - Top 20", "id": "8647707", "mp_subscribe": False},
    {"name": "豆瓣电影 - 古装 - 高分经典", "id": "8648593", "mp_subscribe": False},

    # 运动
    {"name": "豆瓣电影 - 运动 - Top 20", "id": "8647708", "mp_subscribe": False},
    {"name": "豆瓣电影 - 运动 - 高分经典", "id": "8648594", "mp_subscribe": False},

    # 黑色电影
    {"name": "豆瓣电影 - 黑色电影 - Top 20", "id": "8647709", "mp_subscribe": False}
]

# 8. 海报封面抓取策略配置
# 【针对作用域：自定义 TMDb 榜单 (CUSTOM_LISTS) & 豆瓣 28 大分类 (DOUBAN_GENRE_LISTS)】
# "list"    = 绝对榜单第一：不管库里有没有，强制抓取 TMDb 榜单第一名的海报作封面
# "library" = 库内第一名：抓取你的 Emby 库中实际拥有的、在榜单中排名最高的那部影视作封面
LIST_POSTER_MODE = "library" 

# 【针对作用域：国产电影 & 国产电视剧 智能聚合合集】
# "premiere" = 最新上映：按官方首映日期(PremiereDate)倒序，取最新的一部作封面
# "added"    = 最新入库：按你本地洗版/下载的时间(DateCreated)倒序，取最新加入的一部作封面
DOMESTIC_POSTER_MODE = "premiere"

# =================================================================

# 初始化带防挂重试机制的会话
session = requests.Session()
retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retry))
session.mount('https://', HTTPAdapter(max_retries=retry))
session.verify = False

# 统一存储运行统计数据
sync_stats = {
    "movies": 0, "series": 0, "favs": 0, "fixed_covers": 0,
    "fixed_cover_names": [],
    "mp_subscribed": 0, "mp_existed": 0, "mp_failed": [], 
    "mp_excluded": 0,
    "poster_failed": [],
    "pending_posters": [], 
    "lists_report": {}
}

def get_emby_users():
    try: return session.get(f"{EMBY_URL}/emby/Users", params={"api_key": API_KEY}).json()
    except: return []

def add_to_all_users_favorites(item_id, item_name):
    users = get_emby_users()
    count = 0
    for user in users:
        uid = user["Id"]
        try:
            check_url = f"{EMBY_URL}/emby/Users/{uid}/Items/{item_id}"
            item_info = session.get(check_url, params={"api_key": API_KEY}).json()
            if not item_info.get("UserData", {}).get("IsFavorite", False):
                session.post(f"{EMBY_URL}/emby/Users/{uid}/FavoriteItems/{item_id}", params={"api_key": API_KEY})
                count += 1
        except: continue
    if count > 0: sync_stats["favs"] += count

def get_emby_items(item_type, fields="ProductionLocations,Path,ProviderIds,PremiereDate,DateCreated"):
    url = f"{EMBY_URL}/emby/Items"
    params = {"api_key": API_KEY, "IncludeItemTypes": item_type, "Recursive": True, "Fields": fields, "Limit": 20000}
    return session.get(url, params=params).json().get("Items", [])

def purge_collection_metadata(col_id):
    """自动清理遗留的锁定"""
    try:
        users = get_emby_users()
        if not users: return
        item_info = session.get(f"{EMBY_URL}/emby/Users/{users[0]['Id']}/Items/{col_id}", params={"api_key": API_KEY}, timeout=10).json()
        if "LockedFields" in item_info and "ProviderIds" in item_info["LockedFields"]:
            item_info["LockedFields"].remove("ProviderIds") 
            session.post(f"{EMBY_URL}/emby/Items/{col_id}", params={"api_key": API_KEY}, json=item_info, timeout=10)
    except Exception: pass

def get_original_poster(tmdb_id, item_type="movie"):
    """获取指定影视的【原语言】竖版海报路径"""
    try:
        # 1. 查出原语言 (original_language)
        detail_url = f"https://api.themoviedb.org/3/{item_type}/{tmdb_id}"
        detail_res = session.get(detail_url, params={"api_key": TMDB_KEY}, proxies=PROXIES, timeout=5).json()
        orig_lang = detail_res.get("original_language", "en")
        
        # 2. 获取所有的海报列表 (不传 language 参数获取全部)
        img_url = f"https://api.themoviedb.org/3/{item_type}/{tmdb_id}/images"
        img_res = session.get(img_url, params={"api_key": TMDB_KEY}, proxies=PROXIES, timeout=5).json()
        posters = img_res.get("posters", [])
        
        # 3. 筛选第一张匹配原语言的海报
        for p in posters:
            if p.get("iso_639_1") == orig_lang:
                return p.get("file_path")
        
        # 4. 兜底逻辑：如果没有严格匹配的，拿评分最高的第一张，或默认的 poster_path
        if posters:
            return posters[0].get("file_path")
        return detail_res.get("poster_path", "")
    except Exception:
        return ""

def upload_poster_to_emby(col_id, poster_path, col_name):
    """
    恢复 Emby 特色的 Base64 上传方式，配合错峰延时与强制刷新解决卡封面问题
    """
    if not poster_path: return False
    
    # 强制获取最高清(original)的图片
    image_url = f"https://image.tmdb.org/t/p/original{poster_path}"
    try:
        img_res = session.get(image_url, proxies=PROXIES, timeout=15)
        if img_res.status_code == 200:
            # 1. 转回 Base64，Emby 底层强制要求 Body 为 Base64 格式
            b64_image = base64.b64encode(img_res.content).decode('utf-8')
            mime_type = img_res.headers.get('Content-Type', 'image/jpeg')
            
            # 强制删除旧的封面，防止 Emby 缓存卡死
            try:
                # 预清理缓存
                session.delete(f"{EMBY_URL}/emby/Items/{col_id}/Images/Primary", params={"api_key": API_KEY}, timeout=5)
                time.sleep(1.0) # 给予底层文件系统 IO 删除时间
            except Exception: pass
            
            url = f"{EMBY_URL}/emby/Items/{col_id}/Images/Primary"
            # Header 声明是图片，Body 传 Base64
            headers = {"Content-Type": mime_type}
            
            res = session.post(
                url, params={"api_key": API_KEY}, data=b64_image, 
                headers=headers, proxies={"http": None, "https": None}, timeout=10
            )
            
            if res.status_code in [200, 204]:
                # 2. 致命一击：强制要求 Emby 抛弃旧缓存，深度刷新前端图片数据
                try:
                    session.post(
                        f"{EMBY_URL}/emby/Items/{col_id}/Refresh", 
                        params={"api_key": API_KEY, "Recursive": False, "ImageRefreshMode": "FullRefresh"}, 
                        timeout=5
                    )
                except Exception: pass
                
                print(f"    🖼️ 已成功为【{col_name}】注入原语言精美海报！")
                return True
            else:
                print(f"    ⚠️ 【{col_name}】海报推送被拒绝，状态码: {res.status_code}")
                return False
                
    except Exception as e:
        print(f"    ⚠️ 海报注入异常: {e}")
    return False

def fix_missing_collection_posters():
    """扫描所有合集，如果没有封面，取合集内最新的影视海报进行修复 (自动排除脚本管理的榜单)"""
    # 动态生成排除列表：包含所有自定义榜单、豆瓣分类以及国产合集
    exclude_names = [lst["name"] for lst in CUSTOM_LISTS] + \
                    [lst["name"] for lst in DOUBAN_GENRE_LISTS] + \
                    ["国产电影", "国产电视剧"]
    
    print("\n" + "="*45 + "\n🖼️ 阶段四：全局无封面合集修复 (自动排除榜单)\n" + "="*45)
    try:
        collections = session.get(f"{EMBY_URL}/emby/Items", params={
            "api_key": API_KEY, "IncludeItemTypes": "BoxSet", "Recursive": True, "Fields": "ImageTags"
        }).json().get("Items", [])

        fixed_count = 0
        for col in collections:
            col_name = col["Name"]
            # 命中排除列表，直接跳过
            if col_name in exclude_names:
                continue
            # 校验是否缺少 Primary 封面
            if "Primary" not in col.get("ImageTags", {}):
                col_id = col["Id"]
                col_name = col["Name"]
                print(f"  [扫描] 发现无封面合集: {col_name}，正在尝试智能修复...")

                # 获取合集内的所有条目，并按首映时间(PremiereDate)升序排列（越早越前）
                items_in_col = session.get(f"{EMBY_URL}/emby/Items", params={
                    "api_key": API_KEY, "ParentId": col_id, "Fields": "PremiereDate,ProviderIds", 
                    "SortBy": "PremiereDate", "SortOrder": "Ascending"
                }).json().get("Items", [])

                if items_in_col:
                    # 找到第一个拥有 TMDb ID 的有效影视
                    for item in items_in_col:
                        tmdb_id = item.get("ProviderIds", {}).get("Tmdb")
                        if tmdb_id:
                            item_type = "movie" if item.get("Type") == "Movie" else "tv"
                            poster_path = get_original_poster(tmdb_id, item_type)
                            if poster_path:
                                sync_stats["pending_posters"].append({"id": col_id, "path": poster_path, "name": col_name})
                                sync_stats["fixed_cover_names"].append(col_name) # <--- 新增这行，记录名字
                                fixed_count += 1
                            break # 无论成功与否，只尝试最老的一部即可跳出
                            
        sync_stats["fixed_covers"] = fixed_count
        if fixed_count > 0:
            print(f"✅ 扫描完毕，发现 {fixed_count} 个无封面合集待修复！")
        else:
            print("✅ 扫描完毕，未发现需要修复的无封面合集。")
            
    except Exception as e:
        print(f"  [错误] 修复无封面合集时发生异常: {e}")

def update_collection_by_name(name, item_ids, list_desc="", poster_path=""):
    """
    逻辑：先删除同名合集再重新创建，以确保合集在 Emby 中按“添加日期”排序时处于最前。
    """
    if not item_ids:
        print(f"  [跳过] 列表【{name}】无匹配影片，不执行创建。")
        return

    try:
        # 1. 查找现有合集 (修复 500 错误：移除 SearchTerm，改用本地精确匹配，防止 Emby 搜索含特殊字符时服务端崩溃)
        search_res = session.get(f"{EMBY_URL}/emby/Items", params={
            "api_key": API_KEY, 
            "IncludeItemTypes": "BoxSet", 
            "Recursive": True
        }).json()
        
        # 本地精确比对 Name
        existing_col = next((i for i in search_res.get("Items", []) if i["Name"] == name), None)

        # 2. 如果合集已存在，先将其删除
        if existing_col:
            try:
                del_res = session.delete(f"{EMBY_URL}/emby/Items/{existing_col['Id']}", params={"api_key": API_KEY})
                if del_res.status_code in [200, 204]:
                    print(f"    🗑️ 已清理旧合集并准备置顶重排: {name}")
                else:
                    print(f"    ⚠️ 删除旧合集失败 (HTTP {del_res.status_code})，忽略并尝试直接更新...")
            except Exception as e:
                # 即使删除报错也直接无视，继续往下走
                print(f"    ⚠️ 删除请求发生异常，已忽略: {e}")

        # 3. 创建全新合集
        # 先推入第一批数据以创建合集容器
        initial_batch = item_ids[:BATCH_SIZE]
        create_res = session.post(f"{EMBY_URL}/emby/Collections", params={
            "api_key": API_KEY, 
            "Name": name, 
            "Ids": ",".join(initial_batch)
        }).json()
        
        col_id = create_res.get("Id")
        if not col_id:
            print(f"  [错误] 无法获取新创建的合集 ID: {name}")
            return

        print(f"📦 [成功] 已重新生成合集: {name} (共 {len(item_ids)} 部影片)")
        
        # 4. 如果影片总数超过初始批次，循环添加剩余影片
        if len(item_ids) > BATCH_SIZE:
            for i in range(BATCH_SIZE, len(item_ids), BATCH_SIZE):
                session.post(f"{EMBY_URL}/emby/Collections/{col_id}/Items", params={
                    "api_key": API_KEY, 
                    "Ids": ",".join(item_ids[i:i+BATCH_SIZE])
                })
                time.sleep(0.1) # 轻微防抖

        # 5. 元数据与高级功能维护
        if col_id:
            if list_desc:
                try:
                    # 获取该合集的元数据结构
                    users = get_emby_users()
                    if users:
                        uid = users[0]['Id']
                        item_info = session.get(f"{EMBY_URL}/emby/Users/{uid}/Items/{col_id}", params={"api_key": API_KEY}).json()
                        item_info["Overview"] = list_desc
                        # 回传更新后的元数据
                        session.post(f"{EMBY_URL}/emby/Items/{col_id}", params={"api_key": API_KEY}, json=item_info)
                        print(f"    📝 已同步合集简介")
                except Exception as e:
                    print(f"    ⚠️ 合集简介写入失败: {e}")

            # B. 全员收藏功能
            add_to_all_users_favorites(col_id, name)

            # C. 海报注入任务加入队列，推迟统一执行
            if poster_path:
                sync_stats["pending_posters"].append({"id": col_id, "path": poster_path, "name": name})

    except Exception as e:
        print(f"  [错误] 合集置顶重组过程异常 ({name}): {e}")

def fetch_tmdb_list_data(list_id):
    items = []
    description = ""
    page = 1
    while True:
        url = f"https://api.themoviedb.org/3/list/{list_id}"
        params = {"api_key": TMDB_KEY, "language": "zh-CN", "page": page}
        try:
            res = session.get(url, params=params, proxies=PROXIES, timeout=10)
            # 兼容 V4 列表 ID 降级
            if res.status_code == 404:
                url = f"https://api.themoviedb.org/4/list/{list_id}"
                res = session.get(url, params=params, proxies=PROXIES, timeout=10)

            if res.status_code != 200:
                print(f"  [错误] 提取列表失败: {res.status_code} - {res.text}")
                break
                
            data = res.json()
            if page == 1:
                description = data.get("description", "")
                
            page_items = data.get("results") or data.get("items") or []
            if not page_items: break
            
            items.extend(page_items)
            total_pages = data.get("total_pages", 1)
            if page >= total_pages: break
            page += 1
            time.sleep(0.2)
        except Exception as e:
            print(f"  [错误] 提取 TMDb 列表 {list_id} 异常: {e}")
            break
            
    return items, description

def get_existing_mp_subscriptions():
    """获取 MP 目前已有的所有订阅，用于后续防重比对"""
    if not MP_ENABLE: return set()
    base_url = MP_URL.rstrip('/')
    try:
        res = session.get(
            f"{base_url}/api/v1/subscribe/", 
            params={"apikey": MP_API_TOKEN},
            proxies={"http": None, "https": None},
            timeout=10
        )
        if res.status_code == 200:
            data = res.json()
            items = data if isinstance(data, list) else data.get("data", [])
            return set(str(item.get("tmdbid")) for item in items if item.get("tmdbid"))
    except Exception: pass
    return set()

def subscribe_to_moviepilot(name, year, tmdb_id, item_type):
    """推送到 MoviePilot 进行订阅"""
    if not MP_ENABLE: return False, "未启用订阅功能"
    
    # 清理一下结尾可能多写的斜杠，防止拼接出错误路径
    base_url = MP_URL.rstrip('/')
    headers = {"Content-Type": "application/json"}
    # 转换媒体类型给 MP 识别
    mp_type = "电影" if item_type == "Movie" else "电视剧"
    
    payload = {
        "name": name,
        "year": year,
        "type": mp_type,
        "tmdbid": int(tmdb_id)
    }

    # 如果是电视剧，显式指定 season 参数为 0 (代表订阅全季)
    if item_type == "Series":
        payload["season"] = 0
    
    try:
        res = session.post(
            f"{base_url}/api/v1/subscribe/", 
            headers=headers, params={"apikey": MP_API_TOKEN},
            json=payload, proxies={"http": None, "https": None}, timeout=10
        )
        if res.status_code == 200:
            data = res.json()
            if data.get("success") == True or data.get("code") == 0:
                return True, ""
            return False, f"API 业务拒绝 ({data.get('message') or str(data)})"
        return False, f"HTTP 状态码错误 {res.status_code}"
    except requests.exceptions.Timeout: return False, "网络请求超时 (10s)"
    except Exception as e: return False, f"异常: {str(e)[:30]}"

def process_custom_list(list_info, mp_existing_ids, is_genre=False):
    name = list_info["name"]
    list_id = list_info["id"]
    item_type = list_info.get("type", "Movie")
    tmdb_item_type = "movie" if item_type == "Movie" else "tv"
    mp_sub_switch = list_info.get("mp_subscribe", False)
    
    print(f"\n🔍 正在扫描同步 TMDb 列表: {name}")
    tmdb_items, list_desc = fetch_tmdb_list_data(list_id)
    
    if not tmdb_items:
        print("  [警告] 获取到的 TMDb 列表为空！请检查列表 ID 或网络。")
        sync_stats["lists_report"][name] = {"is_genre": is_genre, "total": 0, "matched": 0, "missing": []}
        return

    emby_items = get_emby_items(item_type, "ProviderIds,Name")
    emby_tmdb_map = {}
    for i in emby_items:
        tmdb_val = i.get("ProviderIds", {}).get("Tmdb")
        if tmdb_val: emby_tmdb_map[str(tmdb_val)] = i["Id"]

    # 智能提取海报
    poster_path = ""
    target_tmdb_id = None
    
    if tmdb_items:
        if LIST_POSTER_MODE == "library":
            for item in tmdb_items:
                if str(item.get("id")) in emby_tmdb_map:
                    target_tmdb_id = item.get("id")
                    print(f"    ✨ 策略命中(库内第一) -> {item.get('title') or item.get('name')} 作封面")
                    break
        else:
            target_tmdb_id = tmdb_items[0].get("id")
            
        if target_tmdb_id:
            poster_path = get_original_poster(target_tmdb_id, tmdb_item_type)

    matched_ids = []
    missing_items = []
    
    for idx, item in enumerate(tmdb_items, 1):
        t_id = str(item.get("id"))
        t_title = item.get("title") or item.get("name") or "未知名称"
        t_year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
        display_name = f"{t_title} ({t_year})"
        
        if t_id in emby_tmdb_map:
            matched_ids.append(emby_tmdb_map[t_id])
            print(f"  [{idx:03d}] 🟢 已匹配: {display_name}")
        else:
            missing_info = f"No.{idx} {display_name} {{tmdb-{t_id}}}"
            missing_items.append(missing_info)
            print(f"  [{idx:03d}] ❌ 库内缺失: {missing_info}")
            
            should_subscribe = False
            
            if mp_sub_switch is True:
                should_subscribe = True
            # 注意: Python 中 bool 是 int 的子类，所以必须排除 bool 类型
            elif isinstance(mp_sub_switch, int) and not isinstance(mp_sub_switch, bool):
                # idx 从 1 开始，正好对应榜单排名
                if idx <= mp_sub_switch:
                    should_subscribe = True
                else:
                    print(f"    -> ⏭️ 排名 {idx} 超过设定阈值 ({mp_sub_switch})，仅报告不订阅")
            
            # 动态选择对应的排除列表 ---
            current_exclude_list = MP_EXCLUDE_MOVIE_IDS if item_type == "Movie" else MP_EXCLUDE_SERIES_IDS
            
            # 触发 MoviePilot 自动订阅并防重
            if MP_ENABLE and should_subscribe:
                if t_id in current_exclude_list: # --- 新增: 判断是否在排除列表中 ---
                    print("    -> 🚫 命中排除列表，跳过订阅")
                    sync_stats["mp_excluded"] += 1
                elif t_id in mp_existing_ids:
                    print("    -> 🍿 已存在于 MP，跳过重复订阅")
                    sync_stats["mp_existed"] += 1
                else:
                    success, reason = subscribe_to_moviepilot(t_title, t_year, t_id, item_type)
                    if success:
                        print("    -> 🍿 已成功推送 MP 订阅")
                        sync_stats["mp_subscribed"] += 1
                        mp_existing_ids.add(t_id) # 标记为已订阅，防止单次执行时的跨榜单重复推送
                    else:
                        print(f"    -> ❌ MP 推送失败: {reason}")
                        sync_stats["mp_failed"].append(f"{t_title} (失败原因: {reason})")
            
    if matched_ids:
        unique_ids = list(dict.fromkeys(matched_ids))
        if len(unique_ids) >= 2:
            update_collection_by_name(name, unique_ids, list_desc, poster_path)
        else:
            print(f"  [跳过] 本地匹配资源不足 2 部 ({len(unique_ids)} 部)，暂不创建合集")
        
    # 新增提取 notify_missing 配置，默认为 True
    sync_stats["lists_report"][name] = {
        "is_genre": is_genre, "total": len(tmdb_items), 
        "matched": len(matched_ids), "missing": missing_items,
        "notify_missing": list_info.get("notify_missing", True) 
    }

def process():
    start_time = time.time()
    
    if USE_PROXY: print(f"🌍 全局代理已开启 -> {TMDB_PROXY}")
    
    # 初始化 MoviePilot 订阅比对集合
    mp_existing_ids = set()
    if MP_ENABLE: 
        print(f"🍿 MoviePilot 自动订阅已启用 -> {MP_URL}")
        mp_existing_ids = get_existing_mp_subscriptions()

    # --- 阶段一：同步豆瓣分类榜单 (最先执行，排序在后) ---
    print("\n" + "="*45 + "\n📂 阶段一：同步豆瓣分类榜单\n" + "="*45)
    # 使用 reversed 确保列表第一项比最后一项晚创建，从而排在前面
    for lst in reversed(DOUBAN_GENRE_LISTS): 
        process_custom_list(lst, mp_existing_ids, is_genre=True)

    # --- 阶段二：处理国产影视系列 (中间执行) ---
    print("\n" + "="*45 + "\n🇨🇳 阶段二：处理国产影视系列...\n" + "="*45)
    
    sort_key = "DateCreated" if DOMESTIC_POSTER_MODE == "added" else "PremiereDate"
    
    # 1. 处理国产电视剧
    all_series = get_emby_items("Series")
    dom_series = []
    for s in all_series:
        tmdb_id = s.get("ProviderIds", {}).get("Tmdb")
        if tmdb_id:
            try:
                res = session.get(f"https://api.themoviedb.org/3/tv/{tmdb_id}", params={"api_key": TMDB_KEY}, proxies=PROXIES, timeout=5)
                if any(code in TMDB_DOMESTIC_CODES for code in res.json().get("origin_country", [])):
                    dom_series.append(s)
            except: pass
            
    # 修复隐患：防止 PremiereDate 为 None 导致排序报错
    dom_series.sort(key=lambda x: x.get(sort_key) or "0000-00-00", reverse=True)
    
    dom_series_poster = ""
    # 修复逻辑：遍历查找第一个有 tmdb 且能获取到海报的剧集
    for s in dom_series:
        tmdb_id = s.get("ProviderIds", {}).get("Tmdb")
        if tmdb_id:
            dom_series_poster = get_original_poster(tmdb_id, "tv")
            if dom_series_poster:  # 确保真拿到海报路径了再跳出
                print(f"    ✨ 国产剧集命中 -> {s.get('Name')} 作封面")
                break
            
    update_collection_by_name("国产电视剧", [s["Id"] for s in dom_series], "", dom_series_poster)
    sync_stats["series"] = len(dom_series)

    # 2. 处理国产电影
    all_movies = get_emby_items("Movie")
    dom_movies = [m for m in all_movies if any(pk in m.get("Path", "") for pk in PATH_KEYWORDS) or 
                  any(any(kw.lower() in loc.lower() for kw in DOMESTIC_KEYWORDS) for loc in m.get("ProductionLocations", []))]
                  
    # 修复隐患：防止 PremiereDate 为 None 导致排序报错
    dom_movies.sort(key=lambda x: x.get(sort_key) or "0000-00-00", reverse=True)
    
    dom_movie_poster = ""
    # 修复逻辑：遍历查找第一个有 tmdb 且能获取到海报的电影
    for m in dom_movies:
        tmdb_id = m.get("ProviderIds", {}).get("Tmdb")
        if tmdb_id:
            dom_movie_poster = get_original_poster(tmdb_id, "movie")
            if dom_movie_poster:  # 确保真拿到海报路径了再跳出
                print(f"    ✨ 国产电影命中 -> {m.get('Name')} 作封面")
                break
            
    update_collection_by_name("国产电影", [m["Id"] for m in dom_movies], "", dom_movie_poster)
    sync_stats["movies"] = len(dom_movies)

    # --- 阶段三：同步核心榜单 (最后执行，排序最前) ---
    print("\n" + "="*45 + "\n🎬 阶段三：同步核心榜单\n" + "="*45)
    # 使用 reversed 确保 CUSTOM_LISTS 里的第一个榜单最后被创建，稳居 Emby 首位
    for lst in reversed(CUSTOM_LISTS): 
        process_custom_list(lst, mp_existing_ids, is_genre=False)

    # --- 阶段四：全局扫描修复无封面合集 ---
    fix_missing_collection_posters()

    # --- 阶段五：统一处理海报注入与缓存刷新 ---
    if sync_stats["pending_posters"]:
        print("\n" + "="*45 + "\n🖼️ 阶段五：统一结算海报注入与缓存刷新\n" + "="*45)
        print(f"  ⏳ 正在等待 Emby 后台队列消化其他任务 (延时 5 秒)...")
        time.sleep(5)
        
        for p in sync_stats["pending_posters"]:
            poster_injected = upload_poster_to_emby(p["id"], p["path"], p["name"])
            if not poster_injected:
                sync_stats["poster_failed"].append(p["name"])
            time.sleep(0.5) # 连续请求间的轻微防抖

    # --- 阶段六：生成整理报告与推送 ---
    report = ["📊 Emby 智能合集整理汇总", "━━━━━━━━━━━━━━"]
    genre_matched = 0
    genre_missing_summary = []
    
    for list_name, data in reversed(list(sync_stats["lists_report"].items())):
        if data.get("is_genre"):
            if data["matched"] >= 2: genre_matched += 1
            if data["missing"]:
                # 智能截取名字，防止概览通知过长，比如把 "豆瓣电影 - 剧情 - Top 20" 变成 "剧情"
                short_name = list_name.replace("豆瓣电影 - ", "").replace(" - Top 20", "")
                genre_missing_summary.append(f"{short_name}(缺{len(data['missing'])})")
        else:
            report.append(f"🎬 {list_name}")
            report.append(f"  - 列表总数: {data['total']} | 库内匹配: {data['matched']} | 库内缺失: {len(data['missing'])}")
        
    report.extend([
        f"", f"📂 豆瓣分类同步: 达标生成 {genre_matched} 个合集", f"🇨🇳 国产影视整理",
        f"  - 国产电影: {sync_stats['movies']} 部", f"  - 国产剧集: {sync_stats['series']} 部", f""
    ])
    
    # 动态分析 MP 订阅状态并组装智能话术
    if MP_ENABLE:
        sub, ext, fails = sync_stats['mp_subscribed'], sync_stats['mp_existed'], sync_stats['mp_failed']
        excl = sync_stats['mp_excluded']
        if sub == 0 and ext > 0 and len(fails) == 0: report.append(f"🍿 MP 订阅状态: 之前已全部添加 (已存在 {ext} 部, 排除 {excl} 部)")
        elif len(fails) == 0: report.append(f"🍿 MP 订阅状态: 成功新增 {sub} 部 (跳过已有 {ext} 部, 排除 {excl} 部)")
        else: report.append(f"🍿 MP 订阅状态: 新增 {sub} 部，跳过已有 {ext} 部，排除 {excl} 部，失败 {len(fails)} 部")
    else: report.append("🍿 MoviePilot 自动订阅未开启")

    # 计算当前脚本专属榜单的海报注入数量（总数 - 现成合集修复数）
    list_poster_count = len(sync_stats['pending_posters']) - sync_stats['fixed_covers']
    
    report.extend([
        f"⭐ 同步全员收藏人次: {sync_stats['favs']}",
        f"🖼️ 榜单合集海报注入: {list_poster_count} 个",
        f"🛠️ 本地无封面合集修复: {sync_stats['fixed_covers']} 个",
        f"⏱️ 任务总耗时: {int(time.time() - start_time)} 秒", "━━━━━━━━━━━━━━"
    ])
    
    custom_missing_summary = [] # 用于收集被折叠的主榜单概览
    
    for list_name, data in reversed(list(sync_stats["lists_report"].items())):
        if not data.get("is_genre") and data["missing"]:
            if data.get("notify_missing", True):
                # 开启了详细通知的榜单，展示前3个缺失影片
                report.append(f"\n📝 【{list_name}】缺失清单:")
                for m in data["missing"][:3]: report.append(f"  • {m}")
                if len(data["missing"]) > 3: report.append(f"  • ... 等共 {len(data['missing'])} 部")
            else:
                # 关闭详细通知的榜单，提取精简名字加入折叠概览
                short_name = list_name.replace("豆瓣 - ", "").replace("电影节", "").replace("最佳", "")
                custom_missing_summary.append(f"{short_name}(缺{len(data['missing'])})")

    # 1. 输出被折叠的主榜单概览
    if custom_missing_summary:
        report.append(f"\n📝 【其他榜单缺失概览】:\n" + " | ".join(custom_missing_summary))

    # 2. 恢复并输出豆瓣28大分类的精简概览模式
    #if genre_missing_summary: 
    #    report.append(f"\n📝 【豆瓣分类缺失概览】:\n" + " | ".join(genre_missing_summary))
    
    # 追加 MP 订阅失败清单
    if sync_stats['mp_failed']:
        report.append("\n⚠️ 【MP 订阅失败清单】:")
        for f in sync_stats['mp_failed'][:3]: report.append(f"  • {f}")
        if len(sync_stats['mp_failed']) > 3: report.append(f"  • ... 等共 {len(sync_stats['mp_failed'])} 部")

    # 追加海报注入失败清单
    if sync_stats["poster_failed"]:
        report.append("\n🖼️⚠️ 【海报注入失败清单】:")
        for f in sync_stats["poster_failed"]: 
            report.append(f"  • {f}")

    # 追加无封面合集修复清单
    if sync_stats["fixed_cover_names"]:
        report.append("\n🛠️ 【无封面合集修复清单】:")
        for f in sync_stats["fixed_cover_names"]:
            report.append(f"  • {f}")

    # 通过青龙原生通知渠道发送报告
    send("Emby 智能合集整理报告", "\n".join(report))

if __name__ == "__main__":
    process()
