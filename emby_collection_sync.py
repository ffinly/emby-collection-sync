#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Emby 合集同步：每日重建置顶、缺失报告、MoviePilot 订阅和封面修复。
单文件运行；常用参数在最前面，连接默认读取环境变量。使用说明见 README.md。
Emby 合集同步：每日重建置頂、缺失報告、MoviePilot 訂閱和封面修復。
單檔執行；常用參數在最前面，連線預設讀取環境變數。使用說明見 README.zh-TW.md。
Emby collection sync: daily rebuild ordering, missing-title reports, MoviePilot subscriptions, and poster repair.
Single-file deployment; common settings come first and connections read environment variables by default.
See README.en.md. Qinglong / Python 3.9+.
"""

import os

# 常用参数 / 常用參數 / Common settings
# 直接运行本脚本；通常只需调整本区参数与下方榜单策略。
# 直接執行本腳本；通常只需調整本區參數與下方榜單策略。
# Run this script directly; normally only this section and the list policies need editing.
# LANGUAGE 控制日志、通知、内置榜单和国家合集名称。
# LANGUAGE 控制日誌、通知、內建榜單和國家合集名稱。
# LANGUAGE controls logs, notifications, bundled list names, and country collection names.
LANGUAGE = "zh-CN"                # 简体中文 / 繁體中文 / English: zh-CN / zh-TW / en

# 每个代码生成电影与剧集合集；本脚本约定 CN 合并中国大陆、香港、台湾、澳门。
# 每個代碼產生電影與劇集合集；本腳本約定 CN 合併中國大陸、香港、臺灣、澳門。
# Each code creates movie/TV collections; in this script CN groups mainland China, Hong Kong, Taiwan, and Macao.
# CN 的 TMDb 匹配范围 / CN 的 TMDb 比對範圍 / TMDb codes matched by CN: CN, HK, TW, MO
# 不写 CN 则不生成国产合集；[] 关闭所有国家/地区合集，不影响榜单同步。
# 不寫 CN 則不產生國產合集；[] 關閉所有國家/地區合集，不影響榜單同步。
# Omit CN to skip Chinese collections; [] disables all country collections, leaving list sync enabled.
COUNTRY_CODES = ["CN"]                 # 示例 / 範例 / Example: ["CN", "JP", "US"]

FAVORITES_ENABLE = True            # 自动收藏开关 / 自動收藏開關 / Enable automatic favorites
# 例外用户：填写 Emby 用户名，精确匹配、区分大小写；不填写用户 ID。
# 例外使用者：填寫 Emby 使用者名稱，精確比對、區分大小寫；不填寫使用者 ID。
# Excluded users: exact, case-sensitive Emby usernames, not user IDs.
FAVORITES_EXCLUDE_USERS = []        # 示例 / 範例 / Example: ["kids", "guest"]
MP_ENABLE = False                 # 自动订阅开关 / 自動訂閱開關 / Enable MoviePilot subscriptions
USE_PROXY = False                 # TMDb 代理开关 / TMDb 代理開關 / Enable the TMDb proxy

# 连接配置：默认读取同名环境变量；也可把 os.getenv(...) 改为带引号的具体值。
# 連線設定：預設讀取同名環境變數；也可把 os.getenv(...) 改為帶引號的具體值。
# Connections: read matching environment variables by default, or replace os.getenv(...) with a quoted value.
# 示例 / 範例 / Example: MP_URL = "http://192.168.1.10:3000"
# 手动赋值时以该值为准；未改动的项目继续从环境变量读取。
# 手動賦值時以該值為準；未改動的項目繼續從環境變數讀取。
# A literal assignment takes precedence; unchanged settings still read the environment.
EMBY_URL = os.getenv("EMBY_URL")              # Emby 根地址 / 根位址 / Root URL: http://192.168.1.100:8096
# EMBY_URL = "http://192.168.1.100:8096"
EMBY_API_KEY = os.getenv("EMBY_API_KEY")      # Emby API 密钥 / 金鑰 / key
# EMBY_API_KEY = "your-emby-api-key"
TMDB_API_KEY = os.getenv("TMDB_API_KEY")      # TMDb v3 API 密钥 / 金鑰 / key
# TMDB_API_KEY = "your-tmdb-api-key"
MP_URL = os.getenv("MP_URL")                  # MoviePilot 地址 / 位址 / URL: http://192.168.1.10:3000
# MP_URL = "http://192.168.1.10:3000"
MP_API_TOKEN = os.getenv("MP_API_TOKEN")      # MP 开启时必填 / 啟用時必填 / Required when MP is enabled
# MP_API_TOKEN = "your-mp-api-token"
PROXY_URL = os.getenv("PROXY_URL")            # 代理地址 / 代理位址 / Proxy URL: http://192.168.1.5:6152
# PROXY_URL = "http://192.168.1.5:6152"
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")  # 可选 / 可選 / Optional: TMDb v4 Bearer token
# TMDB_ACCESS_TOKEN = "your-tmdb-read-access-token"


# 默认验证 HTTPS 证书；自签证书仅在必要时关闭对应服务的验证，不影响 TMDb。
# 預設驗證 HTTPS 憑證；自簽憑證僅在必要時關閉對應服務的驗證，不影響 TMDb。
# Verify HTTPS by default; disable only for a service needing self-signed certificates. TMDb stays verified.
EMBY_VERIFY_SSL = True
MP_VERIFY_SSL = True

# library：库内榜单第一；list：榜单第一，无论是否在库。
# library：庫內榜單第一；list：榜單第一，無論是否在庫。
# library: highest-ranked local title; list: highest-ranked title, even if not in the library.
LIST_POSTER_MODE = "library"
# 国家合集海报：premiere 按最新上映；added 按最新入库。
# 國家合集海報：premiere 按最新上映；added 按最新入庫。
# Country collection poster: premiere = latest release; added = latest library addition.
DOMESTIC_POSTER_MODE = "premiere"
POSTER_SIZE = "w780"               # 海报尺寸 / 海報尺寸 / Poster size: w780 / original
COUNTRY_CACHE_DAYS = 90            # 产地缓存天数 / 產地快取天數 / Country-cache lifetime in days

# EMBY_SYNC_CACHE 指定国家缓存路径，默认在主脚本旁保存 .emby_country_cache.json。
# EMBY_SYNC_CACHE 指定國家快取路徑，預設在主腳本旁儲存 .emby_country_cache.json。
# EMBY_SYNC_CACHE sets the country-cache path; default: .emby_country_cache.json beside the main script.

# MoviePilot API 类型值，不随界面语言变化 / API 類型值不隨介面語言變化 / Protocol values, independent of UI language
MP_MEDIA_TYPES = {"Movie": "电影", "Series": "电视剧"}

# 订阅排除的 TMDb ID：电影与剧集分开，避免相同数字 ID 互相干扰。
# 訂閱排除的 TMDb ID：電影與劇集分開，避免相同數字 ID 互相干擾。
# Excluded TMDb IDs: keep movie and TV IDs separate because their numeric IDs can overlap.
MP_EXCLUDE_MOVIE_IDS = []           # 电影 / 電影 / Movies
MP_EXCLUDE_SERIES_IDS = []          # 剧集 / 劇集 / TV shows

# CN 分组的 TMDb 产地代码；电影按 production_countries、剧集按 origin_country 匹配。
# CN 分組的 TMDb 產地代碼；電影按 production_countries、劇集按 origin_country 比對。
# TMDb country codes in the CN group; movies use production_countries, TV uses origin_country.
TMDB_DOMESTIC_CODES = ["CN", "HK", "TW", "MO"]
BATCH_SIZE = 50                    # 每批条目数 / 每批項目數 / Items per request batch

# 榜单订阅策略（只有 MP_ENABLE = True 才提交订阅）：
# 榜單訂閱策略（只有 MP_ENABLE = True 才提交訂閱）：
# Per-list subscription policy (actual subscriptions require MP_ENABLE = True):
# mp_subscribe = True：全部缺失项 / 全部缺失項 / All missing titles
# mp_subscribe = False：只报告 / 只報告 / Report only
# mp_subscribe = N：仅订阅榜单前 N 名中的缺失项，N 为正整数；0 等同 False。
# mp_subscribe = N：僅訂閱榜單前 N 名中的缺失項，N 為正整數；0 等同 False。
# mp_subscribe = N: subscribe only to missing titles ranked in the top N; N is positive, and 0 acts like False.
# notify_missing：核心榜单是否显示缺失详情；分类榜单保持精简统计。
# notify_missing：核心榜單是否顯示缺失詳情；分類榜單維持精簡統計。
# notify_missing: show missing-title details for core lists; category lists retain compact totals.


# 梯队名称与对应语言 README 一致；列表靠前的榜单最后重建，按添加日期倒序时排在前面。
# 梯隊名稱與對應語言 README 一致；清單靠前的榜單最後重建，按新增日期倒序時排在前面。
# Tier names match each language’s README; earlier lists are rebuilt last and appear first when sorted by date added descending.
CUSTOM_LISTS = [
    # === 第一梯队：大众必看 ===
    # 第一梯隊：大眾必看
    # Tier 1: Mainstream Essentials
    {"name": "IMDb Top 250 Movies", "id": "8647021", "type": "Movie", "mp_subscribe": True, "notify_missing": True},
    {"name": "IMDb Top 250 TV Shows", "id": "8647022", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣电影 Top 250", "id": "8647023", "type": "Movie", "mp_subscribe": True, "notify_missing": True},

    # === 第二梯队：影史殿堂 ===
    # 第二梯隊：影史殿堂
    # Tier 2: Cinematic Hall of Fame
    {"name": "S&S Directors - Greatest Films", "id": "8649058", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "S&S Critics - Greatest Films", "id": "8649050", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "AFI Top 100 (2007)", "id": "8649041", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "Harvard Film PhD Program", "id": "8714340", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "NYT - 100 Best Movies of the 21st Century (2025)", "id": "8701141", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "NYT - 100 Best TV Shows of the 21st Century (2026)", "id": "8701142", "type": "Series", "mp_subscribe": False, "notify_missing": False},

    # === 第三梯队：全球最具含金量大奖矩阵 ===
    # 第三梯隊：全球最具含金量大獎矩陣
    # Tier 3: Global Prestigious Film Awards
    {"name": "奥斯卡历届最佳影片", "id": "8648843", "type": "Movie", "mp_subscribe": 1, "notify_missing": True},
    {"name": "戛纳电影节金棕榈奖", "id": "8648844", "type": "Movie", "mp_subscribe": 1, "notify_missing": True},
    {"name": "威尼斯电影节金狮奖", "id": "8648854", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "柏林电影节金熊奖", "id": "8648852", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "英国电影学院奖最佳影片", "id": "8648848", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "金球奖最佳剧情片", "id": "8648849", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "金球奖最佳音乐/喜剧片", "id": "8648850", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "多伦多电影节人民选择奖", "id": "8648855", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},
    {"name": "独立精神奖最佳长片", "id": "8648851", "type": "Movie", "mp_subscribe": 1, "notify_missing": False},

    # === 第四梯队：高阶影迷社区与名家策展 ===
    # 第四梯隊：高階影迷社區與名家策展
    # Tier 4: Cinephile Communities & Curations
    {"name": "LB Top 500 Films", "id": "8648802", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Films with the Most Fans", "id": "8649224", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Action Films", "id": "8714314", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Animated Films", "id": "8649225", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Biographical Films", "id": "8714315", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Crime Films", "id": "8714316", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Documentary Films", "id": "8649231", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 100 Film Noir Films", "id": "8714317", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Horror Films", "id": "8714318", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 100 Live-Action Fantasy Films", "id": "8714319", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Musical Films", "id": "8714320", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Mystery Films", "id": "8714322", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Romantic Comedy Films", "id": "8714328", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 Science Fiction Films", "id": "8714330", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 100 Sports Films", "id": "8714333", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 250 War Films", "id": "8714334", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "LB Top 100 Western Films", "id": "8714335", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "Roger Ebert's Great Movies", "id": "8649219", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    
    # === 第五梯队：超大体量洗版底仓 ===
    # 第五梯隊：超大體量洗版底倉
    # Tier 5: Ultimate Collection Targets
    {"name": "TSPDT - 1000 Greatest Films", "id": "8648821", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "1001 Movies You Must See Before You Die", "id": "8649029", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "Criterion Collection", "id": "8649108", "type": "Movie", "mp_subscribe": False, "notify_missing": False},

    # === 第六梯队：现代独立与流行厂牌 ===
    # 第六梯隊：現代獨立與流行廠牌
    # Tier 6: Modern Indie Labels & Studios
    {"name": "Every A24 Film", "id": "8649217", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "Every NEON Film", "id": "8649218", "type": "Movie", "mp_subscribe": False, "notify_missing": False},
    {"name": "Every MUBI Film", "id": "8649220", "type": "Movie", "mp_subscribe": False, "notify_missing": False},

    # === 第七梯队：实时口碑与趋势榜 ===
    # 第七梯隊：實時口碑與趨勢榜
    # Tier 7: Trending & Popular
    {"name": "豆瓣 - 一周口碑电影榜", "id": "8648547", "type": "Movie", "mp_subscribe": 3, "notify_missing": True},
    {"name": "豆瓣 - 华语口碑剧集榜", "id": "8648548", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣 - 全球口碑剧集榜", "id": "8648549", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "豆瓣 - 实时热门电影榜", "id": "8648550", "type": "Movie", "mp_subscribe": 3, "notify_missing": True},
    {"name": "豆瓣 - 实时热门电视榜", "id": "8648551", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "TMDB - 热门电影榜", "id": "8706223", "type": "Movie", "mp_subscribe": False, "notify_missing": True},
    {"name": "TMDB - 热门剧集榜", "id": "8706224", "type": "Series", "mp_subscribe": False, "notify_missing": True},
    {"name": "TMDB - 本周趋势电影榜", "id": "8706225", "type": "Movie", "mp_subscribe": False, "notify_missing": True},
    {"name": "TMDB - 本周趋势剧集榜", "id": "8706226", "type": "Series", "mp_subscribe": False, "notify_missing": True}
]

# 榜单图标按 ID 匹配 / 榜單圖示按 ID 比對 / Match list icons by ID, independent of translated names.
LIST_EMOJIS = {
    "8647021": "🍿", "8647022": "📺", "8647023": "🎞️",
    "8649058": "🏛️", "8649050": "🏛️", "8649041": "⭐",
    "8701141": "📰", "8701142": "📡",
    "8648843": "🏆", "8648844": "🌿", "8648848": "🎭",
    "8648849": "🌐", "8648850": "🥂", "8648851": "🕊️",
    "8648852": "🐻", "8648854": "🦁", "8648855": "🍁",
    "8648802": "🎬", "8649224": "🔥", "8649225": "🎨",
    "8649231": "📽️", "8649219": "📝", "8648821": "🎥",
    "8649029": "📖", "8649108": "💽", "8649217": "✨",
    "8649218": "🔴", "8649220": "🎟️", "8648547": "📈",
    "8648548": "📺", "8648549": "🌍", "8648550": "🔥",
    "8648551": "🔥", "8706223": "📈", "8706224": "📺",
    "8706225": "🔥", "8706226": "🔥",
    "8714314": "💥", "8714315": "📖", "8714316": "🚔",
    "8714317": "🌑", "8714318": "👻", "8714319": "🧙",
    "8714320": "💃", "8714322": "🔍", "8714328": "💕",
    "8714330": "🚀", "8714333": "🏃", "8714334": "⚔️",
    "8714335": "🤠", "8714340": "🎓",
}
# 历史名称映射 / 歷史名稱對照 / Historical collection names to replace
# 格式 / 格式 / Format: {"new_name": ["old_name_1", "old_name_2"]}
OLD_COLLECTION_NAMES = {
    "LB Top 500 Films": ["Letterboxd's Top 500 Films"]
}

# 豆瓣电影 28 大分类多维度榜单
# 豆瓣電影 28 大分類多維度榜單
# Douban 28 Movie Genre Lists
# 分类内按 README 顺序排列，仅保留该分类提供的榜单。
# 分類內按 README 順序排列，僅保留該分類提供的榜單。
# Follow the README order within each category; only available lists are included.
DOUBAN_GENRE_LISTS = [
    # 剧情 / 劇情 / Drama
    {"name": "豆瓣电影 - 剧情 - Top 20", "id": "8647681", "mp_subscribe": False},
    {"name": "豆瓣电影 - 剧情 - 高分经典", "id": "8648565", "mp_subscribe": False},

    # 喜剧 / 喜劇 / Comedy
    {"name": "豆瓣电影 - 喜剧 - 近期热门", "id": "8648552", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - Top 20", "id": "8647682", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - 高分经典", "id": "8648566", "mp_subscribe": False},
    {"name": "豆瓣电影 - 喜剧 - 冷门佳作", "id": "8648595", "mp_subscribe": False},

    # 动作 / 動作 / Action
    {"name": "豆瓣电影 - 动作 - 近期热门", "id": "8648555", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - Top 20", "id": "8647683", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - 高分经典", "id": "8648568", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动作 - 冷门佳作", "id": "8648597", "mp_subscribe": False},

    # 爱情 / 愛情 / Romance
    {"name": "豆瓣电影 - 爱情 - 近期热门", "id": "8648553", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - Top 20", "id": "8647684", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - 高分经典", "id": "8648567", "mp_subscribe": False},
    {"name": "豆瓣电影 - 爱情 - 冷门佳作", "id": "8648596", "mp_subscribe": False},

    # 科幻 / 科幻 / Sci-Fi
    {"name": "豆瓣电影 - 科幻 - 近期热门", "id": "8648556", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - Top 20", "id": "8647685", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - 高分经典", "id": "8648570", "mp_subscribe": False},
    {"name": "豆瓣电影 - 科幻 - 冷门佳作", "id": "8648598", "mp_subscribe": False},

    # 动画 / 動畫 / Animation
    {"name": "豆瓣电影 - 动画 - 近期热门", "id": "8648557", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - Top 20", "id": "8647686", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - 高分经典", "id": "8648571", "mp_subscribe": False},
    {"name": "豆瓣电影 - 动画 - 冷门佳作", "id": "8648599", "mp_subscribe": False},

    # 悬疑 / 懸疑 / Mystery
    {"name": "豆瓣电影 - 悬疑 - 近期热门", "id": "8648558", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - Top 20", "id": "8647687", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - 高分经典", "id": "8648572", "mp_subscribe": False},
    {"name": "豆瓣电影 - 悬疑 - 冷门佳作", "id": "8648600", "mp_subscribe": False},

    # 惊悚 / 驚悚 / Thriller
    {"name": "豆瓣电影 - 惊悚 - 近期热门", "id": "8648560", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - Top 20", "id": "8647688", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - 高分经典", "id": "8648574", "mp_subscribe": False},
    {"name": "豆瓣电影 - 惊悚 - 冷门佳作", "id": "8648602", "mp_subscribe": False},

    # 恐怖 / 恐怖 / Horror
    {"name": "豆瓣电影 - 恐怖 - 近期热门", "id": "8648562", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - Top 20", "id": "8647689", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - 高分经典", "id": "8648581", "mp_subscribe": False},
    {"name": "豆瓣电影 - 恐怖 - 冷门佳作", "id": "8648607", "mp_subscribe": False},

    # 纪录片 / 紀錄片 / Documentary
    {"name": "豆瓣电影 - 纪录片 - Top 20", "id": "8647690", "mp_subscribe": False},

    # 短片 / 短片 / Short Film
    {"name": "豆瓣电影 - 短片 - Top 20", "id": "8647691", "mp_subscribe": False},

    # 情色 / 情色 / Erotica
    {"name": "豆瓣电影 - 情色 - Top 20", "id": "8647692", "mp_subscribe": False},
    {"name": "豆瓣电影 - 情色 - 高分经典", "id": "8648586", "mp_subscribe": False},
    {"name": "豆瓣电影 - 情色 - 冷门佳作", "id": "8648612", "mp_subscribe": False},

    # 音乐 / 音樂 / Music
    {"name": "豆瓣电影 - 音乐 - Top 20", "id": "8647693", "mp_subscribe": False},
    {"name": "豆瓣电影 - 音乐 - 高分经典", "id": "8648578", "mp_subscribe": False},
    {"name": "豆瓣电影 - 音乐 - 冷门佳作", "id": "8648604", "mp_subscribe": False},

    # 歌舞 / 歌舞 / Musical
    {"name": "豆瓣电影 - 歌舞 - Top 20", "id": "8647694", "mp_subscribe": False},
    {"name": "豆瓣电影 - 歌舞 - 高分经典", "id": "8648584", "mp_subscribe": False},
    {"name": "豆瓣电影 - 歌舞 - 冷门佳作", "id": "8648610", "mp_subscribe": False},

    # 家庭 / 家庭 / Family
    {"name": "豆瓣电影 - 家庭 - Top 20", "id": "8647695", "mp_subscribe": False},
    {"name": "豆瓣电影 - 家庭 - 高分经典", "id": "8648576", "mp_subscribe": False},

    # 儿童 / 兒童 / Children
    {"name": "豆瓣电影 - 儿童 - Top 20", "id": "8647696", "mp_subscribe": False},
    {"name": "豆瓣电影 - 儿童 - 高分经典", "id": "8648577", "mp_subscribe": False},

    # 传记 / 傳記 / Biography
    {"name": "豆瓣电影 - 传记 - 近期热门", "id": "8648564", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - Top 20", "id": "8647697", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - 高分经典", "id": "8648583", "mp_subscribe": False},
    {"name": "豆瓣电影 - 传记 - 冷门佳作", "id": "8648609", "mp_subscribe": False},

    # 历史 / 歷史 / History
    {"name": "豆瓣电影 - 历史 - Top 20", "id": "8647698", "mp_subscribe": False},
    {"name": "豆瓣电影 - 历史 - 高分经典", "id": "8648579", "mp_subscribe": False},
    {"name": "豆瓣电影 - 历史 - 冷门佳作", "id": "8648605", "mp_subscribe": False},

    # 战争 / 戰爭 / War
    {"name": "豆瓣电影 - 战争 - 近期热门", "id": "8648563", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - Top 20", "id": "8647699", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - 高分经典", "id": "8648582", "mp_subscribe": False},
    {"name": "豆瓣电影 - 战争 - 冷门佳作", "id": "8648608", "mp_subscribe": False},

    # 犯罪 / 犯罪 / Crime
    {"name": "豆瓣电影 - 犯罪 - 近期热门", "id": "8648559", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - Top 20", "id": "8647700", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - 高分经典", "id": "8648573", "mp_subscribe": False},
    {"name": "豆瓣电影 - 犯罪 - 冷门佳作", "id": "8648601", "mp_subscribe": False},

    # 西部 / 西部 / Western
    {"name": "豆瓣电影 - 西部 - Top 20", "id": "8647702", "mp_subscribe": False},
    {"name": "豆瓣电影 - 西部 - 高分经典", "id": "8648588", "mp_subscribe": False},

    # 奇幻 / 奇幻 / Fantasy
    {"name": "豆瓣电影 - 奇幻 - Top 20", "id": "8647703", "mp_subscribe": False},
    {"name": "豆瓣电影 - 奇幻 - 高分经典", "id": "8648580", "mp_subscribe": False},
    {"name": "豆瓣电影 - 奇幻 - 冷门佳作", "id": "8648606", "mp_subscribe": False},

    # 冒险 / 冒險 / Adventure
    {"name": "豆瓣电影 - 冒险 - 近期热门", "id": "8648561", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - Top 20", "id": "8647704", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - 高分经典", "id": "8648575", "mp_subscribe": False},
    {"name": "豆瓣电影 - 冒险 - 冷门佳作", "id": "8648603", "mp_subscribe": False},

    # 灾难 / 災難 / Disaster
    {"name": "豆瓣电影 - 灾难 - Top 20", "id": "8647705", "mp_subscribe": False},
    {"name": "豆瓣电影 - 灾难 - 高分经典", "id": "8648587", "mp_subscribe": False},
    {"name": "豆瓣电影 - 灾难 - 冷门佳作", "id": "8648613", "mp_subscribe": False},

    # 武侠 / 武俠 / Wuxia
    {"name": "豆瓣电影 - 武侠 - Top 20", "id": "8647706", "mp_subscribe": False},
    {"name": "豆瓣电影 - 武侠 - 高分经典", "id": "8648585", "mp_subscribe": False},
    {"name": "豆瓣电影 - 武侠 - 冷门佳作", "id": "8648611", "mp_subscribe": False},

    # 古装 / 古裝 / Period & Costume
    {"name": "豆瓣电影 - 古装 - Top 20", "id": "8647707", "mp_subscribe": False},
    {"name": "豆瓣电影 - 古装 - 高分经典", "id": "8648593", "mp_subscribe": False},

    # 运动 / 運動 / Sports
    {"name": "豆瓣电影 - 运动 - Top 20", "id": "8647708", "mp_subscribe": False},
    {"name": "豆瓣电影 - 运动 - 高分经典", "id": "8648594", "mp_subscribe": False},

    # 黑色电影 / 黑色電影 / Film Noir
    {"name": "豆瓣电影 - 黑色电影 - Top 20", "id": "8647709", "mp_subscribe": False}
]

# 豆瓣电视剧地区与类型榜单
# 豆瓣電視劇地區與類型榜單
# Douban TV Region & Type Lists
DOUBAN_TV_LISTS = [
    # 大陆剧 / 大陸劇 / Mainland China
    {"name": "豆瓣电视剧 - 大陆剧 - 近期热门", "id": "8702683", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 大陆剧 - 高分经典", "id": "8702684", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 大陆剧 - 冷门佳作", "id": "8702685", "type": "Series", "mp_subscribe": False},

    # 美剧 / 美劇 / US
    {"name": "豆瓣电视剧 - 美剧 - 近期热门", "id": "8702686", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 美剧 - 高分经典", "id": "8702687", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 美剧 - 冷门佳作", "id": "8702688", "type": "Series", "mp_subscribe": False},

    # 英剧 / 英劇 / UK
    {"name": "豆瓣电视剧 - 英剧 - 高分经典", "id": "8702689", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 英剧 - 冷门佳作", "id": "8702690", "type": "Series", "mp_subscribe": False},

    # 日剧 / 日劇 / Japan
    {"name": "豆瓣电视剧 - 日剧 - 近期热门", "id": "8702691", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 日剧 - 高分经典", "id": "8702692", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 日剧 - 冷门佳作", "id": "8702693", "type": "Series", "mp_subscribe": False},

    # 韩剧 / 韓劇 / South Korea
    {"name": "豆瓣电视剧 - 韩剧 - 近期热门", "id": "8702694", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 韩剧 - 高分经典", "id": "8702695", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 韩剧 - 冷门佳作", "id": "8702696", "type": "Series", "mp_subscribe": False},

    # 港剧 / 港劇 / Hong Kong
    {"name": "豆瓣电视剧 - 港剧 - 高分经典", "id": "8702697", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 港剧 - 冷门佳作", "id": "8702698", "type": "Series", "mp_subscribe": False},

    # 台剧 / 臺劇 / Taiwan, China
    {"name": "豆瓣电视剧 - 台剧 - 高分经典", "id": "8702699", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 台剧 - 冷门佳作", "id": "8702700", "type": "Series", "mp_subscribe": False},

    # 泰剧 / 泰劇 / Thailand
    {"name": "豆瓣电视剧 - 泰剧 - 冷门佳作", "id": "8702701", "type": "Series", "mp_subscribe": False},

    # 欧洲剧 / 歐洲劇 / Europe
    {"name": "豆瓣电视剧 - 欧洲剧 - 近期热门", "id": "8702702", "type": "Series", "mp_subscribe": False},
    {"name": "豆瓣电视剧 - 欧洲剧 - 高分经典", "id": "8702703", "type": "Series", "mp_subscribe": False},

    # 动画剧集 / 動畫劇集 / Animation
    {"name": "豆瓣电视剧 - 动画剧集 - 高分经典", "id": "8702704", "type": "Series", "mp_subscribe": False},
]

# 内置榜单译名 / 內建榜單譯名 / Localized names of bundled lists
LIST_NAMES = {'8647021': {'zh-CN': 'IMDb Top 250 Movies', 'zh-TW': 'IMDb Top 250 Movies', 'en': 'IMDb Top 250 Movies'},
 '8647022': {'zh-CN': 'IMDb Top 250 TV Shows', 'zh-TW': 'IMDb Top 250 TV Shows', 'en': 'IMDb Top 250 TV Shows'},
 '8647023': {'zh-CN': '豆瓣电影 Top 250', 'zh-TW': '豆瓣電影 Top 250', 'en': 'Douban Movies Top 250'},
 '8647681': {'zh-CN': '豆瓣电影 - 剧情 - Top 20', 'zh-TW': '豆瓣電影 - 劇情 - Top 20', 'en': 'Douban Movies - Drama - Top 20'},
 '8647682': {'zh-CN': '豆瓣电影 - 喜剧 - Top 20', 'zh-TW': '豆瓣電影 - 喜劇 - Top 20', 'en': 'Douban Movies - Comedy - Top 20'},
 '8647683': {'zh-CN': '豆瓣电影 - 动作 - Top 20', 'zh-TW': '豆瓣電影 - 動作 - Top 20', 'en': 'Douban Movies - Action - Top 20'},
 '8647684': {'zh-CN': '豆瓣电影 - 爱情 - Top 20', 'zh-TW': '豆瓣電影 - 愛情 - Top 20', 'en': 'Douban Movies - Romance - Top 20'},
 '8647685': {'zh-CN': '豆瓣电影 - 科幻 - Top 20', 'zh-TW': '豆瓣電影 - 科幻 - Top 20', 'en': 'Douban Movies - Sci-Fi - Top 20'},
 '8647686': {'zh-CN': '豆瓣电影 - 动画 - Top 20', 'zh-TW': '豆瓣電影 - 動畫 - Top 20', 'en': 'Douban Movies - Animation - Top 20'},
 '8647687': {'zh-CN': '豆瓣电影 - 悬疑 - Top 20', 'zh-TW': '豆瓣電影 - 懸疑 - Top 20', 'en': 'Douban Movies - Mystery - Top 20'},
 '8647688': {'zh-CN': '豆瓣电影 - 惊悚 - Top 20', 'zh-TW': '豆瓣電影 - 驚悚 - Top 20', 'en': 'Douban Movies - Thriller - Top 20'},
 '8647689': {'zh-CN': '豆瓣电影 - 恐怖 - Top 20', 'zh-TW': '豆瓣電影 - 恐怖 - Top 20', 'en': 'Douban Movies - Horror - Top 20'},
 '8647690': {'zh-CN': '豆瓣电影 - 纪录片 - Top 20',
             'zh-TW': '豆瓣電影 - 紀錄片 - Top 20',
             'en': 'Douban Movies - Documentary - Top 20'},
 '8647691': {'zh-CN': '豆瓣电影 - 短片 - Top 20', 'zh-TW': '豆瓣電影 - 短片 - Top 20', 'en': 'Douban Movies - Short Film - Top 20'},
 '8647692': {'zh-CN': '豆瓣电影 - 情色 - Top 20', 'zh-TW': '豆瓣電影 - 情色 - Top 20', 'en': 'Douban Movies - Erotica - Top 20'},
 '8647693': {'zh-CN': '豆瓣电影 - 音乐 - Top 20', 'zh-TW': '豆瓣電影 - 音樂 - Top 20', 'en': 'Douban Movies - Music - Top 20'},
 '8647694': {'zh-CN': '豆瓣电影 - 歌舞 - Top 20', 'zh-TW': '豆瓣電影 - 歌舞 - Top 20', 'en': 'Douban Movies - Musical - Top 20'},
 '8647695': {'zh-CN': '豆瓣电影 - 家庭 - Top 20', 'zh-TW': '豆瓣電影 - 家庭 - Top 20', 'en': 'Douban Movies - Family - Top 20'},
 '8647696': {'zh-CN': '豆瓣电影 - 儿童 - Top 20', 'zh-TW': '豆瓣電影 - 兒童 - Top 20', 'en': 'Douban Movies - Children - Top 20'},
 '8647697': {'zh-CN': '豆瓣电影 - 传记 - Top 20', 'zh-TW': '豆瓣電影 - 傳記 - Top 20', 'en': 'Douban Movies - Biography - Top 20'},
 '8647698': {'zh-CN': '豆瓣电影 - 历史 - Top 20', 'zh-TW': '豆瓣電影 - 歷史 - Top 20', 'en': 'Douban Movies - History - Top 20'},
 '8647699': {'zh-CN': '豆瓣电影 - 战争 - Top 20', 'zh-TW': '豆瓣電影 - 戰爭 - Top 20', 'en': 'Douban Movies - War - Top 20'},
 '8647700': {'zh-CN': '豆瓣电影 - 犯罪 - Top 20', 'zh-TW': '豆瓣電影 - 犯罪 - Top 20', 'en': 'Douban Movies - Crime - Top 20'},
 '8647702': {'zh-CN': '豆瓣电影 - 西部 - Top 20', 'zh-TW': '豆瓣電影 - 西部 - Top 20', 'en': 'Douban Movies - Western - Top 20'},
 '8647703': {'zh-CN': '豆瓣电影 - 奇幻 - Top 20', 'zh-TW': '豆瓣電影 - 奇幻 - Top 20', 'en': 'Douban Movies - Fantasy - Top 20'},
 '8647704': {'zh-CN': '豆瓣电影 - 冒险 - Top 20', 'zh-TW': '豆瓣電影 - 冒險 - Top 20', 'en': 'Douban Movies - Adventure - Top 20'},
 '8647705': {'zh-CN': '豆瓣电影 - 灾难 - Top 20', 'zh-TW': '豆瓣電影 - 災難 - Top 20', 'en': 'Douban Movies - Disaster - Top 20'},
 '8647706': {'zh-CN': '豆瓣电影 - 武侠 - Top 20', 'zh-TW': '豆瓣電影 - 武俠 - Top 20', 'en': 'Douban Movies - Wuxia - Top 20'},
 '8647707': {'zh-CN': '豆瓣电影 - 古装 - Top 20',
             'zh-TW': '豆瓣電影 - 古裝 - Top 20',
             'en': 'Douban Movies - Period & Costume - Top 20'},
 '8647708': {'zh-CN': '豆瓣电影 - 运动 - Top 20', 'zh-TW': '豆瓣電影 - 運動 - Top 20', 'en': 'Douban Movies - Sports - Top 20'},
 '8647709': {'zh-CN': '豆瓣电影 - 黑色电影 - Top 20',
             'zh-TW': '豆瓣電影 - 黑色電影 - Top 20',
             'en': 'Douban Movies - Film Noir - Top 20'},
 '8648547': {'zh-CN': '豆瓣 - 一周口碑电影榜', 'zh-TW': '豆瓣 - 一週口碑電影榜', 'en': 'Douban - Weekly Highly Rated Movies'},
 '8648548': {'zh-CN': '豆瓣 - 华语口碑剧集榜', 'zh-TW': '豆瓣 - 華語口碑劇集榜', 'en': 'Douban - Highly Rated Chinese Series'},
 '8648549': {'zh-CN': '豆瓣 - 全球口碑剧集榜', 'zh-TW': '豆瓣 - 全球口碑劇集榜', 'en': 'Douban - Highly Rated Global Series'},
 '8648550': {'zh-CN': '豆瓣 - 实时热门电影榜', 'zh-TW': '豆瓣 - 實時熱門電影榜', 'en': 'Douban - Real-time Hot Movies'},
 '8648551': {'zh-CN': '豆瓣 - 实时热门电视榜', 'zh-TW': '豆瓣 - 實時熱門電視榜', 'en': 'Douban - Real-time Hot TV Shows'},
 '8648552': {'zh-CN': '豆瓣电影 - 喜剧 - 近期热门', 'zh-TW': '豆瓣電影 - 喜劇 - 近期熱門', 'en': 'Douban Movies - Comedy - Trending'},
 '8648553': {'zh-CN': '豆瓣电影 - 爱情 - 近期热门', 'zh-TW': '豆瓣電影 - 愛情 - 近期熱門', 'en': 'Douban Movies - Romance - Trending'},
 '8648555': {'zh-CN': '豆瓣电影 - 动作 - 近期热门', 'zh-TW': '豆瓣電影 - 動作 - 近期熱門', 'en': 'Douban Movies - Action - Trending'},
 '8648556': {'zh-CN': '豆瓣电影 - 科幻 - 近期热门', 'zh-TW': '豆瓣電影 - 科幻 - 近期熱門', 'en': 'Douban Movies - Sci-Fi - Trending'},
 '8648557': {'zh-CN': '豆瓣电影 - 动画 - 近期热门', 'zh-TW': '豆瓣電影 - 動畫 - 近期熱門', 'en': 'Douban Movies - Animation - Trending'},
 '8648558': {'zh-CN': '豆瓣电影 - 悬疑 - 近期热门', 'zh-TW': '豆瓣電影 - 懸疑 - 近期熱門', 'en': 'Douban Movies - Mystery - Trending'},
 '8648559': {'zh-CN': '豆瓣电影 - 犯罪 - 近期热门', 'zh-TW': '豆瓣電影 - 犯罪 - 近期熱門', 'en': 'Douban Movies - Crime - Trending'},
 '8648560': {'zh-CN': '豆瓣电影 - 惊悚 - 近期热门', 'zh-TW': '豆瓣電影 - 驚悚 - 近期熱門', 'en': 'Douban Movies - Thriller - Trending'},
 '8648561': {'zh-CN': '豆瓣电影 - 冒险 - 近期热门', 'zh-TW': '豆瓣電影 - 冒險 - 近期熱門', 'en': 'Douban Movies - Adventure - Trending'},
 '8648562': {'zh-CN': '豆瓣电影 - 恐怖 - 近期热门', 'zh-TW': '豆瓣電影 - 恐怖 - 近期熱門', 'en': 'Douban Movies - Horror - Trending'},
 '8648563': {'zh-CN': '豆瓣电影 - 战争 - 近期热门', 'zh-TW': '豆瓣電影 - 戰爭 - 近期熱門', 'en': 'Douban Movies - War - Trending'},
 '8648564': {'zh-CN': '豆瓣电影 - 传记 - 近期热门', 'zh-TW': '豆瓣電影 - 傳記 - 近期熱門', 'en': 'Douban Movies - Biography - Trending'},
 '8648565': {'zh-CN': '豆瓣电影 - 剧情 - 高分经典', 'zh-TW': '豆瓣電影 - 劇情 - 高分經典', 'en': 'Douban Movies - Drama - Classics'},
 '8648566': {'zh-CN': '豆瓣电影 - 喜剧 - 高分经典', 'zh-TW': '豆瓣電影 - 喜劇 - 高分經典', 'en': 'Douban Movies - Comedy - Classics'},
 '8648567': {'zh-CN': '豆瓣电影 - 爱情 - 高分经典', 'zh-TW': '豆瓣電影 - 愛情 - 高分經典', 'en': 'Douban Movies - Romance - Classics'},
 '8648568': {'zh-CN': '豆瓣电影 - 动作 - 高分经典', 'zh-TW': '豆瓣電影 - 動作 - 高分經典', 'en': 'Douban Movies - Action - Classics'},
 '8648570': {'zh-CN': '豆瓣电影 - 科幻 - 高分经典', 'zh-TW': '豆瓣電影 - 科幻 - 高分經典', 'en': 'Douban Movies - Sci-Fi - Classics'},
 '8648571': {'zh-CN': '豆瓣电影 - 动画 - 高分经典', 'zh-TW': '豆瓣電影 - 動畫 - 高分經典', 'en': 'Douban Movies - Animation - Classics'},
 '8648572': {'zh-CN': '豆瓣电影 - 悬疑 - 高分经典', 'zh-TW': '豆瓣電影 - 懸疑 - 高分經典', 'en': 'Douban Movies - Mystery - Classics'},
 '8648573': {'zh-CN': '豆瓣电影 - 犯罪 - 高分经典', 'zh-TW': '豆瓣電影 - 犯罪 - 高分經典', 'en': 'Douban Movies - Crime - Classics'},
 '8648574': {'zh-CN': '豆瓣电影 - 惊悚 - 高分经典', 'zh-TW': '豆瓣電影 - 驚悚 - 高分經典', 'en': 'Douban Movies - Thriller - Classics'},
 '8648575': {'zh-CN': '豆瓣电影 - 冒险 - 高分经典', 'zh-TW': '豆瓣電影 - 冒險 - 高分經典', 'en': 'Douban Movies - Adventure - Classics'},
 '8648576': {'zh-CN': '豆瓣电影 - 家庭 - 高分经典', 'zh-TW': '豆瓣電影 - 家庭 - 高分經典', 'en': 'Douban Movies - Family - Classics'},
 '8648577': {'zh-CN': '豆瓣电影 - 儿童 - 高分经典', 'zh-TW': '豆瓣電影 - 兒童 - 高分經典', 'en': 'Douban Movies - Children - Classics'},
 '8648578': {'zh-CN': '豆瓣电影 - 音乐 - 高分经典', 'zh-TW': '豆瓣電影 - 音樂 - 高分經典', 'en': 'Douban Movies - Music - Classics'},
 '8648579': {'zh-CN': '豆瓣电影 - 历史 - 高分经典', 'zh-TW': '豆瓣電影 - 歷史 - 高分經典', 'en': 'Douban Movies - History - Classics'},
 '8648580': {'zh-CN': '豆瓣电影 - 奇幻 - 高分经典', 'zh-TW': '豆瓣電影 - 奇幻 - 高分經典', 'en': 'Douban Movies - Fantasy - Classics'},
 '8648581': {'zh-CN': '豆瓣电影 - 恐怖 - 高分经典', 'zh-TW': '豆瓣電影 - 恐怖 - 高分經典', 'en': 'Douban Movies - Horror - Classics'},
 '8648582': {'zh-CN': '豆瓣电影 - 战争 - 高分经典', 'zh-TW': '豆瓣電影 - 戰爭 - 高分經典', 'en': 'Douban Movies - War - Classics'},
 '8648583': {'zh-CN': '豆瓣电影 - 传记 - 高分经典', 'zh-TW': '豆瓣電影 - 傳記 - 高分經典', 'en': 'Douban Movies - Biography - Classics'},
 '8648584': {'zh-CN': '豆瓣电影 - 歌舞 - 高分经典', 'zh-TW': '豆瓣電影 - 歌舞 - 高分經典', 'en': 'Douban Movies - Musical - Classics'},
 '8648585': {'zh-CN': '豆瓣电影 - 武侠 - 高分经典', 'zh-TW': '豆瓣電影 - 武俠 - 高分經典', 'en': 'Douban Movies - Wuxia - Classics'},
 '8648586': {'zh-CN': '豆瓣电影 - 情色 - 高分经典', 'zh-TW': '豆瓣電影 - 情色 - 高分經典', 'en': 'Douban Movies - Erotica - Classics'},
 '8648587': {'zh-CN': '豆瓣电影 - 灾难 - 高分经典', 'zh-TW': '豆瓣電影 - 災難 - 高分經典', 'en': 'Douban Movies - Disaster - Classics'},
 '8648588': {'zh-CN': '豆瓣电影 - 西部 - 高分经典', 'zh-TW': '豆瓣電影 - 西部 - 高分經典', 'en': 'Douban Movies - Western - Classics'},
 '8648593': {'zh-CN': '豆瓣电影 - 古装 - 高分经典',
             'zh-TW': '豆瓣電影 - 古裝 - 高分經典',
             'en': 'Douban Movies - Period & Costume - Classics'},
 '8648594': {'zh-CN': '豆瓣电影 - 运动 - 高分经典', 'zh-TW': '豆瓣電影 - 運動 - 高分經典', 'en': 'Douban Movies - Sports - Classics'},
 '8648595': {'zh-CN': '豆瓣电影 - 喜剧 - 冷门佳作', 'zh-TW': '豆瓣電影 - 喜劇 - 冷門佳作', 'en': 'Douban Movies - Comedy - Niche'},
 '8648596': {'zh-CN': '豆瓣电影 - 爱情 - 冷门佳作', 'zh-TW': '豆瓣電影 - 愛情 - 冷門佳作', 'en': 'Douban Movies - Romance - Niche'},
 '8648597': {'zh-CN': '豆瓣电影 - 动作 - 冷门佳作', 'zh-TW': '豆瓣電影 - 動作 - 冷門佳作', 'en': 'Douban Movies - Action - Niche'},
 '8648598': {'zh-CN': '豆瓣电影 - 科幻 - 冷门佳作', 'zh-TW': '豆瓣電影 - 科幻 - 冷門佳作', 'en': 'Douban Movies - Sci-Fi - Niche'},
 '8648599': {'zh-CN': '豆瓣电影 - 动画 - 冷门佳作', 'zh-TW': '豆瓣電影 - 動畫 - 冷門佳作', 'en': 'Douban Movies - Animation - Niche'},
 '8648600': {'zh-CN': '豆瓣电影 - 悬疑 - 冷门佳作', 'zh-TW': '豆瓣電影 - 懸疑 - 冷門佳作', 'en': 'Douban Movies - Mystery - Niche'},
 '8648601': {'zh-CN': '豆瓣电影 - 犯罪 - 冷门佳作', 'zh-TW': '豆瓣電影 - 犯罪 - 冷門佳作', 'en': 'Douban Movies - Crime - Niche'},
 '8648602': {'zh-CN': '豆瓣电影 - 惊悚 - 冷门佳作', 'zh-TW': '豆瓣電影 - 驚悚 - 冷門佳作', 'en': 'Douban Movies - Thriller - Niche'},
 '8648603': {'zh-CN': '豆瓣电影 - 冒险 - 冷门佳作', 'zh-TW': '豆瓣電影 - 冒險 - 冷門佳作', 'en': 'Douban Movies - Adventure - Niche'},
 '8648604': {'zh-CN': '豆瓣电影 - 音乐 - 冷门佳作', 'zh-TW': '豆瓣電影 - 音樂 - 冷門佳作', 'en': 'Douban Movies - Music - Niche'},
 '8648605': {'zh-CN': '豆瓣电影 - 历史 - 冷门佳作', 'zh-TW': '豆瓣電影 - 歷史 - 冷門佳作', 'en': 'Douban Movies - History - Niche'},
 '8648606': {'zh-CN': '豆瓣电影 - 奇幻 - 冷门佳作', 'zh-TW': '豆瓣電影 - 奇幻 - 冷門佳作', 'en': 'Douban Movies - Fantasy - Niche'},
 '8648607': {'zh-CN': '豆瓣电影 - 恐怖 - 冷门佳作', 'zh-TW': '豆瓣電影 - 恐怖 - 冷門佳作', 'en': 'Douban Movies - Horror - Niche'},
 '8648608': {'zh-CN': '豆瓣电影 - 战争 - 冷门佳作', 'zh-TW': '豆瓣電影 - 戰爭 - 冷門佳作', 'en': 'Douban Movies - War - Niche'},
 '8648609': {'zh-CN': '豆瓣电影 - 传记 - 冷门佳作', 'zh-TW': '豆瓣電影 - 傳記 - 冷門佳作', 'en': 'Douban Movies - Biography - Niche'},
 '8648610': {'zh-CN': '豆瓣电影 - 歌舞 - 冷门佳作', 'zh-TW': '豆瓣電影 - 歌舞 - 冷門佳作', 'en': 'Douban Movies - Musical - Niche'},
 '8648611': {'zh-CN': '豆瓣电影 - 武侠 - 冷门佳作', 'zh-TW': '豆瓣電影 - 武俠 - 冷門佳作', 'en': 'Douban Movies - Wuxia - Niche'},
 '8648612': {'zh-CN': '豆瓣电影 - 情色 - 冷门佳作', 'zh-TW': '豆瓣電影 - 情色 - 冷門佳作', 'en': 'Douban Movies - Erotica - Niche'},
 '8648613': {'zh-CN': '豆瓣电影 - 灾难 - 冷门佳作', 'zh-TW': '豆瓣電影 - 災難 - 冷門佳作', 'en': 'Douban Movies - Disaster - Niche'},
 '8648802': {'zh-CN': 'LB Top 500 Films', 'zh-TW': 'LB Top 500 Films', 'en': 'LB Top 500 Films'},
 '8648821': {'zh-CN': 'TSPDT - 1000 Greatest Films',
             'zh-TW': 'TSPDT - 1000 Greatest Films',
             'en': 'TSPDT - 1000 Greatest Films'},
 '8648843': {'zh-CN': '奥斯卡历届最佳影片', 'zh-TW': '奧斯卡歷屆最佳影片', 'en': 'Oscar Winning Films: Best Picture'},
 '8648844': {'zh-CN': '戛纳电影节金棕榈奖', 'zh-TW': '戛納電影節金棕櫚獎', 'en': "Cannes Film Festival Palme d'Or"},
 '8648848': {'zh-CN': '英国电影学院奖最佳影片', 'zh-TW': '英國電影學院獎最佳影片', 'en': 'BAFTA Award for Best Film'},
 '8648849': {'zh-CN': '金球奖最佳剧情片', 'zh-TW': '金球獎最佳劇情片', 'en': 'Golden Globe Best Drama'},
 '8648850': {'zh-CN': '金球奖最佳音乐/喜剧片', 'zh-TW': '金球獎最佳音樂/喜劇片', 'en': 'Golden Globe Best Musical/Comedy'},
 '8648851': {'zh-CN': '独立精神奖最佳长片', 'zh-TW': '獨立精神獎最佳長片', 'en': 'Indie Spirit Award for Best Feature'},
 '8648852': {'zh-CN': '柏林电影节金熊奖', 'zh-TW': '柏林電影節金熊獎', 'en': 'Berlinale Film Festival Golden Bear'},
 '8648854': {'zh-CN': '威尼斯电影节金狮奖', 'zh-TW': '威尼斯電影節金獅獎', 'en': 'Venice Film Festival Golden Lion'},
 '8648855': {'zh-CN': '多伦多电影节人民选择奖', 'zh-TW': '多倫多電影節人民選擇獎', 'en': 'Toronto Film Festival Audience Award'},
 '8649029': {'zh-CN': '1001 Movies You Must See Before You Die',
             'zh-TW': '1001 Movies You Must See Before You Die',
             'en': '1001 Movies You Must See Before You Die'},
 '8649041': {'zh-CN': 'AFI Top 100 (2007)', 'zh-TW': 'AFI Top 100 (2007)', 'en': 'AFI Top 100 (2007)'},
 '8649050': {'zh-CN': 'S&S Critics - Greatest Films',
             'zh-TW': 'S&S Critics - Greatest Films',
             'en': 'S&S Critics - Greatest Films'},
 '8649058': {'zh-CN': 'S&S Directors - Greatest Films',
             'zh-TW': 'S&S Directors - Greatest Films',
             'en': 'S&S Directors - Greatest Films'},
 '8649108': {'zh-CN': 'Criterion Collection', 'zh-TW': 'Criterion Collection', 'en': 'Criterion Collection'},
 '8649217': {'zh-CN': 'Every A24 Film', 'zh-TW': 'Every A24 Film', 'en': 'Every A24 Film'},
 '8649218': {'zh-CN': 'Every NEON Film', 'zh-TW': 'Every NEON Film', 'en': 'Every NEON Film'},
 '8649219': {'zh-CN': "Roger Ebert's Great Movies",
             'zh-TW': "Roger Ebert's Great Movies",
             'en': "Roger Ebert's Great Movies"},
 '8649220': {'zh-CN': 'Every MUBI Film', 'zh-TW': 'Every MUBI Film', 'en': 'Every MUBI Film'},
 '8649224': {'zh-CN': 'LB Top 250 Films with the Most Fans',
             'zh-TW': 'LB Top 250 Films with the Most Fans',
             'en': 'LB Top 250 Films with the Most Fans'},
 '8649225': {'zh-CN': 'LB Top 250 Animated Films',
             'zh-TW': 'LB Top 250 Animated Films',
             'en': 'LB Top 250 Animated Films'},
 '8649231': {'zh-CN': 'LB Top 250 Documentary Films',
             'zh-TW': 'LB Top 250 Documentary Films',
             'en': 'LB Top 250 Documentary Films'},
 '8701141': {'zh-CN': 'NYT - 100 Best Movies of the 21st Century (2025)',
             'zh-TW': 'NYT - 100 Best Movies of the 21st Century (2025)',
             'en': 'NYT - 100 Best Movies of the 21st Century (2025)'},
 '8701142': {'zh-CN': 'NYT - 100 Best TV Shows of the 21st Century (2026)',
             'zh-TW': 'NYT - 100 Best TV Shows of the 21st Century (2026)',
             'en': 'NYT - 100 Best TV Shows of the 21st Century (2026)'},
 '8702683': {'zh-CN': '豆瓣电视剧 - 大陆剧 - 近期热门',
             'zh-TW': '豆瓣電視劇 - 大陸劇 - 近期熱門',
             'en': 'Douban TV - Mainland China - Trending'},
 '8702684': {'zh-CN': '豆瓣电视剧 - 大陆剧 - 高分经典',
             'zh-TW': '豆瓣電視劇 - 大陸劇 - 高分經典',
             'en': 'Douban TV - Mainland China - Classics'},
 '8702685': {'zh-CN': '豆瓣电视剧 - 大陆剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 大陸劇 - 冷門佳作', 'en': 'Douban TV - Mainland China - Niche'},
 '8702686': {'zh-CN': '豆瓣电视剧 - 美剧 - 近期热门', 'zh-TW': '豆瓣電視劇 - 美劇 - 近期熱門', 'en': 'Douban TV - US - Trending'},
 '8702687': {'zh-CN': '豆瓣电视剧 - 美剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 美劇 - 高分經典', 'en': 'Douban TV - US - Classics'},
 '8702688': {'zh-CN': '豆瓣电视剧 - 美剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 美劇 - 冷門佳作', 'en': 'Douban TV - US - Niche'},
 '8702689': {'zh-CN': '豆瓣电视剧 - 英剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 英劇 - 高分經典', 'en': 'Douban TV - UK - Classics'},
 '8702690': {'zh-CN': '豆瓣电视剧 - 英剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 英劇 - 冷門佳作', 'en': 'Douban TV - UK - Niche'},
 '8702691': {'zh-CN': '豆瓣电视剧 - 日剧 - 近期热门', 'zh-TW': '豆瓣電視劇 - 日劇 - 近期熱門', 'en': 'Douban TV - Japan - Trending'},
 '8702692': {'zh-CN': '豆瓣电视剧 - 日剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 日劇 - 高分經典', 'en': 'Douban TV - Japan - Classics'},
 '8702693': {'zh-CN': '豆瓣电视剧 - 日剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 日劇 - 冷門佳作', 'en': 'Douban TV - Japan - Niche'},
 '8702694': {'zh-CN': '豆瓣电视剧 - 韩剧 - 近期热门', 'zh-TW': '豆瓣電視劇 - 韓劇 - 近期熱門', 'en': 'Douban TV - South Korea - Trending'},
 '8702695': {'zh-CN': '豆瓣电视剧 - 韩剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 韓劇 - 高分經典', 'en': 'Douban TV - South Korea - Classics'},
 '8702696': {'zh-CN': '豆瓣电视剧 - 韩剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 韓劇 - 冷門佳作', 'en': 'Douban TV - South Korea - Niche'},
 '8702697': {'zh-CN': '豆瓣电视剧 - 港剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 港劇 - 高分經典', 'en': 'Douban TV - Hong Kong - Classics'},
 '8702698': {'zh-CN': '豆瓣电视剧 - 港剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 港劇 - 冷門佳作', 'en': 'Douban TV - Hong Kong - Niche'},
 '8702699': {'zh-CN': '豆瓣电视剧 - 台剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 臺劇 - 高分經典', 'en': 'Douban TV - Taiwan, China - Classics'},
 '8702700': {'zh-CN': '豆瓣电视剧 - 台剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 臺劇 - 冷門佳作', 'en': 'Douban TV - Taiwan, China - Niche'},
 '8702701': {'zh-CN': '豆瓣电视剧 - 泰剧 - 冷门佳作', 'zh-TW': '豆瓣電視劇 - 泰劇 - 冷門佳作', 'en': 'Douban TV - Thailand - Niche'},
 '8702702': {'zh-CN': '豆瓣电视剧 - 欧洲剧 - 近期热门', 'zh-TW': '豆瓣電視劇 - 歐洲劇 - 近期熱門', 'en': 'Douban TV - Europe - Trending'},
 '8702703': {'zh-CN': '豆瓣电视剧 - 欧洲剧 - 高分经典', 'zh-TW': '豆瓣電視劇 - 歐洲劇 - 高分經典', 'en': 'Douban TV - Europe - Classics'},
 '8702704': {'zh-CN': '豆瓣电视剧 - 动画剧集 - 高分经典', 'zh-TW': '豆瓣電視劇 - 動畫劇集 - 高分經典', 'en': 'Douban TV - Animation - Classics'},
 '8706223': {'zh-CN': 'TMDB - 热门电影榜', 'zh-TW': 'TMDB - 熱門電影榜', 'en': 'TMDB - Popular Movies'},
 '8706224': {'zh-CN': 'TMDB - 热门剧集榜', 'zh-TW': 'TMDB - 熱門劇集榜', 'en': 'TMDB - Popular TV Shows'},
 '8706225': {'zh-CN': 'TMDB - 本周趋势电影榜', 'zh-TW': 'TMDB - 本週趨勢電影榜', 'en': 'TMDB - Trending Movies This Week'},
 '8706226': {'zh-CN': 'TMDB - 本周趋势剧集榜', 'zh-TW': 'TMDB - 本週趨勢劇集榜', 'en': 'TMDB - Trending TV Shows This Week'},
 '8714314': {'zh-CN': 'LB Top 250 Action Films', 'zh-TW': 'LB Top 250 Action Films', 'en': 'LB Top 250 Action Films'},
 '8714315': {'zh-CN': 'LB Top 250 Biographical Films',
             'zh-TW': 'LB Top 250 Biographical Films',
             'en': 'LB Top 250 Biographical Films'},
 '8714316': {'zh-CN': 'LB Top 250 Crime Films', 'zh-TW': 'LB Top 250 Crime Films', 'en': 'LB Top 250 Crime Films'},
 '8714317': {'zh-CN': 'LB Top 100 Film Noir Films',
             'zh-TW': 'LB Top 100 Film Noir Films',
             'en': 'LB Top 100 Film Noir Films'},
 '8714318': {'zh-CN': 'LB Top 250 Horror Films', 'zh-TW': 'LB Top 250 Horror Films', 'en': 'LB Top 250 Horror Films'},
 '8714319': {'zh-CN': 'LB Top 100 Live-Action Fantasy Films',
             'zh-TW': 'LB Top 100 Live-Action Fantasy Films',
             'en': 'LB Top 100 Live-Action Fantasy Films'},
 '8714320': {'zh-CN': 'LB Top 250 Musical Films',
             'zh-TW': 'LB Top 250 Musical Films',
             'en': 'LB Top 250 Musical Films'},
 '8714322': {'zh-CN': 'LB Top 250 Mystery Films',
             'zh-TW': 'LB Top 250 Mystery Films',
             'en': 'LB Top 250 Mystery Films'},
 '8714328': {'zh-CN': 'LB Top 250 Romantic Comedy Films',
             'zh-TW': 'LB Top 250 Romantic Comedy Films',
             'en': 'LB Top 250 Romantic Comedy Films'},
 '8714330': {'zh-CN': 'LB Top 250 Science Fiction Films',
             'zh-TW': 'LB Top 250 Science Fiction Films',
             'en': 'LB Top 250 Science Fiction Films'},
 '8714333': {'zh-CN': 'LB Top 100 Sports Films', 'zh-TW': 'LB Top 100 Sports Films', 'en': 'LB Top 100 Sports Films'},
 '8714334': {'zh-CN': 'LB Top 250 War Films', 'zh-TW': 'LB Top 250 War Films', 'en': 'LB Top 250 War Films'},
 '8714335': {'zh-CN': 'LB Top 100 Western Films',
             'zh-TW': 'LB Top 100 Western Films',
             'en': 'LB Top 100 Western Films'},
 '8714340': {'zh-CN': 'Harvard Film PhD Program',
             'zh-TW': 'Harvard Film PhD Program',
             'en': 'Harvard Film PhD Program'}}

# 多语言文案：以英文为键，按 zh-CN / zh-TW / en 保存译文；保持 {占位符} 一致。
# 多語言文案：以英文為鍵，按 zh-CN / zh-TW / en 保存譯文；保持 {佔位符} 一致。
# Messages: English keys map to zh-CN / zh-TW / en translations; preserve placeholders.
MESSAGES = {'\n[Notification preview] Title: {v0}\nContent:\n{v1}': {'zh-CN': '\n【模拟通知】标题: {v0}\n内容:\n{v1}',
                                                          'zh-TW': '\n【模擬通知】標題: {v0}\n內容:\n{v1}',
                                                          'en': '\n[Notification preview] Title: {v0}\nContent:\n{v1}'},
 'Missing required connection settings: {names}': {'zh-CN': '缺少必填连接配置：{names}',
                                                   'zh-TW': '缺少必填連線設定：{names}',
                                                   'en': 'Missing required connection settings: {names}'},
 'Invalid URL: {name}': {'zh-CN': '地址格式无效：{name}', 'zh-TW': '地址格式無效：{name}', 'en': 'Invalid URL: {name}'},
 'Setting must be a list: {name}': {'zh-CN': '参数必须是列表：{name}', 'zh-TW': '參數必須是列表：{name}', 'en': 'Setting must be a list: {name}'},
 'Use a supported country/region code or name': {'zh-CN': '请使用受支持的国家/地区代码或名称',
                                            'zh-TW': '請使用支援的國家/地區代碼或名稱',
                                            'en': 'Use a supported country/region code or name'},
 'Invalid list configuration: {name}': {'zh-CN': '榜单配置无效：{name}',
                                        'zh-TW': '榜單配置無效：{name}',
                                        'en': 'Invalid list configuration: {name}'},
 'Duplicate list: {name}': {'zh-CN': '重复榜单：{name}', 'zh-TW': '重複榜單：{name}', 'en': 'Duplicate list: {name}'},
 'Invalid Emby user response': {'zh-CN': 'Emby 用户列表格式异常', 'zh-TW': 'Emby 用戶列表格式異常', 'en': 'Invalid Emby user response'},
 'Incomplete Emby library pagination': {'zh-CN': 'Emby 媒体库分页不完整',
                                        'zh-TW': 'Emby 媒體庫分頁不完整',
                                        'en': 'Incomplete Emby library pagination'},
 '    ⏭️ [{v0}] already has a primary image; skipping': {'zh-CN': '    ⏭️ 【{v0}】已有主封面，跳过修复',
                                                         'zh-TW': '    ⏭️ 【{v0}】已有主封面，跳過修復',
                                                         'en': '    ⏭️ [{v0}] already has a primary image; skipping'},
 '    ⚠️ [{v0}] upload accepted, but primary image not yet confirmed': {'zh-CN': '    ⚠️ 【{v0}】上传已接收，但未确认主封面，稍后检查',
                                                                        'zh-TW': '    ⚠️ 【{v0}】上傳已接收，但未確認主封面，稍後檢查',
                                                                        'en': '    ⚠️ [{v0}] upload accepted, but primary image '
                                                                              'not yet confirmed'},
 '    🖼️ Poster uploaded: {v0}': {'zh-CN': '    🖼️ 已上传海报：{v0}', 'zh-TW': '    🖼️ 已上傳海報：{v0}', 'en': '    🖼️ Poster uploaded: {v0}'},
 '    ⚠️ [{v0}] poster upload rejected, status: {v1}': {'zh-CN': '    ⚠️ 【{v0}】海报推送被拒绝，状态码: {v1}',
                                                        'zh-TW': '    ⚠️ 【{v0}】海報推送被拒絕，狀態碼: {v1}',
                                                        'en': '    ⚠️ [{v0}] poster upload rejected, status: {v1}'},
 '    ⚠️ Poster upload error: {v0}': {'zh-CN': '    ⚠️ 海报注入异常: {v0}',
                                      'zh-TW': '    ⚠️ 海報注入異常: {v0}',
                                      'en': '    ⚠️ Poster upload error: {v0}'},
 'Movies': {'zh-CN': '电影', 'zh-TW': '電影', 'en': 'Movies'},
 'TV Shows': {'zh-CN': '剧集', 'zh-TW': '劇集', 'en': 'TV Shows'},
 '  [Scan] {v0} without primary images: {v1}': {'zh-CN': '  [扫描] 无主封面{v0}: {v1} 部',
                                                'zh-TW': '  [掃描] 無主封面{v0}: {v1} 部',
                                                'en': '  [Scan] {v0} without primary images: {v1}'},
 '  [Skip] {v0}: missing TMDb ID': {'zh-CN': '  [跳过] {v0}，缺少 TMDb ID',
                                    'zh-TW': '  [跳過] {v0}，缺少 TMDb ID',
                                    'en': '  [Skip] {v0}: missing TMDb ID'},
 '{v0} (missing TMDb ID)': {'zh-CN': '{v0}（缺少 TMDb ID）', 'zh-TW': '{v0}（缺少 TMDb ID）', 'en': '{v0} (missing TMDb ID)'},
 '  [Skip] {v0}: original-language poster unavailable; check TMDb images or network': {'zh-CN': '  [跳过] {v0}，未获取到原语言海报，请检查 TMDb '
                                                                                                '图片或网络',
                                                                                       'zh-TW': '  [跳過] {v0}，未獲取到原語言海報，請檢查 TMDb '
                                                                                                '圖片或網絡',
                                                                                       'en': '  [Skip] {v0}: original-language '
                                                                                             'poster unavailable; check TMDb '
                                                                                             'images or network'},
 '{v0} (original-language poster unavailable)': {'zh-CN': '{v0}（未获取到原语言海报）',
                                                 'zh-TW': '{v0}（未獲取到原語言海報）',
                                                 'en': '{v0} (original-language poster unavailable)'},
 '  [Pending repair] {v0}': {'zh-CN': '  [待修复] {v0}', 'zh-TW': '  [待修復] {v0}', 'en': '  [Pending repair] {v0}'},
 '\n🖼️ Stage 4: Repair missing collection and media posters (excluding list collections)\n': {'zh-CN': '\n'
                                                                                                       '🖼️ 阶段四：合集与影视无封面修复 '
                                                                                                       '(合集自动排除榜单)\n',
                                                                                              'zh-TW': '\n'
                                                                                                       '🖼️ 階段四：合集與影視無封面修復 '
                                                                                                       '(合集自動排除榜單)\n',
                                                                                              'en': '\n'
                                                                                                    '🖼️ Stage 4: Repair missing '
                                                                                                    'collection and media '
                                                                                                    'posters (excluding list '
                                                                                                    'collections)\n'},
 '  [Scan] Collection without a poster: {v0}; checking...': {'zh-CN': '  [扫描] 发现无封面合集: {v0}，正在尝试智能修复...',
                                                             'zh-TW': '  [掃描] 發現無封面合集: {v0}，正在嘗試智能修復...',
                                                             'en': '  [Scan] Collection without a poster: {v0}; checking...'},
 '✅ Scan complete: {v0} collection posters queued for repair': {'zh-CN': '✅ 扫描完毕，发现 {v0} 个无封面合集待修复！',
                                                                'zh-TW': '✅ 掃描完畢，發現 {v0} 個無封面合集待修復！',
                                                                'en': '✅ Scan complete: {v0} collection posters queued for '
                                                                      'repair'},
 '✅ Scan complete: no collection posters need repair': {'zh-CN': '✅ 扫描完毕，未发现需要修复的无封面合集。',
                                                        'zh-TW': '✅ 掃描完畢，未發現需要修復的無封面合集。',
                                                        'en': '✅ Scan complete: no collection posters need repair'},
 '  [Error] Collection poster repair failed: {v0}': {'zh-CN': '  [错误] 修复无封面合集时发生异常: {v0}',
                                                     'zh-TW': '  [錯誤] 修復無封面合集時發生異常: {v0}',
                                                     'en': '  [Error] Collection poster repair failed: {v0}'},
 '  [Skip] No local matches for [{v0}]; keeping the existing collection': {'zh-CN': '  [跳过] 合集【{v0}】无本地匹配，保留现有合集。', 'zh-TW': '  [跳過] 合集【{v0}】無本機匹配，保留現有合集。', 'en': '  [Skip] No local matches for [{v0}]; keeping the existing collection'},
 'Cannot obtain the newly created collection ID': {'zh-CN': '无法获取新创建的合集 ID',
                                                   'zh-TW': '無法獲取新創建的合集 ID',
                                                   'en': 'Cannot obtain the newly created collection ID'},
 'New collection membership verification failed; keeping the old collection': {'zh-CN': '新合集条目校验失败，保留旧合集',
                                                                               'zh-TW': '新合集條目校驗失敗，保留舊合集',
                                                                               'en': 'New collection membership verification '
                                                                                     'failed; keeping the old collection'},
 'Emby user list is empty; keeping the old collection': {'zh-CN': 'Emby 用户列表为空，保留旧合集',
                                                         'zh-TW': 'Emby 用戶列表爲空，保留舊合集',
                                                         'en': 'Emby user list is empty; keeping the old collection'},
 '📦 [Success] Collection rebuilt: {v0} ({v1} items)': {'zh-CN': '📦 [成功] 已重新生成合集: {v0} (共 {v1} 部)',
                                                       'zh-TW': '📦 [成功] 已重新生成合集: {v0} (共 {v1} 部)',
                                                       'en': '📦 [Success] Collection rebuilt: {v0} ({v1} items)'},
 'Collection rebuild failed: {name} ({error})': {'zh-CN': '合集重建失败：{name}（{error}）',
                                                 'zh-TW': '合集重建失敗：{name}（{error}）',
                                                 'en': 'Collection rebuild failed: {name} ({error})'},
 'Temporary collection cleanup failed: {id} ({error})': {'zh-CN': '临时合集清理失败：{id}（{error}）',
                                                         'zh-TW': '臨時合集清理失敗：{id}（{error}）',
                                                         'en': 'Temporary collection cleanup failed: {id} ({error})'},
 'Incomplete TMDb list pagination: {id}': {'zh-CN': 'TMDb 榜单分页不完整：{id}',
                                           'zh-TW': 'TMDb 榜單分頁不完整：{id}',
                                           'en': 'Incomplete TMDb list pagination: {id}'},
 'Subscriptions disabled': {'zh-CN': '未启用订阅功能', 'zh-TW': '未啓用訂閱功能', 'en': 'Subscriptions disabled'},
 'Season lookup failed (HTTP {v0})': {'zh-CN': '查询季度失败 (HTTP {v0})',
                                      'zh-TW': '查詢季度失敗 (HTTP {v0})',
                                      'en': 'Season lookup failed (HTTP {v0})'},
 'Season lookup failed ({v0})': {'zh-CN': '查询季度失败 ({v0})', 'zh-TW': '查詢季度失敗 ({v0})', 'en': 'Season lookup failed ({v0})'},
 'Invalid season response ({v0})': {'zh-CN': '查询季度返回格式异常 ({v0})',
                                    'zh-TW': '查詢季度返回格式異常 ({v0})',
                                    'en': 'Invalid season response ({v0})'},
 'MP returned no seasons': {'zh-CN': 'MP 未查询到任何季度', 'zh-TW': 'MP 未查詢到任何季度', 'en': 'MP returned no seasons'},
 '      -> Season {v0} already exists in MP; skipping': {'zh-CN': '      -> 第 {v0} 季已存在于 MP，跳过',
                                                         'zh-TW': '      -> 第 {v0} 季已存在於 MP，跳過',
                                                         'en': '      -> Season {v0} already exists in MP; skipping'},
 '      -> Season {v0} subscribed': {'zh-CN': '      -> 第 {v0} 季订阅成功',
                                     'zh-TW': '      -> 第 {v0} 季訂閱成功',
                                     'en': '      -> Season {v0} subscribed'},
 'Season {v0}: {v1}': {'zh-CN': '第{v0}季: {v1}', 'zh-TW': '第{v0}季: {v1}', 'en': 'Season {v0}: {v1}'},
 ' (succeeded: {v0})': {'zh-CN': '（已成功: {v0}）', 'zh-TW': '（已成功: {v0}）', 'en': ' (succeeded: {v0})'},
 'Some season subscriptions failed ({v0})': {'zh-CN': '部分季度订阅失败 ({v0})',
                                             'zh-TW': '部分季度訂閱失敗 ({v0})',
                                             'en': 'Some season subscriptions failed ({v0})'},
 'All seasons already exist': {'zh-CN': '所有季度均已存在', 'zh-TW': '所有季度均已存在', 'en': 'All seasons already exist'},
 'Season lookup/subscription timed out (connect 10s/read 60s)': {'zh-CN': '查询或订阅季度超时 (连接10s/读取60s)',
                                                                 'zh-TW': '查詢或訂閱季度超時 (連接10s/讀取60s)',
                                                                 'en': 'Season lookup/subscription timed out (connect 10s/read '
                                                                       '60s)'},
 'Season subscription error: {v0}': {'zh-CN': '季度订阅异常: {v0}', 'zh-TW': '季度訂閱異常: {v0}', 'en': 'Season subscription error: {v0}'},
 'API rejected the request ({v0})': {'zh-CN': 'API 业务拒绝 ({v0})',
                                     'zh-TW': 'API 業務拒絕 ({v0})',
                                     'en': 'API rejected the request ({v0})'},
 'HTTP status error {v0}': {'zh-CN': 'HTTP 状态码错误 {v0}', 'zh-TW': 'HTTP 狀態碼錯誤 {v0}', 'en': 'HTTP status error {v0}'},
 'Request timed out (connect 10s/read 60s)': {'zh-CN': '网络请求超时 (连接10s/读取60s)',
                                              'zh-TW': '網絡請求超時 (連接10s/讀取60s)',
                                              'en': 'Request timed out (connect 10s/read 60s)'},
 'Error: {v0}': {'zh-CN': '异常: {v0}', 'zh-TW': '異常: {v0}', 'en': 'Error: {v0}'},
 '\n🔍 Synchronizing TMDb list: {v0}': {'zh-CN': '\n🔍 正在扫描同步 TMDb 列表: {v0}',
                                       'zh-TW': '\n🔍 正在掃描同步 TMDb 列表: {v0}',
                                       'en': '\n🔍 Synchronizing TMDb list: {v0}'},
 'List fetch failed; keeping the existing collection: {name} ({error})': {'zh-CN': '榜单获取失败，保留旧合集：{name}（{error}）',
                                                                          'zh-TW': '榜單獲取失敗，保留舊合集：{name}（{error}）',
                                                                          'en': 'List fetch failed; keeping the existing '
                                                                                'collection: {name} ({error})'},
 '  [Warning] Empty TMDb list; check the list ID or network. Existing collection retained.': {'zh-CN': '  [警告] 获取到的 TMDb '
                                                                                                       '列表为空！请检查列表 ID 或网络。',
                                                                                              'zh-TW': '  [警告] 獲取到的 TMDb '
                                                                                                       '列表爲空！請檢查列表 ID 或網絡。',
                                                                                              'en': '  [Warning] Empty TMDb '
                                                                                                    'list; check the list ID or '
                                                                                                    'network. Existing '
                                                                                                    'collection retained.'},
 '    ✨ First local match -> poster from {v0}': {'zh-CN': '    ✨ 策略命中(库内第一) -> {v0} 作封面',
                                                 'zh-TW': '    ✨ 策略命中(庫內第一) -> {v0} 作封面',
                                                 'en': '    ✨ First local match -> poster from {v0}'},
 'Unknown title': {'zh-CN': '未知名称', 'zh-TW': '未知名稱', 'en': 'Unknown title'},
 '  [{v0:03d}] 🟢 Matched: {v1}': {'zh-CN': '  [{v0:03d}] 🟢 已匹配: {v1}',
                                  'zh-TW': '  [{v0:03d}] 🟢 已匹配: {v1}',
                                  'en': '  [{v0:03d}] 🟢 Matched: {v1}'},
 '  [{v0:03d}] ❌ Missing: {v1}': {'zh-CN': '  [{v0:03d}] ❌ 库内缺失: {v1}',
                                  'zh-TW': '  [{v0:03d}] ❌ 庫內缺失: {v1}',
                                  'en': '  [{v0:03d}] ❌ Missing: {v1}'},
 '    -> ⏭️ Rank {v0} exceeds threshold ({v1}); report only': {'zh-CN': '    -> ⏭️ 排名 {v0} 超过设定阈值 ({v1})，仅报告不订阅',
                                                               'zh-TW': '    -> ⏭️ 排名 {v0} 超過設定閾值 ({v1})，僅報告不訂閱',
                                                               'en': '    -> ⏭️ Rank {v0} exceeds threshold ({v1}); report only'},
 '    -> 🚫 Excluded from subscriptions': {'zh-CN': '    -> 🚫 命中排除列表，跳过订阅',
                                          'zh-TW': '    -> 🚫 命中排除列表，跳過訂閱',
                                          'en': '    -> 🚫 Excluded from subscriptions'},
 '    -> 🍿 Already in MP; skipping duplicate subscription': {'zh-CN': '    -> 🍿 已存在于 MP，跳过重复订阅',
                                                             'zh-TW': '    -> 🍿 已存在於 MP，跳過重複訂閱',
                                                             'en': '    -> 🍿 Already in MP; skipping duplicate subscription'},
 '    -> 🍿 TV show already processed during this run; skipping duplicate': {'zh-CN': '    -> 🍿 本次任务已处理该电视剧，跳过跨榜单重复订阅',
                                                                            'zh-TW': '    -> 🍿 本次任務已處理該電視劇，跳過跨榜單重複訂閱',
                                                                            'en': '    -> 🍿 TV show already processed during '
                                                                                  'this run; skipping duplicate'},
 '    -> 🍿 All seasons already exist in MP; skipping': {'zh-CN': '    -> 🍿 所有季度均已存在于 MP，跳过重复订阅',
                                                        'zh-TW': '    -> 🍿 所有季度均已存在於 MP，跳過重複訂閱',
                                                        'en': '    -> 🍿 All seasons already exist in MP; skipping'},
 '    -> 🍿 MP subscription submitted': {'zh-CN': '    -> 🍿 已成功推送 MP 订阅',
                                        'zh-TW': '    -> 🍿 已成功推送 MP 訂閱',
                                        'en': '    -> 🍿 MP subscription submitted'},
 '    -> ❌ MP subscription failed: {v0}': {'zh-CN': '    -> ❌ MP 推送失败: {v0}',
                                           'zh-TW': '    -> ❌ MP 推送失敗: {v0}',
                                           'en': '    -> ❌ MP subscription failed: {v0}'},
 '{v0} (reason: {v1})': {'zh-CN': '{v0} (失败原因: {v1})', 'zh-TW': '{v0} (失敗原因: {v1})', 'en': '{v0} (reason: {v1})'},
 '  [Skip] Fewer than 2 local matches ({v0}); keeping existing collection': {'zh-CN': '  [跳过] 本地匹配不足 2 部（{v0} 部），保留现有合集。', 'zh-TW': '  [跳過] 本機匹配不足 2 部（{v0} 部），保留現有合集。', 'en': '  [Skip] Fewer than 2 local matches ({v0}); keeping existing collection'},
 'Chinese Movies': {'zh-CN': '国产电影', 'zh-TW': '國產電影', 'en': 'Chinese Movies'},
 'Chinese TV Shows': {'zh-CN': '国产电视剧', 'zh-TW': '國產電視劇', 'en': 'Chinese TV Shows'},
 'Cannot read country cache; querying again': {'zh-CN': '国家缓存无法读取，将重新查询',
                                               'zh-TW': '國家緩存無法讀取，將重新查詢',
                                               'en': 'Cannot read country cache; querying again'},
 'Cannot save country cache: {error}': {'zh-CN': '国家缓存保存失败：{error}',
                                        'zh-TW': '國家緩存保存失敗：{error}',
                                        'en': 'Cannot save country cache: {error}'},
 'TMDb entry not found; skipping country classification: {name} ({type}:{id})': {'zh-CN': 'TMDb 条目不存在，跳过国家分类：{name}（{type}:{id}）', 'zh-TW': 'TMDb 項目不存在，跳過國家分類：{name}（{type}:{id}）', 'en': 'TMDb entry not found; skipping country classification: {name} ({type}:{id})'},
 'Invalid TMDb country data': {'zh-CN': 'TMDb 国家数据格式异常', 'zh-TW': 'TMDb 國家數據格式異常', 'en': 'Invalid TMDb country data'},
 'Country lookup failed; using cached data: {id}': {'zh-CN': '国家查询失败，使用历史缓存：{id}',
                                                    'zh-TW': '國家查詢失敗，使用歷史緩存：{id}',
                                                    'en': 'Country lookup failed; using cached data: {id}'},
 'Cannot determine country; missing TMDb ID: {name}': {'zh-CN': '无法判断产地，缺少 TMDb ID：{name}',
                                                       'zh-TW': '無法判斷產地，缺少 TMDb ID：{name}',
                                                       'en': 'Cannot determine country; missing TMDb ID: {name}'},
 'Country lookup failed; keeping existing country collections for this media type: {name} ({error})': {'zh-CN': '国家查询失败，保留该类型的旧国家合集：{name}（{error}）',
                                                                                                       'zh-TW': '國家查詢失敗，保留該類型的舊國家合集：{name}（{error}）',
                                                                                                       'en': 'Country lookup '
                                                                                                             'failed; keeping '
                                                                                                             'existing country '
                                                                                                             'collections for '
                                                                                                             'this media type: '
                                                                                                             '{name} ({error})'},
 '🌍 TMDb proxy enabled': {'zh-CN': '🌍 TMDb 代理已开启', 'zh-TW': '🌍 TMDb 代理已開啓', 'en': '🌍 TMDb proxy enabled'},
 '🍿 MoviePilot subscriptions enabled -> {v0}': {'zh-CN': '🍿 MoviePilot 自动订阅已启用 -> {v0}',
                                                'zh-TW': '🍿 MoviePilot 自動訂閱已啓用 -> {v0}',
                                                'en': '🍿 MoviePilot subscriptions enabled -> {v0}'},
 '\n📚 Loading Emby library index...': {'zh-CN': '\n📚 正在加载 Emby 媒体库索引...',
                                       'zh-TW': '\n📚 正在加載 Emby 媒體庫索引...',
                                       'en': '\n📚 Loading Emby library index...'},
 '✅ Emby index loaded: {v0} movies, {v1} TV shows': {'zh-CN': '✅ Emby 索引加载完成：电影 {v0} 部，剧集 {v1} 部',
                                                     'zh-TW': '✅ Emby 索引加載完成：電影 {v0} 部，劇集 {v1} 部',
                                                     'en': '✅ Emby index loaded: {v0} movies, {v1} TV shows'},
 '\n📂 Stage 1: Synchronize Douban category lists\n': {'zh-CN': '\n📂 阶段一：同步豆瓣分类榜单\n',
                                                      'zh-TW': '\n📂 階段一：同步豆瓣分類榜單\n',
                                                      'en': '\n📂 Stage 1: Synchronize Douban category lists\n'},
 '\n🎬 Stage 2: Synchronize core lists\n': {'zh-CN': '\n🎬 阶段二：同步核心榜单\n',
                                           'zh-TW': '\n🎬 階段二：同步核心榜單\n',
                                           'en': '\n🎬 Stage 2: Synchronize core lists\n'},
 '\n🌏 Stage 3: Build country/region collections...\n': {'zh-CN': '\n🌏 阶段三：处理国家/地区影视合集...\n',
                                                        'zh-TW': '\n🌏 階段三：處理國家/地區影視合集...\n',
                                                        'en': '\n🌏 Stage 3: Build country/region collections...\n'},
 '\n🖼️ Stage 5: Upload queued posters and refresh image caches\n': {'zh-CN': '\n🖼️ 阶段五：统一结算海报注入与缓存刷新\n',
                                                                    'zh-TW': '\n🖼️ 階段五：統一結算海報注入與緩存刷新\n',
                                                                    'en': '\n'
                                                                          '🖼️ Stage 5: Upload queued posters and refresh image '
                                                                          'caches\n'},
 '  ⏳ Waiting 5 seconds for Emby background processing...': {'zh-CN': '  ⏳ 正在等待 Emby 后台队列消化其他任务 (延时 5 秒)...',
                                                             'zh-TW': '  ⏳ 正在等待 Emby 後臺隊列消化其他任務 (延時 5 秒)...',
                                                             'en': '  ⏳ Waiting 5 seconds for Emby background processing...'},
 '📊 Emby collection sync summary': {'zh-CN': '📊 Emby 智能合集整理汇总',
                                    'zh-TW': '📊 Emby 智能合集整理彙總',
                                    'en': '📊 Emby collection sync summary'},
 'Douban Movies - ': {'zh-CN': '豆瓣电影 - ', 'zh-TW': '豆瓣電影 - ', 'en': 'Douban Movies - '},
 '{v0} ({v1} missing)': {'zh-CN': '{v0}(缺{v1})', 'zh-TW': '{v0}(缺{v1})', 'en': '{v0} ({v1} missing)'},
 '({v0} missing)': {'zh-CN': '(缺{v0})', 'zh-TW': '(缺{v0})', 'en': '({v0} missing)'},
 '🎬 Letterboxd genre lists: {v0} collections meet the match threshold': {'zh-CN': '🎬 Letterboxd 类型片单同步: 匹配达标 {v0} 个合集',
                                                                         'zh-TW': '🎬 Letterboxd 類型片單同步: 匹配達標 {v0} 個合集',
                                                                         'en': '🎬 Letterboxd genre lists: {v0} collections meet '
                                                                               'the match threshold'},
 '📂 Douban movie categories: {v0} collections meet the match threshold': {'zh-CN': '📂 豆瓣电影分类同步: 匹配达标 {v0} 个合集',
                                                                          'zh-TW': '📂 豆瓣電影分類同步: 匹配達標 {v0} 個合集',
                                                                          'en': '📂 Douban movie categories: {v0} collections '
                                                                                'meet the match threshold'},
 '📺 Douban TV categories: {v0} collections meet the match threshold': {'zh-CN': '📺 豆瓣电视剧分类同步: 匹配达标 {v0} 个合集',
                                                                       'zh-TW': '📺 豆瓣電視劇分類同步: 匹配達標 {v0} 個合集',
                                                                       'en': '📺 Douban TV categories: {v0} collections meet the '
                                                                             'match threshold'},
 '🌏 Country/region collections': {'zh-CN': '🌏 国家/地区影视整理', 'zh-TW': '🌏 國家/地區影視整理', 'en': '🌏 Country/region collections'},
 '  - {name}: items: {count}': {'zh-CN': '  - {name}: {count} 部',
                                'zh-TW': '  - {name}: {count} 部',
                                'en': '  - {name}: items: {count}'},
 '⚠️ Failed/skipped collections: {names}': {'zh-CN': '⚠️ 失败/跳过的合集：{names}',
                                            'zh-TW': '⚠️ 失敗/跳過的合集：{names}',
                                            'en': '⚠️ Failed/skipped collections: {names}'},
 '🍿 MP subscription status:': {'zh-CN': '🍿 MP 订阅状态:', 'zh-TW': '🍿 MP 訂閱狀態:', 'en': '🍿 MP subscription status:'},
 'New': {'zh-CN': '新增', 'zh-TW': '新增', 'en': 'New'},
 'Existing': {'zh-CN': '已有', 'zh-TW': '已有', 'en': 'Existing'},
 'Excluded': {'zh-CN': '排除', 'zh-TW': '排除', 'en': 'Excluded'},
 'Failed': {'zh-CN': '失败', 'zh-TW': '失敗', 'en': 'Failed'},
 '{v0} {v1} titles': {'zh-CN': '{v0} {v1} 部', 'zh-TW': '{v0} {v1} 部', 'en': '{v0} {v1} titles'},
 '{v0} titles': {'zh-CN': '{v0} 部', 'zh-TW': '{v0} 部', 'en': '{v0} titles'},
 '{v0} seasons': {'zh-CN': '{v0} 季', 'zh-TW': '{v0} 季', 'en': '{v0} seasons'},
 'Excluded {v0} titles': {'zh-CN': '排除 {v0} 部', 'zh-TW': '排除 {v0} 部', 'en': 'Excluded {v0} titles'},
 '  - Movies: {v0}': {'zh-CN': '  - 电影: {v0}', 'zh-TW': '  - 電影: {v0}', 'en': '  - Movies: {v0}'},
 '  - TV shows: {v0}': {'zh-CN': '  - 电视剧: {v0}', 'zh-TW': '  - 電視劇: {v0}', 'en': '  - TV shows: {v0}'},
 '  - No subscription changes': {'zh-CN': '  - 本次无订阅变动', 'zh-TW': '  - 本次無訂閱變動', 'en': '  - No subscription changes'},
 '🍿 MoviePilot subscriptions disabled': {'zh-CN': '🍿 MoviePilot 自动订阅未开启',
                                         'zh-TW': '🍿 MoviePilot 自動訂閱未開啓',
                                         'en': '🍿 MoviePilot subscriptions disabled'},
 '🛠️ Media posters repaired: {v0}': {'zh-CN': '🛠️ 影视无封面修复: {v0}',
                                     'zh-TW': '🛠️ 影視無封面修復: {v0}',
                                     'en': '🛠️ Media posters repaired: {v0}'},
 '⭐ Favorites added (excluded users skipped): {v0}': {'zh-CN': '⭐ 自动收藏人次（已排除例外用户）: {v0}',
                                                      'zh-TW': '⭐ 自動收藏人次（已排除例外用戶）: {v0}',
                                                      'en': '⭐ Favorites added (excluded users skipped): {v0}'},
 '🖼️ List and country collection posters uploaded: {v0}': {'zh-CN': '🖼️ 榜单与国家合集海报上传：{v0} 个', 'zh-TW': '🖼️ 榜單與國家合集海報上傳：{v0} 個', 'en': '🖼️ List and country collection posters uploaded: {v0}'},
 '🛠️ Other collection posters repaired: {v0}': {'zh-CN': '🛠️ 本地无封面合集修复: {v0} 个',
                                                'zh-TW': '🛠️ 本地無封面合集修復: {v0} 個',
                                                'en': '🛠️ Other collection posters repaired: {v0}'},
 '⏱️ Duration: {v0} seconds': {'zh-CN': '⏱️ 任务总耗时: {v0} 秒', 'zh-TW': '⏱️ 任務總耗時: {v0} 秒', 'en': '⏱️ Duration: {v0} seconds'},
 '\n{v0} [{v1}] Missing titles:': {'zh-CN': '\n{v0} 【{v1}】缺失清单:',
                                   'zh-TW': '\n{v0} 【{v1}】缺失清單:',
                                   'en': '\n{v0} [{v1}] Missing titles:'},
 '  • ... {v0} titles in total': {'zh-CN': '  • ... 等共 {v0} 部',
                                  'zh-TW': '  • ... 等共 {v0} 部',
                                  'en': '  • ... {v0} titles in total'},
 '\n⚠️ [Failed MP subscriptions]:': {'zh-CN': '\n⚠️ 【MP 订阅失败清单】:',
                                     'zh-TW': '\n⚠️ 【MP 訂閱失敗清單】:',
                                     'en': '\n⚠️ [Failed MP subscriptions]:'},
 '\n🖼️⚠️ [Failed poster lookups/uploads]:': {'zh-CN': '\n🖼️⚠️ 【海报获取／上传失败清单】：', 'zh-TW': '\n🖼️⚠️ 【海報取得／上傳失敗清單】：', 'en': '\n🖼️⚠️ [Failed poster lookups/uploads]:'},
 '  • ... {v0} items in total': {'zh-CN': '  • ... 等共 {v0} 个', 'zh-TW': '  • ... 等共 {v0} 個', 'en': '  • ... {v0} items in total'},
 '\n🛠️ [Repaired posters]:': {'zh-CN': '\n🛠️ 【无封面修复清单】:', 'zh-TW': '\n🛠️ 【無封面修復清單】:', 'en': '\n🛠️ [Repaired posters]:'},
 '[Notification preview]': {'zh-CN': '【即将发送的通知消息预览】', 'zh-TW': '【即將發送的通知消息預覽】', 'en': '[Notification preview]'},
 'Emby collection sync report': {'zh-CN': 'Emby 智能合集整理报告', 'zh-TW': 'Emby 智能合集整理報告', 'en': 'Emby collection sync report'},
 'Run failed: {error}': {'zh-CN': '运行失败：{error}', 'zh-TW': '運行失敗：{error}', 'en': 'Run failed: {error}'},
 'Invalid MP subscription list': {'zh-CN': 'MP 订阅列表格式异常', 'zh-TW': 'MP 訂閱列表格式異常', 'en': 'Invalid MP subscription list'},
 'MP duplicate lookup failed; subscriptions disabled for this run: {error}': {'zh-CN': 'MP 防重查询失败，本次停止订阅：{error}',
                                                                              'zh-TW': 'MP 防重查詢失敗，本次停止訂閱：{error}',
                                                                              'en': 'MP duplicate lookup failed; subscriptions '
                                                                                    'disabled for this run: {error}'},
 'Invalid MP duplicate-check response': {'zh-CN': 'MP 防重响应格式异常',
                                         'zh-TW': 'MP 防重回應格式異常',
                                         'en': 'Invalid MP duplicate-check response'}}


# 国家/地区三语名称：离线提供简体中文、繁体中文和英文。
# 國家/地區三語名稱：離線提供簡體中文、繁體中文和英文。
# Offline country/region names in Simplified Chinese, Traditional Chinese, and English.
# 本表是单个地区的名称；COUNTRY_CODES 中 CN 合并四地区的规则独立保留。
# 本表是單一地區的名稱；COUNTRY_CODES 中 CN 合併四地區的規則獨立保留。
# These labels describe individual regions; selecting CN still uses the separate four-region collection group.
# 包含标准及历史地区；运行时无需额外网络请求。
# 包含標準及歷史地區；執行時無需額外網路請求。
# Includes standard and historical regions; no extra network lookups at runtime.
COUNTRY_LABELS = {
    'AC': ('阿森松岛', '阿森松島', 'Ascension Island'),
    'AD': ('安道尔', '安道爾', 'Andorra'),
    'AE': ('阿拉伯联合酋长国', '阿拉伯聯合大公國', 'United Arab Emirates'),
    'AF': ('阿富汗', '阿富汗', 'Afghanistan'),
    'AG': ('安提瓜和巴布达', '安地卡及巴布達', 'Antigua & Barbuda'),
    'AI': ('安圭拉', '安奎拉', 'Anguilla'),
    'AL': ('阿尔巴尼亚', '阿爾巴尼亞', 'Albania'),
    'AM': ('亚美尼亚', '亞美尼亞', 'Armenia'),
    'AN': ('荷属安的列斯群岛', '荷屬安的列斯群島', 'Netherlands Antilles'),
    'AO': ('安哥拉', '安哥拉', 'Angola'),
    'AQ': ('南极洲', '南極洲', 'Antarctica'),
    'AR': ('阿根廷', '阿根廷', 'Argentina'),
    'AS': ('美属萨摩亚', '美屬薩摩亞', 'American Samoa'),
    'AT': ('奥地利', '奧地利', 'Austria'),
    'AU': ('澳大利亚', '澳洲', 'Australia'),
    'AW': ('阿鲁巴', '荷屬阿魯巴', 'Aruba'),
    'AX': ('奥兰群岛', '奧蘭群島', 'Åland Islands'),
    'AZ': ('阿塞拜疆', '亞塞拜然', 'Azerbaijan'),
    'BA': ('波斯尼亚和黑塞哥维那', '波士尼亞與赫塞哥維納', 'Bosnia & Herzegovina'),
    'BB': ('巴巴多斯', '巴貝多', 'Barbados'),
    'BD': ('孟加拉国', '孟加拉', 'Bangladesh'),
    'BE': ('比利时', '比利時', 'Belgium'),
    'BF': ('布基纳法索', '布吉納法索', 'Burkina Faso'),
    'BG': ('保加利亚', '保加利亞', 'Bulgaria'),
    'BH': ('巴林', '巴林', 'Bahrain'),
    'BI': ('布隆迪', '蒲隆地', 'Burundi'),
    'BJ': ('贝宁', '貝南', 'Benin'),
    'BL': ('圣巴泰勒米', '聖巴瑟米', 'St. Barthélemy'),
    'BM': ('百慕大', '百慕達', 'Bermuda'),
    'BN': ('文莱', '汶萊', 'Brunei'),
    'BO': ('玻利维亚', '玻利維亞', 'Bolivia'),
    'BQ': ('荷属加勒比区', '荷蘭加勒比區', 'Caribbean Netherlands'),
    'BR': ('巴西', '巴西', 'Brazil'),
    'BS': ('巴哈马', '巴哈馬', 'Bahamas'),
    'BT': ('不丹', '不丹', 'Bhutan'),
    'BU': ('缅甸', '緬甸', 'Myanmar (Burma)'),
    'BV': ('布韦岛', '布威島', 'Bouvet Island'),
    'BW': ('博茨瓦纳', '波札那', 'Botswana'),
    'BY': ('白俄罗斯', '白俄羅斯', 'Belarus'),
    'BZ': ('伯利兹', '貝里斯', 'Belize'),
    'CA': ('加拿大', '加拿大', 'Canada'),
    'CC': ('科科斯（基林）群岛', '科克斯（基靈）群島', 'Cocos (Keeling) Islands'),
    'CD': ('刚果（金）', '剛果（金夏沙）', 'Congo - Kinshasa'),
    'CF': ('中非共和国', '中非共和國', 'Central African Republic'),
    'CG': ('刚果（布）', '剛果（布拉薩）', 'Congo - Brazzaville'),
    'CH': ('瑞士', '瑞士', 'Switzerland'),
    'CI': ('科特迪瓦', '象牙海岸', 'Côte d’Ivoire'),
    'CK': ('库克群岛', '庫克群島', 'Cook Islands'),
    'CL': ('智利', '智利', 'Chile'),
    'CM': ('喀麦隆', '喀麥隆', 'Cameroon'),
    'CN': ('中国大陆', '中國大陸', 'China mainland'),
    'CO': ('哥伦比亚', '哥倫比亞', 'Colombia'),
    'CP': ('克利珀顿岛', '克里派頓島', 'Clipperton Island'),
    'CQ': ('萨克岛', '薩克島', 'Sark'),
    'CR': ('哥斯达黎加', '哥斯大黎加', 'Costa Rica'),
    'CS': ('塞尔维亚和黑山', '塞爾維亞和黑山', 'Serbia and Montenegro'),
    'CU': ('古巴', '古巴', 'Cuba'),
    'CV': ('佛得角', '維德角', 'Cape Verde'),
    'CW': ('库拉索', '庫拉索', 'Curaçao'),
    'CX': ('圣诞岛', '聖誕島', 'Christmas Island'),
    'CY': ('塞浦路斯', '賽普勒斯', 'Cyprus'),
    'CZ': ('捷克', '捷克', 'Czechia'),
    'DE': ('德国', '德國', 'Germany'),
    'DG': ('迪戈加西亚岛', '迪亞哥加西亞島', 'Diego Garcia'),
    'DJ': ('吉布提', '吉布地', 'Djibouti'),
    'DK': ('丹麦', '丹麥', 'Denmark'),
    'DM': ('多米尼克', '多米尼克', 'Dominica'),
    'DO': ('多米尼加共和国', '多明尼加共和國', 'Dominican Republic'),
    'DZ': ('阿尔及利亚', '阿爾及利亞', 'Algeria'),
    'EA': ('休达及梅利利亚', '休達與梅利利亞', 'Ceuta & Melilla'),
    'EC': ('厄瓜多尔', '厄瓜多', 'Ecuador'),
    'EE': ('爱沙尼亚', '愛沙尼亞', 'Estonia'),
    'EG': ('埃及', '埃及', 'Egypt'),
    'EH': ('西撒哈拉', '西撒哈拉', 'Western Sahara'),
    'ER': ('厄立特里亚', '厄利垂亞', 'Eritrea'),
    'ES': ('西班牙', '西班牙', 'Spain'),
    'ET': ('埃塞俄比亚', '衣索比亞', 'Ethiopia'),
    'EU': ('欧盟', '歐盟', 'European Union'),
    'EZ': ('欧元区', '歐元區', 'Eurozone'),
    'FI': ('芬兰', '芬蘭', 'Finland'),
    'FJ': ('斐济', '斐濟', 'Fiji'),
    'FK': ('福克兰群岛', '福克蘭群島', 'Falkland Islands'),
    'FM': ('密克罗尼西亚', '密克羅尼西亞', 'Micronesia'),
    'FO': ('法罗群岛', '法羅群島', 'Faroe Islands'),
    'FR': ('法国', '法國', 'France'),
    'GA': ('加蓬', '加彭', 'Gabon'),
    'GB': ('英国', '英國', 'United Kingdom'),
    'GD': ('格林纳达', '格瑞那達', 'Grenada'),
    'GE': ('格鲁吉亚', '喬治亞', 'Georgia'),
    'GF': ('法属圭亚那', '法屬圭亞那', 'French Guiana'),
    'GG': ('根西岛', '根息', 'Guernsey'),
    'GH': ('加纳', '迦納', 'Ghana'),
    'GI': ('直布罗陀', '直布羅陀', 'Gibraltar'),
    'GL': ('格陵兰', '格陵蘭', 'Greenland'),
    'GM': ('冈比亚', '甘比亞', 'Gambia'),
    'GN': ('几内亚', '幾內亞', 'Guinea'),
    'GP': ('瓜德罗普', '瓜地洛普', 'Guadeloupe'),
    'GQ': ('赤道几内亚', '赤道幾內亞', 'Equatorial Guinea'),
    'GR': ('希腊', '希臘', 'Greece'),
    'GS': ('南乔治亚和南桑威奇群岛', '南喬治亞與南三明治群島', 'So. Georgia & So. Sandwich Isl.'),
    'GT': ('危地马拉', '瓜地馬拉', 'Guatemala'),
    'GU': ('关岛', '關島', 'Guam'),
    'GW': ('几内亚比绍', '幾內亞比索', 'Guinea-Bissau'),
    'GY': ('圭亚那', '蓋亞那', 'Guyana'),
    'HK': ('中国香港', '中國香港', 'Hong Kong'),
    'HM': ('赫德岛和麦克唐纳群岛', '赫德島及麥唐納群島', 'Heard & McDonald Islands'),
    'HN': ('洪都拉斯', '宏都拉斯', 'Honduras'),
    'HR': ('克罗地亚', '克羅埃西亞', 'Croatia'),
    'HT': ('海地', '海地', 'Haiti'),
    'HU': ('匈牙利', '匈牙利', 'Hungary'),
    'IC': ('加纳利群岛', '加那利群島', 'Canary Islands'),
    'ID': ('印度尼西亚', '印尼', 'Indonesia'),
    'IE': ('爱尔兰', '愛爾蘭', 'Ireland'),
    'IL': ('以色列', '以色列', 'Israel'),
    'IM': ('马恩岛', '曼島', 'Isle of Man'),
    'IN': ('印度', '印度', 'India'),
    'IO': ('查戈斯群岛', '查戈斯群島', 'Chagos Archipelago'),
    'IQ': ('伊拉克', '伊拉克', 'Iraq'),
    'IR': ('伊朗', '伊朗', 'Iran'),
    'IS': ('冰岛', '冰島', 'Iceland'),
    'IT': ('意大利', '義大利', 'Italy'),
    'JE': ('泽西岛', '澤西島', 'Jersey'),
    'JM': ('牙买加', '牙買加', 'Jamaica'),
    'JO': ('约旦', '約旦', 'Jordan'),
    'JP': ('日本', '日本', 'Japan'),
    'KE': ('肯尼亚', '肯亞', 'Kenya'),
    'KG': ('吉尔吉斯斯坦', '吉爾吉斯', 'Kyrgyzstan'),
    'KH': ('柬埔寨', '柬埔寨', 'Cambodia'),
    'KI': ('基里巴斯', '吉里巴斯', 'Kiribati'),
    'KM': ('科摩罗', '葛摩', 'Comoros'),
    'KN': ('圣基茨和尼维斯', '聖克里斯多福及尼維斯', 'St. Kitts & Nevis'),
    'KP': ('朝鲜', '北韓', 'North Korea'),
    'KR': ('韩国', '南韓', 'South Korea'),
    'KW': ('科威特', '科威特', 'Kuwait'),
    'KY': ('开曼群岛', '開曼群島', 'Cayman Islands'),
    'KZ': ('哈萨克斯坦', '哈薩克', 'Kazakhstan'),
    'LA': ('老挝', '寮國', 'Laos'),
    'LB': ('黎巴嫩', '黎巴嫩', 'Lebanon'),
    'LC': ('圣卢西亚', '聖露西亞', 'St. Lucia'),
    'LI': ('列支敦士登', '列支敦斯登', 'Liechtenstein'),
    'LK': ('斯里兰卡', '斯里蘭卡', 'Sri Lanka'),
    'LR': ('利比里亚', '賴比瑞亞', 'Liberia'),
    'LS': ('莱索托', '賴索托', 'Lesotho'),
    'LT': ('立陶宛', '立陶宛', 'Lithuania'),
    'LU': ('卢森堡', '盧森堡', 'Luxembourg'),
    'LV': ('拉脱维亚', '拉脫維亞', 'Latvia'),
    'LY': ('利比亚', '利比亞', 'Libya'),
    'MA': ('摩洛哥', '摩洛哥', 'Morocco'),
    'MC': ('摩纳哥', '摩納哥', 'Monaco'),
    'MD': ('摩尔多瓦', '摩爾多瓦', 'Moldova'),
    'ME': ('黑山', '蒙特內哥羅', 'Montenegro'),
    'MF': ('法属圣马丁', '法屬聖馬丁', 'St. Martin'),
    'MG': ('马达加斯加', '馬達加斯加', 'Madagascar'),
    'MH': ('马绍尔群岛', '馬紹爾群島', 'Marshall Islands'),
    'MK': ('北马其顿', '北馬其頓', 'North Macedonia'),
    'ML': ('马里', '馬利', 'Mali'),
    'MM': ('缅甸', '緬甸', 'Myanmar (Burma)'),
    'MN': ('蒙古', '蒙古', 'Mongolia'),
    'MO': ('中国澳门', '中國澳門', 'Macao'),
    'MP': ('北马里亚纳群岛', '北馬利安納群島', 'Northern Mariana Islands'),
    'MQ': ('马提尼克', '馬丁尼克', 'Martinique'),
    'MR': ('毛里塔尼亚', '茅利塔尼亞', 'Mauritania'),
    'MS': ('蒙特塞拉特', '蒙哲臘', 'Montserrat'),
    'MT': ('马耳他', '馬爾他', 'Malta'),
    'MU': ('毛里求斯', '模里西斯', 'Mauritius'),
    'MV': ('马尔代夫', '馬爾地夫', 'Maldives'),
    'MW': ('马拉维', '馬拉威', 'Malawi'),
    'MX': ('墨西哥', '墨西哥', 'Mexico'),
    'MY': ('马来西亚', '馬來西亞', 'Malaysia'),
    'MZ': ('莫桑比克', '莫三比克', 'Mozambique'),
    'NA': ('纳米比亚', '納米比亞', 'Namibia'),
    'NC': ('新喀里多尼亚', '新喀里多尼亞', 'New Caledonia'),
    'NE': ('尼日尔', '尼日', 'Niger'),
    'NF': ('诺福克岛', '諾福克島', 'Norfolk Island'),
    'NG': ('尼日利亚', '奈及利亞', 'Nigeria'),
    'NI': ('尼加拉瓜', '尼加拉瓜', 'Nicaragua'),
    'NL': ('荷兰', '荷蘭', 'Netherlands'),
    'NO': ('挪威', '挪威', 'Norway'),
    'NP': ('尼泊尔', '尼泊爾', 'Nepal'),
    'NR': ('瑙鲁', '諾魯', 'Nauru'),
    'NU': ('纽埃', '紐埃島', 'Niue'),
    'NZ': ('新西兰', '紐西蘭', 'New Zealand'),
    'OM': ('阿曼', '阿曼', 'Oman'),
    'PA': ('巴拿马', '巴拿馬', 'Panama'),
    'PE': ('秘鲁', '秘魯', 'Peru'),
    'PF': ('法属波利尼西亚', '法屬玻里尼西亞', 'French Polynesia'),
    'PG': ('巴布亚新几内亚', '巴布亞紐幾內亞', 'Papua New Guinea'),
    'PH': ('菲律宾', '菲律賓', 'Philippines'),
    'PK': ('巴基斯坦', '巴基斯坦', 'Pakistan'),
    'PL': ('波兰', '波蘭', 'Poland'),
    'PM': ('圣皮埃尔和密克隆群岛', '聖皮埃與密克隆群島', 'St. Pierre & Miquelon'),
    'PN': ('皮特凯恩群岛', '皮特肯群島', 'Pitcairn Islands'),
    'PR': ('波多黎各', '波多黎各', 'Puerto Rico'),
    'PS': ('巴勒斯坦领土', '巴勒斯坦自治區', 'Palestinian Territories'),
    'PT': ('葡萄牙', '葡萄牙', 'Portugal'),
    'PW': ('帕劳', '帛琉', 'Palau'),
    'PY': ('巴拉圭', '巴拉圭', 'Paraguay'),
    'QA': ('卡塔尔', '卡達', 'Qatar'),
    'QO': ('大洋洲边远群岛', '大洋洲邊疆群島', 'Outlying Oceania'),
    'RE': ('留尼汪', '留尼旺', 'Réunion'),
    'RO': ('罗马尼亚', '羅馬尼亞', 'Romania'),
    'RS': ('塞尔维亚', '塞爾維亞', 'Serbia'),
    'RU': ('俄罗斯', '俄羅斯', 'Russia'),
    'RW': ('卢旺达', '盧安達', 'Rwanda'),
    'SA': ('沙特阿拉伯', '沙烏地阿拉伯', 'Saudi Arabia'),
    'SB': ('所罗门群岛', '索羅門群島', 'Solomon Islands'),
    'SC': ('塞舌尔', '塞席爾', 'Seychelles'),
    'SD': ('苏丹', '蘇丹', 'Sudan'),
    'SE': ('瑞典', '瑞典', 'Sweden'),
    'SG': ('新加坡', '新加坡', 'Singapore'),
    'SH': ('圣赫勒拿', '聖赫勒拿島', 'St. Helena'),
    'SI': ('斯洛文尼亚', '斯洛維尼亞', 'Slovenia'),
    'SJ': ('斯瓦尔巴和扬马延', '挪威屬斯瓦巴及尖棉', 'Svalbard & Jan Mayen'),
    'SK': ('斯洛伐克', '斯洛伐克', 'Slovakia'),
    'SL': ('塞拉利昂', '獅子山共和國', 'Sierra Leone'),
    'SM': ('圣马力诺', '聖馬利諾', 'San Marino'),
    'SN': ('塞内加尔', '塞內加爾', 'Senegal'),
    'SO': ('索马里', '索馬利亞', 'Somalia'),
    'SR': ('苏里南', '蘇利南', 'Suriname'),
    'SS': ('南苏丹', '南蘇丹', 'South Sudan'),
    'ST': ('圣多美和普林西比', '聖多美普林西比', 'São Tomé & Príncipe'),
    'SU': ('苏联', '蘇聯', 'Soviet Union'),
    'SV': ('萨尔瓦多', '薩爾瓦多', 'El Salvador'),
    'SX': ('荷属圣马丁', '荷屬聖馬丁', 'Sint Maarten'),
    'SY': ('叙利亚', '敘利亞', 'Syria'),
    'SZ': ('斯威士兰', '史瓦帝尼', 'Eswatini'),
    'TA': ('特里斯坦-达库尼亚群岛', '特里斯坦達庫尼亞群島', 'Tristan da Cunha'),
    'TC': ('特克斯和凯科斯群岛', '土克斯及開科斯群島', 'Turks & Caicos Islands'),
    'TD': ('乍得', '查德', 'Chad'),
    'TF': ('法属南部领地', '法屬南部屬地', 'French Southern Territories'),
    'TG': ('多哥', '多哥', 'Togo'),
    'TH': ('泰国', '泰國', 'Thailand'),
    'TJ': ('塔吉克斯坦', '塔吉克', 'Tajikistan'),
    'TK': ('托克劳', '托克勞群島', 'Tokelau'),
    'TL': ('东帝汶', '東帝汶', 'Timor-Leste'),
    'TM': ('土库曼斯坦', '土庫曼', 'Turkmenistan'),
    'TN': ('突尼斯', '突尼西亞', 'Tunisia'),
    'TO': ('汤加', '東加', 'Tonga'),
    'TP': ('东帝汶', '東帝汶', 'Timor-Leste'),
    'TR': ('土耳其', '土耳其', 'Türkiye'),
    'TT': ('特立尼达和多巴哥', '千里達及托巴哥', 'Trinidad & Tobago'),
    'TV': ('图瓦卢', '吐瓦魯', 'Tuvalu'),
    'TW': ('中国台湾', '中國台灣', 'Taiwan, China'),
    'TZ': ('坦桑尼亚', '坦尚尼亞', 'Tanzania'),
    'UA': ('乌克兰', '烏克蘭', 'Ukraine'),
    'UG': ('乌干达', '烏干達', 'Uganda'),
    'UM': ('美国本土外小岛屿', '美國本土外小島嶼', 'U.S. Outlying Islands'),
    'UN': ('联合国', '聯合國', 'United Nations'),
    'US': ('美国', '美國', 'United States'),
    'UY': ('乌拉圭', '烏拉圭', 'Uruguay'),
    'UZ': ('乌兹别克斯坦', '烏茲別克', 'Uzbekistan'),
    'VA': ('梵蒂冈', '梵蒂岡', 'Vatican City'),
    'VC': ('圣文森特和格林纳丁斯', '聖文森及格瑞那丁', 'St. Vincent & Grenadines'),
    'VE': ('委内瑞拉', '委內瑞拉', 'Venezuela'),
    'VG': ('英属维尔京群岛', '英屬維京群島', 'British Virgin Islands'),
    'VI': ('美属维尔京群岛', '美屬維京群島', 'U.S. Virgin Islands'),
    'VN': ('越南', '越南', 'Vietnam'),
    'VU': ('瓦努阿图', '萬那杜', 'Vanuatu'),
    'WF': ('瓦利斯和富图纳', '瓦利斯群島和富圖那群島', 'Wallis & Futuna'),
    'WS': ('萨摩亚', '薩摩亞', 'Samoa'),
    'XC': ('捷克斯洛伐克', '捷克斯洛伐克', 'Czechoslovakia'),
    'XG': ('东德', '東德', 'East Germany'),
    'XI': ('北爱尔兰', '北愛爾蘭', 'Northern Ireland'),
    'XK': ('科索沃', '科索沃', 'Kosovo'),
    'XW': ('西德', '西德', 'West Germany'),
    'YE': ('也门', '葉門', 'Yemen'),
    'YT': ('马约特', '馬約特島', 'Mayotte'),
    'YU': ('南斯拉夫', '南斯拉夫', 'Yugoslavia'),
    'ZA': ('南非', '南非', 'South Africa'),
    'ZM': ('赞比亚', '尚比亞', 'Zambia'),
    'ZR': ('刚果（金）', '剛果（金夏沙）', 'Congo - Kinshasa'),
    'ZW': ('津巴布韦', '辛巴威', 'Zimbabwe'),
}

# 代码与三语名称会自动识别；以下补充常见别名。
# 代碼與三語名稱會自動識別；以下補充常見別名。
# Codes and localized names are recognized automatically; these are additional aliases.
COUNTRY_ALIASES = {'antigua and barbuda': 'AG',
 'bosnia and herzegovina': 'BA',
 'british indian ocean territory': 'IO',
 'brunei darussalam': 'BN',
 'burma': 'BU',
 'china': 'CN',
 'cocos  islands': 'CC',
 'congo': 'CG',
 'congo - kinshasa': 'CD',
 "cote d'ivoire": 'CI',
 'czech republic': 'CZ',
 'east timor': 'TP',
 'faeroe islands': 'FO',
 'great britain': 'GB',
 'guadaloupe': 'GP',
 'heard and mcdonald islands': 'HM',
 'holy see': 'VA',
 'hong kong sar': 'HK',
 'kyrgyz republic': 'KG',
 "lao people's democratic republic": 'LA',
 'libyan arab jamahiriya': 'LY',
 'macau': 'MO',
 'macedonia': 'MK',
 'mainland china': 'CN',
 'myanmar': 'MM',
 'myanmar (burma)': 'MM',
 'palestinian territory': 'PS',
 'pitcairn island': 'PN',
 'republic of korea': 'KR',
 'reunion': 'RE',
 'sao tome and principe': 'ST',
 'south georgia and the south sandwich islands': 'GS',
 'st. kitts and nevis': 'KN',
 'st. pierre and miquelon': 'PM',
 'st. vincent and the grenadines': 'VC',
 'svalbard & jan mayen islands': 'SJ',
 'swaziland': 'SZ',
 'syrian arab republic': 'SY',
 'taiwan': 'TW',
 'timor-leste': 'TL',
 'trinidad and tobago': 'TT',
 'turkey': 'TR',
 'turks and caicos islands': 'TC',
 'uk': 'GB',
 'united states minor outlying islands': 'UM',
 'united states of america': 'US',
 'us virgin islands': 'VI',
 'usa': 'US',
 'ussr': 'SU',
 'wallis and futuna islands': 'WF',
 'zaire': 'ZR',
 '东帝汶': 'TL',
 '中国': 'CN',
 '中國': 'CN',
 '中國臺灣': 'TW',
 '刚果（金）': 'CD',
 '剛果（金夏沙）': 'CD',
 '台湾': 'TW',
 '台灣': 'TW',
 '東帝汶': 'TL',
 '澳大利亞': 'AU',
 '澳門': 'MO',
 '澳门': 'MO',
 '緬甸': 'MM',
 '缅甸': 'MM',
 '臺灣': 'TW',
 '韓國': 'KR',
 '香港': 'HK'}

# 旧译名用于识别并替换旧合集，避免改名后出现重复合集。
# 舊譯名用於識別並替換舊合集，避免改名後出現重複合集。
# Previous labels remain migration aliases to avoid duplicate collections after a rename.
COUNTRY_LEGACY_LABELS = {'AU': ('澳大利亚', '澳大利亞', 'Australia'),
 'CN': ('中国大陆', '中國大陸', 'Mainland China'),
 'KR': ('韩国', '韓國', 'South Korea'),
 'TW': ('中国台湾', '中國臺灣', 'Taiwan')}

SUPPORTED_COUNTRY_CODES = set(COUNTRY_LABELS)


# Synchronization logic

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time
import base64
import builtins


def print(*args, **kwargs):
    builtins.print(*(safe_text(arg) for arg in args), **kwargs)


# Qinglong notifications; print to the console when the module is unavailable.
try:
    from notify import send
except ImportError:
    def send(title, content):
        print(tr('\n[Notification preview] Title: {v0}\nContent:\n{v1}', v0=title, v1=content))


def tr(message, **values):
    translations = MESSAGES.get(message, {})
    template = translations.get(LANGUAGE, message)
    return template.format(**values) if values else template


DEFAULT_LIST_NAMES = {str(ident): names.get("zh-CN") for ident, names in LIST_NAMES.items()}


def localize_list_names():
    for item in CUSTOM_LISTS + DOUBAN_GENRE_LISTS + DOUBAN_TV_LISTS:
        ident = str(item["id"])
        default = DEFAULT_LIST_NAMES.get(ident)
        names = LIST_NAMES.get(ident, {})
        # Only translate bundled names, never override a user-supplied collection name.
        if default and item["name"] in [default] + list(names.values()):
            old = OLD_COLLECTION_NAMES.get(default, [])
            item["name"] = names.get(LANGUAGE, default)
            OLD_COLLECTION_NAMES[item["name"]] = list(dict.fromkeys([default] + list(names.values()) + old))
    for kind in ("Movie", "Series"):
        name = country_collection_name(None, kind)
        message = 'Chinese Movies' if kind == "Movie" else 'Chinese TV Shows'
        OLD_COLLECTION_NAMES[name] = [MESSAGES[message][language] for language in ("zh-CN", "zh-TW", "en")]
    for code in COUNTRY_CODES:
        for kind, message in (("Movie", 'Movies'), ("Series", 'TV Shows')):
            labels = tuple(MESSAGES[message][language] for language in ("zh-CN", "zh-TW", "en"))
            variants = [tuple(country_display_name(code, language) for language in ("zh-CN", "zh-TW", "en")),
                        (code, code, code)]
            if code in COUNTRY_LEGACY_LABELS:
                variants.append(COUNTRY_LEGACY_LABELS[code])
            name = country_collection_name(code, kind)
            aliases = [f"{a}{' ' if i == 2 else ''}{b}" for variant in variants
                       for i, (a, b) in enumerate(zip(variant, labels))]
            OLD_COLLECTION_NAMES[name] = list(dict.fromkeys(OLD_COLLECTION_NAMES.get(name, []) + aliases))


# Settings are validated at startup, before any network request.
PROXIES = None
session = None
COUNTRY_CACHE = {}


def safe_text(value):
    """Redact both raw and URL-encoded credentials, including exception URLs."""
    text = str(value)
    secrets = [EMBY_API_KEY, TMDB_API_KEY, TMDB_ACCESS_TOKEN, MP_API_TOKEN]
    if PROXY_URL:
        secrets.append(PROXY_URL)
        try:
            proxy = urlsplit(PROXY_URL)
            secrets.extend([proxy.username, proxy.password])
        except ValueError:
            pass
    for secret in sorted(filter(None, secrets), key=len, reverse=True):
        text = text.replace(secret, "***").replace(quote(secret, safe=""), "***")
    text = re.sub(r"(?i)((?:api_key|api_token|access_token|token)=)[^&\s'\")]+", r"\1***", text)
    return re.sub(r"(https?://)[^/@\s]+:[^/@\s]+@", r"\1***@", text)


class SafeSession(requests.Session):
    """A default timeout and TLS policy scoped to the requested service."""
    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", (10, 30))
        origin = urlsplit(url)
        def same_origin(base):
            other = urlsplit(base or "")
            return (origin.scheme, origin.netloc) == (other.scheme, other.netloc)
        kwargs["verify"] = (EMBY_VERIFY_SSL if same_origin(EMBY_URL) else
                            MP_VERIFY_SSL if same_origin(MP_URL) else True)
        return super().request(method, url, **kwargs)


def initialize():
    global LANGUAGE, PROXIES, session, EMBY_URL, MP_URL, COUNTRY_CODES
    if LANGUAGE not in ("zh-CN", "zh-TW", "en"):
        raise ValueError("LANGUAGE: zh-CN / zh-TW / en")
    for key in ("FAVORITES_ENABLE", "MP_ENABLE", "USE_PROXY", "EMBY_VERIFY_SSL", "MP_VERIFY_SSL"):
        if type(globals()[key]) is not bool:
            raise ValueError(f"{key}: true / false")
    required = ["EMBY_URL", "EMBY_API_KEY", "TMDB_API_KEY"]
    if MP_ENABLE:
        required.extend(["MP_URL", "MP_API_TOKEN"])
    if USE_PROXY:
        required.append("PROXY_URL")
    missing = [key for key in required if not globals().get(key) or not str(globals()[key]).strip()]
    if missing:
        raise ValueError(tr('Missing required connection settings: {names}', names=", ".join(missing)))
    for key in ["EMBY_URL"] + (["MP_URL"] if MP_ENABLE else []) + (["PROXY_URL"] if USE_PROXY else []):
        parsed = urlsplit(globals()[key])
        if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.query or parsed.fragment:
            raise ValueError(tr('Invalid URL: {name}', name=key))
    EMBY_URL = EMBY_URL.rstrip("/")
    MP_URL = (MP_URL or "").rstrip("/")
    for key in ("COUNTRY_CODES", "FAVORITES_EXCLUDE_USERS", "MP_EXCLUDE_MOVIE_IDS", "MP_EXCLUDE_SERIES_IDS",
                "TMDB_DOMESTIC_CODES"):
        if not isinstance(globals()[key], list):
            raise ValueError(tr('Setting must be a list: {name}', name=key))
    if any(not isinstance(value, str) for value in FAVORITES_EXCLUDE_USERS):
        raise ValueError("FAVORITES_EXCLUDE_USERS: [\"username\"]")
    COUNTRY_CODES = list(dict.fromkeys(normalize_country_code(code) for code in COUNTRY_CODES))
    if any(code not in SUPPORTED_COUNTRY_CODES for code in COUNTRY_CODES):
        raise ValueError(tr('Use a supported country/region code or name'))
    for key in ("COUNTRY_CACHE_DAYS", "BATCH_SIZE"):
        if type(globals()[key]) is not int or globals()[key] < 1:
            raise ValueError(f"{key} >= 1")
    for key, choices in (("LIST_POSTER_MODE", ("library", "list")),
                         ("DOMESTIC_POSTER_MODE", ("premiere", "added")),
                         ("POSTER_SIZE", ("w780", "original"))):
        if globals()[key] not in choices:
            raise ValueError(f"{key}: {choices}")
    seen = set()
    for key in ("CUSTOM_LISTS", "DOUBAN_GENRE_LISTS", "DOUBAN_TV_LISTS"):
        lists = globals()[key]
        if not isinstance(lists, list):
            raise ValueError(tr('Setting must be a list: {name}', name=key))
        for item in lists:
            if (not isinstance(item, dict) or not str(item.get("id", "")).isdigit()
                    or not isinstance(item.get("name"), str) or not item["name"].strip()
                    or item.get("type", "Movie") not in ("Movie", "Series")):
                raise ValueError(tr('Invalid list configuration: {name}', name=key))
            switch = item.get("mp_subscribe", False)
            if type(switch) not in (bool, int) or (type(switch) is int and switch < 0):
                raise ValueError("mp_subscribe: true / false / N >= 0")
            ident = (str(item["id"]), item.get("type", "Movie"))
            if ident in seen:
                raise ValueError(tr('Duplicate list: {name}', name=item["name"]))
            seen.add(ident)
    globals()["MP_EXCLUDE_MOVIE_IDS"] = {str(i) for i in MP_EXCLUDE_MOVIE_IDS}
    globals()["MP_EXCLUDE_SERIES_IDS"] = {str(i) for i in MP_EXCLUDE_SERIES_IDS}
    localize_list_names()
    PROXIES = {"http": PROXY_URL, "https": PROXY_URL} if USE_PROXY else None
    session = SafeSession()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=frozenset(["GET", "HEAD", "OPTIONS"]))
    session.mount("http://", HTTPAdapter(max_retries=retry))
    session.mount("https://", HTTPAdapter(max_retries=retry))


# Statistics for this run.
sync_stats = {
    "failed_lists": [], "country_reports": [],
    "movies": 0, "series": 0, "favs": 0, "fixed_covers": 0,
    "fixed_cover_names": [],
    "fixed_media_covers": {"Movie": [], "Series": []},
    "mp_subscribed": 0, "mp_existed": 0, "mp_failed": [], 
    "mp_excluded": 0,
    "mp_movie_subscribed": 0, "mp_movie_existed": 0,
    "mp_movie_failed": 0, "mp_movie_excluded": 0,
    "mp_series_subscribed": 0, "mp_series_existed": 0,
    "mp_series_failed": 0, "mp_series_excluded": 0,
    "mp_season_subscribed": 0, "mp_season_existed": 0,
    "mp_season_failed": 0,
    "poster_failed": [],
    "pending_posters": [], 
    "lists_report": {}
}
# Process each TV show once per run, while checking subscriptions per season.
mp_processed_series_ids = set()

def get_emby_users():
    response = session.get(f"{EMBY_URL}/emby/Users", params={"api_key": EMBY_API_KEY})
    response.raise_for_status()
    users = response.json()
    if not isinstance(users, list):
        raise ValueError(tr('Invalid Emby user response'))
    return users


def add_to_all_users_favorites(item_id, item_name):
    if not FAVORITES_ENABLE:
        return
    for user in get_emby_users():
        if user.get("Name") in FAVORITES_EXCLUDE_USERS:
            continue
        uid = user["Id"]
        response = session.get(f"{EMBY_URL}/emby/Users/{uid}/Items/{item_id}", params={"api_key": EMBY_API_KEY})
        response.raise_for_status()
        if not response.json().get("UserData", {}).get("IsFavorite", False):
            response = session.post(f"{EMBY_URL}/emby/Users/{uid}/FavoriteItems/{item_id}", params={"api_key": EMBY_API_KEY})
            response.raise_for_status()
            sync_stats["favs"] += 1


def get_emby_items(item_type, fields="ProviderIds,PremiereDate,DateCreated,ImageTags", **extra):
    params = {"api_key": EMBY_API_KEY, "IncludeItemTypes": item_type, "Recursive": True,
              "Fields": fields, "Limit": 500, "SortBy": "SortName", "SortOrder": "Ascending"}
    params.update(extra)
    items, seen = [], set()
    start = 0
    expected_total = None
    while True:
        params["StartIndex"] = start
        response = session.get(f"{EMBY_URL}/emby/Items", params=params)
        response.raise_for_status()
        data = response.json()
        batch = data.get("Items")
        if not isinstance(batch, list):
            raise ValueError(tr('Incomplete Emby library pagination'))
        total = data.get("TotalRecordCount")
        if total is not None:
            if type(total) is not int or total < 0 or (expected_total is not None and total != expected_total):
                raise ValueError(tr('Incomplete Emby library pagination'))
            expected_total = total
        if not batch:
            if expected_total is not None and start < expected_total:
                raise ValueError(tr('Incomplete Emby library pagination'))
            break
        for item in batch:
            if not item.get("Id") or item["Id"] in seen:
                raise ValueError(tr('Incomplete Emby library pagination'))
            seen.add(item["Id"])
        items.extend(batch)
        start += len(batch)
        if expected_total is not None and start >= expected_total:
            if start != expected_total:
                raise ValueError(tr('Incomplete Emby library pagination'))
            break
        if expected_total is None and len(batch) < params["Limit"]:
            break
    return items

def build_emby_tmdb_map(items):
    'Build a reusable index from TMDb IDs to Emby item IDs.'
    tmdb_map = {}
    for item in items:
        tmdb_id = item.get("ProviderIds", {}).get("Tmdb")
        if tmdb_id:
            tmdb_map[str(tmdb_id)] = item["Id"]
    return tmdb_map

def get_original_poster(tmdb_id, item_type="movie", strict_original=False):
    'Find a portrait poster in the original language.'
    try:
        # 1. Look up the original language.
        detail_url = f"https://api.themoviedb.org/3/{item_type}/{tmdb_id}"
        detail_response = session.get(detail_url, params={"api_key": TMDB_API_KEY}, proxies=PROXIES, timeout=5)
        detail_response.raise_for_status()
        detail_res = detail_response.json()
        orig_lang = detail_res.get("original_language") or ("" if strict_original else "en")
        
        # 2. Fetch all posters without filtering by language.
        img_url = f"https://api.themoviedb.org/3/{item_type}/{tmdb_id}/images"
        img_response = session.get(img_url, params={"api_key": TMDB_API_KEY}, proxies=PROXIES, timeout=5)
        img_response.raise_for_status()
        img_res = img_response.json()
        posters = img_res.get("posters", [])
        
        # 3. Select the first poster matching the original language.
        for p in posters:
            if orig_lang and p.get("iso_639_1") == orig_lang and p.get("file_path"):
                return p.get("file_path")

        if strict_original:
            return ""
        
        # 4. Fall back to the first available poster or the default poster path.
        if posters:
            return posters[0].get("file_path")
        return detail_res.get("poster_path", "")
    except Exception:
        return ""

def upload_poster_to_emby(col_id, poster_path, col_name, only_if_missing=False):
    'Upload a Base64 poster and refresh the Emby image cache.'
    if not poster_path: return False
    
    # Use the configured image size; w780 reduces daily download traffic.
    image_url = f"https://image.tmdb.org/t/p/{POSTER_SIZE}{poster_path}"
    try:
        img_res = session.get(image_url, proxies=PROXIES, timeout=15)
        if img_res.status_code == 200:
            # 1. Encode the image as Base64 for Emby.
            b64_image = base64.b64encode(img_res.content).decode('utf-8')
            mime_type = img_res.headers.get('Content-Type', 'image/jpeg')
            
            # Recheck missing media images; collection posters retain their replacement behavior.
            if only_if_missing:
                check = session.get(f"{EMBY_URL}/emby/Items/{col_id}/Images", params={"api_key": EMBY_API_KEY}, timeout=10)
                check.raise_for_status()
                if any(image.get("ImageType") == "Primary" for image in check.json()):
                    print(tr('    ⏭️ [{v0}] already has a primary image; skipping', v0=col_name))
                    return None
            url = f"{EMBY_URL}/emby/Items/{col_id}/Images/Primary"
            # Declare the image MIME type and send a Base64 body.
            headers = {"Content-Type": mime_type}
            
            res = session.post(
                url, params={"api_key": EMBY_API_KEY}, data=b64_image, 
                headers=headers, proxies={"http": None, "https": None}, timeout=10
            )
            
            if res.status_code in [200, 204]:
                if only_if_missing:
                    check = session.get(f"{EMBY_URL}/emby/Items/{col_id}/Images", params={"api_key": EMBY_API_KEY}, timeout=10)
                    check.raise_for_status()
                    if not any(image.get("ImageType") == "Primary" for image in check.json()):
                        print(tr('    ⚠️ [{v0}] upload accepted, but primary image not yet confirmed', v0=col_name))
                        return False
                # Refresh the Emby image cache.
                try:
                    if not only_if_missing:
                        session.post(
                            f"{EMBY_URL}/emby/Items/{col_id}/Refresh",
                            params={"api_key": EMBY_API_KEY, "Recursive": False, "ImageRefreshMode": "FullRefresh"},
                            timeout=5
                        )
                except Exception: pass
                
                print(tr('    🖼️ Poster uploaded: {v0}', v0=col_name))
                return True
            else:
                print(tr('    ⚠️ [{v0}] poster upload rejected, status: {v1}', v0=col_name, v1=res.status_code))
                return False
                
    except Exception as e:
        print(tr('    ⚠️ Poster upload error: {v0}', v0=type(e).__name__))
    return False

def fix_missing_media_posters(items):
    'Queue original-language posters only for movies and shows without a primary image.'
    missing = [item for item in items if item.get("Type") in ("Movie", "Series")
               and not (item.get("ImageTags") or {}).get("Primary")]
    for item_type, label in (("Movie", tr('Movies')), ("Series", tr('TV Shows'))):
        print(tr('  [Scan] {v0} without primary images: {v1}', v0=label, v1=sum((item.get('Type') == item_type for item in missing))))
    for item in missing:
        item_type = item["Type"]
        label = tr('Movies') if item_type == "Movie" else tr('TV Shows')
        year = item.get("ProductionYear") or (item.get("PremiereDate") or "")[:4]
        name = f"{label}：{item['Name']}" + (f" ({year})" if year else "")
        tmdb_id = (item.get("ProviderIds") or {}).get("Tmdb")
        if not tmdb_id:
            print(tr('  [Skip] {v0}: missing TMDb ID', v0=name))
            sync_stats["poster_failed"].append(tr('{v0} (missing TMDb ID)', v0=name))
            continue
        poster_path = get_original_poster(tmdb_id, "movie" if item_type == "Movie" else "tv", strict_original=True)
        if not poster_path:
            print(tr('  [Skip] {v0}: original-language poster unavailable; check TMDb images or network', v0=name))
            sync_stats["poster_failed"].append(tr('{v0} (original-language poster unavailable)', v0=name))
            continue
        print(tr('  [Pending repair] {v0}', v0=name))
        sync_stats["pending_posters"].append({"id": item["Id"], "path": poster_path,
                                            "name": name, "media_type": item_type})

def fix_missing_collection_posters():
    'Repair missing collection posters from the earliest title, excluding configured lists.'
    # Exclude configured lists and country collections from generic poster repair.
    exclude_names = [lst["name"] for lst in CUSTOM_LISTS] + \
                    [lst["name"] for lst in DOUBAN_GENRE_LISTS] + \
                    [lst["name"] for lst in DOUBAN_TV_LISTS] + \
                    [country_collection_name(code, kind) for code in COUNTRY_CODES for kind in ("Movie", "Series")]
    
    print("\n" + "="*45 + tr('\n🖼️ Stage 4: Repair missing collection and media posters (excluding list collections)\n') + "="*45)
    try:
        collections = get_emby_items("BoxSet", "ImageTags")

        fixed_count = 0
        for col in collections:
            col_name = col["Name"]
            # Skip collections handled by the list/country sync steps.
            if col_name in exclude_names:
                continue
            # Check for a missing primary image.
            if "Primary" not in col.get("ImageTags", {}):
                col_id = col["Id"]
                col_name = col["Name"]
                print(tr('  [Scan] Collection without a poster: {v0}; checking...', v0=col_name))

                # Read collection members in ascending premiere-date order.
                items_in_col = get_emby_items("", "PremiereDate,ProviderIds", ParentId=col_id,
                                              Recursive=False, SortBy="PremiereDate")

                if items_in_col:
                    # Find the first title with a TMDb ID.
                    for item in items_in_col:
                        tmdb_id = item.get("ProviderIds", {}).get("Tmdb")
                        if tmdb_id:
                            item_type = "movie" if item.get("Type") == "Movie" else "tv"
                            poster_path = get_original_poster(tmdb_id, item_type)
                            if poster_path:
                                sync_stats["pending_posters"].append({"id": col_id, "path": poster_path, "name": col_name, "is_fixed_cover": True})
                                fixed_count += 1
                            break # Try only the earliest eligible title, whether or not a poster is available.
                            
        if fixed_count > 0:
            print(tr('✅ Scan complete: {v0} collection posters queued for repair', v0=fixed_count))
        else:
            print(tr('✅ Scan complete: no collection posters need repair'))
            
    except Exception as e:
        print(tr('  [Error] Collection poster repair failed: {v0}', v0=e))

def update_collection_by_name(name, item_ids, list_desc="", poster_path=""):
    """Keep daily rebuild ordering; finish the replacement before removing old collections.

    Collection names configured here remain reserved for this script.
    No cleanup of unrelated or removed-from-config collections is performed.
    """
    if not item_ids:
        print(tr('  [Skip] No local matches for [{v0}]; keeping the existing collection', v0=name))
        sync_stats['failed_lists'].append(name)
        return False
    col_id = None
    replacement_ready = False
    try:
        collections = get_emby_items("BoxSet")
        target_names = [name] + OLD_COLLECTION_NAMES.get(name, [])
        old_collections = [item for item in collections if item["Name"] in target_names]
        # Use a temporary unique name: Emby may otherwise return an existing same-name collection.
        temporary_name = f"{name} [sync-{time.time_ns()}]"
        create_res = session.post(f"{EMBY_URL}/emby/Collections", params={
            "api_key": EMBY_API_KEY, "Name": temporary_name, "Ids": ",".join(item_ids[:BATCH_SIZE])
        })
        create_res.raise_for_status()
        col_id = create_res.json().get("Id")
        if not col_id or col_id in {item["Id"] for item in old_collections}:
            col_id = None
            raise ValueError(tr('Cannot obtain the newly created collection ID'))
        for index in range(BATCH_SIZE, len(item_ids), BATCH_SIZE):
            response = session.post(f"{EMBY_URL}/emby/Collections/{col_id}/Items", params={
                "api_key": EMBY_API_KEY, "Ids": ",".join(item_ids[index:index+BATCH_SIZE])})
            response.raise_for_status()
        # A successful HTTP response alone does not prove all members were added.
        for attempt in range(3):
            members = get_emby_items("", fields="", ParentId=col_id, Recursive=False)
            if {item["Id"] for item in members} == set(item_ids):
                break
            if attempt < 2:
                time.sleep(1)
        else:
            raise ValueError(tr('New collection membership verification failed; keeping the old collection'))
        users = get_emby_users()
        if not users:
            raise ValueError(tr('Emby user list is empty; keeping the old collection'))
        response = session.get(f"{EMBY_URL}/emby/Users/{users[0]['Id']}/Items/{col_id}",
                               params={"api_key": EMBY_API_KEY})
        response.raise_for_status()
        metadata = response.json()
        metadata["Name"] = name
        if list_desc:
            metadata["Overview"] = list_desc
        response = session.post(f"{EMBY_URL}/emby/Items/{col_id}", params={"api_key": EMBY_API_KEY}, json=metadata)
        response.raise_for_status()
        replacement_ready = True
        for old in old_collections:
            response = session.delete(f"{EMBY_URL}/emby/Items/{old['Id']}", params={"api_key": EMBY_API_KEY})
            response.raise_for_status()
        print(tr('📦 [Success] Collection rebuilt: {v0} ({v1} items)', v0=name, v1=len(item_ids)))
        add_to_all_users_favorites(col_id, name)
        if poster_path:
            sync_stats["pending_posters"].append({"id": col_id, "path": poster_path, "name": name})
        return True
    except Exception as error:
        print(tr('Collection rebuild failed: {name} ({error})', name=name, error=safe_text(error)))
        sync_stats["failed_lists"].append(name)
        # Only remove our newly allocated, unfinished container. Never clean up by name here.
        if col_id and not replacement_ready:
            try:
                response = session.delete(f"{EMBY_URL}/emby/Items/{col_id}", params={"api_key": EMBY_API_KEY})
                response.raise_for_status()
            except Exception as cleanup_error:
                print(tr('Temporary collection cleanup failed: {id} ({error})', id=col_id, error=safe_text(cleanup_error)))
        return False

def fetch_tmdb_list_data(list_id):
    items, description, seen = [], "", set()
    page, version, expected_total = 1, 3, None
    while True:
        params = {"api_key": TMDB_API_KEY, "language": "en-US" if LANGUAGE == "en" else LANGUAGE, "page": page}
        headers = {}
        if version == 4:
            params.pop("api_key")
            headers["Authorization"] = f"Bearer {TMDB_ACCESS_TOKEN}"
        response = session.get(f"https://api.themoviedb.org/{version}/list/{list_id}",
                               params=params, headers=headers, proxies=PROXIES, timeout=10)
        if response.status_code == 404 and version == 3 and page == 1 and TMDB_ACCESS_TOKEN:
            version = 4
            continue
        response.raise_for_status()
        data = response.json()
        batch = data.get("results", data.get("items"))
        pages = data.get("total_pages", 1)
        total = data.get("total_results", data.get("item_count"))
        if (not isinstance(batch, list) or type(pages) is not int or pages < 0
                or (page > 1 and not batch) or (page < pages and not batch)):
            raise ValueError(tr('Incomplete TMDb list pagination: {id}', id=list_id))
        if page == 1:
            description = data.get("description") or ""
            expected_total = total
        elif total != expected_total:
            raise ValueError(tr('Incomplete TMDb list pagination: {id}', id=list_id))
        for item in batch:
            ident = (item.get("media_type"), item.get("id"))
            if not item.get("id") or ident in seen:
                raise ValueError(tr('Incomplete TMDb list pagination: {id}', id=list_id))
            seen.add(ident)
        items.extend(batch)
        if page >= pages:
            break
        page += 1
        time.sleep(0.2)
    if expected_total is not None and expected_total != len(items):
        raise ValueError(tr('Incomplete TMDb list pagination: {id}', id=list_id))
    return items, description

def get_existing_mp_subscriptions():
    """Only movie subscriptions belong in this ID set; TV checks are per season."""
    if not MP_ENABLE:
        return set()
    response = session.get(f"{MP_URL.rstrip('/')}/api/v1/subscribe/",
                           headers={"X-API-KEY": MP_API_TOKEN},
                           proxies={"http": None, "https": None}, timeout=10)
    response.raise_for_status()
    data = response.json()
    items = data if isinstance(data, list) else data.get("data")
    if not isinstance(items, list):
        raise ValueError(tr('Invalid MP subscription list'))
    return {str(item.get("media_id") or item.get("tmdbid")) for item in items
            if item.get("type") in (MP_MEDIA_TYPES["Movie"], "Movie", "movie")
            and item.get("media_source") in (None, "tmdb")
            and (item.get("media_id") or item.get("tmdbid"))}

def subscribe_to_moviepilot(name, year, tmdb_id, item_type):
    'Submit a MoviePilot subscription.'
    empty_detail = {"created_seasons": 0, "existed_seasons": 0, "failed_seasons": 0}
    if not MP_ENABLE: return False, tr('Subscriptions disabled'), empty_detail
    
    # Remove trailing slashes before constructing API paths.
    base_url = MP_URL.rstrip('/')
    headers = {"Content-Type": "application/json", "X-API-KEY": MP_API_TOKEN}
    mp_timeout = (10, 60)  # Connect timeout: 10 seconds; read timeout: 60 seconds.
    # Use MoviePilot's protocol-specific media type values.
    mp_type = MP_MEDIA_TYPES[item_type]
    
    payload = {
        "name": name,
        "year": year,
        "type": mp_type,
        "media_source": "tmdb",
        "media_id": str(tmdb_id)
    }

    # Fetch the complete season list before creating TV subscriptions.
    # Season 0 means specials, not all seasons; subscribe to it when present.
    if item_type == "Series":
        try:
            seasons_res = session.get(
                f"{base_url}/api/v1/media/seasons",
                headers=headers,
                params={"media_source": "tmdb", "media_id": str(tmdb_id)},
                proxies={"http": None, "https": None}, timeout=mp_timeout
            )
            if seasons_res.status_code != 200:
                return False, tr('Season lookup failed (HTTP {v0})', v0=seasons_res.status_code), empty_detail

            seasons_payload = seasons_res.json()
            if isinstance(seasons_payload, dict) and "data" in seasons_payload:
                if seasons_payload.get("success") is False:
                    reason = seasons_payload.get("message") or str(seasons_payload)
                    return False, tr('Season lookup failed ({v0})', v0=reason), empty_detail
                seasons_data = seasons_payload.get("data")
            else:
                seasons_data = seasons_payload
            if not isinstance(seasons_data, list):
                return False, tr('Invalid season response ({v0})', v0=safe_text(seasons_payload)[:80]), empty_detail

            seasons = []
            for season_info in seasons_data:
                try:
                    season = int(season_info.get("season_number"))
                except (TypeError, ValueError, AttributeError):
                    continue
                if season >= 0:
                    seasons.append(season)
            seasons = sorted(set(seasons))

            if not seasons:
                return False, tr('MP returned no seasons'), empty_detail

            created_seasons = []
            existed_seasons = []
            failed_seasons = []

            for season in seasons:
                # Check duplicates per season, not just by TV show ID.
                check_res = session.get(
                    f"{base_url}/api/v1/subscribe/media/{tmdb_id}",
                    headers=headers,
                    params={"media_source": "tmdb", "season": season},
                    proxies={"http": None, "https": None}, timeout=mp_timeout
                )
                check_res.raise_for_status()
                check_data = check_res.json()
                if not isinstance(check_data, dict) or check_data.get("success") is False:
                    raise ValueError(tr('Invalid MP duplicate-check response'))
                if "data" in check_data:
                    check_data = check_data.get("data") or {}
                if not isinstance(check_data, dict):
                    raise ValueError(tr('Invalid MP duplicate-check response'))
                if check_data.get("id"):
                    existed_seasons.append(season)
                    print(tr('      -> Season {v0} already exists in MP; skipping', v0=season))
                    continue

                season_payload = payload.copy()
                season_payload["season"] = season
                res = session.post(
                    f"{base_url}/api/v1/subscribe/",
                    headers=headers, json=season_payload,
                    proxies={"http": None, "https": None}, timeout=mp_timeout
                )

                if res.status_code == 200:
                    data = res.json()
                    if data.get("success") is True or data.get("code") == 0:
                        created_seasons.append(season)
                        print(tr('      -> Season {v0} subscribed', v0=season))
                        continue
                    reason = data.get("message") or str(data)
                else:
                    reason = f"HTTP {res.status_code}"

                failed_seasons.append(tr('Season {v0}: {v1}', v0=season, v1=reason))

            if failed_seasons:
                summary = "；".join(failed_seasons)
                if created_seasons:
                    summary += tr(' (succeeded: {v0})', v0=created_seasons)
                return False, tr('Some season subscriptions failed ({v0})', v0=summary), {
                    "created_seasons": len(created_seasons),
                    "existed_seasons": len(existed_seasons),
                    "failed_seasons": len(failed_seasons)
                }

            if not created_seasons and existed_seasons:
                return True, tr('All seasons already exist'), {
                    "created_seasons": 0,
                    "existed_seasons": len(existed_seasons),
                    "failed_seasons": 0
                }
            return True, "", {
                "created_seasons": len(created_seasons),
                "existed_seasons": len(existed_seasons),
                "failed_seasons": 0
            }

        except requests.exceptions.Timeout:
            return False, tr('Season lookup/subscription timed out (connect 10s/read 60s)'), empty_detail
        except Exception as e:
            return False, tr('Season subscription error: {v0}', v0=safe_text(e)[:50]), empty_detail
    
    try:
        res = session.post(
            f"{base_url}/api/v1/subscribe/",
            headers=headers, json=payload,
            proxies={"http": None, "https": None}, timeout=mp_timeout
        )
        if res.status_code == 200:
            data = res.json()
            if data.get("success") == True or data.get("code") == 0:
                return True, "", empty_detail
            return False, tr('API rejected the request ({v0})', v0=data.get('message') or str(data)), empty_detail
        return False, tr('HTTP status error {v0}', v0=res.status_code), empty_detail
    except requests.exceptions.Timeout: return False, tr('Request timed out (connect 10s/read 60s)'), empty_detail
    except Exception as e: return False, tr('Error: {v0}', v0=safe_text(e)[:30]), empty_detail

def process_custom_list(list_info, mp_existing_ids, emby_tmdb_maps, is_genre=False):
    name = list_info["name"]
    list_id = list_info["id"]
    item_type = list_info.get("type", "Movie")
    tmdb_item_type = "movie" if item_type == "Movie" else "tv"
    mp_sub_switch = list_info.get("mp_subscribe", False)
    
    print(tr('\n🔍 Synchronizing TMDb list: {v0}', v0=name))
    try:
        tmdb_items, list_desc = fetch_tmdb_list_data(list_id)
    except Exception as error:
        sync_stats["failed_lists"].append(name)
        print(tr('List fetch failed; keeping the existing collection: {name} ({error})', name=name, error=safe_text(error)))
        return
    # Mixed movie/TV lists must not match coincidentally identical TMDb IDs.
    tmdb_items = [item for item in tmdb_items if item.get("media_type", tmdb_item_type) == tmdb_item_type]
    
    if not tmdb_items:
        print(tr('  [Warning] Empty TMDb list; check the list ID or network. Existing collection retained.'))
        sync_stats["failed_lists"].append(name)
        return

    # Reuse the library index built by process() rather than scanning for every list.
    emby_tmdb_map = emby_tmdb_maps[item_type]

    # Select a poster according to the configured strategy.
    poster_path = ""
    target_tmdb_id = None
    
    if tmdb_items:
        if LIST_POSTER_MODE == "library":
            for item in tmdb_items:
                if str(item.get("id")) in emby_tmdb_map:
                    target_tmdb_id = item.get("id")
                    print(tr('    ✨ First local match -> poster from {v0}', v0=item.get('title') or item.get('name')))
                    break
        else:
            target_tmdb_id = tmdb_items[0].get("id")
            
        if target_tmdb_id:
            poster_path = get_original_poster(target_tmdb_id, tmdb_item_type)

    matched_ids = []
    missing_items = []
    
    for idx, item in enumerate(tmdb_items, 1):
        t_id = str(item.get("id"))
        t_title = item.get("title") or item.get("name") or tr('Unknown title')
        t_year = (item.get("release_date") or item.get("first_air_date") or "")[:4]
        display_name = f"{t_title} ({t_year})"
        
        if t_id in emby_tmdb_map:
            matched_ids.append(emby_tmdb_map[t_id])
            print(tr('  [{v0:03d}] 🟢 Matched: {v1}', v0=idx, v1=display_name))
        else:
            missing_info = f"No.{idx} {display_name} {{tmdb-{t_id}}}"
            missing_items.append(missing_info)
            print(tr('  [{v0:03d}] ❌ Missing: {v1}', v0=idx, v1=missing_info))
            
            should_subscribe = False
            
            if mp_sub_switch is True:
                should_subscribe = True
            # Python bool is a subclass of int; exclude booleans from numeric thresholds.
            elif isinstance(mp_sub_switch, int) and not isinstance(mp_sub_switch, bool):
                # List ranks start at 1.
                if idx <= mp_sub_switch:
                    should_subscribe = True
                else:
                    print(tr('    -> ⏭️ Rank {v0} exceeds threshold ({v1}); report only', v0=idx, v1=mp_sub_switch))
            
            # Use the exclusion list for the matching media type.
            current_exclude_list = MP_EXCLUDE_MOVIE_IDS if item_type == "Movie" else MP_EXCLUDE_SERIES_IDS
            
            # Apply MoviePilot subscription policy and duplicate checks.
            if MP_ENABLE and should_subscribe:
                if t_id in current_exclude_list:
                    print(tr('    -> 🚫 Excluded from subscriptions'))
                    sync_stats["mp_excluded"] += 1
                    if item_type == "Movie":
                        sync_stats["mp_movie_excluded"] += 1
                    else:
                        sync_stats["mp_series_excluded"] += 1
                # Deduplicate movies by TMDb ID and TV shows by season.
                elif item_type == "Movie" and t_id in mp_existing_ids:
                    print(tr('    -> 🍿 Already in MP; skipping duplicate subscription'))
                    sync_stats["mp_existed"] += 1
                    sync_stats["mp_movie_existed"] += 1
                elif item_type == "Series" and t_id in mp_processed_series_ids:
                    print(tr('    -> 🍿 TV show already processed during this run; skipping duplicate'))
                else:
                    success, reason, mp_detail = subscribe_to_moviepilot(t_title, t_year, t_id, item_type)
                    if item_type == "Series":
                        mp_processed_series_ids.add(t_id)
                        created_seasons = mp_detail["created_seasons"]
                        existed_seasons = mp_detail["existed_seasons"]
                        failed_seasons = mp_detail["failed_seasons"]
                        sync_stats["mp_season_subscribed"] += created_seasons
                        sync_stats["mp_season_existed"] += existed_seasons
                        sync_stats["mp_season_failed"] += failed_seasons
                        if created_seasons:
                            sync_stats["mp_series_subscribed"] += 1
                        # A show can have both existing and newly subscribed seasons; count both.
                        if existed_seasons:
                            sync_stats["mp_series_existed"] += 1
                        if not success:
                            sync_stats["mp_series_failed"] += 1
                    if success:
                        if reason == tr('All seasons already exist'):
                            print(tr('    -> 🍿 All seasons already exist in MP; skipping'))
                            sync_stats["mp_existed"] += 1
                        else:
                            print(tr('    -> 🍿 MP subscription submitted'))
                            sync_stats["mp_subscribed"] += 1
                            if item_type == "Movie":
                                sync_stats["mp_movie_subscribed"] += 1
                        if item_type == "Movie":
                            mp_existing_ids.add(t_id) # Movie and TV TMDb IDs belong to separate namespaces.
                    else:
                        print(tr('    -> ❌ MP subscription failed: {v0}', v0=reason))
                        if item_type == "Movie":
                            sync_stats["mp_movie_failed"] += 1
                        sync_stats["mp_failed"].append(tr('{v0} (reason: {v1})', v0=t_title, v1=reason))
            
    sync_ok = False
    unique_ids = list(dict.fromkeys(matched_ids))
    if len(unique_ids) >= 2:
        sync_ok = update_collection_by_name(name, unique_ids, list_desc, poster_path)
    else:
        print(tr('  [Skip] Fewer than 2 local matches ({v0}); keeping existing collection', v0=len(unique_ids)))
        sync_stats["failed_lists"].append(name)

    # Show missing-title details unless explicitly disabled.
    sync_stats["lists_report"][name] = {
        "is_genre": is_genre, "id": list_id, "type": item_type, "total": len(tmdb_items),
        "matched": len(matched_ids), "missing": missing_items,
        "notify_missing": list_info.get("notify_missing", True), "sync_ok": sync_ok
    }

def normalize_country_code(source):
    """Resolve codes, localized names, and aliases without fuzzy substring matching."""
    text = str(source).strip()
    alias = COUNTRY_ALIASES.get(text.casefold())
    if alias:
        return alias
    code = text.upper()
    if code in SUPPORTED_COUNTRY_CODES:
        return code
    for candidate, labels in COUNTRY_LABELS.items():
        if any(text.casefold() == label.casefold() for label in labels):
            return candidate
    return text


def country_display_name(source, language=None):
    """Use a configured translation, preserving unknown names without guessing."""
    labels = COUNTRY_LABELS.get(normalize_country_code(source))
    if labels is None:
        return str(source).strip()
    return labels[("zh-CN", "zh-TW", "en").index(language or LANGUAGE)]


def country_collection_name(code, item_type):
    if code is None or normalize_country_code(code) == "CN":
        return tr('Chinese Movies') if item_type == "Movie" else tr('Chinese TV Shows')
    label = country_display_name(code)
    kind = tr('Movies') if item_type == "Movie" else tr('TV Shows')
    return f"{label}{' ' if LANGUAGE == 'en' else ''}{kind}"


def country_cache_path():
    return Path(os.getenv("EMBY_SYNC_CACHE", str(Path(__file__).with_name(".emby_country_cache.json"))))


def load_country_cache():
    global COUNTRY_CACHE
    try:
        data = json.loads(country_cache_path().read_text(encoding="utf-8"))
        COUNTRY_CACHE = data if isinstance(data, dict) else {}
    except FileNotFoundError:
        COUNTRY_CACHE = {}
    except (ValueError, OSError):
        COUNTRY_CACHE = {}
        print(tr('Cannot read country cache; querying again'))


def save_country_cache():
    target = country_cache_path()
    temporary = None
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=target.parent, delete=False) as handle:
            temporary = handle.name
            json.dump(COUNTRY_CACHE, handle, ensure_ascii=False)
        os.replace(temporary, target)
    except OSError as error:
        print(tr('Cannot save country cache: {error}', error=safe_text(error)))
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def get_country_codes(tmdb_id, item_type):
    media_type = "movie" if item_type == "Movie" else "tv"
    key = f"{media_type}:{tmdb_id}"
    cached = COUNTRY_CACHE.get(key)
    valid = (isinstance(cached, dict) and isinstance(cached.get("codes"), list)
             and all(code in SUPPORTED_COUNTRY_CODES for code in cached["codes"])
             and isinstance(cached.get("time"), (int, float)))
    if valid and time.time() - cached["time"] < COUNTRY_CACHE_DAYS * 86400:
        return cached["codes"]
    try:
        response = session.get(f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}",
                               params={"api_key": TMDB_API_KEY}, proxies=PROXIES, timeout=10)
        # A missing TMDb entry is item-specific, not a failure of the whole library scan.
        if response.status_code == 404:
            COUNTRY_CACHE.pop(key, None)
            return None
        response.raise_for_status()
        data = response.json()
        raw = data.get("production_countries") if item_type == "Movie" else data.get("origin_country")
        if not isinstance(raw, list):
            raise ValueError(tr('Invalid TMDb country data'))
        codes = [item["iso_3166_1"] for item in raw] if item_type == "Movie" else raw
        if any(code not in SUPPORTED_COUNTRY_CODES for code in codes):
            raise ValueError(tr('Invalid TMDb country data'))
        COUNTRY_CACHE[key] = {"codes": codes, "time": time.time()}
        return codes
    except Exception:
        if valid:
            print(tr('Country lookup failed; using cached data: {id}', id=key))
            return cached["codes"]
        raise


def process_country_collections(all_movies, all_series):
    if not COUNTRY_CODES:
        return
    load_country_cache()
    sort_key = "DateCreated" if DOMESTIC_POSTER_MODE == "added" else "PremiereDate"
    groups = COUNTRY_CODES
    # Match the original order: TV before movies; countries follow the configured priority.
    for item_type, library in (("Series", all_series), ("Movie", all_movies)):
        matches = {code: [] for code in groups}
        complete = True
        for item in library:
            tmdb_id = (item.get("ProviderIds") or {}).get("Tmdb")
            if not tmdb_id:
                print(tr('Cannot determine country; missing TMDb ID: {name}', name=item.get("Name", item["Id"])))
                continue
            try:
                codes = get_country_codes(tmdb_id, item_type)
            except Exception as error:
                print(tr('Country lookup failed; keeping existing country collections for this media type: {name} ({error})',
                         name=item.get("Name", item["Id"]), error=safe_text(error)))
                complete = False
                break
            if codes is None:
                print(tr('TMDb entry not found; skipping country classification: {name} ({type}:{id})',
                         name=item.get("Name", item["Id"]), type="movie" if item_type == "Movie" else "tv", id=tmdb_id))
                continue
            for group in groups:
                if set(codes) & set(TMDB_DOMESTIC_CODES if group == "CN" else [group]):
                    if item not in matches[group]:
                        matches[group].append(item)
        if not complete:
            sync_stats["failed_lists"].extend(country_collection_name(code, item_type) for code in groups)
            continue
        for group in reversed(groups):
            name = country_collection_name(group, item_type)
            media = sorted(matches[group], key=lambda item: item.get(sort_key) or "0000-00-00", reverse=True)
            poster = ""
            for item in media:
                tmdb_id = (item.get("ProviderIds") or {}).get("Tmdb")
                if tmdb_id:
                    poster = get_original_poster(tmdb_id, "movie" if item_type == "Movie" else "tv")
                    if poster:
                        break
            update_collection_by_name(name, [item["Id"] for item in media], "", poster)
            sync_stats["country_reports"].append((name, len(media)))
    save_country_cache()


def process():
    global MP_ENABLE
    start_time = time.time()
    
    if USE_PROXY: print(tr('🌍 TMDb proxy enabled'))
    
    # Load existing MoviePilot subscriptions for duplicate checks.
    mp_existing_ids = set()
    if MP_ENABLE: 
        print(tr('🍿 MoviePilot subscriptions enabled -> {v0}', v0=MP_URL))
        try:
            mp_existing_ids = get_existing_mp_subscriptions()
        except Exception as error:
            MP_ENABLE = False
            sync_stats["mp_failed"].append(tr('MP duplicate lookup failed; subscriptions disabled for this run: {error}', error=safe_text(error)))
            print(sync_stats["mp_failed"][-1])

    # Load the Emby library once and reuse it for lists and country collections.
    print(tr('\n📚 Loading Emby library index...'))
    all_movies = get_emby_items("Movie")
    all_series = get_emby_items("Series")
    emby_tmdb_maps = {
        "Movie": build_emby_tmdb_map(all_movies),
        "Series": build_emby_tmdb_map(all_series),
    }
    print(tr('✅ Emby index loaded: {v0} movies, {v1} TV shows', v0=len(all_movies), v1=len(all_series)))

    # Stage 1: create category collections first so they sort behind core lists.
    print("\n" + "="*45 + tr('\n📂 Stage 1: Synchronize Douban category lists\n') + "="*45)
    # Create in reverse configuration order so the first entry appears first.
    for lst in reversed(DOUBAN_GENRE_LISTS + DOUBAN_TV_LISTS):
        process_custom_list(lst, mp_existing_ids, emby_tmdb_maps, is_genre=True)

    # Stage 2: synchronize core lists.
    print("\n" + "="*45 + tr('\n🎬 Stage 2: Synchronize core lists\n') + "="*45)
    # Create the first configured core list last so it sorts ahead of the others.
    for lst in reversed(CUSTOM_LISTS): 
        process_custom_list(lst, mp_existing_ids, emby_tmdb_maps, is_genre=False)
	
    # Stage 3: create country collections last so they appear first.
    print("\n" + "="*45 + tr('\n🌏 Stage 3: Build country/region collections...\n') + "="*45)
    
    process_country_collections(all_movies, all_series)

    # Stage 4: repair missing collection, movie, and TV posters.
    fix_missing_collection_posters()
    fix_missing_media_posters(all_movies + all_series)

    # Stage 5: upload queued posters and refresh image caches.
    list_poster_count = 0
    if sync_stats["pending_posters"]:
        print("\n" + "="*45 + tr('\n🖼️ Stage 5: Upload queued posters and refresh image caches\n') + "="*45)
        print(tr('  ⏳ Waiting 5 seconds for Emby background processing...'))
        time.sleep(5)
        
        for p in sync_stats["pending_posters"]:
            poster_injected = upload_poster_to_emby(p["id"], p["path"], p["name"], only_if_missing=bool(p.get("media_type")))
            if poster_injected is None:
                continue
            if poster_injected and p.get("media_type"):
                sync_stats["fixed_media_covers"][p["media_type"]].append(p["name"])
            elif poster_injected and p.get("is_fixed_cover"):
                sync_stats["fixed_covers"] += 1
                sync_stats["fixed_cover_names"].append(p["name"])
            elif poster_injected:
                list_poster_count += 1
            elif not poster_injected:
                sync_stats["poster_failed"].append(p["name"])
            time.sleep(0.5) # Pause briefly between consecutive requests.

    # Stage 6: build and send the report.
    report = [tr('📊 Emby collection sync summary'), "━━━━━━━━━━━━━━"]
    genre_matched = 0
    tv_genre_matched = 0
    lb_genre_matched = 0
    
    for list_name, data in reversed(list(sync_stats["lists_report"].items())):
        if data.get("is_genre"):
            if data["matched"] >= 2:
                if data.get("type") == "Series":
                    tv_genre_matched += 1
                else:
                    genre_matched += 1
        elif (
            list_name.startswith(("LB Top 100 ", "LB Top 250 "))
            and list_name.endswith(" Films")
        ):
            if data["matched"] >= 2:
                lb_genre_matched += 1
        else:
            # Use the README icons for bundled lists and media-type icons for custom lists.
            icon = LIST_EMOJIS.get(str(data.get("id")), "📺" if data.get("type") == "Series" else "🎬")
            
            # Show a check mark when nothing is missing; otherwise show the missing count.
            missing_count = len(data['missing'])
            missing_text = "✅" if missing_count == 0 else tr('({v0} missing)', v0=missing_count)
            
            # Build one report line per core list.
            report.append(f"{icon} {list_name}: {data['matched']}/{data['total']} {missing_text}")
        
    report.extend([
        f"", tr('🎬 Letterboxd genre lists: {v0} collections meet the match threshold', v0=lb_genre_matched),
        tr('📂 Douban movie categories: {v0} collections meet the match threshold', v0=genre_matched),
        tr('📺 Douban TV categories: {v0} collections meet the match threshold', v0=tv_genre_matched), tr('🌏 Country/region collections')
    ])
    
    for name, count in reversed(sync_stats["country_reports"]):
        report.append(tr('  - {name}: items: {count}', name=name, count=count))
    if sync_stats["failed_lists"]:
        report.append(tr('⚠️ Failed/skipped collections: {names}', names=" / ".join(sync_stats["failed_lists"])))

    # Report movie and TV subscriptions separately, including season counts.
    if MP_ENABLE:
        report.append(tr('🍿 MP subscription status:'))
        movie_status = []
        for label, key in (
            (tr('New'), "mp_movie_subscribed"),
            (tr('Existing'), "mp_movie_existed"),
            (tr('Excluded'), "mp_movie_excluded"),
            (tr('Failed'), "mp_movie_failed"),
        ):
            if sync_stats[key] > 0:
                movie_status.append(tr('{v0} {v1} titles', v0=label, v1=sync_stats[key]))

        series_status = []
        for label, series_key, season_key in (
            (tr('New'), "mp_series_subscribed", "mp_season_subscribed"),
            (tr('Existing'), "mp_series_existed", "mp_season_existed"),
            (tr('Failed'), "mp_series_failed", "mp_season_failed"),
        ):
            counts = []
            if sync_stats[series_key] > 0:
                counts.append(tr('{v0} titles', v0=sync_stats[series_key]))
            if sync_stats[season_key] > 0:
                counts.append(tr('{v0} seasons', v0=sync_stats[season_key]))
            if counts:
                series_status.append(f"{label} {' / '.join(counts)}")
        if sync_stats["mp_series_excluded"] > 0:
            series_status.append(tr('Excluded {v0} titles', v0=sync_stats['mp_series_excluded']))

        if movie_status:
            report.append(tr('  - Movies: {v0}', v0='，'.join(movie_status)))
        if series_status:
            report.append(tr('  - TV shows: {v0}', v0='，'.join(series_status)))
        if not movie_status and not series_status:
            report.append(tr('  - No subscription changes'))
    else: report.append(tr('🍿 MoviePilot subscriptions disabled'))

    media_cover_status = [tr('{v0} {v1} titles', v0=label, v1=len(sync_stats['fixed_media_covers'][item_type]))
                          for item_type, label in (("Movie", tr('Movies')), ("Series", tr('TV Shows')))
                          if sync_stats["fixed_media_covers"][item_type]]
    if media_cover_status:
        report.append(tr('🛠️ Media posters repaired: {v0}', v0='，'.join(media_cover_status)))

    report.extend([
        tr('⭐ Favorites added (excluded users skipped): {v0}', v0=sync_stats['favs']),
        tr('🖼️ List and country collection posters uploaded: {v0}', v0=list_poster_count),
        tr('🛠️ Other collection posters repaired: {v0}', v0=sync_stats['fixed_covers']),
        tr('⏱️ Duration: {v0} seconds', v0=int(time.time() - start_time)), "━━━━━━━━━━━━━━"
    ])
    
    for list_name, data in reversed(list(sync_stats["lists_report"].items())):
        if not data.get("is_genre") and data["missing"]:
            if data.get("notify_missing", True):
                # Show the first three missing titles for lists with detailed notifications enabled.
                icon = LIST_EMOJIS.get(str(data.get("id")), "📝")
                report.append(tr('\n{v0} [{v1}] Missing titles:', v0=icon, v1=list_name))
                for m in data["missing"][:3]: report.append(f"  • {m}")
                if len(data["missing"]) > 3: report.append(tr('  • ... {v0} titles in total', v0=len(data['missing'])))

    # Append failed MoviePilot subscriptions.
    if sync_stats['mp_failed']:
        report.append(tr('\n⚠️ [Failed MP subscriptions]:'))
        for f in sync_stats['mp_failed'][:3]: report.append(f"  • {f}")
        if len(sync_stats['mp_failed']) > 3: report.append(tr('  • ... {v0} titles in total', v0=len(sync_stats['mp_failed'])))

    # Append failed poster uploads.
    if sync_stats["poster_failed"]:
        report.append(tr('\n🖼️⚠️ [Failed poster lookups/uploads]:'))
        for f in sync_stats["poster_failed"][:3]:
            report.append(f"  • {f}")
        if len(sync_stats["poster_failed"]) > 3:
            report.append(tr('  • ... {v0} items in total', v0=len(sync_stats['poster_failed'])))

    # Append repaired posters.
    fixed_cover_names = sync_stats["fixed_cover_names"] + sync_stats["fixed_media_covers"]["Movie"] + sync_stats["fixed_media_covers"]["Series"]
    if fixed_cover_names:
        report.append(tr('\n🛠️ [Repaired posters]:'))
        for f in fixed_cover_names:
            report.append(f"  • {f}")

    # Print the report before sending it.
    print(tr('[Notification preview]'))
    print("\n".join(report))
    
    # Send the report through Qinglong's notification channel.
    send(tr('Emby collection sync report'), safe_text("\n".join(report)))

if __name__ == "__main__":
    argparse.ArgumentParser(description="Emby Collection Sync").parse_args()
    try:
        initialize()
        process()
    except Exception as error:
        print(tr('Run failed: {error}', error=safe_text(error)))
        sys.exit(1)
