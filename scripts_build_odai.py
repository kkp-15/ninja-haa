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
# 公開日と更新日。更新日は中身（お題・本文）を変えた日に手で進める。再生成しただけでは進めない
PUBLISHED, UPDATED = '2026-09-05', '2026-09-19'

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
 ('市販のカードゲーム『はぁって言うゲーム』のお題と同じですか？',
  '違います。当サイトは非公式で、市販品のお題は一切含んでいません。すべて独自に作成したものです。'),
 ('シチュエーションは何通りありますか？',
  f'{N_WORD}のお題に、それぞれ8通りのシチュエーションを用意しています（全{N_ACT}通り）。人数が8人未満のときは上から必要な数だけ使います。'),
 ('自分でお題を作るコツは？',
  '同じ一言でも「誰に・どんな場面で」言うかを変えると成立します。分かりやすい気持ち（怒り・喜び）と、紛らわしい気持ち（照れ隠し・ごまかし）を混ぜると当てにくくなり盛り上がります。'),
]
faq_ld = json.dumps({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[
  {'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}, ensure_ascii=False)
# 学級レク・授業で使うとき（カテゴリが無くなったらビルドを止める）
for need in ('gakkou', 'kodomo'):
    if need not in data:
        raise SystemExit(f'[NG] 学級レク節からリンクしているカテゴリ {need} が data.js にありません')
page_ld = json.dumps({'@context':'https://schema.org','@type':'Article',
  'headline': f'声と表情で演じるお題一覧【全{N_WORD}お題・{N_ACT}通り】',
  'datePublished': PUBLISHED, 'dateModified': UPDATED, 'inLanguage':'ja',
  'mainEntityOfPage': f'{SITE}/odai/',
  'image': f'{SITE}/ogp.png',
  'author':{'@type':'Organization','name':'web忍者の砦','url':'https://kkpwebninja.com/'},
  'publisher':{'@type':'Organization','name':'web忍者の砦','url':'https://kkpwebninja.com/'}}, ensure_ascii=False)
faq_html = ''.join(f'<dt>{esc(q)}</dt><dd>{esc(a)}</dd>' for q,a in FAQ)

TITLE = f'声と表情で演じるお題一覧【全{N_WORD}お題・{N_ACT}通り】'
DESC  = (f'はぁって言うゲームのように、同じ一言を演じ分けて当て合う遊びのお題一覧。「はぁ」「えっ」など{N_WORD}のお題に8通りずつ、'
         f'全{N_ACT}通り。すべてオリジナル（非公式・市販品のお題は含みません）。学級レクや授業での進め方も。')

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
<script type="application/ld+json">{page_ld}</script>
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
/* 読み物ページ：地は白、本文16px・#333・行間1.8。クリームは見出し帯とボタンまわりだけ */
:root{{--orange:#ff8a3d;--orange-d:#e07b39;--cream:#fff8f0;
  --ink:#333;--muted:#6b5a48;--line:#e6dccb}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--ink);
  font-family:"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN",system-ui,sans-serif;
  font-size:16px;line-height:1.8;-webkit-text-size-adjust:100%}}
.wrap{{max-width:760px;margin:0 auto;padding:18px 16px 60px}}
h1{{font-size:1.4rem;line-height:1.5;margin:.2rem 0 .4rem}}
h1 .c{{display:block;font-size:1rem;color:var(--muted);font-weight:700}}
.upd{{font-size:.85rem;color:var(--muted);margin:0 0 .8rem}}
.lead{{margin:0 0 1rem}}
.cta{{display:block;text-align:center;background:var(--orange);color:#fff;font-weight:800;font-size:.95rem;
  padding:.75rem .5rem;border-radius:8px;text-decoration:none;margin:0 0 1.2rem}}
.toc{{margin:0 0 1.6rem;padding:.5rem 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.toc a{{display:inline-block;padding:.35rem 0;margin-right:1.1rem;white-space:nowrap}}
.toc a span{{color:var(--muted);font-size:.85rem;margin-left:.2rem}}
h2{{font-size:20px;line-height:1.5;margin:0 0 .5rem;padding-left:.6rem;border-left:4px solid var(--orange)}}
.cat,.sec{{margin:0 0 2.4rem}}
.cat h2 .n{{font-size:.85rem;color:var(--muted);font-weight:400;margin-left:.6rem}}
.cd{{margin:0 0 .8rem}}
.sec ol{{margin:0 0 .8rem;padding-left:1.4rem}}
.sec li{{margin:0 0 .3rem}}
.w{{margin:0 0 1.2rem}}
.w h3{{margin:0 0 .3rem;font-size:1.1rem;line-height:1.5;background:var(--cream);padding:.25rem .6rem}}
.w ol{{margin:0;padding-left:2rem}}
.play{{margin:.4rem 0 0}}
.play .btn{{display:inline-block;font-size:.95rem;color:#b3541a;text-decoration:none;font-weight:700;
  background:var(--cream);border:1px solid var(--orange);border-radius:6px;padding:.3rem .9rem}}
details.block{{border-top:1px solid var(--line);padding:.2rem 0;margin:0}}
details.block:last-of-type{{border-bottom:1px solid var(--line)}}
details.block summary{{cursor:pointer;padding:.6rem 0}}
details.block h2{{display:inline;border:0;padding:0;margin:0}}
details.block p{{margin:0 0 .8rem}}
dt{{font-weight:700;margin-top:1rem}}
dd{{margin:.2rem 0 0}}
dl{{margin:0 0 1rem}}
a{{color:#1565c0}}
.ad-slot{{margin:1.6rem 0 0;padding:12px 0;text-align:center;
  border-top:1px dashed var(--line);border-bottom:1px dashed var(--line)}}
.ad-label{{font-size:10.5px;letter-spacing:.14em;color:var(--muted);margin-bottom:6px}}
.ad-slot ins.adsbygoogle{{display:block;width:320px;height:100px;margin:0 auto}}
@media(min-width:760px){{h2{{font-size:22px}}.ad-slot ins.adsbygoogle{{width:728px;height:90px}}}}
</style>
</head>
<body>
<div class="wrap">

<h1>声と表情で演じるお題一覧<span class="c">【全{N_WORD}お題・{N_ACT}通り】</span></h1>
<p class="upd">更新日 <time datetime="{UPDATED}">{UPDATED}</time></p>
<p class="lead">『はぁって言うゲーム』のように、同じ一言をそれぞれ違う気持ちで演じ分けて当て合う遊びのお題です。
1つのお題につき8通りのシチュエーションを用意しています。
お題はすべて当サイトのオリジナルで、市販のカードのお題は含みません（非公式のページです）。</p>

<a class="cta" href="{SITE}/">このお題でいますぐ遊ぶ（無料・登録不要）</a>

<nav class="toc" aria-label="カテゴリ目次">{toc}</nav>

<section class="sec" id="class">
<h2>学級レク・授業で使うとき</h2>
<ol>
<li>3〜8人の班に分かれ、班ごとにスマホかタブレットを1台用意して<a href="{SITE}/">ツール</a>を開きます。配役の配布から投票・得点まで端末がやるので、カードやチップの準備は要りません。</li>
<li>カテゴリは<a href="#gakkou">「学校」（{len(data['gakkou'])}お題）</a>か<a href="#kodomo">「こども」（{len(data['kodomo'])}お題）</a>から選びます。</li>
<li>演じるのは声と表情だけで、身振りは使いません。全員が演じ終わったら端末を回して投票します。</li>
<li>端末が教室に1台だけのときは、この一覧をスクリーンに映し、演じる人にだけ番号を伝えて、見ている全員が何番かを当てる形でも進められます。</li>
</ol>
<p>お題は紙やカードに書き写して使ってかまいません。</p>
</section>

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
