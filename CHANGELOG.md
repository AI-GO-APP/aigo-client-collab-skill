# Changelog

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
