# Claude Codeへ：このスキルの入れ方

ユーザーが「このZIPのスキルを入れて」「セットアップをお願いします」と言ったら、この手順で進めてください。

1. **ZIPを展開する。** ユーザーのZIPファイルを一時フォルダに展開する（Windowsは PowerShell の `Expand-Archive`、macOS・Linuxは `unzip`）。展開した中から、`SKILL.md` を含む `week-prep` フォルダを探す（GitHubの「Download ZIP」だと、1段深い `week-prep-skill-main/week-prep/` にある）
2. **置き場所を決める。** ユーザーに次のどちらかを聞く。答えがなければ1を使う
   1. どのフォルダで開いても使う：`~/.claude/skills/week-prep/`
   2. 今のプロジェクトだけで使う：`<今のプロジェクト>/.claude/skills/week-prep/`
3. **コピーする。** `week-prep` フォルダをそこにコピーする。同じ場所にすでに `week-prep` がある場合は、上書きする前にユーザーに確認し、既存の `my-profile.md` は残す（新しいフォルダへ移す）
4. **確かめる。** コピー先に `SKILL.md`・`references/`・`assets/`・`scripts/` があることを確認する
5. **セットアップを始める。** コピー先の `SKILL.md` を読み、`my-profile.md` がなければ `references/setup.md` のセットアップを始める
6. **伝える。** 次回からは「来週の準備をして」または `/week-prep` で使えること（新しいセッションで認識される）を、ユーザーに一言伝える

注意：

- このスキルは、メール・チャットの送信や予定の変更をしない前提で作られている。セットアップの途中でも、書き込み系の操作は試さない
- 展開に使った一時フォルダは、最後に片付けてよいかユーザーに聞く
