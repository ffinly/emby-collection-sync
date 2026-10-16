# Emby Collection Sync

**简体中文** | [繁體中文](README.zh-TW.md) | [English](README.en.md)

---

🚀 **面向 Emby 影音库的全自动合集管理与追新补片流水线。**

一键同步 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 等权威主榜、全球 9 大权威电影节大奖、豆瓣电影 28 大分类多维度榜单（近期热门、Top 20、高分经典、冷门佳作）及豆瓣电视剧地区与类型榜单，智能排查本地缺失，**并支持自定义排除列表联动 MoviePilot 实现自动化补片**。系统支持自动聚合华语影视，并**原生支持原语言海报直入与灵活的智能抓取策略，结合底层异步队列引擎，彻底解决 Emby 生成默认四宫格封面导致的卡死痛点**。实现从全自动化整理到观影的完整闭环。

## 🔗 线上公开最新榜单列表

以下 TMDB 列表完全由自动化爬虫与 ETL 流水线自动维护。**系统会在每天早上 7:30 (UTC+8) 定时执行数据抓取、比对与同步更新**，确保榜单排名与官方时刻保持一致。

### 🏆 第一/二梯队：大众必看与影史殿堂

* 🍿 **IMDb Top 250 Movies**: [查看网格墙视图](https://www.themoviedb.org/list/8647021?view=grid)
* 📺 **IMDb Top 250 TV Shows**: [查看网格墙视图](https://www.themoviedb.org/list/8647022?view=grid)
* 🎞️ **豆瓣电影 Top 250**: [查看网格墙视图](https://www.themoviedb.org/list/8647023?view=grid)
* 🏛️ **S&S Directors - Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649058?view=grid)
* 🏛️ **S&S Critics - Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649050?view=grid)
* ⭐ **AFI Top 100 (2007)**: [查看网格墙视图](https://www.themoviedb.org/list/8649041?view=grid)
* 📰 **NYT - 100 Best Movies of the 21st Century (2025)**: [查看网格墙视图](https://www.themoviedb.org/list/8701141?view=grid)
* 📡 **NYT - 100 Best TV Shows of the 21st Century (2026)**: [查看网格墙视图](https://www.themoviedb.org/list/8701142?view=grid)

### 🌍 第三梯队：全球最具含金量大奖矩阵

* 🏆 **奥斯卡历届最佳影片**: [查看网格墙视图](https://www.themoviedb.org/list/8648843?view=grid)
* 🌿 **戛纳电影节金棕榈奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648844?view=grid)
* 🎭 **英国电影学院奖最佳影片**: [查看网格墙视图](https://www.themoviedb.org/list/8648848?view=grid)
* 🌐 **金球奖最佳剧情片**: [查看网格墙视图](https://www.themoviedb.org/list/8648849?view=grid)
* 🥂 **金球奖最佳音乐/喜剧片**: [查看网格墙视图](https://www.themoviedb.org/list/8648850?view=grid)
* 🕊️ **独立精神奖最佳长片**: [查看网格墙视图](https://www.themoviedb.org/list/8648851?view=grid)
* 🐻 **柏林电影节金熊奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648852?view=grid)
* 🦁 **威尼斯电影节金狮奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648854?view=grid)
* 🍁 **多伦多电影节人民选择奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648855?view=grid)

### 🎬 第四梯队：高阶影迷社区与名家策展

* 🎬 **LB Top 500 Films**: [查看网格墙视图](https://www.themoviedb.org/list/8648802?view=grid)
* 🔥 **LB Top 250 Films with the Most Fans**: [查看网格墙视图](https://www.themoviedb.org/list/8649224?view=grid)
* 🎨 **LB Top 250 Animated Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649225?view=grid)
* 📽️ **LB Top 250 Documentary Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649231?view=grid)
* 📝 **Roger Ebert's Great Movies**: [查看网格墙视图](https://www.themoviedb.org/list/8649219?view=grid)

### 📚 第五梯队：超大体量洗版底仓

* 🎥 **TSPDT - 1000 Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8648821?view=grid)
* 📖 **1001 Movies You Must See Before You Die**: [查看网格墙视图](https://www.themoviedb.org/list/8649029?view=grid)
* 💽 **Criterion Collection**: [查看网格墙视图](https://www.themoviedb.org/list/8649108?view=grid)

### ✨ 第六梯队：现代独立与流行厂牌

* ✨ **Every A24 Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649217?view=grid)
* 🔴 **Every NEON Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649218?view=grid)
* 🎞️ **Every MUBI Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649220?view=grid)

### 📈 第七梯队：实时口碑与趋势榜 (Trending & Popular)

* 📈 **豆瓣 - 一周口碑电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648547?view=grid)
* 📺 **豆瓣 - 华语口碑剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648548?view=grid)
* 🌍 **豆瓣 - 全球口碑剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648549?view=grid)
* 🔥 **豆瓣 - 实时热门电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648550?view=grid)
* 🔥 **豆瓣 - 实时热门电视榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648551?view=grid)
* 📈 **TMDB - 热门电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8706223?view=grid)
* 📺 **TMDB - 热门剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8706224?view=grid)
* 🔥 **TMDB - 本周趋势电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8706225?view=grid)
* 🔥 **TMDB - 本周趋势剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8706226?view=grid)

### 📂 豆瓣电影 28 大分类多维度榜单

* 🎭 **剧情**: [Top 20](https://www.themoviedb.org/list/8647681?view=grid) | [高分经典](https://www.themoviedb.org/list/8648565?view=grid)
* 😂 **喜剧**: [近期热门](https://www.themoviedb.org/list/8648552?view=grid) | [Top 20](https://www.themoviedb.org/list/8647682?view=grid) | [高分经典](https://www.themoviedb.org/list/8648566?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648595?view=grid)
* 💥 **动作**: [近期热门](https://www.themoviedb.org/list/8648555?view=grid) | [Top 20](https://www.themoviedb.org/list/8647683?view=grid) | [高分经典](https://www.themoviedb.org/list/8648568?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648597?view=grid)
* ❤️ **爱情**: [近期热门](https://www.themoviedb.org/list/8648553?view=grid) | [Top 20](https://www.themoviedb.org/list/8647684?view=grid) | [高分经典](https://www.themoviedb.org/list/8648567?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648596?view=grid)
* 🚀 **科幻**: [近期热门](https://www.themoviedb.org/list/8648556?view=grid) | [Top 20](https://www.themoviedb.org/list/8647685?view=grid) | [高分经典](https://www.themoviedb.org/list/8648570?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648598?view=grid)
* 🎨 **动画**: [近期热门](https://www.themoviedb.org/list/8648557?view=grid) | [Top 20](https://www.themoviedb.org/list/8647686?view=grid) | [高分经典](https://www.themoviedb.org/list/8648571?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648599?view=grid)
* 🔍 **悬疑**: [近期热门](https://www.themoviedb.org/list/8648558?view=grid) | [Top 20](https://www.themoviedb.org/list/8647687?view=grid) | [高分经典](https://www.themoviedb.org/list/8648572?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648600?view=grid)
* 😱 **惊悚**: [近期热门](https://www.themoviedb.org/list/8648560?view=grid) | [Top 20](https://www.themoviedb.org/list/8647688?view=grid) | [高分经典](https://www.themoviedb.org/list/8648574?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648602?view=grid)
* 👻 **恐怖**: [近期热门](https://www.themoviedb.org/list/8648562?view=grid) | [Top 20](https://www.themoviedb.org/list/8647689?view=grid) | [高分经典](https://www.themoviedb.org/list/8648581?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648607?view=grid)
* 📽️ **纪录片**: [Top 20](https://www.themoviedb.org/list/8647690?view=grid)
* ⏱️ **短片**: [Top 20](https://www.themoviedb.org/list/8647691?view=grid)
* 🔞 **情色**: [Top 20](https://www.themoviedb.org/list/8647692?view=grid) | [高分经典](https://www.themoviedb.org/list/8648586?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648612?view=grid)
* 🎵 **音乐**: [Top 20](https://www.themoviedb.org/list/8647693?view=grid) | [高分经典](https://www.themoviedb.org/list/8648578?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648604?view=grid)
* 💃 **歌舞**: [Top 20](https://www.themoviedb.org/list/8647694?view=grid) | [高分经典](https://www.themoviedb.org/list/8648584?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648610?view=grid)
* 🏠 **家庭**: [Top 20](https://www.themoviedb.org/list/8647695?view=grid) | [高分经典](https://www.themoviedb.org/list/8648576?view=grid)
* 👶 **儿童**: [Top 20](https://www.themoviedb.org/list/8647696?view=grid) | [高分经典](https://www.themoviedb.org/list/8648577?view=grid)
* 📖 **传记**: [近期热门](https://www.themoviedb.org/list/8648564?view=grid) | [Top 20](https://www.themoviedb.org/list/8647697?view=grid) | [高分经典](https://www.themoviedb.org/list/8648583?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648609?view=grid)
* 📜 **历史**: [Top 20](https://www.themoviedb.org/list/8647698?view=grid) | [高分经典](https://www.themoviedb.org/list/8648579?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648605?view=grid)
* ⚔️ **战争**: [近期热门](https://www.themoviedb.org/list/8648563?view=grid) | [Top 20](https://www.themoviedb.org/list/8647699?view=grid) | [高分经典](https://www.themoviedb.org/list/8648582?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648608?view=grid)
* 🚔 **犯罪**: [近期热门](https://www.themoviedb.org/list/8648559?view=grid) | [Top 20](https://www.themoviedb.org/list/8647700?view=grid) | [高分经典](https://www.themoviedb.org/list/8648573?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648601?view=grid)
* 🤠 **西部**: [Top 20](https://www.themoviedb.org/list/8647702?view=grid) | [高分经典](https://www.themoviedb.org/list/8648588?view=grid)
* 🧙 **奇幻**: [Top 20](https://www.themoviedb.org/list/8647703?view=grid) | [高分经典](https://www.themoviedb.org/list/8648580?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648606?view=grid)
* 🗺️ **冒险**: [近期热门](https://www.themoviedb.org/list/8648561?view=grid) | [Top 20](https://www.themoviedb.org/list/8647704?view=grid) | [高分经典](https://www.themoviedb.org/list/8648575?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648603?view=grid)
* 🌋 **灾难**: [Top 20](https://www.themoviedb.org/list/8647705?view=grid) | [高分经典](https://www.themoviedb.org/list/8648587?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648613?view=grid)
* 🗡️ **武侠**: [Top 20](https://www.themoviedb.org/list/8647706?view=grid) | [高分经典](https://www.themoviedb.org/list/8648585?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8648611?view=grid)
* 🏮 **古装**: [Top 20](https://www.themoviedb.org/list/8647707?view=grid) | [高分经典](https://www.themoviedb.org/list/8648593?view=grid)
* 🏃 **运动**: [Top 20](https://www.themoviedb.org/list/8647708?view=grid) | [高分经典](https://www.themoviedb.org/list/8648594?view=grid)
* 🌑 **黑色电影**: [Top 20](https://www.themoviedb.org/list/8647709?view=grid)

### 📺 豆瓣电视剧地区与类型榜单

* 🇨🇳 **大陆剧**: [近期热门](https://www.themoviedb.org/list/8702683?view=grid) | [高分经典](https://www.themoviedb.org/list/8702684?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702685?view=grid)
* 🇺🇸 **美剧**: [近期热门](https://www.themoviedb.org/list/8702686?view=grid) | [高分经典](https://www.themoviedb.org/list/8702687?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702688?view=grid)
* 🇬🇧 **英剧**: [高分经典](https://www.themoviedb.org/list/8702689?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702690?view=grid)
* 🇯🇵 **日剧**: [近期热门](https://www.themoviedb.org/list/8702691?view=grid) | [高分经典](https://www.themoviedb.org/list/8702692?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702693?view=grid)
* 🇰🇷 **韩剧**: [近期热门](https://www.themoviedb.org/list/8702694?view=grid) | [高分经典](https://www.themoviedb.org/list/8702695?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702696?view=grid)
* 🇭🇰 **港剧**: [高分经典](https://www.themoviedb.org/list/8702697?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702698?view=grid)
* 🇨🇳 **台剧**: [高分经典](https://www.themoviedb.org/list/8702699?view=grid) | [冷门佳作](https://www.themoviedb.org/list/8702700?view=grid)
* 🇹🇭 **泰剧**: [冷门佳作](https://www.themoviedb.org/list/8702701?view=grid)
* 🇪🇺 **欧洲剧**: [近期热门](https://www.themoviedb.org/list/8702702?view=grid) | [高分经典](https://www.themoviedb.org/list/8702703?view=grid)
* 🎨 **动画剧集**: [高分经典](https://www.themoviedb.org/list/8702704?view=grid)

## ✨ 核心特性

* **🏆 顶级榜单全自动维护**
  * 支持 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 主榜单、**全球 9 大权威电影节大奖**、**豆瓣电影 28 大分类多维度榜单（近期热门、Top 20、高分经典、冷门佳作）及豆瓣电视剧地区与类型榜单**。
  * **自动简介同步**：抓取 TMDb 列表描述并写入 Emby 合集 `Overview` 字段。
  * **全员收藏**：自动将生成的合集加入所有 Emby 用户的“我的收藏”，提升常用榜单的曝光度。
* **🖼️ 海报直入与异步性能引擎**
  * **告别四宫格假死**：彻底终结 Emby 默认生成拼图时导致的服务器卡死或刮削阻塞问题。
  * **异步队列注入**：引入全局任务队列与动态延时结算机制，将海报注入与合集创建解耦，大幅缩短运行时间并完美规避 SQLite 数据库锁死覆盖问题。
  * **智能抓取策略**：支持高度自定义的海报提取逻辑（榜单绝对第一 vs 库内拥有最高排名；最新上映 vs 最新入库），打造个性化封面墙。
  * **合集封面修复**：扫描库内无封面的合集，提取合集内最早上映影视的海报进行修复。
  * **电影与剧集封面修复**：为缺少主封面的电影和剧集补充 TMDb 原语言海报。已有主封面自动跳过；缺少 TMDb ID 或未获取到原语言海报时记录原因，不使用其他语言图片替代。
* **🍿 MoviePilot 联动自动补片**
  * **精准订阅策略**：比对缺失后自动调用 MoviePilot API。**支持按榜单独立配置订阅模式：全量订阅 (True)、完全关闭 (False) 或设置排名阈值（如传入整数 3，则仅自动订阅榜单前 3 名的缺失项），精细化管理资源获取。**
  * **防误杀排除列表**：支持配置独立的电影/剧集 TMDb ID 排除列表 (`MP_EXCLUDE_MOVIE_IDS` / `MP_EXCLUDE_SERIES_IDS`)，智能跳过无需订阅的特定条目，并在推送报告中体现拦截统计。
  * **防重机制**：推送前自动比对 MP 已有订阅，避免重复下发任务。
* **📁 智能查漏补缺与报告**
  * 详细的推送通知报告：精确列出缺失影片、排名及对应的 `{tmdb-id}`，并动态展示 MP 订阅成功、已有及排除的数量。
  * **封面修复报告**：分别统计合集、电影和剧集的修复数量，并统一展示成功修复清单及失败原因。
  * **自适应通知排版**：针对分类榜单采用精简概览模式，防止消息过长被通讯软件截断。
* **🇨🇳 国产/华语特色聚合**
  * 通过目录关键词与 TMDb 产地代码（`CN/HK/TW`）自动聚合国产影视资源。
* **🛡️ 工业级容错机制**
  * 针对部分 Emby 版本优化了 API 请求路径，规避 JSON 解析异常，确保脚本在复杂网络环境下稳定运行。

## 📸 运行效果展示

![Emby Collection Sync Demo](assets/images/showcase.png)
*(图：全自动生成的 Emby 专属海报墙与合集分类)*

## 🚀 快速开始 (以青龙面板为例)

1. **放置脚本**：将 `emby_collection_sync.py` 放入青龙面板的 `scripts` 文件夹。
2. **安装依赖**：在青龙的“依赖管理”中安装 Python3 依赖：`requests` 和 `urllib3`。
3. **填写配置**：打开脚本，在配置区域填入你的 **Emby**、**TMDb** 和 **MoviePilot** 地址及对应密钥。
4. **订阅策略定制**：在脚本 `CUSTOM_LISTS` 中调整 `mp_subscribe` 参数：
   - `True`: 只要缺失即订阅。
   - `False`: 仅在通知中报告缺失，不执行订阅。
   - `整数 (如 3)`: 仅当该条目在榜单前 3 名且库内缺失时，才发给 MP 执行下载。
5. **定时任务**：新增任务，命令为 `task emby_collection_sync.py`（建议定时规则：`0 30 8 * * *`）。

## 📈 Star History

<a href="https://www.star-history.com/?repos=ffinly%2Femby-collection-sync&amp;type=date&amp;legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;theme=dark&amp;legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;legend=top-left" />
  </picture>
</a>

## 📄 License

本项目基于 [GPL-3.0 license](LICENSE) 协议开源 - 详情请查看 LICENSE 文件。
