# -*- coding: utf-8 -*-
"""「協作開發 開口指南」PDF 範本：通用內容在這裡（進版控），客戶資料在客戶的 client.json（離線保存，不進版控）。

用法（在客戶的離線資料夾裡）：
    python <本 skill>/pdf/guide.py client.json
    node <present skill>/scripts/render.mjs --html "AI GO 客戶 協作開發 開口指南 v1 YYYYMMDD.html" --png preview

版型用 ai-go-app-present-skill 的 deck_kit（AI GO 品牌母版）。present skill 的路徑：環境變數 PRESENT_SKILL，
或 client.json 的 "present_skill"。client.json 的欄位見 client.example.json。
"""
import json
import os
import re
import sys
from html import escape
from pathlib import Path

CLIENT = Path(sys.argv[1] if len(sys.argv) > 1 else "client.json").resolve()
C = json.loads(CLIENT.read_text(encoding="utf-8"))
PRESENT = Path(os.environ.get("PRESENT_SKILL") or C.get("present_skill") or "")
if not (PRESENT / "scripts" / "deck_kit.py").exists():
    sys.exit("找不到 ai-go-app-present-skill：設定環境變數 PRESENT_SKILL，或在 client.json 寫 present_skill")
sys.path.insert(0, str(PRESENT / "scripts"))
from deck_kit import Deck  # noqa: E402

SKILLS = ("https://github.com/AI-GO-APP/aigo-app-builder-skill", "https://github.com/AI-GO-APP/aigo-client-collab-skill")
MODE = "用協作開發模式。"

CSS = """
.pr { border: 2px dashed var(--blue); background: var(--tint); border-radius: 12px; padding: 12px 18px 14px; }
.pr-h { font-size: 13px; font-weight: 700; color: var(--blue); letter-spacing: .04em; margin-bottom: 4px; }
.pr-b { font-size: 19px; line-height: 1.65; color: var(--ink); font-weight: 500; }
.pr-b .fill { color: var(--warn); font-weight: 700; }
.pr-b .url { white-space: nowrap; }
.pr.big .pr-b { font-size: 21px; }
table.t.roomy th { font-size: 13px; }
table.t.roomy td { font-size: 18px; padding: 13px 16px 13px 0; }
.sc { background: #fff; border: 1px solid var(--card-line); border-radius: 14px; padding: 18px 22px 16px;
      display: flex; flex-direction: column; gap: 10px; }
.sc h3 { margin: 0; font-size: 25px; font-weight: 900; color: var(--ink); }
.sc .when { font-size: 16px; color: var(--ink-2); line-height: 1.5; }
.sc .ex { font-size: 15px; color: var(--ink-2); line-height: 1.5; }
.sc .ex b { color: var(--ink); }
.sc .ask { font-size: 15px; color: var(--ink-2); line-height: 1.55; }
.sc .ask b { color: var(--blue-deep); }
.pr.mig .pr-b { font-size: 20px; line-height: 1.6; }
.lkrow { font-size: 14px; color: var(--ink-2); display: flex; gap: 10px; align-items: baseline; }
.lkrow span { flex: none; font-weight: 700; }
a.lk { color: var(--blue-deep); text-decoration: none; font-size: 14px; }
"""

d = Deck(tenant=C["tenant"], app="協作開發", purposes=["操作說明"], title="開口指南",
         version=C.get("version", "v1"), made=C.get("made"), extra_css=CSS)
T, S, N, B = d.table, d.steps, d.note, d.bullets
P0, PA, PB, PC = "開始之前", "A　情境開場白", "B　一起合作", "C　原系統搬遷任務"
EX = C.get("examples", {})


def fill(text):
    """【要填的地方】標成橘色；網址不折行（PDF 裡折行的網址複製出來會斷成兩段）；其餘照原文（可含 <br>）。"""
    text = re.sub(r"https?://[A-Za-z0-9./_-]+", lambda m: f'<span class="url">{m.group(0)}</span>', text)
    return re.sub(r"【[^】]*】", lambda m: f'<span class="fill">{escape(m.group(0))}</span>', text)


def prompt(text, label="複製這段，貼給 AI", cls=""):
    return f'<div class="pr {cls}"><div class="pr-h">{label}</div><div class="pr-b">{fill(text)}</div></div>'


def scenario(title, when, text, asks, example=None):
    ex = f'<div class="ex"><b>例：</b>{escape(example)}</div>' if example else ""
    ask = "".join(f"<li>{a}</li>" for a in asks)
    return (f'<div class="sc"><h3>{title}</h3><div class="when">{when}</div>{prompt(MODE + text)}{ex}'
            f'<div class="ask"><b>AI 接著會問你</b><ul class="bl">{ask}</ul></div></div>')


def pair(a, b=None):
    return d.row(d.col(a, 680), d.col(b, 680) if b else "")


projects = C["projects"]
TC = C["tenant_code"]  # AI GO 網址開頭：https://<tenant_code>.ai-go.app
repo_urls = "<br>".join(f"https://github.com/{p['repo']}" for p in projects)
contact = C.get("tech_contact", {})
who = contact.get("name", "工程師") + (f"（GitHub @{contact['github']}）" if contact.get("github") else "")

# ── 封面、目錄 ──
d.cover("不會寫程式也能一起改系統：<br>找到你的情境，複製那句話貼給 AI，回答它的問題就好",
        meta=[("對象", C.get("audience", "一起開發系統的同仁")), ("適用", "Claude Code、Codex")])
d.toc()

# ── 開始之前 ──
d.slide(P0, "這份指南怎麼用", "AI 已經學過怎麼跟你合作，你只需要開口。", d.row(
    d.col(S([("找到你現在的情境", "想加功能、畫面不對、壞了、收到工程師發來的請求……每個情境一張卡"),
             ("複製那段話，貼給 AI", "藍色虛線框裡的字可以直接複製；<b>橘色【】的地方換成你自己的話</b>"),
             ("回答 AI 的問題", "它會把要問的整理成幾題，你照編號回答；重要的決定會先用白話講清楚，你說可以才做"),
             ("做完先看、驗收過才上線", "每個功能 AI 都會實際操作一次給你看；想找工程師一起看，AI 會幫你寫好")]), 760),
    d.col(prompt(MODE + "我想【用一句話說你想做的事】。", label="最萬用的一句", cls="big")
          + N("<b>每段話都用「用協作開發模式。」開頭</b>：AI 會切換成白話、先問清楚再做的工作方式。")
          + N("不確定怎麼講也沒關係，直接說「我不知道從哪開始」，AI 會列出選項給你選。")
          + N("<b>要用 AI GO 取代現在在用的系統</b>（例：" + escape(EX.get("migration", "104 人資後台")) + "）：看 PART C「原系統搬遷任務」。"))))

# 貼這段時協作 skill 還沒裝，AI 只看得到這段字：指令要寫明（-y 免互動、-a 只裝 Claude Code 與 Codex）
install = ("請幫我完成 AI GO 協作開發的安裝，每一步用白話告訴我在做什麼，需要我動手的地方講清楚：<br>"
           "1. 確認有 Node.js、Python、uv、GitHub CLI，沒有就先幫我裝；再安裝兩個 skill，"
           "各執行一次 npx skills add 網址 -g -y -a claude-code codex：<br>"
           f"{SKILLS[0]}<br>{SKILLS[1]}<br>"
           "2. 用 gh auth status 確認 GitHub 已登入，沒登入就用 gh auth login --web 帶我登入<br>"
           f"3. 用 aigo-builder 的 aigo_auth.py setup-workspace 在我家目錄建 <span class=\"url\">aigo-projects/{escape(TC)}</span> 工作區"
           f"（網址 https://{escape(TC)}.ai-go.app），再用 gh repo clone 把這些專案下載到工作區裡：<br>{repo_urls}<br>"
           "4. 執行 aigo-client-collab 的 scripts/install_hooks.py，設定每次開新對話自動檢查更新")
d.slide(P0, "第一次使用：安裝", "只要做一次。打開 Claude Code 或 Codex，開一個新對話，貼上這段。", d.row(
    d.col(prompt(install, label="第一次使用，複製這段貼給 AI"), 860),
    d.col(T(["開始前要有", "沒有的話"], [
        ["GitHub 帳號", "到 github.com 免費註冊，把帳號名稱告訴工程師，請他加進專案"],
        ["AI GO 帳號", "用平時登入系統的帳號；第一次用到時，可以選用瀏覽器登入，或存在你的電腦裡"],
        ["Claude Code 或 Codex", "請工程師協助安裝其中一個"],
    ], ["200px", "auto"], cls="roomy") + N("裝好後<b>關掉 AI 工具重開</b>（或開新對話），新的工作方式才會生效。")
          + N("過程中瀏覽器會打開 GitHub 請你授權：<b>密碼只在瀏覽器的登入頁輸入，不要打在對話框裡。</b>", "warn"))))

rows = [[f"<b>{escape(p['name'])}</b>", escape(p.get("desc", "")), escape(p["repo"].split("/")[-1])] for p in projects]
d.slide(P0, "每次開始：先開對的資料夾", "一支系統一個資料夾。要改哪一支，就在 AI 工具裡打開那個資料夾，再開新對話。", d.row(
    d.col(T(["系統", "內容", "資料夾名稱"], rows, ["240px", "auto", "240px"], cls="roomy")
          + N("不知道資料夾在哪：在任何對話裡問「我的專案資料夾在哪裡？」"), 860),
    d.col(S([("打開 AI 工具，選資料夾", "Claude Code 桌面版：選擇資料夾；Codex：開啟專案資料夾"),
             ("開一個新對話", "一件事一個對話最清楚；做完或換題目就開新的"),
             ("貼上情境卡的那段話", "下一部分有 12 張情境卡")]))))

# ── A 情境開場白 ──
d.divider(PA, "PART A", "情境開場白", "找到你現在的情況，複製那段話。橘色【】換成你的話。")

cards = [
    scenario("想加或改功能", "想多一個欄位、多一個按鈕、多一種報表，或改現在的做法。",
             "我想在【哪個畫面】加上【什麼功能】，因為【原因】。",
             ["誰會用、要做什麼、做完想看到什麼（整理成幾題，照編號回答）", "有沒有例外情況（例：跨月、離職）", "動手前會先給你一份白話的做法摘要"], EX.get("feature")),
    scenario("畫面跟我想的不一樣", "排版、文字、欄位順序、顏色、按鈕位置不順手。",
             "【哪個畫面】的【哪個地方】跟我想的不一樣，我希望【改成怎樣】。（可以附截圖）",
             ["確認是哪個畫面、哪個位置", "改好先給你看，你說可以才上線"], EX.get("screen")),
    scenario("有東西壞了", "按了沒反應、出現錯誤訊息、資料不對或不見。",
             "【哪個畫面】有問題：我【做了什麼】，以為會【預期的結果】，結果【實際看到的】。（附截圖最快）",
             ["什麼時候開始的、每次都會嗎", "影響很多人的話，要不要先退回上一版"], EX.get("broken")),
    scenario("想了解現在怎麼運作", "想知道某個數字怎麼算、某個按鈕會做什麼，先不改。",
             "用白話解釋給我聽：【哪個功能】現在是怎麼運作的？",
             ["AI 會讀系統後用「情境 → 結果」回答", "聽完想改，再說「那幫我改成…」"], EX.get("explain")),
    scenario("有想法但不知道怎麼講", "只有一個模糊的念頭，或不知道從哪開始。",
             "我有個想法但不知道怎麼講，請一題一題問我。",
             ["你現在怎麼做這件事、哪裡不方便", "會給你 2～3 個做法，每個說清楚結果，讓你選"]),
    scenario("接續上次", "上次的對話關掉了，想從上次停下的地方繼續。",
             "上次做到哪裡了？告訴我還差什麼。",
             ["AI 會整理：做完的、做一半的、等工程師回覆的", "問你要從哪一件繼續"]),
    scenario("查資料或匯出", "想查某些資料、匯出成 Excel，或一次改一批資料。",
             "幫我【查／匯出／改】【哪些資料，例：這個月全所的請假紀錄】，【用途，例：給所長看】。",
             ["範圍：哪段期間、哪些人、要哪些欄位", "要改資料時，先算會動到幾筆、先備份、先改一筆給你看"], EX.get("data")),
    scenario("邀請同事、調權限", "新同事要開帳號，或某人要能看到、改到更多資料。",
             "幫我【邀請新同事／調整某人的權限】：【誰、要做什麼】。",
             ["對方的 Email、要給哪一種角色", "寄邀請信或改權限前，會先跟你確認一次"], EX.get("member")),
    scenario("收到工程師發來的請求", "工程師傳來一個網址（GitHub issue），請你幫忙研究或回答問題。",
             "請讀工程師發來的這個請求，開始研究：【網址】",
             ["工程師想知道什麼、要怎麼查", "跟你的業務有關的問題，一次一題", "整理好的結果先給你看，你說可以才回覆工程師"]),
    scenario("做完了，要上線", "改好的地方你已經看過，想讓同事開始用。",
             "剛剛改的我看過了，可以上線。",
             ["AI 會先給你看驗收結果，講這次改了什麼、誰會受影響", "你說好才上線；上線後它會到正式網址再操作一次"]),
    scenario("上線後發現有問題", "新版上線後，同事反映不對勁。",
             "剛上線的【哪個功能】有問題：【狀況】。先告訴我要不要退回上一版。",
             ["要先退回讓大家能用，還是直接修", "退回或修好後，請你再確認一次"]),
]
cards.append('<div class="sc"><h3>其他情況</h3><div class="when">上面都對不上也沒關係，用自己的話說。</div>'
             + prompt(MODE + "【用你自己的話，說你想做的事或遇到的狀況】")
             + '<div class="ask"><b>AI 會怎麼做</b><ul class="bl"><li>先判斷是哪一種情況，對不上就列選項讓你選</li>'
               '<li>把要問的整理成幾題，問清楚才動手</li></ul></div></div>')
titles = ["加功能・改畫面", "壞了・想了解", "不知道怎麼講・接續", "查資料・邀請同事", "收到請求・要上線", "上線後・其他情況"]
for i in range(0, len(cards), 2):
    d.slide(PA, titles[i // 2], "複製藍框裡的字，把橘色【】換成你的話。", pair(*cards[i:i + 2]), bg="soft")

# ── B 合作規則 ──
d.divider(PB, "PART B", "一起合作", "怎麼跟工程師一起合作、上線前後會發生什麼、怎麼保護資料。")

d.slide(PB, "跟工程師一起合作", "工程師是隊友，不是關卡：每一步你都可以自己完成，需要時再找他。", d.row(
    d.col(T(["什麼時候", "AI 會幫你"], [
        ["同一個問題試兩次還沒解開", "寫一張請協助的單子，附上查到的，請工程師一起看"],
        ["會影響其他系統或其他部門", "在單子上 @工程師 說一聲，照常進行"],
        ["想先請人看過再上線", "請工程師看一眼；要不要等他，由你決定"],
        ["做到一半想請工程師接手", "把做到一半的整理好交給他，正式版不受影響"],
        ["AI GO 平台本身出問題", "整理一份回報給 AI GO 開發團隊，你說可以才送"],
    ], ["380px", "auto"], cls="roomy"), 900),
    d.col(S([("AI 先寫好草稿給你看", "代表你發言的東西，都會先給你看"),
             ("你說可以，AI 才送出", f"工程師（{escape(who)}）會在上面回覆"),
             ("工程師請你幫忙研究", "他會傳一個網址給你，貼給 AI 就好")]))))

d.slide(PB, "上線前後", "你可以自己決定上線；上線前 AI 一定會先跟你確認。", d.row(
    d.col(S([("實際操作驗收", "每個做完的功能，AI 都會實際點一次（或跑自動測試），截圖給你看"),
             ("先給你看", "能先看試印版（只有你看得到）就先看；不能的話會用文字說明做完的樣子"),
             ("講清楚影響", "這次改了什麼、哪些同事會看到不一樣；改了就回不去的地方會特別講"),
             ("確認線上的版本", "工程師剛好也發布了新版時，AI 會先跟你說，免得互相蓋掉"),
             ("你說好才上線", "上線後 AI 會到大家在用的網址再操作一次，並把這次的修改存進專案紀錄")]), 760),
    d.col(prompt(MODE + "剛上線的【哪個功能】有問題，先幫我退回上一版。", label="上線後有問題，最快的一句")
          + N("上線是全部同事都會用到的版本。<b>拿不準就先別上線</b>，說「先不要上線，我想再看一次」。"))))

d.slide(PB, "保護資料與小訣竅", "幾個習慣，讓合作更順、資料更安全。", d.row(
    d.col("<h3 style='margin:0 0 8px;font-size:22px'>保護資料</h3>" + B([
        "<b>密碼自己輸入</b>：在瀏覽器的登入頁，或 AI 幫你打開的設定檔裡打，不要貼進對話",
        "描述問題時不用貼真實的個資或薪資，說「某位員工」「一筆 3 月的請假」就好",
        "截圖前，可以的話先遮掉身分證號、薪資這類資料；AI 不會把真實資料寫進單子或程式",
        "匯出的資料放在專案以外的資料夾，AI 會告訴你在哪",
        "AI 要送出單子或留言前會先給你看；不想送就說「先不要」",
    ]), 680),
    d.col("<h3 style='margin:0 0 8px;font-size:22px'>對話小訣竅</h3>" + T(["想要", "就說"], [
        ["聽不懂", "「用白話再講一次」"],
        ["先看計畫再動手", "「先別動手，先說你打算怎麼做」"],
        ["馬上停下來", "「停」"],
        ["一次只處理一件", "「先做第一件，其他的記下來」"],
        ["確認現在的狀態", "「現在改到哪裡了？上線了嗎？」"],
    ], ["220px", "auto"], cls="roomy"), 680)))

# ── C 原系統搬遷任務 ──
SVC = EX.get("migration", "104 人資後台")
STORE_CLAUDE = "https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn"
STORE_CODEX = "https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg"
DOC_CODEX = "https://learn.chatgpt.com/docs/chrome-extension"


def link(url):
    return f'<a class="url lk" href="{url}">{url}</a>'


def ext_card(title, lines, links):
    li = "".join(f"<li>{x}</li>" for x in lines)
    lk = "".join(f'<div class="lkrow"><span>{k}</span>{link(u)}</div>' for k, u in links)
    return f'<div class="sc"><h3>{title}</h3><ul class="bl ask">{li}</ul>{lk}</div>'


d.divider(PC, "PART C", "原系統搬遷任務",
          f"要用 AI GO 取代一套正在用的系統（例：{escape(SVC)}）時，讓 AI 把原系統從裡到外研究一遍，再一批一批搬過來。")

d.slide(PC, "先準備：Chrome 擴充套件與登入", "AI 要透過你的 Chrome 去看原系統，所以先裝一個擴充套件，再由你登入原系統。", d.row(
    d.col(S([("裝 Chrome 擴充套件", "用 Claude Code 的裝 Claude 的；用 Codex 的裝 OpenAI 的（右邊兩張卡）"),
             ("在 Chrome 登入原系統", f"例：打開 {escape(SVC)}，用平常的帳號登入，停在登入後的首頁"),
             ("回到 AI 工具，開新對話", "在要接手的那支系統的資料夾裡開新對話"),
             ("貼上下一頁的提示詞", "AI 會先確認連得上 Chrome、看得到原系統，再開始")])
          + N("<b>密碼只在 Chrome 的登入頁輸入</b>；需要手機驗證碼時你自己處理。AI 不會幫你輸入密碼。", "warn"), 640),
    d.col(ext_card("用 Claude Code", [
              "到 Chrome 商店按「加到 Chrome」，用同一個 Claude 帳號登入（需要 Claude 付費方案）",
              "回到 Claude Code 說「幫我確認 Chrome 擴充套件有沒有連上」"],
              [("Chrome 商店", STORE_CLAUDE)])
          + ext_card("用 Codex", [
              "在 Codex 桌面版的「外掛（Plugins）」加入 Chrome，照畫面裝好擴充套件，看到「已連線」",
              "回到 Codex 說「幫我確認 Chrome 擴充套件有沒有連上」（對話裡可用 @Chrome）"],
              [("Chrome 商店", STORE_CODEX), ("官方說明", DOC_CODEX)]), 720)), bg="soft")

migrate = (MODE + "走「原系統搬遷任務」。我們要用 AI GO 取代【原系統名稱，例：" + escape(SVC) + "】，"
           "我已經在 Chrome 登入好了，網址是【原系統網址】，要由【哪一支 AI GO 系統，或「開一支新的」】接手。"
           "請用 Chrome 擴充套件照下面順序做，<b>每一段做完先給我看，我說可以才往下</b>：<br>"
           "1. 功能研究：逐一點開每個選單，列出所有畫面、欄位、流程、報表、通知、角色權限和系統自動算的數字，附截圖（遮掉個資）。<br>"
           "2. 歷史資料：列出有哪些資料、各多少筆、最早到哪一年，問我要搬哪些、哪段期間；能用原系統的匯出就匯出，"
           "沒有匯出才一頁一頁讀；檔案放在我電腦的搬遷資料夾、不放進專案，最後核對筆數。<br>"
           "3. 資料怎麼進 AI GO：每種資料放到 AI GO 的哪本帳冊、哪一欄，對不上的怎麼處理，舊編號怎麼對新編號；"
           "先匯入 1 筆給我看，我說可以再整批匯入，匯完核對筆數。<br>"
           "4. 值得保留的功能：列出原系統做得好、希望 AI GO 也有的功能，和不方便、不要照搬的地方，讓我分成「一定要／最好有／不需要」。<br>"
           "5. 規格書：依我選的內容寫規格（誰用、哪個畫面、流程、例外）、資料結構、權限，排好分幾批做、先做哪批。<br>"
           "6. 衝突點：跟 AI GO 現有功能、之前定的規則、其他系統共用的資料，還有原系統做法跟我們實際做法不一樣的地方，"
           "一條一條列出，各給 2～3 個做法和你的建議，讓我決定。<br>"
           "7. 實作與驗收：一批一批做，每個功能做完都要實際操作驗收，並拿同一筆資料跟原系統比對結果。<br>"
           "8. 切換：一起定好新舊並行多久、哪天停用原系統、停用前最後一次匯出、出問題怎麼辦。<br>"
           "研究時對原系統只看不改，要按會改東西或會通知別人的按鈕前先問我；要匯出檔案前也先問我。")
d.slide(PC, "搬遷任務的提示詞", "準備好之後，在要接手的系統資料夾開新對話，貼上這一整段。橘色【】換成你的內容。",
        prompt(migrate, label="原系統搬遷任務，複製這一整段貼給 AI", cls="mig"))

d.slide(PC, "搬遷過程中，你要做的事", "整個搬遷會分很多次對話完成。每一段 AI 做完都會停下來，等你確認。", d.row(
    d.col(T(["階段", "你要做的"], [
        ["1 功能研究", "看功能清單，補上漏掉的、標出其實沒在用的"],
        ["2 歷史資料", "決定搬哪些、哪段期間；每次匯出前 AI 會先問你"],
        ["3 資料對應", "確認每種資料放到哪；看過試匯入的 1 筆，說可以再整批匯入"],
        ["4 保留的功能", "把功能分成「一定要／最好有／不需要」"],
        ["5 規格書", "看白話摘要，確認誰用、做什麼、看到什麼"],
        ["6 衝突點", "每一條選一個做法"],
        ["7 實作與驗收", "看操作截圖和新舊系統比對的結果，說可以才上線"],
        ["8 切換", "一起定並行多久、哪天停用原系統"],
    ], ["220px", "auto"], cls="roomy"), 900),
    d.col(B([
        "<b>研究時原系統只看不改</b>：要按會改東西的按鈕前，AI 會先問你",
        "匯出的資料有個資，<b>放在你電腦的工作區資料夾</b>，不會放進專案",
        "原系統跳出驗證碼或限制次數時，AI 會停下來，改用官方匯出或請你向廠商要資料",
        "做到一半可以說「先停在這裡」；下次開新對話說「接續上次的搬遷」就能繼續",
    ]) + prompt(MODE + "接續上次的原系統搬遷任務，告訴我做到哪一段、下一步要我確認什麼。", label="下次繼續時貼這句"))))

d.back_cover("有問題時", "先問 AI；需要時，它會幫你寫給工程師。",
             contact=C.get("contact", []))

stem = f"AI GO {C['tenant']} 協作開發 開口指南 {d.version} {d.made:%Y%m%d}"
d.write(CLIENT.parent / f"{stem}.html")
