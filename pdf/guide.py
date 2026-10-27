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
"""

d = Deck(tenant=C["tenant"], app="協作開發", purposes=["操作說明"], title="開口指南",
         version=C.get("version", "v1"), made=C.get("made"), extra_css=CSS)
T, S, N, B = d.table, d.steps, d.note, d.bullets
P0, PA, PB = "開始之前", "A　情境開場白", "B　合作規則"
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
repo_urls = "<br>".join(f"https://github.com/{p['repo']}" for p in projects)
contact = C.get("tech_contact", {})
who = contact.get("name", "工程師") + (f"（GitHub @{contact['github']}）" if contact.get("github") else "")

# ── 封面、目錄 ──
d.cover("不會寫程式也能一起改系統：<br>找到你的情境，複製那句話貼給 AI，回答它的問題就好",
        meta=[("對象", C.get("audience", "一起開發系統的同仁")), ("適用", "Claude Code、Codex")])
d.toc()

# ── 開始之前 ──
d.slide(P0, "這份指南怎麼用", "AI 已經學過怎麼跟你合作，你只需要開口。", d.row(
    d.col(S([("找到你現在的情境", "想加功能、畫面不對、壞了、收到工程師的工單……每個情境一張卡"),
             ("複製那段話，貼給 AI", "藍色虛線框裡的字可以直接複製；<b>橘色【】的地方換成你自己的話</b>"),
             ("回答 AI 的問題", "它會一次問一題，問清楚才動手；做完會請你看過、你說可以才上線"),
             ("碰到難題，AI 會交給工程師", "它會幫你寫好工單（issue），你看過說可以就送出")]), 760),
    d.col(prompt(MODE + "我想【用一句話說你想做的事】。", label="最萬用的一句", cls="big")
          + N("<b>每段話都用「用協作開發模式。」開頭</b>：AI 會切換成白話、先問清楚再做的工作方式。")
          + N("不確定怎麼講也沒關係，直接說「我不知道從哪開始」，AI 會列出選項給你選。"))))

# 貼這段時協作 skill 還沒裝，AI 只看得到這段字：指令要寫明（-y 免互動、-a 只裝 Claude Code 與 Codex）
install = ("請幫我完成 AI GO 協作開發的安裝，每一步用白話告訴我在做什麼，需要我動手的地方講清楚：<br>"
           "1. 安裝兩個 skill，各執行一次 npx skills add 網址 -g -y -a claude-code codex（沒有 Node.js 就先幫我裝）：<br>"
           f"{SKILLS[0]}<br>{SKILLS[1]}<br>"
           "2. 用 gh auth status 確認 GitHub 已登入；沒有 gh 就先裝，沒登入就用 gh auth login --web 帶我登入<br>"
           f"3. 用 gh repo clone 把這些專案下載到我家目錄的 aigo-projects 資料夾：<br>{repo_urls}")
d.slide(P0, "第一次使用：安裝", "只要做一次。打開 Claude Code 或 Codex，開一個新對話，貼上這段。", d.row(
    d.col(prompt(install, label="第一次使用，複製這段貼給 AI", cls="big")
          + N("過程中瀏覽器會打開 GitHub 請你授權：<b>密碼只在瀏覽器的登入頁輸入，不要打在對話框裡。</b>", "warn"), 820),
    d.col(T(["開始前要有", "沒有的話"], [
        ["GitHub 帳號", "到 github.com 免費註冊，把帳號名稱告訴工程師，請他加進專案"],
        ["AI GO 帳號", "用平時登入系統的帳號；要上線新版時才會用到"],
        ["Claude Code 或 Codex", "請工程師協助安裝其中一個"],
    ], ["200px", "auto"], cls="roomy") + N("裝好後<b>關掉 AI 工具重開</b>（或開新對話），新的工作方式才會生效。"))))

rows = [[f"<b>{escape(p['name'])}</b>", escape(p.get("desc", "")), escape(p["repo"].split("/")[-1])] for p in projects]
d.slide(P0, "每次開始：先開對的資料夾", "一支系統一個資料夾。要改哪一支，就在 AI 工具裡打開那個資料夾，再開新對話。", d.row(
    d.col(T(["系統", "內容", "資料夾名稱"], rows, ["240px", "auto", "240px"], cls="roomy")
          + N("不知道資料夾在哪：在任何對話裡問「我的專案資料夾在哪裡？」"), 860),
    d.col(S([("打開 AI 工具，選資料夾", "Claude Code 桌面版：選擇資料夾；Codex：開啟專案資料夾"),
             ("開一個新對話", "一件事一個對話最清楚；做完或換題目就開新的"),
             ("貼上情境卡的那段話", "下一部分有 10 張情境卡")]))))

# ── A 情境開場白 ──
d.divider(PA, "PART A", "情境開場白", "找到你現在的情況，複製那段話。橘色【】換成你的話。")

cards = [
    scenario("想加或改功能", "想多一個欄位、多一個按鈕、多一種報表，或改現在的做法。",
             "我想在【哪個畫面】加上【什麼功能】，因為【原因】。",
             ["誰會用、什麼時候用", "做完後你希望看到什麼", "有沒有例外情況（例：跨月、離職）"], EX.get("feature")),
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
    scenario("收到工程師的工單", "工程師傳來一個 GitHub issue 網址，請你研究或回答問題。",
             "請讀這個 issue 開始研究：【issue 網址】",
             ["工程師想知道什麼、要怎麼查", "跟你的業務有關的問題，一次一題", "整理好的結果先給你看，你說可以才回覆工程師"]),
    scenario("做完了，要上線", "改好的地方你已經看過，想讓同事開始用。",
             "剛剛改的我看過了，可以上線。",
             ["AI 會先講這次改了什麼、誰會受影響，你說好才上線", "上線後它會到正式網址檢查一次"]),
    scenario("上線後發現有問題", "新版上線後，同事反映不對勁。",
             "剛上線的【哪個功能】有問題：【狀況】。先告訴我要不要退回上一版。",
             ["要先退回讓大家能用，還是直接修", "退回或修好後，請你再確認一次"]),
]
cards.append('<div class="sc"><h3>其他情況</h3><div class="when">上面都對不上也沒關係，用自己的話說。</div>'
             + prompt(MODE + "【用你自己的話，說你想做的事或遇到的狀況】")
             + '<div class="ask"><b>AI 會怎麼做</b><ul class="bl"><li>先判斷是哪一種情況，對不上就列選項讓你選</li>'
               '<li>一次問一題，問清楚才動手</li></ul></div></div>')
titles = ["加功能・改畫面", "壞了・想了解", "不知道怎麼講・接續", "收到工單・要上線", "上線後・其他情況"]
for i in range(0, len(cards), 2):
    d.slide(PA, titles[i // 2], "複製藍框裡的字，把橘色【】換成你的話。", pair(*cards[i:i + 2]), bg="soft")

# ── B 合作規則 ──
d.divider(PB, "PART B", "合作規則", "AI 什麼時候會交給工程師、上線前後會發生什麼、怎麼保護資料。")

d.slide(PB, "什麼時候交給工程師", "碰到下面這些，AI 不會自己動手，會幫你寫好工單交給工程師。", d.row(
    d.col(T(["情況", "為什麼"], [
        ["改誰看得到什麼資料、角色權限", "像換整棟大樓的門禁，改錯會讓不該看的人看到"],
        ["刪除或改動已經有資料的欄位", "帳冊裡已有資料，改格式可能弄壞舊資料"],
        ["一次改、匯入或刪除大量資料", "改到很多筆真實資料，沒有復原鍵"],
        ["算錢的規則：金額、稅、薪資、費率", "改錯會直接算錯帳"],
        ["跟其他系統串接、定時自動執行", "需要鑰匙與線路設定"],
        ["邀請成員、平台設定", "平台的總開關"],
        ["同一個問題 AI 試兩次還解不開", "換工程師看比較快"],
    ], ["420px", "auto"], cls="roomy"), 900),
    d.col(S([("AI 跟你說「這題交給工程師」", "已經問清楚的內容都會寫進去"),
             ("你看工單草稿", "沒問題就說「可以，送出」"),
             ("AI 送出，給你工單網址", f"工程師（{escape(who)}）會在工單上回覆"),
             ("你可以先做別的事", "工程師如果請你研究，會傳工單網址給你")]))))

d.slide(PB, "上線前後", "你可以自己決定上線；上線前 AI 一定會先跟你確認。", d.row(
    d.col(S([("先給你看", "能先看試印版（只有你看得到）就先看；不能的話會用文字說明做完的樣子"),
             ("講清楚影響", "這次改了什麼、哪些同事會看到不一樣的地方"),
             ("檢查工程師有沒有也在改", "工程師剛好也在改同一支系統時，AI 會先停下來，免得互相蓋掉"),
             ("你說好才上線", "上線後 AI 會到大家在用的網址檢查一次，並把這次的修改存進專案紀錄")]), 760),
    d.col(prompt(MODE + "剛上線的【哪個功能】有問題，先幫我退回上一版。", label="上線後有問題，最快的一句")
          + N("上線是全部同事都會用到的版本。<b>拿不準就先別上線</b>，說「先不要上線，我想再看一次」。"))))

d.slide(PB, "保護資料與小訣竅", "幾個習慣，讓合作更順、資料更安全。", d.row(
    d.col("<h3 style='margin:0 0 8px;font-size:22px'>保護資料</h3>" + B([
        "<b>不要把密碼、鑰匙貼進對話</b>：要登入時，瀏覽器會打開登入頁，在那裡輸入",
        "描述問題時不用貼真實的個資或薪資，說「某位員工」「一筆 3 月的請假」就好",
        "截圖前，可以的話先遮掉身分證號、薪資這類資料；AI 不會把真實資料寫進工單或程式",
        "AI 要送出工單或回覆前會先給你看；不想送就說「先不要」",
    ]), 680),
    d.col("<h3 style='margin:0 0 8px;font-size:22px'>對話小訣竅</h3>" + T(["想要", "就說"], [
        ["聽不懂", "「用白話再講一次」"],
        ["先看計畫再動手", "「先別動手，先說你打算怎麼做」"],
        ["馬上停下來", "「停」"],
        ["一次只處理一件", "「先做第一件，其他的記下來」"],
        ["確認現在的狀態", "「現在改到哪裡了？上線了嗎？」"],
    ], ["220px", "auto"], cls="roomy"), 680)))

d.back_cover("有問題時", "先問 AI；AI 處理不了的，它會幫你寫工單給工程師。",
             contact=C.get("contact", []))

stem = f"AI GO {C['tenant']} 協作開發 開口指南 {d.version} {d.made:%Y%m%d}"
d.write(CLIENT.parent / f"{stem}.html")
