#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.js を index.html に埋め込む。

お題の正本は data.js。index.html は生成物として扱う。
（単一HTML原則を守りつつ、お題の編集場所を1か所に固定するため。
  itoで「生成物を直接編集して sync に戻される」事故を起こしたので最初から向きを決める）

使い方: python3 build.py  → index.html の該当ブロックを差し替える

FAQ（表示と FAQPage 構造化データ）もここが正本。index.html の FAQ:BEGIN〜END は生成物。
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
data = open(os.path.join(ROOT, 'data.js'), encoding='utf-8').read().strip()
p = os.path.join(ROOT, 'index.html')
html = open(p, encoding='utf-8').read()

BEGIN = '<!-- DATA:BEGIN 自動生成。編集は data.js を直して build.py を実行 -->'
END   = '<!-- DATA:END -->'
block = BEGIN + '\n<script>\n' + data + '\n</script>\n' + END

if BEGIN in html:
    html = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END), block, html, flags=re.S)
else:
    # 初回：外部読み込みを置き換える
    old = '<script src="/data.js"></script>'
    if old not in html:
        sys.exit('[NG] 差し込み位置が見つかりません')
    html = html.replace(old, block)

# 件数を実数で反映（ハードコードで食い違う事故を防ぐ）
words = re.findall(r"word: '([^']+)'", data)
n_word = len(words)
n_act = sum(len(re.findall(r"'[^']*'", m)) for m in re.findall(r'acts: \[([^\]]+)\]', data))
html = re.sub(r'お題\d+種', f'お題{n_word}種', html)
html = re.sub(r'シチュエーション\d+通り', f'シチュエーション{n_act}通り', html)
html = re.sub(r'\d+種類のお題に', f'{n_word}種類のお題に', html)
html = re.sub(r'全\d+通り', f'全{n_act}通り', html)
# お題一覧へのリンク文言（「全29お題・232通り」）も実数に合わせる
html = re.sub(r'(data-word-count>)\d+(<)', rf'\g<1>{n_word}\g<2>', html)
html = re.sub(r'お題・\d+通り', f'お題・{n_act}通り', html)


# ---- FAQ：表示するHTMLと FAQPage 構造化データを同じ正本から作る ----------------
# （別々に書くと食い違うので、ここ1か所だけを直す。例題は data.js から実物を引く）
import json
from html import escape

def acts_of(word, n=3):
    m = re.search(r"\{ word: '" + re.escape(word) + r"', acts: \[([^\]]+)\] \}", data)
    if not m:
        sys.exit(f'[NG] FAQの例に使うお題「{word}」が data.js にありません')
    return [a.strip("'") for a in re.findall(r"'[^']*'", m.group(1))][:n]

ex1, ex2 = acts_of('おはよう'), acts_of('やばい')
FAQ = [
 ('『はぁって言うゲーム』のカードがなくても遊べますか？',
  '遊べます。スマホ1台を順番に回すだけで、各自の配役をこっそり確認できます。投票と得点計算も自動なので、チップや紙は要りません。お題は当サイトのオリジナルで、市販のカードのお題は入っていません。'),
 ('無料ですか？アプリのインストールは要りますか？',
  '無料です。ブラウザで開くだけで遊べるので、アプリのインストールも会員登録も要りません。ページ内に広告を表示しています。'),
 ('何人から遊べますか？',
  '3人から8人まで遊べます。4〜6人がいちばん当てにくく盛り上がります。人数に合わせて配役の数も自動で調整されます。'),
 ('2人でも遊べますか？',
  'このツールは3人から8人用で、2人では始められません。2人のときは、お題一覧を見ながら1人が演じ、もう1人が当てる形なら遊べます。'),
 ('どうやって遊ぶの？',
  '全員が同じ一言（例：「はぁ」）を、それぞれ違うシチュエーションで演じます。声と表情だけを使い、身振りは使いません。演技のあと、誰がどのシチュエーションだったかを全員で当てます。'),
 ('どんなお題（例題）がありますか？',
  f'たとえば「おはよう」というお題なら、{ex1[0]}／{ex1[1]}／{ex1[2]} など。「やばい」なら、{ex2[0]}／{ex2[1]}／{ex2[2]} など。1つのお題に8通りあり、全部をお題一覧ページに載せています。'),
 ('お題は何種類ありますか？',
  f'{n_word}種類のお題に、それぞれ8通りのシチュエーションを用意しています（全{n_act}通り）。すべてこのサイトのオリジナルです。'),
 ('市販のカード版との違いは？',
  '市販の『はぁって言うゲーム』（幻冬舎）はカードを配って遊びます。このツールは、配役の配布・投票・集計・得点計算をスマホが引き受けるところが違います。お題は別物で、市販品のお題は含みません。非公式のツールなので、カードで遊びたい方や公式のお題で遊びたい方は市販品をお求めください。'),
]
faq_html = '\n'.join(f'    <dt>{escape(q)}</dt><dd>{escape(a)}</dd>' for q, a in FAQ)
faq_ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
    {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]},
    ensure_ascii=False)

def put(html, begin, end, body):
    if begin not in html or end not in html:
        sys.exit(f'[NG] 差し込み位置が見つかりません: {begin}')
    return re.sub(re.escape(begin) + r'.*?' + re.escape(end), lambda m: begin + '\n' + body + '\n' + end, html, flags=re.S)

html = put(html, '<!-- FAQ:BEGIN 自動生成。編集は build.py の FAQ を直して build.py を実行 -->', '<!-- FAQ:END -->', faq_html)
html = put(html, '<!-- FAQLD:BEGIN 自動生成。編集は build.py の FAQ を直して build.py を実行 -->', '<!-- FAQLD:END -->',
           '<script type="application/ld+json">' + faq_ld + '</script>')

open(p, 'w', encoding='utf-8').write(html)
print(f'[ok] index.html にお題を埋め込み  {n_word}種 / {n_act}通り  FAQ {len(FAQ)}問  {len(html)} bytes')
