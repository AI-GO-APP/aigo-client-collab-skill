# AI GO 客戶協作開發 Skill（aigo-client-collab）

讓**不會寫程式的客戶**用 AI Coding（Claude Code、Codex）跟技術端一起開發 AI GO app：

- **疊在 [aigo-builder](https://github.com/AI-GO-APP/aigo-app-builder-skill) 上的引導層**：做法、技術判斷、危險操作前的提醒全部照 builder；
  本 skill 不另定流程、不加任何禁止事項。客戶能做的事和工程師一樣（開 app、加功能、接外部服務、邀請同事、匯入資料、發布）
- **白話引導**：builder 的每個問題、每個確認都翻成白話與固定比喻，讓客戶看得懂、做得了決定
- **操作驗收**：每個做完的功能都實際操作一次（E2E 或介面操作），發布後在正式網址再驗一次
- **跟工程師協作**：何時值得找、請協助／知會／請審閱／交接的範本；平台問題照 builder 回報給 AI GO 開發團隊
- **研究模式**：客戶貼上工程師發來的研究任務網址，研究結果經客戶確認後回貼到 issue
- **原系統搬遷研究**：用 Chrome 擴充套件研究客戶已登入的舊系統，接 builder 的遷入流程

專案自己的做法寫在各 repo 的 `AGENTS.md`。

## 安裝

客戶端兩個 skill 都要裝（[skills CLI](https://github.com/vercel-labs/skills) 會自動裝到 Claude Code、Codex 等 agent）：

```bash
npx skills add AI-GO-APP/aigo-app-builder-skill -g -y -a claude-code codex
npx skills add AI-GO-APP/aigo-client-collab-skill -g -y -a claude-code codex
```

客戶通常不自己打指令，而是照「開口指南」PDF 把安裝那段話貼給 AI，由 AI 安裝、帶他登入 GitHub、下載專案（`references/setup.md`）。

## 保持更新

機制與 [aigo-builder](https://github.com/AI-GO-APP/aigo-app-builder-skill) 相同（`scripts/check_update.py` 照抄，只換 repo 與狀態檔名）：

- **版本**：`VERSION` 加上 `CHANGELOG.md`。比對本地與 GitHub 上的 `VERSION`，**遠端較新時直接把本機所有已註冊安裝強制同步到遠端 main**，
  不詢問、不保留本地修改。git 安裝用 `fetch`＋`reset --hard`，`npx skills add` 的複製式安裝下載 `main.zip` 鏡像覆蓋。
- **節流**：遠端版本抓一次快取 3 小時（狀態檔 `~/.aigo/collab_update_check.json`，和 aigo-builder 的分開），版本比對每次都做；
  離線或逾時一律靜默略過。開發用副本（本地版本高於遠端、或 git 不在 main／master）不碰。
- **什麼時候檢查**：
  1. **每次開新對話**（SessionStart hook，建議）：`scripts/install_hooks.py` 一次幫 Claude Code 與 Codex 裝好
     aigo-client-collab 和 aigo-builder 兩個 skill 的 hook，在 skill 載入前就同步完。客戶第一次安裝時由 AI 執行（`references/setup.md` §5）。
     手動設定的範本在 `resources/hooks/`。Codex 會請使用者核准新的 hook。
  2. **每次 skill 觸發**（`SKILL.md` Phase -1）：沒裝 hook 的 agent 也會更新；同步後 AI 重新讀取 `SKILL.md` 並告知客戶。

```bash
python scripts/check_update.py               # 檢查並同步（macOS/Linux 用 python3）；沒動作就沒輸出
python scripts/check_update.py --force       # 忽略節流
python scripts/check_update.py --check-only  # 只報告不同步（維護者／CI 用）
python scripts/install_hooks.py --check      # 看 hook 裝了沒（exit 0＝都裝好）
```

> 維護者注意：**改 skill 內容走 PR，合併前同步 bump `VERSION` 並在 `CHANGELOG.md` 補一節**，否則客戶端不會收到更新。
> 安裝目錄裡的修改會被覆蓋。

## 給技術端

1. 在專案的 `AGENTS.md` 加「客戶協作」一節：工程師帳號、正式網址、希望先知會的事、測試資料（範本：`references/project-setup.md`）。
2. 把客戶的 GitHub 帳號加進 repo，確認他的 AI GO 帳號有對應權限。
3. 產生這位客戶的「開口指南」PDF 交給他（`pdf/README.md`）。**客戶資料與 PDF 離線保存，不進任何 repo。**
4. 要請客戶研究或回答問題時，照 `references/engineer-collab.md` §5 的「研究任務」格式開 issue，把網址傳給客戶。

## 檔案

| 檔案 | 內容 |
|---|---|
| `SKILL.md` | 定位、開場準備、情境對照（對到 builder 的哪條線）、白話引導、操作驗收、修問題／解釋／接續、跟工程師協作 |
| `references/builder-guide.md` | builder 每個環節的白話問法與確認範本（需求四問、計畫摘要、不可逆選擇、寫入、成員、外部服務、發布、平台回報） |
| `references/metaphors.md` | 固定比喻（技術詞 → 白話） |
| `references/engineer-collab.md` | 跟工程師協作：何時找、兩種管道、請協助／知會／請審閱／交接範本、研究模式 |
| `references/setup.md` | 第一次使用：工具與 skill、GitHub 登入、租戶工作區、下載專案、平台登入（瀏覽器／帳密檔）、自動更新 |
| `references/migration.md` | 原系統搬遷研究（Chrome 擴充套件研究原系統 → 資料 → 規格 → 衝突 → 分批實作驗收 → 切換），技術做法接 builder 遷入線 |
| `references/project-setup.md` | 給技術端：專案開放客戶協作的設定與檢查 |
| `pdf/` | 開口指南 PDF 範本（`guide.py`）與客戶資料範例 |
| `scripts/check_update.py` | 自我更新 |
