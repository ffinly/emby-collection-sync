# Emby Collection Sync

[简体中文](README.md) | **繁體中文** | [English](README.en.md)

---

🚀 **面向 Emby 影音庫的全自動合集管理與追新補片流水線。**

一鍵同步 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 等權威主榜、全球 9 大權威電影節大獎、豆瓣電影 28 大分類多維度榜單（近期熱門、Top 20、高分經典、冷門佳作）及豆瓣電視劇地區與類型榜單，智能排查本地缺失，**並支持自定義排除列表聯動 MoviePilot 實現自動化補片**。系統支持自動聚合華語影視，並**原生支持原語言海報直入與靈活的智能抓取策略，結合底層異步隊列引擎，徹底解決 Emby 生成默認四宮格封面導致的卡死痛點**。實現從全自動化整理到觀影的完整閉環。

## 🔗 線上公開最新榜單列表

以下 TMDB 列表完全由自動化爬蟲與 ETL 流水線自動維護。**系統會在每天早上 7:30 (UTC+8) 定時執行數據抓取、比對與同步更新**，確保榜單排名與官方時刻保持一致。

### 🏆 第一/二梯隊：大衆必看與影史殿堂

* 🍿 **IMDb Top 250 Movies**: [查看網格牆視圖](https://www.themoviedb.org/list/8647021?view=grid)
* 📺 **IMDb Top 250 TV Shows**: [查看網格牆視圖](https://www.themoviedb.org/list/8647022?view=grid)
* 🎞️ **豆瓣電影 Top 250**: [查看網格牆視圖](https://www.themoviedb.org/list/8647023?view=grid)
* 🏛️ **S&S Directors - Greatest Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8649058?view=grid)
* 🏛️ **S&S Critics - Greatest Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8649050?view=grid)
* ⭐ **AFI Top 100 (2007)**: [查看網格牆視圖](https://www.themoviedb.org/list/8649041?view=grid)
* 📰 **NYT - 100 Best Movies of the 21st Century (2025)**: [查看網格牆視圖](https://www.themoviedb.org/list/8701141?view=grid)
* 📡 **NYT - 100 Best TV Shows of the 21st Century (2026)**: [查看網格牆視圖](https://www.themoviedb.org/list/8701142?view=grid)

### 🌍 第三梯隊：全球最具含金量大獎矩陣

* 🏆 **奧斯卡歷屆最佳影片**: [查看網格牆視圖](https://www.themoviedb.org/list/8648843?view=grid)
* 🌿 **戛納電影節金棕櫚獎**: [查看網格牆視圖](https://www.themoviedb.org/list/8648844?view=grid)
* 🎭 **英國電影學院獎最佳影片**: [查看網格牆視圖](https://www.themoviedb.org/list/8648848?view=grid)
* 🌐 **金球獎最佳劇情片**: [查看網格牆視圖](https://www.themoviedb.org/list/8648849?view=grid)
* 🥂 **金球獎最佳音樂/喜劇片**: [查看網格牆視圖](https://www.themoviedb.org/list/8648850?view=grid)
* 🕊️ **獨立精神獎最佳長片**: [查看網格牆視圖](https://www.themoviedb.org/list/8648851?view=grid)
* 🐻 **柏林電影節金熊獎**: [查看網格牆視圖](https://www.themoviedb.org/list/8648852?view=grid)
* 🦁 **威尼斯電影節金獅獎**: [查看網格牆視圖](https://www.themoviedb.org/list/8648854?view=grid)
* 🍁 **多倫多電影節人民選擇獎**: [查看網格牆視圖](https://www.themoviedb.org/list/8648855?view=grid)

### 🎬 第四梯隊：高階影迷社區與名家策展

* 🎬 **LB Top 500 Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8648802?view=grid)
* 🔥 **LB Top 250 Films with the Most Fans**: [查看網格牆視圖](https://www.themoviedb.org/list/8649224?view=grid)
* 🎨 **LB Top 250 Animated Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8649225?view=grid)
* 📽️ **LB Top 250 Documentary Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8649231?view=grid)
* 📝 **Roger Ebert's Great Movies**: [查看網格牆視圖](https://www.themoviedb.org/list/8649219?view=grid)

### 📚 第五梯隊：超大體量洗版底倉

* 🎥 **TSPDT - 1000 Greatest Films**: [查看網格牆視圖](https://www.themoviedb.org/list/8648821?view=grid)
* 📖 **1001 Movies You Must See Before You Die**: [查看網格牆視圖](https://www.themoviedb.org/list/8649029?view=grid)
* 💽 **Criterion Collection**: [查看網格牆視圖](https://www.themoviedb.org/list/8649108?view=grid)

### ✨ 第六梯隊：現代獨立與流行廠牌

* ✨ **Every A24 Film**: [查看網格牆視圖](https://www.themoviedb.org/list/8649217?view=grid)
* 🔴 **Every NEON Film**: [查看網格牆視圖](https://www.themoviedb.org/list/8649218?view=grid)
* 🎞️ **Every MUBI Film**: [查看網格牆視圖](https://www.themoviedb.org/list/8649220?view=grid)

### 📈 第七梯隊：實時口碑與趨勢榜 (Trending & Popular)

* 📈 **豆瓣 - 一週口碑電影榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8648547?view=grid)
* 📺 **豆瓣 - 華語口碑劇集榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8648548?view=grid)
* 🌍 **豆瓣 - 全球口碑劇集榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8648549?view=grid)
* 🔥 **豆瓣 - 實時熱門電影榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8648550?view=grid)
* 🔥 **豆瓣 - 實時熱門電視榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8648551?view=grid)
* 📈 **TMDB - 熱門電影榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8706223?view=grid)
* 📺 **TMDB - 熱門劇集榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8706224?view=grid)
* 🔥 **TMDB - 本週趨勢電影榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8706225?view=grid)
* 🔥 **TMDB - 本週趨勢劇集榜**: [查看網格牆視圖](https://www.themoviedb.org/list/8706226?view=grid)

### 📂 豆瓣電影 28 大分類多維度榜單

* 🎭 **劇情**: [Top 20](https://www.themoviedb.org/list/8647681?view=grid) | [高分經典](https://www.themoviedb.org/list/8648565?view=grid)
* 😂 **喜劇**: [近期熱門](https://www.themoviedb.org/list/8648552?view=grid) | [Top 20](https://www.themoviedb.org/list/8647682?view=grid) | [高分經典](https://www.themoviedb.org/list/8648566?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648595?view=grid)
* 💥 **動作**: [近期熱門](https://www.themoviedb.org/list/8648555?view=grid) | [Top 20](https://www.themoviedb.org/list/8647683?view=grid) | [高分經典](https://www.themoviedb.org/list/8648568?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648597?view=grid)
* ❤️ **愛情**: [近期熱門](https://www.themoviedb.org/list/8648553?view=grid) | [Top 20](https://www.themoviedb.org/list/8647684?view=grid) | [高分經典](https://www.themoviedb.org/list/8648567?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648596?view=grid)
* 🚀 **科幻**: [近期熱門](https://www.themoviedb.org/list/8648556?view=grid) | [Top 20](https://www.themoviedb.org/list/8647685?view=grid) | [高分經典](https://www.themoviedb.org/list/8648570?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648598?view=grid)
* 🎨 **動畫**: [近期熱門](https://www.themoviedb.org/list/8648557?view=grid) | [Top 20](https://www.themoviedb.org/list/8647686?view=grid) | [高分經典](https://www.themoviedb.org/list/8648571?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648599?view=grid)
* 🔍 **懸疑**: [近期熱門](https://www.themoviedb.org/list/8648558?view=grid) | [Top 20](https://www.themoviedb.org/list/8647687?view=grid) | [高分經典](https://www.themoviedb.org/list/8648572?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648600?view=grid)
* 😱 **驚悚**: [近期熱門](https://www.themoviedb.org/list/8648560?view=grid) | [Top 20](https://www.themoviedb.org/list/8647688?view=grid) | [高分經典](https://www.themoviedb.org/list/8648574?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648602?view=grid)
* 👻 **恐怖**: [近期熱門](https://www.themoviedb.org/list/8648562?view=grid) | [Top 20](https://www.themoviedb.org/list/8647689?view=grid) | [高分經典](https://www.themoviedb.org/list/8648581?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648607?view=grid)
* 📽️ **紀錄片**: [Top 20](https://www.themoviedb.org/list/8647690?view=grid)
* ⏱️ **短片**: [Top 20](https://www.themoviedb.org/list/8647691?view=grid)
* 🔞 **情色**: [Top 20](https://www.themoviedb.org/list/8647692?view=grid) | [高分經典](https://www.themoviedb.org/list/8648586?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648612?view=grid)
* 🎵 **音樂**: [Top 20](https://www.themoviedb.org/list/8647693?view=grid) | [高分經典](https://www.themoviedb.org/list/8648578?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648604?view=grid)
* 💃 **歌舞**: [Top 20](https://www.themoviedb.org/list/8647694?view=grid) | [高分經典](https://www.themoviedb.org/list/8648584?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648610?view=grid)
* 🏠 **家庭**: [Top 20](https://www.themoviedb.org/list/8647695?view=grid) | [高分經典](https://www.themoviedb.org/list/8648576?view=grid)
* 👶 **兒童**: [Top 20](https://www.themoviedb.org/list/8647696?view=grid) | [高分經典](https://www.themoviedb.org/list/8648577?view=grid)
* 📖 **傳記**: [近期熱門](https://www.themoviedb.org/list/8648564?view=grid) | [Top 20](https://www.themoviedb.org/list/8647697?view=grid) | [高分經典](https://www.themoviedb.org/list/8648583?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648609?view=grid)
* 📜 **歷史**: [Top 20](https://www.themoviedb.org/list/8647698?view=grid) | [高分經典](https://www.themoviedb.org/list/8648579?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648605?view=grid)
* ⚔️ **戰爭**: [近期熱門](https://www.themoviedb.org/list/8648563?view=grid) | [Top 20](https://www.themoviedb.org/list/8647699?view=grid) | [高分經典](https://www.themoviedb.org/list/8648582?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648608?view=grid)
* 🚔 **犯罪**: [近期熱門](https://www.themoviedb.org/list/8648559?view=grid) | [Top 20](https://www.themoviedb.org/list/8647700?view=grid) | [高分經典](https://www.themoviedb.org/list/8648573?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648601?view=grid)
* 🤠 **西部**: [Top 20](https://www.themoviedb.org/list/8647702?view=grid) | [高分經典](https://www.themoviedb.org/list/8648588?view=grid)
* 🧙 **奇幻**: [Top 20](https://www.themoviedb.org/list/8647703?view=grid) | [高分經典](https://www.themoviedb.org/list/8648580?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648606?view=grid)
* 🗺️ **冒險**: [近期熱門](https://www.themoviedb.org/list/8648561?view=grid) | [Top 20](https://www.themoviedb.org/list/8647704?view=grid) | [高分經典](https://www.themoviedb.org/list/8648575?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648603?view=grid)
* 🌋 **災難**: [Top 20](https://www.themoviedb.org/list/8647705?view=grid) | [高分經典](https://www.themoviedb.org/list/8648587?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648613?view=grid)
* 🗡️ **武俠**: [Top 20](https://www.themoviedb.org/list/8647706?view=grid) | [高分經典](https://www.themoviedb.org/list/8648585?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8648611?view=grid)
* 🏮 **古裝**: [Top 20](https://www.themoviedb.org/list/8647707?view=grid) | [高分經典](https://www.themoviedb.org/list/8648593?view=grid)
* 🏃 **運動**: [Top 20](https://www.themoviedb.org/list/8647708?view=grid) | [高分經典](https://www.themoviedb.org/list/8648594?view=grid)
* 🌑 **黑色電影**: [Top 20](https://www.themoviedb.org/list/8647709?view=grid)

### 📺 豆瓣電視劇地區與類型榜單

* 🇨🇳 **大陸劇**: [近期熱門](https://www.themoviedb.org/list/8702683?view=grid) | [高分經典](https://www.themoviedb.org/list/8702684?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702685?view=grid)
* 🇺🇸 **美劇**: [近期熱門](https://www.themoviedb.org/list/8702686?view=grid) | [高分經典](https://www.themoviedb.org/list/8702687?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702688?view=grid)
* 🇬🇧 **英劇**: [高分經典](https://www.themoviedb.org/list/8702689?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702690?view=grid)
* 🇯🇵 **日劇**: [近期熱門](https://www.themoviedb.org/list/8702691?view=grid) | [高分經典](https://www.themoviedb.org/list/8702692?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702693?view=grid)
* 🇰🇷 **韓劇**: [近期熱門](https://www.themoviedb.org/list/8702694?view=grid) | [高分經典](https://www.themoviedb.org/list/8702695?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702696?view=grid)
* 🇭🇰 **港劇**: [高分經典](https://www.themoviedb.org/list/8702697?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702698?view=grid)
* 🇨🇳 **臺劇**: [高分經典](https://www.themoviedb.org/list/8702699?view=grid) | [冷門佳作](https://www.themoviedb.org/list/8702700?view=grid)
* 🇹🇭 **泰劇**: [冷門佳作](https://www.themoviedb.org/list/8702701?view=grid)
* 🇪🇺 **歐洲劇**: [近期熱門](https://www.themoviedb.org/list/8702702?view=grid) | [高分經典](https://www.themoviedb.org/list/8702703?view=grid)
* 🎨 **動畫劇集**: [高分經典](https://www.themoviedb.org/list/8702704?view=grid)

## ✨ 核心特性

* **🏆 頂級榜單全自動維護**
  * 支持 IMDb/豆瓣 Top 250/Letterboxd/TSPDT 主榜單、**全球 9 大權威電影節大獎**、**豆瓣電影 28 大分類多維度榜單（近期熱門、Top 20、高分經典、冷門佳作）及豆瓣電視劇地區與類型榜單**。
  * **自動簡介同步**：抓取 TMDb 列表描述並寫入 Emby 合集 `Overview` 字段。
  * **全員收藏**：自動將生成的合集加入所有 Emby 用戶的“我的收藏”，提升常用榜單的曝光度。
* **🖼️ 海報直入與異步性能引擎**
  * **告別四宮格假死**：徹底終結 Emby 默認生成拼圖時導致的服務器卡死或刮削阻塞問題。
  * **異步隊列注入**：引入全局任務隊列與動態延時結算機制，將海報注入與合集創建解耦，大幅縮短運行時間並完美規避 SQLite 數據庫鎖死覆蓋問題。
  * **智能抓取策略**：支持高度自定義的海報提取邏輯（榜單絕對第一 vs 庫內擁有最高排名；最新上映 vs 最新入庫），打造個性化封面牆。
  * **合集封面修復**：掃描庫內無封面的合集，提取合集內最早上映影視的海報進行修復。
  * **電影與劇集封面修復**：爲缺少主封面的電影和劇集補充 TMDb 原語言海報。已有主封面自動跳過；缺少 TMDb ID 或未獲取到原語言海報時記錄原因，不使用其他語言圖片替代。
* **🍿 MoviePilot 聯動自動補片**
  * **精準訂閱策略**：比對缺失後自動調用 MoviePilot API。**支持按榜單獨立配置訂閱模式：全量訂閱 (True)、完全關閉 (False) 或設置排名閾值（如傳入整數 3，則僅自動訂閱榜單前 3 名的缺失項），精細化管理資源獲取。**
  * **防誤殺排除列表**：支持配置獨立的電影/劇集 TMDb ID 排除列表 (`MP_EXCLUDE_MOVIE_IDS` / `MP_EXCLUDE_SERIES_IDS`)，智能跳過無需訂閱的特定條目，並在推送報告中體現攔截統計。
  * **防重機制**：推送前自動比對 MP 已有訂閱，避免重複下發任務。
* **📁 智能查漏補缺與報告**
  * 詳細的推送通知報告：精確列出缺失影片、排名及對應的 `{tmdb-id}`，並動態展示 MP 訂閱成功、已有及排除的數量。
  * **封面修復報告**：分別統計合集、電影和劇集的修復數量，並統一展示成功修復清單及失敗原因。
  * **自適應通知排版**：針對分類榜單採用精簡概覽模式，防止消息過長被通訊軟件截斷。
* **🇨🇳 國產/華語特色聚合**
  * 通過目錄關鍵詞與 TMDb 產地代碼（`CN/HK/TW`）自動聚合國產影視資源。
* **🛡️ 工業級容錯機制**
  * 針對部分 Emby 版本優化了 API 請求路徑，規避 JSON 解析異常，確保腳本在複雜網絡環境下穩定運行。

## 📸 運行效果展示

![Emby Collection Sync Demo](assets/images/showcase.png)
*(圖：全自動生成的 Emby 專屬海報牆與合集分類)*

## 🚀 快速開始 (以青龍面板爲例)

1. **放置腳本**：將 `emby_collection_sync.py` 放入青龍面板的 `scripts` 文件夾。
2. **安裝依賴**：在青龍的“依賴管理”中安裝 Python3 依賴：`requests` 和 `urllib3`。
3. **填寫配置**：打開腳本，在配置區域填入你的 **Emby**、**TMDb** 和 **MoviePilot** 地址及對應密鑰。
4. **訂閱策略定製**：在腳本 `CUSTOM_LISTS` 中調整 `mp_subscribe` 參數：
   - `True`: 只要缺失即訂閱。
   - `False`: 僅在通知中報告缺失，不執行訂閱。
   - `整數 (如 3)`: 僅當該條目在榜單前 3 名且庫內缺失時，才發給 MP 執行下載。
5. **定時任務**：新增任務，命令爲 `task emby_collection_sync.py`（建議定時規則：`0 30 8 * * *`）。

## 📈 Star History

<a href="https://www.star-history.com/?repos=ffinly%2Femby-collection-sync&amp;type=date&amp;legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;theme=dark&amp;legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=ffinly/emby-collection-sync&amp;type=date&amp;legend=top-left" />
  </picture>
</a>

## 📄 License

本項目基於 [GPL-3.0 license](LICENSE) 協議開源 - 詳情請查看 LICENSE 文件。
