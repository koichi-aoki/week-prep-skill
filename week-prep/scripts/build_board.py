# -*- coding: utf-8 -*-
"""来週の準備ボードを作る: データ(JSON) + 雛形(assets/board-template.html) → HTML

使い方:
  python build_board.py <board-data.json> [出力.html] [--open]
  出力を省略すると board-data.json と同じフォルダに「準備ボード.html」を書く。
  --open を付けると、できたボードを既定のブラウザで開く。
標準ライブラリだけで動く（Python 3.8以上）。データの形式は references/board-data.md。
"""
import html
import json
import sys
import webbrowser
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "board-template.html"

STATUSES = {"you", "made", "ready", "ask"}
IMPROVE_CLS = {"i-now", "i-info", "i-perm"}
FOCUS_COLORS = {"green", "amber"}


def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)


def need(obj, keys, where):
    for k in keys:
        if k not in obj or obj[k] in (None, ""):
            fail(f"{where} に {k} がない")


def validate(d):
    warns = []
    need(d, ["meta", "actions", "made", "ready", "asks", "improve", "focus", "days", "events", "notes"], "データ")
    need(d["meta"], ["title"], "meta")
    if len(d["meta"]["title"]) > 20:
        warns.append(f"タイトルが長い（{len(d['meta']['title'])}字）。『M/D週 準備ボード』程度の名前にする")

    ids = set()
    for g in d["actions"]:
        need(g, ["g", "items"], "actions のグループ")
        for a in g["items"]:
            need(a, ["id", "when", "t", "how", "done"], f"actions「{g['g']}」の項目")
            if a["id"] in ids:
                fail(f"actions の id が重複: {a['id']}")
            ids.add(a["id"])
            a.setdefault("dur", "")
            a.setdefault("use", "―")

    for m in d["made"]:
        need(m, ["t", "when", "what", "state", "p"], "made")
    for r in d["ready"]:
        if not isinstance(r, list) or len(r) != 5:
            fail(f"ready は5列（もの・使う日・誰がいつ・場所・当日の一言）: {r}")

    aids = set()
    for a in d["asks"]:
        need(a, ["side", "id", "who", "via", "sendAt", "req", "text"], "asks")
        a.setdefault("by", "―")
        if a["side"] not in ("in", "out"):
            fail(f"asks.side は in か out: {a['id']}")
        if a["id"] in aids:
            fail(f"asks の id が重複: {a['id']}")
        aids.add(a["id"])
        n = a["text"].count("【")
        if n:
            warns.append(f"{a['id']}（{a['who']}）に【】が{n}か所。本人が埋める箇所として最終メッセージで伝える")

    for col in d["improve"]:
        need(col, ["cls", "h", "items"], "improve")
        if col["cls"] not in IMPROVE_CLS:
            fail(f"improve.cls は {sorted(IMPROVE_CLS)}: {col['cls']}")
        col.setdefault("lead", "")
        for it in col["items"]:
            need(it, ["t", "need", "gain"], f"improve「{col['h']}」")
            it.setdefault("where", "―")

    for f in d["focus"]:
        need(f, ["no", "t", "s", "w", "r"], "focus")
        if f["s"][0] not in FOCUS_COLORS:
            fail(f"focus.s[0] は green か amber: {f['t']}")

    nd = len(d["days"])
    for e in d["events"]:
        need(e, ["time", "title", "status"], "events")
        if not (0 <= int(e["day"]) < nd):
            fail(f"events.day が範囲外: {e}")
        if e["status"] not in STATUSES:
            fail(f"events.status は {sorted(STATUSES)}: {e}")
    for n in d["notes"]:
        need(n, ["t", "body"], "notes")
    return warns


def main():
    args = [a for a in sys.argv[1:] if a != "--open"]
    if not args:
        print(__doc__)
        sys.exit(2)
    src = Path(args[0]).resolve()
    out = Path(args[1]).resolve() if len(args) > 1 else src.with_name("準備ボード.html")
    d = json.loads(src.read_text(encoding="utf-8"))
    warns = validate(d)
    # 「パスをコピー」で使う基準のフォルダ。省略時は board-data.json のあるフォルダ
    d.setdefault("root", src.parent.as_posix() + "/")
    d["meta"].setdefault("owner", "あなた")

    tpl = TEMPLATE.read_text(encoding="utf-8")
    payload = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    page = tpl.replace("__TITLE__", html.escape(d["meta"]["title"]), 1).replace("__DATA__", payload, 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    n_act = sum(len(g["items"]) for g in d["actions"])
    n_imp = sum(len(c["items"]) for c in d["improve"])
    print(f"wrote {out}")
    print(f"{d['meta']['owner']}が動く {n_act} / AIが作った {len(d['made'])} / 準備済み {len(d['ready'])} / "
          f"依頼 {len(d['asks'])}（社内 {sum(a['side'] == 'in' for a in d['asks'])}・社外 {sum(a['side'] == 'out' for a in d['asks'])}） / "
          f"提案 {n_imp} / 予定 {len(d['events'])}")
    for w in warns:
        print("WARN:", w)
    if "--open" in sys.argv[1:]:
        webbrowser.open(out.as_uri())


if __name__ == "__main__":
    main()
