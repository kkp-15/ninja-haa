#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日本語版 index.html を土台に en/index.html を組み立てる。

英語版は翻訳ページではない。お題（data.en.js）は英語の間投詞で作り直してある。
UIと本文だけを日本語版から引き継ぐので、日本語版の画面を直せば英語版も追従する。

狙いはESL/EFLの授業。「同じ一言を違う感情で言って当てさせる」活動は英語圏の
教室で定番なのに、配役配布と投票・集計まで面倒を見るツールが見当たらない。

使い方: python3 build_en.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(ROOT, 'index.html')
OUT  = os.path.join(ROOT, 'en', 'index.html')
DATA = os.path.join(ROOT, 'data.en.js')

html = io.open(SRC, encoding='utf-8').read()
data = io.open(DATA, encoding='utf-8').read().strip()

# ---- 1. お題データを英語版に差し替え -------------------------------------
BEGIN = '<!-- DATA:BEGIN 自動生成。編集は data.js を直して build.py を実行 -->'
END   = '<!-- DATA:END -->'
block = ('<!-- DATA:BEGIN generated. edit data.en.js and run build_en.py -->\n'
         '<script>\n' + data + '\n</script>\n<!-- DATA:END -->')
if BEGIN not in html:
    sys.exit('[NG] お題ブロックが見つかりません。先に build.py を実行してください')
html = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END), lambda m: block, html, flags=re.S)

n_word = len(re.findall(r"word: '", data))
n_act  = sum(len(re.findall(r"'[^']*'", m)) for m in re.findall(r'acts: \[([^\]]+)\]', data))

# ---- 2. head をまるごと英語版に ------------------------------------------
HEAD = '''<title>Emotion Charades Online — Say One Line With a Secret Feeling (Free, One Phone)</title>
<meta name="description" content="Emotion charades for teens, adults and ESL classes. Everyone says the same line, each with a secret emotion — pass one phone around, act it out, then guess the emotion. Roles, voting and scoring are handled for you. %d prompts, %d ways to say them. Free, no sign-up, no app.">
<link rel="canonical" href="https://haa.kkpwebninja.com/en/">
<link rel="alternate" hreflang="ja" href="https://haa.kkpwebninja.com/">
<link rel="alternate" hreflang="en" href="https://haa.kkpwebninja.com/en/">
<link rel="alternate" hreflang="x-default" href="https://haa.kkpwebninja.com/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#e8843a">

<meta property="og:title" content="Emotion Charades Online — one phone, one line, a secret feeling">
<meta property="og:description" content="Say the same word eight different ways and see who can tell them apart. Roles, voting and scoring on a single phone.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://haa.kkpwebninja.com/en/">
<meta property="og:site_name" content="Emotion Charades">
<meta property="og:image" content="https://haa.kkpwebninja.com/ogp.png?d=20260906">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://haa.kkpwebninja.com/ogp.png?d=20260906">

<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Emotion Charades Online","url":"https://haa.kkpwebninja.com/en/","applicationCategory":"GameApplication","operatingSystem":"Web","inLanguage":"en","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"author":{"@type":"Organization","name":"web忍者の砦"},"publisher":{"@type":"Organization","name":"web忍者の砦","url":"https://kkpwebninja.com/"}}
</script>''' % (n_word, n_act)

head_start = html.index('<title>')
head_end   = html.index('</script>', html.index('application/ld+json')) + len('</script>')
html = html[:head_start] + HEAD + html[head_end:]
html = html.replace('<html lang="ja">', '<html lang="en">')

# ---- 3. 日本向けの物販・相互リンクを英語圏向けに --------------------------
# 日本のカードゲームのアフィリエイトは海外の読者には使えないので、まるごと外す。
html = re.sub(r'\s*<div class="shop">.*?</div>\s*(?=</div>)', '\n  ', html, flags=re.S)

RELATED = '''<!-- WEBNINJA_RELATED_APPS -->
<div style="max-width:680px;margin:2rem auto 0;padding:1rem 1.2rem;background:#fffcf7;border:1px solid #f0e6d2;border-radius:12px;font-family:inherit;">
  <div style="font-weight:800;color:#8b6b3d;font-size:0.9rem;margin-bottom:0.3rem;">More one-phone party games</div>
  <!-- 英語版が実在するものだけ並べる。/en/ が日本語ページを返すサイトを入れない -->
  <a href="https://ito.kkpwebninja.com/en/" style="display:block;padding:0.4rem 0;color:#1565c0;text-decoration:none;font-size:0.92rem;line-height:1.6;border-top:1px solid #f3ecd9;">ito — line up your secret numbers without saying them</a>
</div>'''
html = re.sub(r'<!-- WEBNINJA_RELATED_APPS -->.*?\n</div>', RELATED, html, count=1, flags=re.S)

FOOTER = '''<!-- WEBNINJA_UNIFIED_FOOTER -->
<footer style="text-align:center;padding:2rem 1rem 2.5rem;font-size:0.78rem;color:#94a3b8;line-height:2;border-top:1px solid #f0e6d2;margin-top:2.5rem;background:#fffcf7;">
  <div style="font-weight:800;color:#8b6b3d;font-size:0.85rem;margin-bottom:0.4rem;">web忍者の砦</div>
  <div>
    <a href="https://kkpwebninja.com/" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">All our free web apps</a>·
    <a href="https://privacypolicy.kkpwebninja.com/en/" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">Privacy policy</a>·
    <a href="https://x.com/kkp_webninja" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">@kkp_webninja</a>
  </div>
  <div style="margin-top:0.5rem;color:#bfa97a;">© 2025-2026 web忍者の砦</div>
</footer>'''
html = re.sub(r'<!-- WEBNINJA_UNIFIED_FOOTER -->.*?</footer>', FOOTER, html, count=1, flags=re.S)

# ---- 4. UIと本文の文字列 --------------------------------------------------
# 長いものから当てる（短い語が先に食うと崩れる）
T = [
 # head 以外に残る大物
 ('<h1>声と表情で当てるゲーム</h1>', '<h1>Emotion Charades<span class="h1-sub">Say one line with a secret feeling</span></h1>'),
 # 本家（幻冬舎）を応援する一文は日本語版だけ（英語圏では知られていないため、導入文と同じ扱い）
 ('      <p class="hero-fan">『はぁって言うゲーム』を楽しむための非公式ツール。本家のカードは<a href="https://www.gentosha.co.jp/s/haa-game/" target="_blank" rel="noopener">こちら（幻冬舎の公式ページ）</a></p>\n', ''),
 ('<p>同じ一言を、それぞれ違う気持ちで演じて当て合う。<br>アプリ不要で配役から得点まで。非公式の無料ツール。</p>',
  '<p>Everyone says the same line with a different feeling.<br>One phone handles the roles, the voting and the score. No app, no sign-up.</p>'),
 # 遊び方
 ('遊び方（30秒で読めます）', 'How to play (30 seconds)'),
 # 日本の市販カードゲームに触れる導入は、英語版では出さない（英語圏では知られていないため）
 ('    <p>『はぁって言うゲーム』（幻冬舎のカードゲーム）と同じように、同じ一言を声と表情だけで演じ分け、誰がどの気持ちだったかを当て合う遊びです。ここではカードの代わりにスマホ1台で進めます。</p>\n', ''),
 ('1. 人数とお題を決めます。お題は「はぁ」「えっ」のような短い一言です。',
  '1. Pick the number of players and a line. The lines are short — "Huh?", "Oh.", "Sure."'),
 ('2. スマホを回して、各自が自分の<b>気持ち</b>をこっそり確認します。全員ちがう気持ちが配られます。',
  '2. Pass the phone around. Each player privately checks the <b>feeling</b> they were given. Everyone gets a different one.'),
 ('3. 順番に、その一言だけを言います。<b>身振りは使わず、声と表情だけ</b>で表現してください。',
  '3. Take turns saying that one line. <b>No gestures</b> — voice and face only.'),
 ('4. 全員の演技が終わったら、もう一度スマホを回して投票します。誰がどの気持ちだったかを当てます。',
  '4. Once everyone has performed, pass the phone again and vote on who had which feeling.'),
 ('5. 正解発表。当てた人にも、当ててもらえた人にも点が入ります。',
  '5. Reveal. You score for guessing right, and for being guessed right.'),
 ('よくある質問', 'Questions'),
 ('『はぁって言うゲーム』のような、声と表情で演じ分けて当て合う遊びを、スマホ1台でできるようにした非公式のツールです。<br>',
  'An unofficial tool that puts this acting-and-guessing game on a single phone.<br>'),
 ('幻冬舎および公式とは関係ありません。お題はすべて当サイトのオリジナルで、市販品の内容は含みません。',
  'Every prompt here is our own writing.'),
 # 画面
 ('STEP 1</span>人数を選ぶ</h2>', 'STEP 1</span>Players</h2>'),
 ('STEP 2</span>お題を選ぶ</h2>', 'STEP 2</span>Pick a line</h2>'),
 ('STEP 3</span>順番にタップして自分の役を見る</h2>', 'STEP 3</span>Tap in turn to see your role</h2>'),
 ('STEP 4</span>順番に演じる</h2>', 'STEP 4</span>Perform in turn</h2>'),
 ('STEP 5</span>投票</h2>', 'STEP 5</span>Vote</h2>'),
 ('STEP 6</span>答え合わせ</h2>', 'STEP 6</span>Reveal</h2>'),
 ('<span class="unit">人</span>', '<span class="unit">players</span>'),
 ('3〜8人で遊べます。4〜6人がいちばん当てにくいです', '3 to 8 players. 4 to 6 is the hardest to read'),
 ('お題を選ばなくても自動で決まります', 'Skip this and one will be picked for you'),
 ('↺ 別の3つを見る', '↺ Show three others'),
 # 挿し絵の alt（日本語版 2026-09-25 追加分）
 ('alt="表情豊かに一言を言う男の子と、首をかしげて聞く女の子"',
  'alt="A boy saying one line with a big expression, and a girl tilting her head as she listens"'),
 ('<button class="btn-primary" id="startGame">おまかせで始める</button>',
  '<button class="btn-primary" id="startGame">Start</button>'),
 ("'「'+S.theme.word+'」で始める' : 'お題を選んで始める'",
  '\'Start with \\u201c\'+S.theme.word+\'\\u201d\' : \'Pick a line to start\''),
 ('全員が同じ「<b id="dealWord"></b>」を言います。<br>気持ちだけが1人ずつ違います。他の人に見られないように！',
  'Everyone says the same "<b id="dealWord"></b>".<br>Only the feeling differs. Do not let anyone else see!'),
 ('全員見終わった → 演じる', 'Everyone has looked → perform'),
 ('↺ 設定に戻る', '↺ Back to setup'),
 ('身振りは使わず、<b>声と表情だけ</b>で。<br>1人ずつ「<b id="performWord"></b>」と言ってください。',
  '<b>Voice and face only</b> — no gestures.<br>Take turns saying "<b id="performWord"></b>".'),
 ('全員演じ終わった → 投票へ', 'Everyone has performed → vote'),
 ('スマホを回して、1人ずつ投票します。<br>自分以外の人が「どの気持ち」だったかを選んでください。',
  'Pass the phone and vote one at a time.<br>Choose the feeling you think each of the others had.'),
 ('もう1回遊ぶ', 'Play again'),
 ('広告', 'Advertisement'),
 ('もっと遊びたくなったら', 'If you want more'),
 ('PR・アフィリエイト広告を含みます', 'Contains affiliate links'),
 ('誰にも見せないでください', 'Keep this to yourself'),
 ('覚えた！次の人へ', 'Got it — next player'),
 ('1人減らす', 'one fewer player'),
 ('1人増やす', 'one more player'),
 ('お題のカテゴリ', 'prompt categories'),
 # JSの組み立て文字列
 ("'<b>'+STATS.plays+'</b> 回目'", "'game <b>'+STATS.plays+'</b>'"),
 ("'<span class=\"sb-r\">お題 <b>'+STATS.seen.length+'</b> / '+total+'</span>'",
  "'<span class=\"sb-r\">lines <b>'+STATS.seen.length+'</b> / '+total+'</span>'"),
 ("w.textContent='「'+t.word+'」'", 'w.textContent=\'\\u201c\'+t.word+\'\\u201d\''),
 ("t.acts.slice(0,3).join('／')+' …ほか'", "t.acts.slice(0,3).join(' / ')+' …and more'"),
 ("(i+1)+'人目 '+c.n+' の役を見る'", "'player '+(i+1)+' '+c.n+' — see your role'"),
 ("(i+1)+'人目・'+c.n+' のあなた'", "'You are player '+(i+1)+' · '+c.n"),
 ("'言う言葉は「'+S.theme.word+'」'", '\'Your line: \\u201c\'+S.theme.word+\'\\u201d\''),
 ("'<span class=\"nm\">'+(n+1)+'番目</span><span class=\"act\">'+(p+1)+'人目・'+c.n+'</span>'",
  "'<span class=\"nm\">#'+(n+1)+'</span><span class=\"act\">player '+(p+1)+' · '+c.n+'</span>'"),
 ("'📱 '+(S.voter+1)+'人目・'+vc.n+' さんの番'", "'📱 player '+(S.voter+1)+' · '+vc.n+', your turn'"),
 ("'<b>'+(S.target+1)+'人目・'+tc.n+'</b> さんは、どの気持ちだった？'",
  "'How did <b>player '+(S.target+1)+' · '+tc.n+'</b> feel?'"),
 ("'投票 '+done+' / '+total", "'votes '+done+' / '+total"),
 ("'<span class=\"nm\">'+(i+1)+'人目</span>'", "'<span class=\"nm\">player '+(i+1)+'</span>'"),
 ("'<h3>得点</h3>'", "'<h3>Score</h3>'"),
 ("'</span><b>'+o.v+'点</b></div>'", "'</span><b>'+o.v+'</b></div>'"),
 ("'<div class=\"sr\"><span>'+(o.i+1)+'人目・'+c.n", "'<div class=\"sr\"><span>player '+(o.i+1)+' · '+c.n"),
 # 2026-10-02: 投票なしの答え合わせ・じぶんで作る
 ('<button class="btn-sub" id="toReveal">投票しないで答えを見る</button>', '<button class="btn-sub" id="toReveal">Skip voting — just reveal</button>'),
 ('口で当て合ったあとに。人数が多いときや小さい子がいるときに', 'Guess out loud first. Handy for big groups or young kids'),
 ('投票をここでやめて答えを見る', 'Stop voting and reveal now'),
 ("'みんなで考えた一言でも遊べます。この端末にだけ保存されます。'", "'Use your own line and feelings. Saved on this device only.'"),
 ("'＋じぶんで作る'", "'+ Make your own'"),
 # 日英は同じオリジンなので、自作お題の保存先を分ける（日本語の自作が英語画面に出ないように）
 ("MY_STORE = 'haa-mine'", "MY_STORE = 'haa-mine-en'"),
 ("'まず、全員が言う一言を書いてください'", "'First, write the line everyone will say'"),
 ("'気持ちが '+v.acts.length+' 個。'+S.players+'人なら '+S.players+' 個以上いります'", "v.acts.length+' feelings. '+S.players+' players need at least '+S.players"),
 ("'気持ち '+v.acts.length+' 個。このまま始められます'", "v.acts.length+' feelings. Ready to start'"),
 ('<label for="myWord">全員が言う一言</label>', '<label for="myWord">The line everyone says</label>'),
 ('placeholder="例：おめでとう"', 'placeholder="e.g. Congratulations"'),
 ('<label for="myActs">気持ち（1行に1つ・人数ぶん以上・8個まで）</label>', '<label for="myActs">Feelings (one per line, at least one per player, up to 8)</label>'),
 ('placeholder="うれしくて&#10;照れながら&#10;びっくりして&#10;そっけなく"', 'placeholder="happy&#10;shy&#10;surprised&#10;bored"'),
 ("'<p class=\"quick-note\">投票なしで答え合わせしました。口で当てた答えと比べてみてください。</p>'", "'<p class=\"quick-note\">No votes this round. Check the answers against your guesses.</p>'"),
 # 2026-10-03: 画面下の主ボタン欄（#dock）の進み具合
 ("'カードを順番にタップ（見た人 '+seenN+' / '+S.players+'人）'", "'Tap the cards in turn (seen '+seenN+' / '+S.players+')'"),
 # 色名
 ("{n:'あか',", "{n:'Red',"), ("{n:'あお',", "{n:'Blue',"),
 ("{n:'みどり',", "{n:'Green',"), ("{n:'きいろ',", "{n:'Yellow',"),
 ("{n:'むらさき',", "{n:'Purple',"), ("{n:'みずいろ',", "{n:'Sky',"),
 ("{n:'オレンジ',", "{n:'Orange',"), ("{n:'ピンク',", "{n:'Pink',"),
 # CSSの擬似要素
 ('content:"タップ"', 'content:"tap"'),
 ('content:"確認ずみ"', 'content:"done"'),
 # フォント（英語では丸ゴシックの日本語フォントは効かない）
 ('font-family:"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN",system-ui,sans-serif;',
  'font-family:"Nunito","Avenir Next","Segoe UI",system-ui,sans-serif;'),
]
for a, b in T:
    html = html.replace(a, b)

# ---- 4b. 2026-10-20 10/8 以降に日本語版へ入った機能の英語化 ----------------
# 英語版（授業・同じ部屋で1台を回す）では、日本語向けの配信モード・離れて遊ぶリンク・市販版の紹介・振り返りの記録は出さない（EN_HIDE）。
# 画面に出る文字はここで英語にする。日本語版の文言が変わってペアが当たらなくなったら止める（取り残し防止）。
# 画面に日本語が残っていないかは check_en.mjs（実際に開いて1回通しで遊ぶ）で確かめる
T2 = [
 # 見出し・遊んでいる間の帯
 ('<div class="hbar"><span class="hb-name">声と表情で当てるゲーム</span>', '<div class="hbar"><span class="hb-name">Emotion Charades</span>'),
 ("const stepName = {deal:'役を見る 3/6', perform:'演じる 4/6', vote:'投票 5/6', result:'答え合わせ 6/6'};",
  "const stepName = {deal:'Roles 3/6', perform:'Perform 4/6', vote:'Vote 5/6', result:'Reveal 6/6'};"),
 # 人数
 ('3〜8人がふつう。4〜6人がいちばん当てにくいです。1〜2人は、配信やまわりの人が当てる形で', '3 to 8 players. 4 to 6 is the hardest to read'),
 ("? '3〜8人がふつう。4〜6人がいちばん当てにくいです'", "? '3 to 8 players. 4 to 6 is the hardest to read'"),
 ("(S.players === 1 ? '1人で演じて、視聴者やまわりの人が候補から当てる形。投票はありません。候補の数は下で選べます'",
  "(S.players === 1 ? 'One person acts and everyone around guesses from the list. No voting'"),
 (": '2人なら、1人が演じてもう1人が当てる形。候補は3つ出ます');", ": 'With two, one acts and the other guesses from three feelings');"),
 ('<p class="act-lbl">1回に演じる人</p>', '<p class="act-lbl">Actors per round</p>'),
 ('aria-label="演じる人をone fewer player"', 'aria-label="one fewer actor"'),
 ('aria-label="演じる人をone more player"', 'aria-label="one more actor"'),
 ('<p class="hint" id="actHint">ふつうは全員が演じます。1人ずつ交代で遊ぶときは減らせます（演じない人は投票だけ）</p>',
  '<p class="hint" id="actHint">Usually everyone acts. Lower it to take turns one at a time (the others only vote)</p>'),
 ("? (S.players === 1 ? '演じるのはあなた1人です' : 'ふつうは全員が演じます。1人ずつ交代で遊ぶときは減らせます（演じない人は投票だけ）')",
  "? (S.players === 1 ? 'You are the only actor' : 'Usually everyone acts. Lower it to take turns one at a time (the others only vote)')"),
 (": (k === 1 ? '演じない'+(S.players-k)+'人は投票だけ。気持ちの候補は'+poolN()+'つ'",
  ": (k === 1 ? 'The other '+(S.players-k)+' only vote. '+poolN()+' feelings to choose from'"),
 (": '演じるのは'+k+'人（毎回交代）。ほかの'+(S.players-k)+'人は投票だけします。気持ちの候補は'+poolN()+'つから選びます');",
  ": k+' act each round (taking turns). The other '+(S.players-k)+' only vote. '+poolN()+' feelings to choose from');"),
 # 名前
 ('<summary class="names-sum">プレイヤー名を入れる（任意）<span id="namesCount"></span></summary>', '<summary class="names-sum">Player names (optional)<span id="namesCount"></span></summary>'),
 ('<button type="button" class="names-clear" id="namesClear">名前をすべて消す</button>', '<button type="button" class="names-clear" id="namesClear">Clear all names</button>'),
 ("inp.placeholder = (i+1)+'人目・'+c.n;", "inp.placeholder = 'Player '+(i+1)+' · '+c.n;"),
 ("inp.setAttribute('aria-label', (i+1)+'人目の名前');", "inp.setAttribute('aria-label', 'Name of player '+(i+1));"),
 ("function pLabel(i){ return (S.names[i]||'').trim() ? pName(i) : (i+1)+'人目・'+pName(i); }",
  "function pLabel(i){ return (S.names[i]||'').trim() ? pName(i) : 'Player '+(i+1)+' · '+pName(i); }"),
 # 演じる人を選ぶ
 ('<div class="actor-pick" id="apFirst"><p class="ap-h">最初に演じる人</p><div class="ap-row" role="group" aria-label="最初に演じる人"></div></div>',
  '<div class="actor-pick" id="apFirst"><p class="ap-h">Who acts first</p><div class="ap-row" role="group" aria-label="Who acts first"></div></div>'),
 ('<div class="actor-pick" id="apNext"><p class="ap-h">次に演じる人</p><div class="ap-row" role="group" aria-label="次に演じる人"></div></div>',
  '<div class="actor-pick" id="apNext"><p class="ap-h">Who acts next</p><div class="ap-row" role="group" aria-label="Who acts next"></div></div>'),
 # お題を選ぶ
 ('<button type="button" class="redraw" id="redraw">ほかの3つを見る ↺</button>', '<button type="button" class="redraw" id="redraw">Show three others ↺</button>'),
 ('content:"選択中"', 'content:"selected"'),
 ("<span class=\"pi-s\">'+esc(t.acts.slice(0,3).join('／'))+' …ほか</span>", "<span class=\"pi-s\">'+esc(t.acts.slice(0,3).join(' / '))+' …and more</span>"),
 # いまの状態の1行
 ("const who = S.k >= S.players && S.players > 1 ? '全員' : S.act.map(p=>'<b>'+esc(pName(p))+'</b>さん').join('・');",
  "const who = S.k >= S.players && S.players > 1 ? 'everyone' : S.act.map(p=>'<b>'+esc(pName(p))+'</b>').join(', ');"),
 ("const what = {deal:'役を見る時間', perform:(S.players === 1 ? '演じて当ててもらう時間' : '演じて当てる時間'), vote:'投票の時間',",
  "const what = {deal:'checking roles', perform:'acting and guessing', vote:'voting',"),
 ("result:(S.vopen ? '投票結果' : document.body.classList.contains('veiling') ? '答えを見る前' : '答え合わせ')}[step];",
  "result:(S.vopen ? 'votes' : document.body.classList.contains('veiling') ? 'before the reveal' : 'reveal')}[step];"),
 ("na.innerHTML = (S.gno||1)+'回目・'+(step === 'result' ? '演じた人：' : 'いま演じる人：')+who+'・'+what;",
  "na.innerHTML = 'Round '+(S.gno||1)+' · '+(step === 'result' ? 'acted: ' : 'acting: ')+who+' · '+what;"),
 # 配る
 ('<p class="hint">全員が同じ「<b id="dealWord"></b>」を言います。<br>気持ちだけが1人ずつ違います。みんなには、こっそり見てね</p>',
  '<p class="hint">Everyone says the same "<b id="dealWord"></b>".<br>Only the feeling differs. Keep yours secret!</p>'),
 ("$('dockMsg').textContent = 'カードを順番にタップ（見た人 '+seenN+' / '+S.k+'人）';", "$('dockMsg').textContent = 'Tap the cards in turn (seen '+seenN+' / '+S.k+')';"),
 ("b.setAttribute('aria-label', pLabel(p)+' の役を見る');", "b.setAttribute('aria-label', pLabel(p)+' — see your role');"),
 ("$('revealWho').textContent = pLabel(S.act[i])+' さん';", "$('revealWho').textContent = pLabel(S.act[i]);"),
 ('<div class="warn" id="revealWarn">ほかの人には内緒にしておいてね</div>', '<div class="warn" id="revealWarn">Keep this to yourself</div>'),
 # 演じる
 ("+ '<div class=\"st-who\">'+(S.k===1 ? esc(pLabel(S.act[0]))+' さんの番' : S.k+'人が順番に演じます')+'</div>'",
  "+ '<div class=\"st-who\">'+(S.k===1 ? esc(pLabel(S.act[0]))+', your turn' : S.k+' players take turns')+'</div>'"),
 ("+ '<div class=\"st-word\">「'+esc(S.theme.word)+'」</div>'", "+ '<div class=\"st-word\">\\u201c'+esc(S.theme.word)+'\\u201d</div>'"),
 ("+ '<div class=\"st-sub\">声と表情だけで。どの気持ちかを当ててもらう</div>'", "+ '<div class=\"st-sub\">Voice and face only. Let them guess the feeling</div>'"),
 ("+ '<div class=\"st-chat\">リスナーのみなさん、コメントで番号を当ててください（例：③）</div>';", "+ '';"),
 ("cw.innerHTML = '<div class=\"cl\">気持ちの候補（この中のどれかを演じます）</div><ul>'", "cw.innerHTML = '<div class=\"cl\">The feelings (each actor has one of these)</div><ul>'"),
 ('<p class="hint perf-hint">身振りは使わず、<b>声と表情だけ</b>で。1人ずつ「<b id="performWord"></b>」と言ってください。</p>',
  '<p class="hint perf-hint"><b>Voice and face only</b> — no gestures. Take turns saying "<b id="performWord"></b>".</p>'),
 ("row.innerHTML = '<span class=\"nm\">'+(n+1)+'番目</span><span class=\"act\">'+esc(pLabel(p))+'</span>';", "row.innerHTML = '<span class=\"nm\">#'+(n+1)+'</span><span class=\"act\">'+esc(pLabel(p))+'</span>';"),
 # 投票
 ('<p class="hint" id="voteHint">スマホを回して、1人ずつ投票します。<br>自分以外の演じた人が「どの気持ち」だったかを選んでください。</p>',
  '<p class="hint" id="voteHint">Pass the phone and vote one at a time.<br>Choose the feeling you think each of the other actors had.</p>'),
 ("$('voteWho').textContent = '📱 '+pLabel(S.voter)+' さんの番';", "$('voteWho').textContent = '📱 '+pLabel(S.voter)+', your turn';"),
 ("$('voteTarget').innerHTML = '<b>'+esc(pLabel(S.act[S.target]))+'</b> さんは、どの気持ちだった？';", "$('voteTarget').innerHTML = 'How did <b>'+esc(pLabel(S.act[S.target]))+'</b> feel?';"),
 ('<button type="button" class="np-link vote-undo" id="voteUndo" hidden>↶ 1つ前の票をやり直す</button>', '<button type="button" class="np-link vote-undo" id="voteUndo" hidden>↶ Undo the last vote</button>'),
 ("'投票がそろいました。「せーの」で答えを見ましょう';", "'All votes are in. Reveal together on three!';"),
 ('<button type="button" class="btn-primary unveil" id="unveil" hidden>答えを見る</button>', '<button type="button" class="btn-primary unveil" id="unveil" hidden>Reveal</button>'),
 ("$('resCands').innerHTML = '<div class=\"cl\">気持ちの候補「'+esc(S.theme.word)+'」</div><ul>'", "$('resCands').innerHTML = '<div class=\"cl\">The feelings for \\u201c'+esc(S.theme.word)+'\\u201d</div><ul>'"),
 # 答え合わせ・得点
 ("+ '<div class=\"ans-main\"><span class=\"ans-kick\">正解</span><span class=\"ans-no\">'+numOf(ai)+'</span>", "+ '<div class=\"ans-main\"><span class=\"ans-kick\">Answer</span><span class=\"ans-no\">'+numOf(ai)+'</span>"),
 ("let h = '<h3>'+(S.rounds > 1 ? '合計得点<span class=\"sr-rd\">'+S.rounds+'回目まで</span>' : '得点')+'</h3>', rank = 0, prev = null;",
  "let h = '<h3>'+(S.rounds > 1 ? 'Total score<span class=\"sr-rd\">after '+S.rounds+' rounds</span>' : 'Score')+'</h3>', rank = 0, prev = null;"),
 ("const hitTxt = pp ? '<small class=\"sr-hit\">当てた '+pp.hit+'/'+pp.tries+'・伝わった '+pp.got+'回</small>' : '';",
  "const hitTxt = pp ? '<small class=\"sr-hit\">guessed '+pp.hit+'/'+pp.tries+' · read '+pp.got+'×</small>' : '';"),
 ("<span class=\"sr-rk\">'+rank+'位</span>", "<span class=\"sr-rk\">#'+rank+'</span>"),
 ("</i></span><b>'+o.v+'点'+(S.rounds > 1", "</i></span><b>'+o.v+(S.rounds > 1"),
 ("const ASKS = ['当たった？外れた？','今の演技、どうだった？','この気持ち、分かった人いる？','次はだれに演じてほしい？','ほかの気持ちに聞こえた人いる？','いちばん迷ったのは何番だった？'];",
  "const ASKS = ['Did you get it?','How was that performance?','Did anyone read that feeling?','Who should act next?','Did it sound like a different feeling?','Which number fooled you most?'];"),
 ("ASKS[ASK_I].indexOf('だれに') >= 0", "ASKS[ASK_I].indexOf('Who should') >= 0"),
 # 次のお題
 ('<div class="np-h"><span class="np-t">次のお題を選ぶ</span><span class="np-ts">次のお題、どれがいい？</span><span class="np-cat" id="npCat"></span></div>',
  '<div class="np-h"><span class="np-t">Pick the next line</span><span class="np-ts">Which line next?</span><span class="np-cat" id="npCat"></span></div>'),
 ('<button type="button" class="np-link" id="npMore">ほかの3つ ↺</button><button type="button" class="np-link" id="npCatChange">カテゴリを変える</button>',
  '<button type="button" class="np-link" id="npMore">Three others ↺</button><button type="button" class="np-link" id="npCatChange">Change category</button>'),
 # 答えを見る・投票なし・合計のリセット（2026-10-20）
 ("tr.textContent = both ? '答えだけ見る' : (quick ? '答えを見る' : '投票しないで答えを見る');", "tr.textContent = both ? 'Just reveal' : (quick ? 'Reveal' : 'Skip voting — just reveal');"),
 ("$('unveil').textContent = '答えを見る';", "$('unveil').textContent = 'Reveal';"),
 ("'投票なしで答え合わせしました。口で当てた答えと比べてみてください。'", "'No votes this round. Check the answers against your guesses.'"),
 ("<span class=\"ans-word\">「'+esc(S.theme.word)+'」</span>", "<span class=\"ans-word\">\\u201c'+esc(S.theme.word)+'\\u201d</span>"),
 ("id=\"scoreReset\">合計を0に戻す</button>", "id=\"scoreReset\">Reset the total</button>"),
 ("rb.textContent = '本当に0に戻す？（もう一度押す）';", "rb.textContent = 'Reset to 0? (tap again)';"),
 ("rb.textContent = '合計を0に戻す';", "rb.textContent = 'Reset the total';"),
 ("$('newGame').textContent = on ? '「'+t.word+'」で始める' : 'Play again';", "$('newGame').textContent = on ? 'Start with \\u201c'+t.word+'\\u201d' : 'Play again';"),
 ("b.innerHTML = '<span class=\"pi-w\">「'+esc(t.word)+'」</span>", "b.innerHTML = '<span class=\"pi-w\">\\u201c'+esc(t.word)+'\\u201d</span>"),
]
# 日本語版の文言が変わってペアが見つからないときは、止めずに飛ばして最後に一覧を出す
# （その所は日本語のまま残る。英語版を日本語版に追いつかせるときに、この一覧を見てペアを直す）
MISSING = []
for a, b in T2:
    if a not in html:
        MISSING.append(a)
        continue
    html = html.replace(a, b)

# 英語版で出さない部品（日本語向けの機能）。要素は残して隠す（JS が id で触るため）
EN_HIDE = ('<style id="en-hide">\n'
  '/* 英語版では出さない：配信モード・離れて遊ぶリンク・市販版（日本の商品）・振り返りの記録・はじめての方へ・配信から来た人への一言 */\n'
  '#streamSw,#castSw,#playMode,.pm-sp,.cand-n,.sfx-sw,#viewOpen,#streamNote,#firstGuide,#fromStream,.shop-mini,\n'
  '.deal-link,.deal-qr,#joinBox,#sentHint,.deal-remote,#annBox,#logLinks,#recStrip,.deal-scroll{display:none!important}\n'
  '</style>\n</head>')
html = html.replace('</head>', EN_HIDE, 1)
# 配信モードは英語版では使わない（PCでも配信モードにしない）
html, n_st = re.subn(r"if \(/\[\?&\]mode=stream\\b/\.test\(location\.search\)\) on = true;", "on = false; // 英語版は配信モードなし", html, count=1)
if n_st != 1:
    sys.exit('[NG] 配信モードの判定（mode=stream）が見つかりません')

# お題一覧ページへのリンクは英語版にまだ無いので、行ごと落とす
html = re.sub(r'\s*<p style="text-align:center;font-size:\.85rem;margin-top:\.8rem">\s*<a href="/odai/".*?</a>\s*</p>', '', html, flags=re.S)

# FAQ を差し替え（日本語版は build.py が静的HTMLで差し込んでいるので、そのブロックごと英語に置き換える）
FAQ = [
 ('Do we need the card game to play?',
  'No. Pass one phone around and each player sees their role privately. Voting and scoring are automatic, so there are no chips or paper to keep track of.'),
 ('How many players?',
  'Three to eight. Four to six is the sweet spot — hard to read, easy to run. The number of roles adjusts to your group.'),
 ('How does it actually work?',
  'Everyone says the same short line, but each player is secretly given a different feeling to put behind it. Voice and face only, no gestures. Then everyone votes on who had which feeling.'),
 ('Can I use this in an English class?',
  'Yes — that is what the school and greetings sets are for. It drills intonation and emotional register with real speaking time for every student, and the phone handles the admin.'),
 ('How do I run it with a whole class?',
  'Split the class into groups of three to eight (four to six works best) and give each group one phone or tablet. Each group plays on its own, so every student gets speaking turns at the same time. If voting takes too long, tap "Skip voting — just reveal" and let students guess out loud.'),
 ('Is it free? Do students need an app or an account?',
  'Free, with no app and no sign-up. It runs in the browser on iPhone, Android, iPad or a Chromebook. There are ads on the page.'),
 ('Can we make our own lines?',
  'Yes. Choose "+ Make your own", type the line everyone will say and one feeling per player. Roles, voting and scoring work the same way. What you type stays on this device.'),
 ('How many prompts are there?',
  '%d prompts with 8 ways to say each one — %d in total. All written by us.'),
]
FAQ[-1] = (FAQ[-1][0], FAQ[-1][1] % (n_word, n_act))
faq_block = '\n'.join('    <dt>%s</dt><dd>%s</dd>' % (q, a) for q, a in FAQ)
html, n_faq = re.subn(r'<!-- FAQ:BEGIN.*?<!-- FAQ:END -->', lambda m: faq_block, html, count=1, flags=re.S)
if n_faq != 1:
    sys.exit('[NG] FAQ の差し込み位置（FAQ:BEGIN〜END）が見つかりません')
# 日本語の FAQPage 構造化データは英語版に持ち込まない
html = re.sub(r'<!-- FAQLD:BEGIN.*?<!-- FAQLD:END -->\n?', '', html, count=1, flags=re.S)

# 言語切り替えリンクを header に足す（日本語版にある「English version」＝英語版から自分自身へのリンクは外す）
# 2026-10-20 日本語版の見出し（D4 化）で「配信・実況で使う方へ」と「English version」が1行になった。英語版ではこの行を日本語版への切り替えにする
html, n_self = re.subn(r'<p class="hen"><a href="/haishin/">[^<]*</a>[^<]*<a href="/en/">English version</a></p>', '<p class="hen"><a href="/">日本語版はこちら</a></p>', html, count=1)
if n_self != 1:
    sys.exit('[NG] 日本語版の「English version」リンクが見つかりません（ヘッダーの言語切り替え）')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
io.open(OUT, 'w', encoding='utf-8').write(html)

# ---- 5. 日本語の消し残しを検出 -------------------------------------------
# 画面に出る日本語だけを見る。コード内のコメントは保守する側のものなので残す。
visible = re.sub(r'<!--.*?-->', '', html, flags=re.S)
visible = re.sub(r'/\*.*?\*/', '', visible, flags=re.S)
visible = re.sub(r'(?m)^\s*//.*$', '', visible)
visible = re.sub(r'\s//[^\n\'"]*$', '', visible, flags=re.M)
leftover = []
for i, line in enumerate(visible.split('\n'), 1):
    line = line.replace('web忍者の砦', '')      # ブランド名は残す
    if '日本語版はこちら' in line:               # 言語切り替えリンクも残す
        continue
    if re.search(r'[ぁ-んァ-ヶ一-龠「」／]', line):
        leftover.append('  %s' % line.strip()[:110])
print('[ok] en/index.html  %d prompts / %d ways  %d bytes' % (n_word, n_act, len(html)))
# 2026-10-20 日本語版に配信モード・離れて遊ぶリンク（参加者画面）・振り返りなどが入り、英語版では動かない（EN_HIDE で隠す）部分の
# コードにも日本語が残るようになった。ソースの行数は目安として出すだけにして、画面に出るかどうかは check_en.mjs で実際に遊んで確かめる
if leftover:
    print('[info] ソースに日本語を含む行 %d（英語版では出さない部分を含む）。画面の確認: node check_en.mjs' % len(leftover))
    if '-v' in sys.argv:
        print('\n'.join(leftover))
if MISSING:
    print('[warn] 日本語版で見つからなかった英語化のペア %d（その所は日本語のまま。英語版を追いつかせるときに直す）:' % len(MISSING))
    for a in MISSING:
        print('  - ' + a[:90].replace('\n', ' '))
