# Changelog

## 1.0.0

### 改成疊在 aigo-builder 上的引導層：拿掉所有限制，改成引導與協作

前提改了：非技術客戶需要的是**更多引導與說明，不是更多限制**。真正高危險的操作 aigo-builder 本來就會停下來確認。

- **拿掉**紅線表、「永遠不做」清單、「交給工程師」的硬規定，以及「專案 AGENTS.md ＞ 本 skill ＞ builder」的優先序。
  客戶能做的事和工程師一樣：開 app、接外部服務、邀請同事、匯入資料、發布
- **做法全部照 builder**：需求怎麼問（四問一輪問完）、計畫怎麼確認、資料操作線、成員管理、外部服務、更新失敗、平台問題回報；
  本 skill 不另定流程
- 新增 `references/builder-guide.md`：builder 每個環節的白話問法與確認範本（需求四問、計畫摘要、不可逆選擇、寫入閘門、成員、外部服務、發布、平台回報）
- `references/issue-format.md` → `references/engineer-collab.md`：工程師是隊友不是關卡；何時值得找（建議）、兩種管道
  （這支 app → 專案 issue／PR；平台本身 → builder `report_issue.py`）、請協助／知會／請審閱／交接範本、研究模式；
  建標籤改用 `--force`（Windows／macOS 都能跑）
- 情境對照新增：查資料／匯出、邀請同事／調權限、做一支新系統、接外部系統，各自對到 builder 的哪條線
- 操作驗收保留：每個功能 E2E 或介面操作驗收；正式網址驗收可以用測試資料
- `references/setup.md`：補 Python、uv；**每個租戶一個工作區**（`~/aigo-projects/<租戶代號>/`，builder `setup-workspace`），
  專案放在工作區裡、匯出資料放工作區 `exports/`；平台登入支援瀏覽器登入（builder `login --browser`）與帳密檔兩種
- Phase 0 補「拿專案最新版」（`git pull --ff-only`）；更新指令改成完整路徑
- `references/migration.md`：拿掉工程師複核與「整批匯入交給工程師」，匯入照 builder §2.5 與寫入閘門；研究原系統改成「要按會改東西的按鈕先問客戶」
- `references/project-setup.md`：「客戶協作」一節改成工程師、正式網址、希望先知會的事、測試資料，沒有紅線
- 開口指南：PART B 改成「一起合作」（跟工程師一起合作、上線前後、保護資料）；情境卡 12 張（新增查資料或匯出、邀請同事與調權限）；
  安裝那段話補工具與租戶工作區；搬遷提示詞第 3 段改成先匯 1 筆給客戶看；`client.json` 新增 `tenant_code`、`examples.data`、`examples.member`

## 0.3.0

### 原系統搬遷任務、每個功能都要實際操作驗收

- 新增 `references/migration.md` 與 SKILL.md「F 原系統搬遷」：要用 AI GO 取代既有系統（例：104 人資後台）時，
  確認 Chrome 擴充套件（Claude／Codex）已連上、客戶已在 Chrome 登入原系統，依序做功能研究、歷史資料匯出或讀取、
  資料對應、值得保留的功能、規格書與資料結構、衝突點排解、分批實作與驗收（含新舊比對）、切換計畫；每段給客戶確認，
  對原系統唯讀，真實資料只放客戶電腦的搬遷資料夾
- SKILL.md A 功能新增第 6 步「驗收」（硬規則）：每個做完的功能至少要有 E2E 測試或介面操作驗收（測試資料、截圖留證），
  發布後到正式網址再操作一次；B 修問題的驗收要重現原本的狀況
- 用語：工程師開給客戶的 issue 改說「工程師發來的請求」（原「工單」只留給客戶這邊開給工程師的）
- 開口指南：新增 PART C「原系統搬遷任務」（擴充套件連結、登入、整段提示詞、過程中客戶要做的事）；
  情境卡「收到工程師的工單」改成「收到工程師發來的請求」；上線前後多「實際操作驗收」一步；`client.json` 新增選填 `examples.migration`
- `references/project-setup.md`：「客戶測試用資料」改為驗收必填

## 0.2.0

### 每次開新對話自動檢查更新（SessionStart hook）

原本只在 skill 觸發時（Phase -1）檢查更新；客戶不會自己改 AI 工具的設定，所以照 aigo-builder README「保持更新」推薦的 hook 做成腳本，由 AI 代裝。

- 新增 `scripts/install_hooks.py`：一次幫 Claude Code（`~/.claude/settings.json`）與 Codex（`~/.codex/config.toml`）裝好
  aigo-client-collab 與 aigo-builder 兩個 skill 的 SessionStart hook；只追加、先備份成 `.bak-aigo`、重複執行不重複加、`--check` 只檢查
- `resources/hooks/`：手動設定範本（照 aigo-builder）
- `SKILL.md` Phase 0 多一項「自動更新 hook 有裝」；`references/setup.md` 新增 §5
- 開口指南的安裝那段話多一步：執行 `install_hooks.py`（已發出的 PDF 不必重發：Phase 0 會補裝）
- README「保持更新」改寫成和 aigo-builder 對齊的完整說明

## 0.1.2

### 開口指南：情境卡數量

- 「每次開始」頁的情境數改成 10 張（含「其他情況」），原本寫 9 種

## 0.1.1

### 安裝指令寫明 agent 與免互動

- 安裝改為 `npx skills add <repo> -g -y -a claude-code codex`：只裝 Claude Code 與 Codex，不再對其他不支援的 agent 報錯（`references/setup.md`、README）
- 開口指南的安裝那段話直接寫出指令：貼這段時協作 skill 還沒裝，AI 只看得到這段字；GitHub 登入與下載專案也寫明用 `gh`

## 0.1.0

### 第一版

- `SKILL.md`：說話規則（白話、固定比喻、一次一題、先複述再動手）、情境分流（功能、修問題、解釋、研究、接續、上線、上線後有問題）、
  紅線與「交給工程師」流程；客戶可以自己發布，發布前核對線上版本
- `references/`：比喻庫、兩種 issue 格式與研究模式、第一次使用的安裝流程、技術端的專案設定範本
- `pdf/`：「協作開發 開口指南」PDF 範本（用 ai-go-app-present-skill 的版型；客戶資料離線保存）
- `scripts/check_update.py`：自我更新（照 aigo-builder 1.72.0 的機制）
