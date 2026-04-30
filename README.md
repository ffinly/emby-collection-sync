# Emby Collection Sync

[简体中文](#简体中文) | [English Version](#english-version)

---

## 简体中文

🚀 **面向 Emby 影音库的全自动合集管理与追新补片流水线。**

一键同步 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 等权威主榜、全球 9 大权威电影节大奖及豆瓣 28 大细分领域多维度榜单（近期热门、Top 20、高分经典、冷门佳作），智能排查本地缺失，**并支持自定义排除列表联动 MoviePilot 实现自动化补片**。系统支持自动聚合华语影视，并**原生支持原语言海报直入与灵活的智能抓取策略，结合底层异步队列引擎，彻底解决 Emby 生成默认四宫格封面导致的卡死痛点**。实现从全自动化整理到观影的完整闭环。

### 🔗 线上公开最新榜单列表
以下 TMDB 列表完全由自动化爬虫与 ETL 流水线自动维护。**系统会在每天早上 7:30 (UTC+8) 定时执行数据抓取、比对与同步更新**，确保榜单排名与官方时刻保持一致。

#### 🏆 第一/二梯队：大众必看与影史殿堂
* 🍿 **IMDb Top 250 Movies**: [查看网格墙视图](https://www.themoviedb.org/list/8647021?view=grid)
* 📺 **IMDb Top 250 TV Shows**: [查看网格墙视图](https://www.themoviedb.org/list/8647022?view=grid)
* 🎞️ **豆瓣电影 Top 250**: [查看网格墙视图](https://www.themoviedb.org/list/8647023?view=grid)
* 🏛️ **S&S Directors - Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649058?view=grid)
* 🏛️ **S&S Critics - Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649050?view=grid)
* ⭐ **AFI Top 100 (2007)**: [查看网格墙视图](https://www.themoviedb.org/list/8649041?view=grid)

#### 🌍 第三梯队：全球最具含金量大奖矩阵
* 🏆 **奥斯卡历届最佳影片**: [查看网格墙视图](https://www.themoviedb.org/list/8648843?view=grid)
* 🌿 **戛纳电影节金棕榈奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648844?view=grid)
* 🎭 **英国电影学院奖最佳影片**: [查看网格墙视图](https://www.themoviedb.org/list/8648848?view=grid)
* 🌐 **金球奖最佳剧情片**: [查看网格墙视图](https://www.themoviedb.org/list/8648849?view=grid)
* 🥂 **金球奖最佳音乐/喜剧片**: [查看网格墙视图](https://www.themoviedb.org/list/8648850?view=grid)
* 🕊️ **独立精神奖最佳长片**: [查看网格墙视图](https://www.themoviedb.org/list/8648851?view=grid)
* 🐻 **柏林电影节金熊奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648852?view=grid)
* 🦁 **威尼斯电影节金狮奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648854?view=grid)
* 🍁 **多伦多电影节人民选择奖**: [查看网格墙视图](https://www.themoviedb.org/list/8648855?view=grid)

#### 🎬 第四梯队：高阶影迷社区与名家策展
* 🎬 **LB Top 500 Films**: [查看网格墙视图](https://www.themoviedb.org/list/8648802?view=grid)
* 🔥 **LB Top 250 Films with the Most Fans**: [查看网格墙视图](https://www.themoviedb.org/list/8649224?view=grid)
* 🎨 **LB Top 250 Animated Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649225?view=grid)
* 📽️ **LB Top 250 Documentary Films**: [查看网格墙视图](https://www.themoviedb.org/list/8649231?view=grid)
* 📝 **Roger Ebert's Great Movies**: [查看网格墙视图](https://www.themoviedb.org/list/8649219?view=grid)

#### 📚 第五梯队：超大体量洗版底仓
* 🎥 **TSPDT - 1000 Greatest Films**: [查看网格墙视图](https://www.themoviedb.org/list/8648821?view=grid)
* 📖 **1001 Movies You Must See Before You Die**: [查看网格墙视图](https://www.themoviedb.org/list/8649029?view=grid)
* 💽 **Criterion Collection**: [查看网格墙视图](https://www.themoviedb.org/list/8649108?view=grid)

#### ✨ 第六梯队：现代独立与流行厂牌
* ✨ **Every A24 Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649217?view=grid)
* 🔴 **Every NEON Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649218?view=grid)
* 🎞️ **Every MUBI Film**: [查看网格墙视图](https://www.themoviedb.org/list/8649220?view=grid)

#### 📈 第七梯队：实时口碑与趋势榜 (Trending & Popular)
* 📈 **豆瓣 - 一周口碑电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648547?view=grid)
* 📺 **豆瓣 - 华语口碑剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648548?view=grid)
* 🌍 **豆瓣 - 全球口碑剧集榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648549?view=grid)
* 🔥 **豆瓣 - 实时热门电影榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648550?view=grid)
* 🔥 **豆瓣 - 实时热门电视榜**: [查看网格墙视图](https://www.themoviedb.org/list/8648551?view=grid)

#### 📂 豆瓣 28 大分类多维度榜单
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

### ✨ 核心特性

* **🏆 顶级榜单全自动维护**
  * 支持 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 主榜单、**全球 9 大权威电影节大奖**及 **28 大豆瓣细分领域多维度榜单（近期热门、Top 20、高分经典、冷门佳作）**。
  * **自动简介同步**：抓取 TMDb 列表描述并写入 Emby 合集 `Overview` 字段。
  * **全员收藏**：自动将生成的合集加入所有 Emby 用户的“我的收藏”，提升常用榜单的曝光度。
* **🖼️ 海报直入与异步性能引擎**
  * **告别四宫格假死**：彻底终结 Emby 默认生成拼图时导致的服务器卡死或刮削阻塞问题。
  * **异步队列注入**：引入全局任务队列与动态延时结算机制，将海报注入与合集创建解耦，大幅缩短运行时间并完美规避 SQLite 数据库锁死覆盖问题。
  * **智能抓取策略**：支持高度自定义的海报提取逻辑（榜单绝对第一 vs 库内拥有最高排名；最新上映 vs 最新入库），打造个性化封面墙。
  * **无封面自动修复**：自动扫描库内无封面的合集，智能提取合集内“最早上映”影片的海报进行兜底修复。
* **🍿 MoviePilot 联动自动补片**
  * **精准订阅策略**：比对缺失后自动调用 MoviePilot API。**支持按榜单独立配置订阅模式：全量订阅 (True)、完全关闭 (False) 或设置排名阈值（如传入整数 3，则仅自动订阅榜单前 3 名的缺失项），精细化管理资源获取。**
  * **防误杀排除列表**：支持配置独立的电影/剧集 TMDb ID 排除列表 (`MP_EXCLUDE_MOVIE_IDS` / `MP_EXCLUDE_SERIES_IDS`)，智能跳过无需订阅的特定条目，并在推送报告中体现拦截统计。
  * **防重机制**：推送前自动比对 MP 已有订阅，避免重复下发任务。
* **📁 智能查漏补缺与报告**
  * 详细的推送通知报告：精确列出缺失影片、排名及对应的 `{tmdb-id}`，并动态展示 MP 订阅成功、已有及排除的数量。
  * **自适应通知排版**：针对分类榜单采用精简概览模式，防止消息过长被通讯软件截断。
* **🇨🇳 国产/华语特色聚合**
  * 通过目录关键词与 TMDb 产地代码（`CN/HK/TW`）自动聚合国产影视资源。
* **🛡️ 工业级容错机制**
  * 针对部分 Emby 版本优化了 API 请求路径，规避 JSON 解析异常，确保脚本在复杂网络环境下稳定运行。

### 📸 运行效果展示
![Emby Collection Sync Demo](https://github.com/user-attachments/assets/87ad54c0-b474-4a6a-a402-e6a539da865d)
*(图：全自动生成的 Emby 专属海报墙与合集分类)*

### 🚀 快速开始 (以青龙面板为例)

1. **放置脚本**：将 `emby_collection_sync.py` 放入青龙面板的 `scripts` 文件夹。
2. **安装依赖**：在青龙的“依赖管理”中安装 Python3 依赖：`requests` 和 `urllib3`。
3. **填写配置**：打开脚本，在配置区域填入你的 **Emby**、**TMDb** 和 **MoviePilot** 地址及对应密钥。
4. **订阅策略定制**：在脚本 `CUSTOM_LISTS` 中调整 `mp_subscribe` 参数：
   - `True`: 只要缺失即订阅。
   - `False`: 仅在通知中报告缺失，不执行订阅。
   - `整数 (如 3)`: 仅当该条目在榜单前 3 名且库内缺失时，才发给 MP 执行下载。
5. **定时任务**：新增任务，命令为 `task emby_collection_sync.py`（建议定时规则：`0 30 8 * * *`）。

### 📄 License
本项目基于 [GPL-3.0 license](LICENSE) 协议开源 - 详情请查看 LICENSE 文件。

---

## English Version

🚀 **A fully automated collection management and media acquisition pipeline for Emby.**

Seamlessly synchronize authoritative lists like IMDb/Douban Top 250/Letterboxd/TSPDT, **9 Global Prestigious Film Awards**, and Douban's 28 Genre multi-dimensional lists (Trending, Top 20, Classics, Niche Masterpieces). It intelligently scans your local library for missing media, and **supports custom exclusion lists to seamlessly integrate with MoviePilot for automated downloading**. The system auto-aggregates Chinese-language media and **natively injects original-language posters using smart fetching strategies and an async queue engine to permanently resolve Emby's performance bottlenecks (UI freezes) caused by default collage generation.** Realize a complete closed-loop from automated library management to immersive viewing.

### 🔗 Publicly Maintained TMDb Lists
The following TMDb lists are fully maintained by automated crawlers and ETL pipelines. **Data fetching, comparison, and synchronization run daily at 07:30 (UTC+8)** to ensure rankings remain perfectly aligned with official sources.

#### 🏆 Tiers 1 & 2: Mainstream Essentials & Cinematic Hall of Fame
* 🍿 **IMDb Top 250 Movies**: [View Grid](https://www.themoviedb.org/list/8647021?view=grid)
* 📺 **IMDb Top 250 TV Shows**: [View Grid](https://www.themoviedb.org/list/8647022?view=grid)
* 🎞️ **Douban Movies Top 250**: [View Grid](https://www.themoviedb.org/list/8647023?view=grid)
* 🏛️ **S&S Directors - Greatest Films**: [View Grid](https://www.themoviedb.org/list/8649058?view=grid)
* 🏛️ **S&S Critics - Greatest Films**: [View Grid](https://www.themoviedb.org/list/8649050?view=grid)
* ⭐ **AFI Top 100 (2007)**: [View Grid](https://www.themoviedb.org/list/8649041?view=grid)

#### 🌍 Tier 3: Global Prestigious Film Awards
* 🏆 **Oscar Winning Films: Best Picture**: [View Grid](https://www.themoviedb.org/list/8648843?view=grid)
* 🌿 **Cannes Film Festival Palme d'Or**: [View Grid](https://www.themoviedb.org/list/8648844?view=grid)
* 🎭 **BAFTA Award for Best Film**: [View Grid](https://www.themoviedb.org/list/8648848?view=grid)
* 🌐 **Golden Globe Best Drama**: [View Grid](https://www.themoviedb.org/list/8648849?view=grid)
* 🥂 **Golden Globe Best Musical/Comedy**: [View Grid](https://www.themoviedb.org/list/8648850?view=grid)
* 🕊️ **Indie Spirit Award for Best Feature**: [View Grid](https://www.themoviedb.org/list/8648851?view=grid)
* 🐻 **Berlinale Film Festival Golden Bear**: [View Grid](https://www.themoviedb.org/list/8648852?view=grid)
* 🦁 **Venice Film Festival Golden Lion**: [View Grid](https://www.themoviedb.org/list/8648854?view=grid)
* 🍁 **Toronto Film Festival Audience Award**: [View Grid](https://www.themoviedb.org/list/8648855?view=grid)

#### 🎬 Tier 4: Cinephile Communities & Curations
* 🎬 **LB Top 500 Films**: [View Grid](https://www.themoviedb.org/list/8648802?view=grid)
* 🔥 **LB Top 250 Films with the Most Fans**: [View Grid](https://www.themoviedb.org/list/8649224?view=grid)
* 🎨 **LB Top 250 Animated Films**: [View Grid](https://www.themoviedb.org/list/8649225?view=grid)
* 📽️ **LB Top 250 Documentary Films**: [View Grid](https://www.themoviedb.org/list/8649231?view=grid)
* 📝 **Roger Ebert's Great Movies**: [View Grid](https://www.themoviedb.org/list/8649219?view=grid)

#### 📚 Tier 5: Ultimate Collection Targets (1000+ Films)
* 🎥 **TSPDT - 1000 Greatest Films**: [View Grid](https://www.themoviedb.org/list/8648821?view=grid)
* 📖 **1001 Movies You Must See Before You Die**: [View Grid](https://www.themoviedb.org/list/8649029?view=grid)
* 💽 **Criterion Collection**: [View Grid](https://www.themoviedb.org/list/8649108?view=grid)

#### ✨ Tier 6: Modern Indie Labels & Studios
* ✨ **Every A24 Film**: [View Grid](https://www.themoviedb.org/list/8649217?view=grid)
* 🔴 **Every NEON Film**: [View Grid](https://www.themoviedb.org/list/8649218?view=grid)
* 🎞️ **Every MUBI Film**: [View Grid](https://www.themoviedb.org/list/8649220?view=grid)

#### 📈 Tier 7: Trending & Popular
* 📈 **Douban - Weekly Highly Rated Movies**: [View Grid](https://www.themoviedb.org/list/8648547?view=grid)
* 📺 **Douban - Highly Rated Chinese Series**: [View Grid](https://www.themoviedb.org/list/8648548?view=grid)
* 🌍 **Douban - Highly Rated Global Series**: [View Grid](https://www.themoviedb.org/list/8648549?view=grid)
* 🔥 **Douban - Real-time Hot Movies**: [View Grid](https://www.themoviedb.org/list/8648550?view=grid)
* 🔥 **Douban - Real-time Hot TV Shows**: [View Grid](https://www.themoviedb.org/list/8648551?view=grid)

#### 📂 Douban 28 Genre Lists
* 🎭 **Drama**: [Top 20](https://www.themoviedb.org/list/8647681?view=grid) | [Classics](https://www.themoviedb.org/list/8648565?view=grid)
* 😂 **Comedy**: [Trending](https://www.themoviedb.org/list/8648552?view=grid) | [Top 20](https://www.themoviedb.org/list/8647682?view=grid) | [Classics](https://www.themoviedb.org/list/8648566?view=grid) | [Niche](https://www.themoviedb.org/list/8648595?view=grid)
* 💥 **Action**: [Trending](https://www.themoviedb.org/list/8648555?view=grid) | [Top 20](https://www.themoviedb.org/list/8647683?view=grid) | [Classics](https://www.themoviedb.org/list/8648568?view=grid) | [Niche](https://www.themoviedb.org/list/8648597?view=grid)
* ❤️ **Romance**: [Trending](https://www.themoviedb.org/list/8648553?view=grid) | [Top 20](https://www.themoviedb.org/list/8647684?view=grid) | [Classics](https://www.themoviedb.org/list/8648567?view=grid) | [Niche](https://www.themoviedb.org/list/8648596?view=grid)
* 🚀 **Sci-Fi**: [Trending](https://www.themoviedb.org/list/8648556?view=grid) | [Top 20](https://www.themoviedb.org/list/8647685?view=grid) | [Classics](https://www.themoviedb.org/list/8648570?view=grid) | [Niche](https://www.themoviedb.org/list/8648598?view=grid)
* 🎨 **Animation**: [Trending](https://www.themoviedb.org/list/8648557?view=grid) | [Top 20](https://www.themoviedb.org/list/8647686?view=grid) | [Classics](https://www.themoviedb.org/list/8648571?view=grid) | [Niche](https://www.themoviedb.org/list/8648599?view=grid)
* 🔍 **Mystery**: [Trending](https://www.themoviedb.org/list/8648558?view=grid) | [Top 20](https://www.themoviedb.org/list/8647687?view=grid) | [Classics](https://www.themoviedb.org/list/8648572?view=grid) | [Niche](https://www.themoviedb.org/list/8648600?view=grid)
* 😱 **Thriller**: [Trending](https://www.themoviedb.org/list/8648560?view=grid) | [Top 20](https://www.themoviedb.org/list/8647688?view=grid) | [Classics](https://www.themoviedb.org/list/8648574?view=grid) | [Niche](https://www.themoviedb.org/list/8648602?view=grid)
* 👻 **Horror**: [Trending](https://www.themoviedb.org/list/8648562?view=grid) | [Top 20](https://www.themoviedb.org/list/8647689?view=grid) | [Classics](https://www.themoviedb.org/list/8648581?view=grid) | [Niche](https://www.themoviedb.org/list/8648607?view=grid)
* 📽️ **Documentary**: [Top 20](https://www.themoviedb.org/list/8647690?view=grid)
* ⏱️ **Short Film**: [Top 20](https://www.themoviedb.org/list/8647691?view=grid)
* 🔞 **Erotica**: [Top 20](https://www.themoviedb.org/list/8647692?view=grid) | [Classics](https://www.themoviedb.org/list/8648586?view=grid) | [Niche](https://www.themoviedb.org/list/8648612?view=grid)
* 🎵 **Music**: [Top 20](https://www.themoviedb.org/list/8647693?view=grid) | [Classics](https://www.themoviedb.org/list/8648578?view=grid) | [Niche](https://www.themoviedb.org/list/8648604?view=grid)
* 💃 **Musical**: [Top 20](https://www.themoviedb.org/list/8647694?view=grid) | [Classics](https://www.themoviedb.org/list/8648584?view=grid) | [Niche](https://www.themoviedb.org/list/8648610?view=grid)
* 🏠 **Family**: [Top 20](https://www.themoviedb.org/list/8647695?view=grid) | [Classics](https://www.themoviedb.org/list/8648576?view=grid)
* 👶 **Children**: [Top 20](https://www.themoviedb.org/list/8647696?view=grid) | [Classics](https://www.themoviedb.org/list/8648577?view=grid)
* 📖 **Biography**: [Trending](https://www.themoviedb.org/list/8648564?view=grid) | [Top 20](https://www.themoviedb.org/list/8647697?view=grid) | [Classics](https://www.themoviedb.org/list/8648583?view=grid) | [Niche](https://www.themoviedb.org/list/8648609?view=grid)
* 📜 **History**: [Top 20](https://www.themoviedb.org/list/8647698?view=grid) | [Classics](https://www.themoviedb.org/list/8648579?view=grid) | [Niche](https://www.themoviedb.org/list/8648605?view=grid)
* ⚔️ **War**: [Trending](https://www.themoviedb.org/list/8648563?view=grid) | [Top 20](https://www.themoviedb.org/list/8647699?view=grid) | [Classics](https://www.themoviedb.org/list/8648582?view=grid) | [Niche](https://www.themoviedb.org/list/8648608?view=grid)
* 🚔 **Crime**: [Trending](https://www.themoviedb.org/list/8648559?view=grid) | [Top 20](https://www.themoviedb.org/list/8647700?view=grid) | [Classics](https://www.themoviedb.org/list/8648573?view=grid) | [Niche](https://www.themoviedb.org/list/8648601?view=grid)
* 🤠 **Western**: [Top 20](https://www.themoviedb.org/list/8647702?view=grid) | [Classics](https://www.themoviedb.org/list/8648588?view=grid)
* 🧙 **Fantasy**: [Top 20](https://www.themoviedb.org/list/8647703?view=grid) | [Classics](https://www.themoviedb.org/list/8648580?view=grid) | [Niche](https://www.themoviedb.org/list/8648606?view=grid)
* 🗺️ **Adventure**: [Trending](https://www.themoviedb.org/list/8648561?view=grid) | [Top 20](https://www.themoviedb.org/list/8647704?view=grid) | [Classics](https://www.themoviedb.org/list/8648575?view=grid) | [Niche](https://www.themoviedb.org/list/8648603?view=grid)
* 🌋 **Disaster**: [Top 20](https://www.themoviedb.org/list/8647705?view=grid) | [Classics](https://www.themoviedb.org/list/8648587?view=grid) | [Niche](https://www.themoviedb.org/list/8648613?view=grid)
* 🗡️ **Wuxia**: [Top 20](https://www.themoviedb.org/list/8647706?view=grid) | [Classics](https://www.themoviedb.org/list/8648585?view=grid) | [Niche](https://www.themoviedb.org/list/8648611?view=grid)
* 🏮 **Period & Costume**: [Top 20](https://www.themoviedb.org/list/8647707?view=grid) | [Classics](https://www.themoviedb.org/list/8648593?view=grid)
* 🏃 **Sports**: [Top 20](https://www.themoviedb.org/list/8647708?view=grid) | [Classics](https://www.themoviedb.org/list/8648594?view=grid)
* 🌑 **Film Noir**: [Top 20](https://www.themoviedb.org/list/8647709?view=grid)

### ✨ Core Features

* **🏆 Automated Top List Maintenance**
  * Supports IMDb/Douban Top 250/Letterboxd/TSPDT Lists, **9 Global Prestigious Film Awards**, and **Multi-dimensional Douban Genre Lists (Recent Hot, Top 20, High-Scoring Classics, Niche Masterpieces)**.
  * **Metadata Sync**: Fetches TMDb list descriptions and writes them to the Emby Collection `Overview`.
  * **Global Favorites**: Automatically adds generated collections to "My Favorites" for all Emby users, boosting visibility.
* **🖼️ Poster Injection & Async Performance Engine**
  * **Eliminate UI Freezes**: Prevents Emby server crashes or scraping bottlenecks caused by generating default 4-grid collage thumbnails.
  * **Async Queue Injection**: Introduces a global task queue with dynamic delayed batch processing. Decouples collection creation from poster injection to significantly reduce execution time and prevent SQLite database locks/overwrites.
  * **Smart Fetching Strategies**: Highly customizable poster extraction logic (absolute list top vs. highest-ranked in local library; newest premiere vs. latest added) for a personalized poster wall.
  * **Auto-Repair Missing Covers**: Scans the library for coverless collections and intelligently extracts the poster of the "earliest released" movie as a fallback.
* **🍿 MoviePilot Integration**
  * **Smart Subscription Policies**: Automatically triggers MoviePilot API to subscribe to missing media. **Supports flexible policies: toggle per list (True/False) or set a rank threshold (Integer, e.g., 3, to only subscribe to the top 3 missing items), providing precise control over resource acquisition.**
  * **Custom Exclusion Lists**: Configure separate movie and series exclusion lists (`MP_EXCLUDE_MOVIE_IDS` / `MP_EXCLUDE_SERIES_IDS`) to skip specific media from auto-downloading, with intercepted counts displayed in the final report.
  * **Anti-Duplication**: Cross-checks existing MP subscriptions before pushing requests to avoid duplicate entries.
* **📁 Gap Analysis & Reporting**
  * Precise push notifications detailing missing items, their rankings, `{tmdb-id}`, and dynamic stats for successful, existing, and excluded MP subscriptions.
  * **Adaptive Formatting**: Uses a concise overview mode for genre lists to prevent notifications from being truncated by messaging apps.
* **🇨🇳 Regional Media Aggregation**
  * Automatically groups Chinese-language media based on directory keywords and TMDb origin country codes (`CN/HK/TW`).
* **🛡️ Robust Error Handling**
  * Optimized API request paths for various Emby versions to bypass JSON parsing exceptions, ensuring stable execution in complex network environments.

### 📸 Showcase
![Emby Collection Sync Demo](https://github.com/user-attachments/assets/87ad54c0-b474-4a6a-a402-e6a539da865d)
*(Auto-generated customized poster walls and collection categories in Emby)*

### 🚀 Quick Start (via Qinglong Panel)

1. **Deploy Script**: Place `emby_collection_sync.py` into the `scripts` directory of your Qinglong Panel.
2. **Install Dependencies**: Install the `requests` and `urllib3` Python packages.
3. **Configuration**: Open the script and configure your **Emby**, **TMDb**, and **MoviePilot** URLs and API Keys.
4. **Subscription Policy**: Adjust `mp_subscribe` in the `CUSTOM_LISTS` config:
   - `True`: Subscribe to all missing items.
   - `False`: Report only.
   - `Integer (e.g., 3)`: Only subscribe to missing items ranked within the top 3.
5. **Cron Job**: Create a new scheduled task with the command `task emby_collection_sync.py` (Recommended cron expression: `0 30 8 * * *` for daily execution at 08:30).

### 📄 License
This project is licensed under the [GPL-3.0 license](LICENSE) - see the LICENSE file for details.
