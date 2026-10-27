# Changelog

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
