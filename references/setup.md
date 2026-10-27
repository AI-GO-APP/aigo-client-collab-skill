# 第一次使用：安裝與準備

客戶照「開口指南」PDF 貼了安裝那句話時，照這裡做。**每一步做完用一句白話回報**，需要客戶動手的地方講清楚「點哪裡、會看到什麼」。

## 1. 安裝兩個 skill

```bash
npx skills add AI-GO-APP/aigo-app-builder-skill -g -y
npx skills add AI-GO-APP/aigo-client-collab-skill -g -y
```

- `-g` 裝在使用者層級，之後每個專案都能用；skills CLI 會自動偵測電腦上的 Claude Code、Codex 並裝到對的位置。
- 沒有 `npx`（沒裝 Node.js）→ 跟客戶說「要先裝一個工具（Node.js）」，依作業系統帶他安裝：
  Windows `winget install OpenJS.NodeJS.LTS`、macOS `brew install node`（沒有 brew 就帶他到 https://nodejs.org 下載 LTS 版）。
  裝完要重開終端機或 AI 工具，再重跑上面兩行。
- 裝完請客戶**重開 AI 工具或開新對話**，新 skill 才會載入。

## 2. GitHub 登入

```bash
gh auth status
```

- 沒有 `gh` → 安裝 GitHub CLI：Windows `winget install GitHub.cli`、macOS `brew install gh`。
- 沒登入 → 執行 `gh auth login --web --git-protocol https`，畫面會出現一組代碼：
  跟客戶說「瀏覽器會打開 GitHub，請貼上這組代碼並按授權；沒有 GitHub 帳號的話先註冊一個，再把帳號名稱告訴工程師」。
  **你不輸入密碼、不幫客戶註冊帳號。**
- 登入後用 `gh repo view <專案 repo>` 確認看得到專案；看不到 → 跟客戶說「工程師還沒把你的帳號加進專案，
  請把你的 GitHub 帳號名稱（`gh api user -q .login`）傳給工程師」。

## 3. 下載專案

PDF 上會寫這個客戶有哪些專案（repo 網址）。

```bash
gh repo clone <組織/repo> "<客戶指定的位置>/<repo>"
```

- 位置沒指定就放使用者家目錄底下的 `aigo-projects/`，並告訴客戶資料夾在哪。
- 已經下載過 → 不重下，改成 `git -C <資料夾> pull` 拿最新版（有未存的改動先停下來問）。
- 下載完告訴客戶：「之後要改這支 app，就在 AI 工具裡打開這個資料夾再開始對話」。
  Claude Code：在該資料夾開啟（桌面版選資料夾、終端機 `cd` 進去後執行 `claude`）；Codex 同理。

## 4. AI GO 平台登入

等到第一次要看草稿或發布時才做，照 aigo-builder 的登入流程（Phase 1）。帳密只放專案的 `.aigo/`，
不寫進程式、不貼進對話以外的地方。

## 5. 完成

回報三件事：裝好了什麼、專案資料夾在哪、接下來可以怎麼開口（「直接說你想改什麼，或說『我不知道從哪開始』」）。
