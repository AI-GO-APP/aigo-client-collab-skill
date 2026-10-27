# AI GO 客戶協作開發 Skill（aigo-client-collab）

讓**不會寫程式的客戶**用 AI Coding（Claude Code、Codex）跟技術端一起開發 AI GO app：

- 全程白話加固定比喻，一次問一題，先複述再動手
- 把功能問清楚後直接實作、給客戶看、客戶同意後發布並驗證
- 碰到技術紅線（權限、既有資料表、大量正式資料、算錢規則、外部串接、平台設定…）就整理成 issue 交給工程師
- 客戶貼上工程師開的 issue 網址，就進入研究模式，研究結果經客戶確認後回貼到 issue

技術操作（同步、編譯、發布、資料表、權限）交給 [aigo-builder](https://github.com/AI-GO-APP/aigo-app-builder-skill)；
專案自己的規則寫在各 repo 的 `AGENTS.md`（優先於本 skill）。

## 安裝

客戶端兩個 skill 都要裝（[skills CLI](https://github.com/vercel-labs/skills) 會自動裝到 Claude Code、Codex 等 agent）：

```bash
npx skills add AI-GO-APP/aigo-app-builder-skill -g -y
npx skills add AI-GO-APP/aigo-client-collab-skill -g -y
```

客戶通常不自己打指令，而是照「開口指南」PDF 把安裝那段話貼給 AI，由 AI 安裝、帶他登入 GitHub、下載專案（`references/setup.md`）。

## 保持更新

每次觸發時 `scripts/check_update.py` 比對本地與 GitHub 上的 `VERSION`，遠端較新就強制同步本機所有安裝
（機制同 aigo-builder）。**改 skill 內容請對本 repo 開 PR**，安裝目錄裡的修改會被覆蓋。

## 給技術端

1. 在專案的 `AGENTS.md` 加「客戶協作」一節：技術窗口、能不能自己發布、正式網址、紅線增減（範本：`references/project-setup.md`）。
2. 把客戶的 GitHub 帳號加進 repo，確認他的 AI GO 帳號有對應權限。
3. 產生這位客戶的「開口指南」PDF 交給他（`pdf/README.md`）。**客戶資料與 PDF 離線保存，不進任何 repo。**
4. 要請客戶研究或回答問題時，照 `references/issue-format.md` 的「研究任務」格式開 issue，把網址傳給客戶。

## 檔案

| 檔案 | 內容 |
|---|---|
| `SKILL.md` | 說話規則、情境分流、功能／修問題／解釋／研究／接續流程、紅線、開 issue |
| `references/metaphors.md` | 固定比喻（技術詞 → 白話） |
| `references/issue-format.md` | 「需要技術支援」「研究任務」兩種 issue 格式、研究模式流程與結果格式 |
| `references/setup.md` | 第一次使用：安裝、GitHub 登入、下載專案 |
| `references/project-setup.md` | 給技術端：專案開放客戶協作的設定與檢查 |
| `pdf/` | 開口指南 PDF 範本（`guide.py`）與客戶資料範例 |
| `scripts/check_update.py` | 自我更新 |
