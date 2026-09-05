#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.js を index.html に埋め込む。

お題の正本は data.js。index.html は生成物として扱う。
（単一HTML原則を守りつつ、お題の編集場所を1か所に固定するため。
  itoで「生成物を直接編集して sync に戻される」事故を起こしたので最初から向きを決める）

使い方: python3 build.py  → index.html の該当ブロックを差し替える
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

open(p, 'w', encoding='utf-8').write(html)
print(f'[ok] index.html にお題を埋め込み  {n_word}種 / {n_act}通り  {len(html)} bytes')
