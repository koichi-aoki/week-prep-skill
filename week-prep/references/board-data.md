# ボードのデータ形式（board-data.json）

`scripts/build_board.py` が読む。全部そろった見本は [../assets/sample-board-data.json](../assets/sample-board-data.json)（架空の会社・人物の例）。
必須の項目がないとERRORで止まる。依頼文に【】が残っているとWARNで知らせる（最終メッセージで伝える）。

```json
{
  "meta": {
    "title": "10/5週 準備ボード",
    "owner": "山田さん",
    "focusTitle": "今週の重点アクションは達成できるか",
    "eyebrow": "Week of 10/5 – 10/9",
    "lead": "予定◯件・チャット◯件・メール◯件…を突き合わせ、来週の準備を分けました。◯/◯（金）夜時点。",
    "countdown": [{"v": "10/9", "l": "◯◯の締切", "hot": true}],
    "footer": "元データ：…。取れなかった範囲：…",
    "folder": "week-prep-output/20261005/"
  },
  "actions": [
    {"g": "今夜〜月曜の朝まで", "items": [
      {"id": "a1", "when": "月 8:00〜8:20", "dur": "20分", "t": "やること（1行）",
       "how": "どうやるか・何を決めるか", "use": "使うもの", "done": "終わりの目安"}
    ]}
  ],
  "made":  [{"t": "作ったもの", "when": "使う場面", "what": "中身", "state": "そのまま使える／◯◯を埋める", "p": "03_経営定例の資料.md"}],
  "ready": [["もの", "使う日", "誰が・いつ", "場所", "当日の一言"]],
  "asks":  [{"side": "in", "id": "D1", "who": "宛先", "via": "Teams 1:1", "sendAt": "月曜朝", "by": "期限", "req": "お願いすること（1行）", "text": "全文"}],
  "improve": [
    {"cls": "i-now",  "h": "OKをもらえれば、今すぐやれること", "lead": "…", "items": [{"t": "…", "need": "必要なもの", "gain": "できること", "where": "効く場面・相談先"}]},
    {"cls": "i-info", "h": "情報をもらえれば、精度が上がること", "lead": "…", "items": []},
    {"cls": "i-perm", "h": "権限・設定があれば、ここまで任せられること", "lead": "…", "items": []}
  ],
  "focus":  [{"no": "①", "t": "重点アクション", "s": ["amber", "見込みの一言"], "w": "来週の山場", "r": "詰まりどころ"}],
  "days":   [{"date": "10/5", "dow": "月", "label": "", "hot": false}],
  "events": [{"day": 0, "time": "9:00", "title": "予定の名前（短く）", "status": "you"}],
  "notes":  [{"t": "気づいた点の見出し", "body": "中身"}]
}
```

## 決まり

- `meta.title` は「M/D週 準備ボード」程度の名前（20字以内）。説明は `lead` に書く
- `meta.owner` はボードでの本人の呼び方（`my-profile.md`）。省略すると「あなた」
- `meta.focusTitle` は重点アクションの欄の見出し。省略すると「今週の重点アクションは達成できるか」
- `made[].p` は、出力フォルダからの相対パス（「パスをコピー」で出力フォルダの絶対パスと合わせてコピーされる）
- `actions[].items[].id` と `asks[].id` は重複させない。依頼の `id` は文面集の番号（D1〜）と合わせる
- `asks[].side` は `in`（社内）か `out`（社外）
- `events[].day` は `days` の並び（0始まり）。`status` は `you` `made` `ready` `ask` のどれか
- `days[].hot` を `true` にした日は見出しが強調色になる（締切日など1日だけ）
- `focus[].s[0]` は `green` か `amber`
- 依頼文 `text` の改行は、JSONでは `\n`。ボードでは全文を表示し、コピーボタンが付く
- 「本人が動く」のチェック状態は、見ている人のブラウザにだけ残る
