# 第一次使用：安裝與準備

客戶照「開口指南」PDF 貼了安裝那段話時，照這裡做。**每一步做完用一句白話回報**，需要客戶動手的地方講清楚「點哪裡、會看到什麼」。
指令由你執行；客戶只需要在瀏覽器登入、授權、輸入自己的密碼。

## 1. 工具與兩個 skill

先確認這幾個工具在（`--version` 看得到就是有），沒有就依作業系統裝，裝完重開終端機或 AI 工具：

| 工具 | 用途 | Windows | macOS |
|---|---|---|---|
| Node.js（`npx`） | 安裝 skill | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
| Python 3 | skill 的腳本 | `winget install Python.Python.3.12` | `brew install python` |
| uv | aigo-builder 的腳本 | `winget install astral-sh.uv` | `brew install uv` |
| GitHub CLI（`gh`） | 下載專案、issue、PR | `winget install GitHub.cli` | `brew install gh` |

macOS 沒有 brew 就帶客戶到各工具官網下載安裝檔。接著裝兩個 skill：

```bash
npx skills add AI-GO-APP/aigo-app-builder-skill -g -y -a claude-code codex
npx skills add AI-GO-APP/aigo-client-collab-skill -g -y -a claude-code codex
```

- `-g` 裝在使用者層級，每個專案都能用；`-y` 免互動；`-a claude-code codex` 只裝這兩個（實體在 `~/.agents/skills/`，Claude Code 用連結指過去）。
  連結建立失敗（Windows 權限）時改加 `--copy` 重跑。
- 裝完請客戶**重開 AI 工具或開新對話**，新 skill 才會載入。

## 2. GitHub 登入

```bash
gh auth status
```

- 沒登入 → `gh auth login --web --git-protocol https`，畫面會出現一組代碼：
  跟客戶說「瀏覽器會打開 GitHub，請貼上這組代碼並按授權；沒有 GitHub 帳號的話先註冊一個，再把帳號名稱告訴工程師」。
- 登入後用 `gh repo view <專案 repo>` 確認看得到專案；看不到 → 跟客戶說「工程師還沒把你的帳號加進專案，
  請把你的 GitHub 帳號名稱（`gh api user -q .login`）傳給工程師」。

## 3. 工作區：一個公司（租戶）一個資料夾

aigo-builder 的工作區＝**一個租戶一個資料夾**（裡面的 `.aigo/config.json` 記這個租戶的網址），專案放在工作區裡面：

```
~/aigo-projects/<租戶代號>/          ← 工作區（例：~/aigo-projects/houchencpa/）
  .aigo/config.json                  ← 租戶網址、app 登錄表（builder 建）
  exports/                           ← 匯出的真實資料放這裡（不在任何 repo 裡）
  <repo-1>/  <repo-2>/ …             ← 專案
```

租戶代號是 AI GO 網址的開頭（`https://<租戶代號>.ai-go.app`），PDF 上有寫。

```bash
uv run --project <aigo-builder 目錄>/scripts python <aigo-builder 目錄>/scripts/aigo_auth.py setup-workspace ~/aigo-projects/<租戶代號>
```

建好後把 `.aigo/config.json` 的 `base_url` 填成 `https://<租戶代號>.ai-go.app`（你來填，不用客戶動手），再建 `exports/`。
已經有工作區就不重建。

## 4. 下載專案

PDF 上會寫這個客戶有哪些專案（repo 網址）。

```bash
gh repo clone <組織/repo> ~/aigo-projects/<租戶代號>/<repo>
```

- 已經下載過 → 不重下，改成 `git -C <資料夾> pull --ff-only` 拿最新版（有沒存的改動先問）。
- 下載完告訴客戶：「之後要改這支 app，就在 AI 工具裡打開這個資料夾再開始對話」。
  Claude Code：在該資料夾開啟（桌面版選資料夾、終端機 `cd` 進去後執行 `claude`）；Codex 同理。
- 專案的工具若要找 aigo-builder 或工作區，照專案 `AGENTS.md` 的指令區；找不到時用 `~/.agents/skills/aigo-builder`。

## 5. AI GO 平台登入（兩種方式，客戶選）

等到第一次要用平台時才做（builder 的時機：開發前 review、資料操作、成員管理）。兩種都可以，問客戶喜歡哪一種：

> 要登入 AI GO 有兩種方式：
> 1. **用瀏覽器登入**（建議）：我打開登入頁，你跟平常一樣登入，之後一段時間不用再登入
> 2. **把帳號密碼存在你電腦的設定檔**：我開好檔案，你自己打上帳號密碼，之後我自動登入

**方式 1：瀏覽器登入**（aigo-builder 1.73.0 起）

```bash
uv run --project <aigo-builder 目錄>/scripts python <aigo-builder 目錄>/scripts/aigo_auth.py login --browser
```

會打開租戶的登入頁；跟客戶說「瀏覽器打開了 AI GO 的登入頁，請登入，看到『可以關掉這個分頁』就完成了」。
過期後重跑同一行。builder 版本較舊沒有 `--browser` 時，先照 Phase -1 更新，或改用方式 2。

**方式 2：帳密設定檔**

```bash
uv run --project <aigo-builder 目錄>/scripts python <aigo-builder 目錄>/scripts/aigo_auth.py setup   # 建 ~/.aigo/.env 範本
```

用編輯器打開那個檔案給客戶（Windows `notepad %USERPROFILE%\.aigo\.env`、macOS `open -e ~/.aigo/.env`），
跟客戶說「請在 `AIGO_EMAIL=` 後面打上登入帳號、`AIGO_PASSWORD=` 後面打上密碼，存檔關掉跟我說」。
然後執行 `aigo_auth.py login` 驗證（不印 token）。

兩種方式都是**客戶自己輸入密碼**，你不經手、不讀出檔案內容。登入好之後用 `aigo_auth.py status` 確認生效的租戶是對的。

## 6. 自動更新（每次開新對話先檢查）

```bash
python <aigo-client-collab 的目錄>/scripts/install_hooks.py      # macOS / Linux 用 python3
```

- 一次幫 Claude Code（`~/.claude/settings.json`）與 Codex（`~/.codex/config.toml`）裝好兩個 skill
  （aigo-client-collab、aigo-builder）的 SessionStart hook：每次開新對話先比對 GitHub 上的版本，有新版就同步。
  只追加、會先備份成 `.bak-aigo`，重複執行不會重複加。
- 跟客戶說：「我幫你設定好了，之後每次開新對話會自動檢查有沒有新版。」
- 用 Codex 的話，Codex 下次啟動會請客戶核准這個 hook：跟客戶說「看到要不要信任新設定的提示，選允許」。
- 輸出 `error`（設定檔格式壞了）→ 跟客戶說「AI 工具的設定檔格式有問題，我先不動它」，請工程師看（`engineer-collab.md` §3.1）。

## 7. 完成

回報三件事：裝好了什麼、專案資料夾在哪、接下來可以怎麼開口（「直接說你想改什麼，或說『我不知道從哪開始』」）。
