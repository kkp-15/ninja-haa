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
HEAD = '''<title>Say It With Feeling — the guess-the-emotion game for one phone</title>
<meta name="description" content="Everyone says the same line. Each person is secretly given a different emotion. Pass one phone around, act, then vote — roles, voting and scoring are all handled for you. %d prompts, %d ways to say them. Free, no sign-up, no app.">
<link rel="canonical" href="https://haa.kkpwebninja.com/en/">
<link rel="alternate" hreflang="ja" href="https://haa.kkpwebninja.com/">
<link rel="alternate" hreflang="en" href="https://haa.kkpwebninja.com/en/">
<link rel="alternate" hreflang="x-default" href="https://haa.kkpwebninja.com/">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#e8843a">

<meta property="og:title" content="Say It With Feeling — one phone, one line, eight emotions">
<meta property="og:description" content="Say the same word eight different ways and see who can tell them apart. Roles, voting and scoring on a single phone.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://haa.kkpwebninja.com/en/">
<meta property="og:site_name" content="Say It With Feeling">
<meta property="og:image" content="https://haa.kkpwebninja.com/ogp.png?d=20260906">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://haa.kkpwebninja.com/ogp.png?d=20260906">

<link rel="icon" type="image/png" sizes="32x32" href="/favicon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">

<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"Say It With Feeling","url":"https://haa.kkpwebninja.com/en/","applicationCategory":"GameApplication","operatingSystem":"Web","inLanguage":"en","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"author":{"@type":"Organization","name":"web忍者の砦"},"publisher":{"@type":"Organization","name":"web忍者の砦","url":"https://kkpwebninja.com/"}}
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
    <a href="https://privacypolicy.kkpwebninja.com/" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">Privacy policy</a>·
    <a href="https://x.com/kkp_webninja" target="_blank" rel="noopener" style="color:#8b6b3d;text-decoration:none;margin:0 0.5rem;">@kkp_webninja</a>
  </div>
  <div style="margin-top:0.5rem;color:#bfa97a;">© 2025-2026 web忍者の砦</div>
</footer>'''
html = re.sub(r'<!-- WEBNINJA_UNIFIED_FOOTER -->.*?</footer>', FOOTER, html, count=1, flags=re.S)

# ---- 4. UIと本文の文字列 --------------------------------------------------
# 長いものから当てる（短い語が先に食うと崩れる）
T = [
 # head 以外に残る大物
 ('<h1>声と表情で当てるゲーム</h1>', '<h1>Say It With Feeling</h1>'),
 ('<p>同じ一言を、それぞれ違う気持ちで演じて当て合う。<br>スマホ1台で配役から得点まで。</p>',
  '<p>Everyone says the same line with a different feeling.<br>One phone handles the roles, the voting and the score.</p>'),
 # 遊び方
 ('遊び方（30秒で読めます）', 'How to play (30 seconds)'),
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
 ('声と表情で演じ分けて当て合う遊びを、スマホ1台でできるようにした非公式のツールです。<br>',
  'An unofficial tool that puts this acting-and-guessing game on a single phone.<br>'),
 ('お題はすべて当サイトのオリジナルで、市販品の内容は含みません。',
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
 # 共有ブロック。英語ではLINEを出さず、ラベルも英語にする
 ('<div data-fortress-share\n       data-site="ninja-haa"\n       data-trigger="result"\n       data-label="この結果を教える"\n       data-text-fn="getShareText"\n       data-hashtags="#パーティーゲーム #飲み会ゲーム"></div>',
  '<div data-fortress-share\n       data-site="ninja-haa-en"\n       data-lang="en"\n       data-trigger="result"\n       data-label="Share this round"\n       data-text-fn="getShareText"\n       data-hashtags="#partygames #icebreaker"></div>'),
 ("'「'+S.theme.word+'」を'+S.players+'人で演じ分けました。\\n'",
  "'We each said \\u201c'+S.theme.word+'\\u201d a different way, '+S.players+' of us.\\n'"),
 ("(max===0 ? 'まさかの全員はずれ。声だけで気持ちを伝えるの、むずかしい'\n                    : '最高'+max+'点。同じ一言でも、人によって全然ちがう')",
  "(max===0 ? 'Nobody guessed a single one. Voice alone is harder than it looks'\n                    : 'Top score '+max+'. Same word, very different people')"),
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

# お題一覧ページへのリンクは英語版にまだ無いので、行ごと落とす
html = re.sub(r'\s*<p style="text-align:center;font-size:\.85rem;margin-top:\.8rem">\s*<a href="/odai/".*?</a>\s*</p>', '', html, flags=re.S)

# FAQ を差し替え
FAQ = """const FAQ = [
 ['Do we need the card game to play?','No. Pass one phone around and each player sees their role privately. Voting and scoring are automatic, so there are no chips or paper to keep track of.'],
 ['How many players?','Three to eight. Four to six is the sweet spot — hard to read, easy to run. The number of roles adjusts to your group.'],
 ['How does it actually work?','Everyone says the same short line, but each player is secretly given a different feeling to put behind it. Voice and face only, no gestures. Then everyone votes on who had which feeling.'],
 ['Can I use this in an English class?','Yes — that is what the school and greetings sets are for. It drills intonation and emotional register with real speaking time for every student, and the phone handles the admin.'],
 ['How many prompts are there?','%d prompts with 8 ways to say each one — %d in total. All written by us.']
];""" % (n_word, n_act)
html = re.sub(r'const FAQ = \[.*?\];', lambda m: FAQ, html, count=1, flags=re.S)

# 言語切り替えリンクを header に足す
html = html.replace('</header>',
  '  <p style="font-size:.8rem;margin:.4rem 0 0"><a href="/" style="color:#8a7560">日本語版はこちら</a></p>\n</header>')

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
if leftover:
    print('[NG] 日本語が %d 行残っています:' % len(leftover))
    print('\n'.join(leftover))
    sys.exit(1)
