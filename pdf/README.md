# 開口指南 PDF

給客戶的「協作開發 開口指南」：安裝、每次怎麼開始、9 種情境的開場白、合作規則。**範本是通用的、進版控；
每個客戶的資料與產出的 PDF 離線保存，不進任何 repo**（裡面有客戶的 repo 名稱與聯絡方式）。

| 檔案 | 用途 |
|---|---|
| `guide.py` | 範本：版面與通用內容；讀客戶的 `client.json` 產生 HTML |
| `client.example.json` | 客戶資料的欄位範例 |

## 需要

- [ai-go-app-present-skill](https://github.com/AI-GO-APP/ai-go-app-present-skill)（版型 `deck_kit` 與 `render.mjs`；在它的目錄跑過 `npm install`）
- Python 3、Node 18+、Google Chrome（或設 `CHROME_PATH`）

## 產生一位客戶的 PDF

```bash
# 1. 在客戶的離線資料夾（例：<客戶工作區>/交付/開口指南/）放 client.json（照 client.example.json 改）
# 2. 產生 HTML（PRESENT_SKILL 也可以寫在 client.json 的 present_skill）
PRESENT_SKILL="<present skill 路徑>" python <本 skill>/pdf/guide.py client.json
# 3. 轉 PDF，並輸出每頁 PNG 逐頁目視
node "<present skill 路徑>/scripts/render.mjs" --html "AI GO <客戶> 協作開發 開口指南 v1 YYYYMMDD.html" --png preview
```

`client.json` 欄位：

| 欄位 | 說明 |
|---|---|
| `tenant` | 客戶名稱（封面、頁尾、檔名） |
| `tenant_code` | AI GO 網址開頭（`https://<tenant_code>.ai-go.app`），安裝時建工作區用 |
| `version`、`made` | 版本與製作日（檔名與封面）；改版時版本加一號 |
| `audience` | 封面的「對象」 |
| `tech_contact` | 工程師名稱與 GitHub 帳號（「跟工程師一起合作」那頁） |
| `projects` | 這位客戶可以改的系統：名稱、內容、repo（安裝那段話會自動帶入下載網址） |
| `examples` | 選填：用客戶業務寫的例句（`feature` 加功能、`screen` 改畫面、`broken` 壞了、`explain` 想了解、`data` 查資料或匯出、`member` 邀請同事或調權限），沒有就不顯示；`migration` 是 PART C 搬遷任務舉例的原系統名稱，沒有就用「104 人資後台」 |
| `contact` | 封底的聯絡方式 |

## 交付與改版

- 檔名：`AI GO <客戶> 協作開發 開口指南 <版本> <YYYYMMDD>.pdf`，封面也印版本與製作日。
- 同資料夾放一份 `交付紀錄.md`：哪一版、哪天、給了誰、改了什麼。
- **什麼時候要重發**：客戶的系統、repo、工程師窗口變了；或本範本的開場白、安裝方式改了。
  skill 本身的行為改版不用重發 PDF（skill 會自動更新，開場白只寫意圖）。
- 開場白都以「用協作開發模式。」開頭，這句要和 `SKILL.md` 的 description 保持一致，改其中一邊就要改另一邊。
