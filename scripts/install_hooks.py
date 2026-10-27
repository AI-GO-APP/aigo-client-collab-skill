"""
install_hooks.py — 幫 Claude Code、Codex 裝 SessionStart hook：每次開新對話先檢查兩個 skill
（aigo-client-collab、aigo-builder）有沒有新版，有就同步（實際同步由各自的 check_update.py 做）。

客戶不會自己改設定檔，所以由 AI 在第一次安裝時執行本腳本（references/setup.md §5）。

設計約束：
- **零相依**：只用標準函式庫（Python 3.9+；檢查 Codex 設定需要 3.11+ 的 tomllib，沒有就略過驗證）。
- **冪等**：設定裡已經有指到同一支 check_update.py 的 hook 就不再加；可以重複執行。
- **不破壞既有設定**：只追加；寫之前先備份成 `<檔名>.bak-aigo`；Claude Code 設定不是合法 JSON 就不動並回報。
- 只處理電腦上有的 agent（有 `~/.claude` 才寫 Claude Code，有 `~/.codex` 才寫 Codex）。
- Codex 會要求使用者在 Codex 裡核准新的 hook（hooks.state 的 trusted_hash），核准前不會執行。

用法：
    python install_hooks.py            # 安裝（有缺才寫）
    python install_hooks.py --check    # 只檢查，不寫；全部裝好 exit 0，有缺 exit 1
    python install_hooks.py --json     # 機器可讀輸出
"""

from __future__ import annotations
import argparse
import json
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_NAMES = ("aigo-client-collab", "aigo-builder")
PYTHON = "python" if sys.platform == "win32" else "python3"
TIMEOUT = 120  # 同步要下載 main.zip 或 git fetch；沒新版時 3 秒內結束（同 aigo-builder 範本）
MATCHER = "startup|resume"


def _skill_dirs() -> dict[str, Path]:
    """找兩個 skill 的安裝目錄：本 skill 就是 SKILL_DIR；aigo-builder 先找同層，再找常見位置。"""
    found = {"aigo-client-collab": SKILL_DIR}
    home = Path.home()
    for cand in (SKILL_DIR.parent / "aigo-builder", home / ".agents" / "skills" / "aigo-builder",
                 home / ".claude" / "skills" / "aigo-builder", home / ".codex" / "skills" / "aigo-builder"):
        if (cand / "scripts" / "check_update.py").exists():
            found["aigo-builder"] = cand.resolve()
            break
    return found


def _script(skill_dir: Path) -> str:
    return (skill_dir / "scripts" / "check_update.py").as_posix()


def _command(skill_dir: Path) -> str:
    return f'{PYTHON} "{_script(skill_dir)}"'


def _mentions(text: str, skill_dir: Path) -> bool:
    """設定裡是否已有這個 skill 的 check_update.py hook。只比對 `<skill 目錄名>/scripts/check_update.py`：
    同一個 skill 常有兩個路徑（~/.agents/skills 的實體與 ~/.claude/skills 的連結），任一個裝過就算有。
    JSON 裡的反斜線是跳脫過的（\\\\），所以先把連續反斜線都換成 /。"""
    norm = lambda s: s.replace("\\\\", "/").replace("\\", "/").lower()
    return f"/{skill_dir.name}/scripts/check_update.py".lower() in norm(text)


def _backup(path: Path) -> None:
    if path.exists():
        shutil.copy2(path, path.with_name(path.name + ".bak-aigo"))


# ───────── Claude Code：~/.claude/settings.json ─────────
def claude_code(skills: dict[str, Path], write: bool) -> dict:
    home = Path.home() / ".claude"
    if not home.exists():
        return {"agent": "claude-code", "status": "skipped", "reason": "沒有 ~/.claude（沒裝 Claude Code）"}
    path = home / "settings.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}
    except ValueError as e:
        return {"agent": "claude-code", "status": "error", "reason": f"{path} 不是合法 JSON，未修改：{e}"}
    raw = json.dumps(data, ensure_ascii=False)
    missing = [n for n, d in skills.items() if not _mentions(raw, d)]
    if not missing:
        return {"agent": "claude-code", "status": "ok", "file": str(path)}
    if not write:
        return {"agent": "claude-code", "status": "missing", "missing": missing, "file": str(path)}
    groups = data.setdefault("hooks", {}).setdefault("SessionStart", [])
    groups.append({"matcher": MATCHER, "hooks": [
        {"type": "command", "command": _command(skills[n]), "timeout": TIMEOUT} for n in missing]})
    _backup(path)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"agent": "claude-code", "status": "installed", "added": missing, "file": str(path)}


# ───────── Codex：~/.codex/config.toml ─────────
def _toml_block(name: str, skill_dir: Path) -> str:
    return (f"\n# {name}：每次開新對話先檢查並同步 skill 更新（aigo-client-collab scripts/install_hooks.py 加的）\n"
            f"[[hooks.SessionStart]]\nmatcher = \"{MATCHER}\"\n\n[[hooks.SessionStart.hooks]]\ntype = \"command\"\n"
            f"command = '{_command(skill_dir)}'\ntimeout = {TIMEOUT}\nstatusMessage = \"檢查並同步 {name} Skill 更新\"\n")


def codex(skills: dict[str, Path], write: bool) -> dict:
    home = Path.home() / ".codex"
    if not home.exists():
        return {"agent": "codex", "status": "skipped", "reason": "沒有 ~/.codex（沒裝 Codex）"}
    path = home / "config.toml"
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    missing = [n for n, d in skills.items() if not _mentions(text, d)]
    if not missing:
        return {"agent": "codex", "status": "ok", "file": str(path)}
    if not write:
        return {"agent": "codex", "status": "missing", "missing": missing, "file": str(path)}
    new = text.rstrip("\n") + "\n" + "".join(_toml_block(n, skills[n]) for n in missing)
    try:
        import tomllib  # Python 3.11+
        tomllib.loads(new)
    except ModuleNotFoundError:
        pass
    except Exception as e:  # 合併後不是合法 TOML 就不寫
        return {"agent": "codex", "status": "error", "reason": f"合併後的 {path} 不是合法 TOML，未修改：{e}"}
    _backup(path)
    path.write_text(new, encoding="utf-8")
    return {"agent": "codex", "status": "installed", "added": missing, "file": str(path),
            "note": "Codex 會請使用者核准新的 hook，核准後才會執行"}


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description="幫 Claude Code、Codex 裝兩個 skill 的自動更新 hook")
    ap.add_argument("--check", action="store_true", help="只檢查不寫；有缺 exit 1")
    ap.add_argument("--json", action="store_true", help="機器可讀輸出")
    args = ap.parse_args()

    skills = _skill_dirs()
    results = [claude_code(skills, not args.check), codex(skills, not args.check)]
    absent = [n for n in SKILL_NAMES if n not in skills]
    if args.json:
        print(json.dumps({"skills": {k: str(v) for k, v in skills.items()}, "not_installed": absent,
                          "agents": results}, ensure_ascii=False, indent=2))
    else:
        if absent:
            print(f"找不到 skill：{'、'.join(absent)}（先安裝再重跑本腳本）")
        for r in results:
            detail = r.get("reason") or "、".join(r.get("added") or r.get("missing") or []) or r.get("file", "")
            print(f"[{r['agent']}] {r['status']}：{detail}" + (f"（{r['note']}）" if r.get("note") else ""))
    bad = absent or any(r["status"] in ("missing", "error") for r in results)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
