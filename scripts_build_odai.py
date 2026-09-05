#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""data.js から odai/index.html を生成する。

正本は data.js。この一覧ページは生成物なので直接編集しない。
お題を足したら data.js を直して build.py と このスクリプトの両方を実行する。
"""
import os, re, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = 'https://haa.kkpwebninja.com'
GA, PUB = 'G-2LM85GJN0L', 'ca-pub-1298304917726270'

src = open(os.path.join(ROOT, 'data.js'), encoding='utf-8').read()

# data.js を JSON に寄せて読む（構造が単純なので正規表現で十分）
cats = re.findall(r"(\w+): \{\s*label: '([^']+)',\s*desc: '([^']+)',\s*list: \[(.*?)\n    \]\s*\}", src, re.S)
data, order = {}, []
for cid, label, desc, body in cats:
    items = []
    for m in re.finditer(r"\{ word: '([^']+)', acts: \[([^\]]+)\] \}", body):
        acts = [a.strip().strip("'") for a in re.findall(r"'[^']*'", m.group(2))]
        items.append((m.group(1), acts))
    if items:
        order.append((cid, label, desc))
        data[cid] = items

N_WORD = sum(len(v) for v in data.values())
N_ACT  = sum(len(a) for v in data.values() for _, a in v)

def esc(t): return html.escape(t, quote=True)

toc = ''.join(f'<a href="#{cid}">{esc(label)}<span>{len(data[cid])}</span></a>' for cid, label, _ in order)

blocks = []
for cid, label, desc in order:
    rows = ''.join(
        f'<div class="w"><h3>「{esc(w)}」</h3><ol>' +
        ''.join(f'<li>{esc(a)}</li>' for a in acts) + '</ol></div>'
        for w, acts in data[cid])
    blocks.append(
        f'<section class="cat" id="{cid}"><h2>{esc(label)}<span class="n">{len(data[cid])}お題</span></h2>'
        f'<p class="cd">{esc(desc)}</p>{rows}'
        f'<p class="play"><a class="btn" href="{SITE}/">このお題で遊ぶ</a></p></section>')

FAQ = [
 ('お題は自由に使えますか？',
  'この一覧のお題はすべて当サイトのオリジナルです。紙に書き写して遊んでいただいてかまいません。ただし、そのまま転載して配布することはご遠慮ください。'),
 ('市販のカードゲームのお題と同じですか？',
  '違います。市販品のお題は一切含んでいません。すべて独自に作成したものです。'),
 ('シチュエーションは何通りありますか？',
  f'{N_WORD}のお題に、それぞれ8通りのシチュエーションを用意しています（全{N_ACT}通り）。人数が8人未満のときは上から必要な数だけ使います。'),
 ('自分でお題を作るコツは？',
  '同じ一言でも「誰に・どんな場面で」言うかを変えると成立します。分かりやすい気持ち（怒り・喜び）と、紛らわしい気持ち（照れ隠し・ごまかし）を混ぜると当てにくくなり盛り上がります。'),
]
faq_ld = json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[
  {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}, ensure_ascii=False)
faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q,a in FAQ)

TITLE = f'声と表情で演じるお題一覧【全{N_WORD}お題・{N_ACT}通り】'
DESC  = (f'「はぁ」「えっ」など{N_WORD}のお題と、それぞれ8通りのシチュエーションを一覧にしました。'
         f'全{N_ACT}通り。すべてオリジナルで、そのままスマホ1台で配れます。')

out = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<link rel="canonical" href="{SITE}/odai/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:type" content="article">
<meta property="og:url" content="{SITE}/odai/">
<meta property="og:site_name" content="声と表情で当てるゲーム">
<meta property="og:image" content="{SITE}/ogp.png?d=20260905">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<script type="application/ld+json">{faq_ld}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA}');
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={PUB}" crossorigin="anonymous"></script>
<style>
:root{{--orange:#ff8a3d;--orange-d:#e07b39;--cream:#fff8f0;--paper:#fffdf9;
  --ink:#3b2c22;--muted:#8a7560;--line:#f0e2cc}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--cream);color:var(--ink);
  font-family:"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN",system-ui,sans-serif;
  font-size:16px;line-height:1.8;-webkit-text-size-adjust:100%}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 14px 60px}}
h1{{font-size:1.24rem;line-height:1.5;margin:.2rem 0 .5rem;text-wrap:balance}}
h1 .c{{color:var(--orange-d)}}
.lead{{font-size:.9rem;color:var(--muted);margin:0 0 1rem}}
.cta{{display:block;text-align:center;background:var(--orange);color:#fff;font-weight:800;
  padding:.75rem 1rem;border-radius:12px;text-decoration:none;margin:0 0 1.2rem;
  box-shadow:0 4px 12px rgba(224,123,57,.28)}}
.toc{{display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 1.4rem}}
.toc a{{display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .7rem;background:var(--paper);
  border:1px solid var(--line);border-radius:999px;color:var(--ink);text-decoration:none;
  font-size:.82rem;white-space:nowrap}}
.toc a span{{color:var(--muted);font-size:.74rem}}
.cat{{margin:0 0 1.8rem}}
.cat h2{{font-size:1.04rem;margin:0 0 .2rem;display:flex;align-items:baseline;gap:.5rem}}
.cat h2 .n{{font-size:.76rem;color:var(--muted);font-weight:400}}
.cd{{font-size:.82rem;color:var(--muted);margin:0 0 .7rem}}
.w{{background:var(--paper);border:1px solid var(--line);border-radius:12px;
  padding:.7rem .9rem .8rem;margin:0 0 .6rem}}
.w h3{{margin:0 0 .35rem;font-size:1.05rem;color:var(--orange-d)}}
.w ol{{margin:0;padding-left:1.3rem;font-size:.88rem;line-height:1.9}}
.w li{{color:#5c4b3c}}
.play{{margin:.4rem 0 0;text-align:right}}
.play .btn{{display:inline-block;font-size:.8rem;color:var(--orange-d);text-decoration:none;
  border:1px solid var(--orange);border-radius:999px;padding:.25rem .8rem}}
details.block{{background:var(--paper);border:1px solid var(--line);border-radius:12px;
  padding:.1rem .9rem;margin:0 0 .7rem}}
details.block summary{{cursor:pointer;font-weight:700;padding:.6rem 0;font-size:.95rem}}
details.block h2{{display:inline;font-size:.95rem;margin:0}}
dt{{font-weight:700;margin-top:.7rem;font-size:.9rem}}
dd{{margin:.2rem 0 0;font-size:.86rem;color:#5c4b3c}}
a{{color:#1565c0}}
.ad-slot{{margin:1.6rem 0 0;padding:12px 0;text-align:center;
  border-top:1px dashed var(--line);border-bottom:1px dashed var(--line)}}
.ad-label{{font-size:10.5px;letter-spacing:.14em;color:var(--muted);margin-bottom:6px}}
.ad-slot ins.adsbygoogle{{display:block;width:320px;height:100px;margin:0 auto}}
@media(min-width:760px){{.ad-slot ins.adsbygoogle{{width:728px;height:90px}}}}
</style>
</head>
<body>
<div class="wrap">

<h1>声と表情で演じるお題一覧<span class="c">【全{N_WORD}お題・{N_ACT}通り】</span></h1>
<p class="lead">同じ一言を、それぞれ違う気持ちで演じ分けるゲームのお題です。
1つのお題につき8通りのシチュエーションを用意しています。すべてオリジナルです。</p>

<a class="cta" href="{SITE}/">このお題でいますぐ遊ぶ（無料・登録不要）</a>

<nav class="toc" aria-label="カテゴリ目次">{toc}</nav>

{''.join(blocks)}

<details class="block">
  <summary><h2>お題選びのコツ</h2></summary>
  <div>
    <p><b>はじめての人がいる</b>なら「定番」から。日常でよく聞く言い方ばかりなので、演じ方に迷いません。</p>
    <p><b>職場の懇親会</b>では「仕事」が安全です。誰も傷つけずに、共通の場面で笑えます。</p>
    <p><b>子どもと</b>遊ぶなら「学校」「あいさつ」。短い言葉なので低学年でも演じられます。</p>
    <p><b>慣れてきたら</b>「表情だけ」。声を使わないので難易度が上がり、当てにくくなります。</p>
  </div>
</details>

<details class="block">
  <summary><h2>よくある質問</h2></summary>
  <div><dl>{faq_html}</dl></div>
</details>

<div class="ad-slot">
  <div class="ad-label">広告</div>
  <ins class="adsbygoogle" style="display:block"
       data-ad-client="{PUB}" data-ad-format="horizontal" data-full-width-responsive="false"></ins>
</div>

<!-- WEBNINJA_RELATED_APPS -->
<div style="max-width:680px;margin:2rem auto 0;padding:1rem 1.2rem;background:#fffcf7;border:1px solid #f0e6d2;border-radius:12px;font-family:inherit;">
  <div style="font-weight:800;color:#8b6b3d;font-size:0.9rem;margin-bottom:0.3rem;">あわせて使えるアプリ</div>
  <a href="https://wordwolf.kkpwebninja.com/" style="display:block;padding:0.4rem 0;color:#1565c0;text-decoration:none;font-size:0.92rem;line-height:1.6;border-top:1px solid #f3ecd9;">ワードウルフ — 少数派をさがす定番パーティーゲーム</a>
  <a href="https://ito.kkpwebninja.com/" style="display:block;padding:0.4rem 0;color:#1565c0;text-decoration:none;font-size:0.92rem;line-height:1.6;border-top:1px solid #f3ecd9;">ito お題と数字の配布 — スマホ1台で遊べる協力ゲーム</a>
  <a href="https://gesture.kkpwebninja.com/" style="display:block;padding:0.4rem 0;color:#1565c0;text-decoration:none;font-size:0.92rem;line-height:1.6;border-top:1px solid #f3ecd9;">ジェスチャーおでこ当て — 言葉を使わずお題を伝える</a>
  <a href="https://bingomachine.kkpwebninja.com/" style="display:block;padding:0.4rem 0;color:#1565c0;text-decoration:none;font-size:0.92rem;line-height:1.6;border-top:1px solid #f3ecd9;">ビンゴマシン — 1〜75を重複なしで抽選</a>
</div>

<!-- WEBNINJA_UNIFIED_FOOTER -->
<footer style="text-align:center;padding:2rem 1rem 2.5rem;font-size:0.78rem;color:#94a3b8;line-height:2;border-top:1px solid #f0e6d2;margin-top:2.5rem;background:#fffcf7;">
  <div style="font-weight:800;color:#8b6b3d;font-size:0.85rem;margin-bottom:0.4rem;">web忍者の砦</div>
  <div>
    <a href="https://kkpwebninja.com/" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">本丸トップ</a>·
    <a href="https://privacypolicy.kkpwebninja.com/" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">プライバシーポリシー</a>·
    <a href="https://kkpwebninja.com/otoiawase" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">お問い合わせ</a>·
    <a href="https://x.com/kkp_webninja" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">@kkp_webninja</a>
  </div>
  <div style="margin-top:0.5rem;color:#bfa97a;">© 2025-2026 web忍者の砦</div>
</footer>
</div>
<script>
(function(){{ try {{ (adsbygoogle = window.adsbygoogle || []).push({{}}); }} catch(e) {{}} }})();
</script>
</body>
</html>
'''
os.makedirs(os.path.join(ROOT,'odai'), exist_ok=True)
open(os.path.join(ROOT,'odai','index.html'),'w',encoding='utf-8').write(out)
print(f'[ok] odai/index.html  {N_WORD}お題 / {N_ACT}通り / {len(order)}カテゴリ  {len(out)} bytes')
