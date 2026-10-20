// 英語版 /en/ を実際に開いて1回通しで遊び、画面に出る日本語（文字・placeholder・aria-label・title・alt）が残っていないかを見る。
// build_en.py のあとに: python3 -m http.server 8981 --bind 127.0.0.1 を立てて  node check_en.mjs [http://127.0.0.1:8981/en/]
// 配信しないファイル（deploy.yml で消す）。広告・計測のリクエストは止めて開く
import {spawn} from 'node:child_process'; import fs from 'node:fs';
const URL0 = process.argv[2] || 'http://127.0.0.1:8981/en/';
const sleep = ms => new Promise(r=>setTimeout(r,ms));
const JA = /[ぁ-んァ-ヶ一-龠「」／・、。（）]/;
const found = new Map(); const errs = [];
async function run(w, h, mobile, tag){
  const port = 9300 + Math.floor(Math.random()*500), dir = '/tmp/_haaen_'+port+'_'+Date.now();
  const ch = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new','--disable-gpu','--no-first-run',`--remote-debugging-port=${port}`,'--user-data-dir='+dir,`--window-size=${w},${h}`], {stdio:'ignore'});
  try {
    let t; for (let i=0;i<40;i++){ try { t = await (await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json(); break; } catch { await sleep(300); } }
    const ws = new WebSocket(t.webSocketDebuggerUrl); let id=0; const pend={};
    const send=(m,p={})=>new Promise(r=>{const i=++id;pend[i]=r;ws.send(JSON.stringify({id:i,method:m,params:p}))});
    await new Promise(r=>ws.onopen=r);
    ws.onmessage=e=>{const d=JSON.parse(e.data); if(d.id&&pend[d.id]){pend[d.id](d.result||d.error);delete pend[d.id]} if(d.method==='Runtime.exceptionThrown') errs.push(tag+' '+(d.params.exceptionDetails.exception?.description||'').slice(0,160));};
    await send('Runtime.enable'); await send('Network.enable');
    await send('Network.setBlockedURLs',{urls:['*googletagmanager*','*google-analytics*','*googlesyndication*','*doubleclick*','*adtrafficquality*','*fundingchoices*']});
    await send('Emulation.setDeviceMetricsOverride',{width:w,height:h,deviceScaleFactor:1,mobile});
    const js = async s => { const r = await send('Runtime.evaluate',{expression:`(async()=>{const $=id=>document.getElementById(id); const sleep=ms=>new Promise(r=>setTimeout(r,ms)); const vis=el=>!!el&&el.getClientRects().length>0&&getComputedStyle(el).visibility!=='hidden'; ${s}})()`,awaitPromise:true,returnByValue:true,userGesture:true}); return r.result?.value; };
    const scan = async (step) => {
      const list = await js(`const out=[]; const re=${JA}; const ok=t=>{ t=String(t||'').replace(/web忍者の砦/g,'').replace(/日本語版はこちら/g,''); return re.test(t) ? t.trim().slice(0,90) : ''; };
        if (ok(document.title)) out.push('title: '+document.title);
        const w=document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
        while((n=w.nextNode())){ const el=n.parentElement; if(!el||!vis(el)||/^(SCRIPT|STYLE)$/.test(el.tagName)) continue; const r=el.getBoundingClientRect(); if(!r.width||!r.height) continue; const t=ok(n.nodeValue); if(t) out.push(t); }
        document.querySelectorAll('[placeholder],[aria-label],[title],img[alt]').forEach(el=>{ if(!vis(el)) return; ['placeholder','aria-label','title','alt'].forEach(a=>{ const t=ok(el.getAttribute(a)); if(t) out.push('@'+a+': '+t); }); });
        document.querySelectorAll('*').forEach(el=>{ if(!vis(el)) return; ['::before','::after'].forEach(p=>{ const c=getComputedStyle(el,p).content; if(c&&c!=='none'&&c!=='normal'){ const t=ok(c); if(t) out.push(p+': '+t); } }); });
        return out;`);
      for (const s of list||[]) { const k = s; if (!found.has(k)) found.set(k, tag+' '+step); }
    };
    await send('Page.navigate',{url:URL0}); await sleep(2500);
    await scan('setup');
    await js(`document.querySelectorAll('details').forEach(d=>{ if(vis(d)) d.open=true; }); return 1`); await sleep(300); await scan('setup-open');
    await js(`const b=$('mineBtn')||[...document.querySelectorAll('button')].find(b=>vis(b)&&/Make your own/.test(b.textContent)); if(b){ b.click(); } return !!b`); await sleep(500); await scan('mine');
    await send('Page.navigate',{url:URL0+'?nc=2'}); await sleep(2200);
    for (let round=0; round<2; round++){
      if (round===0) await js(`$('startGame').click(); return 1`); else await js(`await sleep(900); $('newGame').click(); return 1`);
      await sleep(1000); await scan('deal');
      const k = await js(`return document.querySelectorAll('#dealGrid .deal-card').length`);
      for (let i=0;i<k;i++){ await js(`document.querySelectorAll('#dealGrid .deal-card')[${i}].click(); return 1`); await sleep(500); await scan('reveal'); await js(`$('revealClose').click(); return 1`); await sleep(400); }
      await scan('deal-done');
      await js(`await sleep(900); $('toPerform').click(); return 1`); await sleep(1000); await scan('perform');
      await js(`await sleep(900); $('toVote').click(); return 1`); await sleep(1000); await scan('vote');
      for (let v=0; v<30; v++){
        const st = await js(`if (!vis($('step-vote'))) return 'done'; const bs=[...document.querySelectorAll('#voteList button')].filter(b=>vis(b)&&!b.disabled); if (bs.length){ bs[${v}%bs.length].click(); return 'v'; } if (vis($('unveil'))) return 'unveil'; return 'wait'`);
        await sleep(750); if (v===1) await scan('vote2');
        if (st==='done' || st==='unveil') break;
      }
      await scan('voted');
      await js(`if (vis($('unveil'))) { await sleep(900); $('unveil').click(); } return 1`); await sleep(5200); await scan('result');
      await js(`if (vis($('logOpen'))) $('logOpen').click(); return 1`); await sleep(600); await scan('log');
      await js(`if (vis($('logClose'))) $('logClose').click(); return 1`); await sleep(300);
      await js(`const it=document.querySelector('#npList .pick-item'); if(it&&vis(it)) it.click(); const r=$('scoreReset'); if(r&&vis(r)) r.click(); return 1`); await sleep(400); await scan('next-pick');
    }
    // 投票なしの答え合わせ
    await js(`await sleep(900); $('newGame').click(); await sleep(900); document.querySelectorAll('#dealGrid .deal-card').forEach(c=>{ c.click(); $('revealClose').click(); }); await sleep(900); $('toPerform').click(); await sleep(1000); $('toReveal').click(); if ($('toReveal').dataset.ask){ await sleep(400); $('toReveal').click(); } return 1`);
    await sleep(5500); await scan('quick-result');
  } finally { try { ch.kill('SIGKILL'); } catch(e){} await sleep(300); try { fs.rmSync(dir,{recursive:true,force:true}); } catch(e){} }
}
await run(390, 844, true, 'sp');
await run(1280, 800, false, 'pc');
if (errs.length) console.log('JS errors:\n'+errs.join('\n'));
if (found.size){ console.log('[NG] 画面に日本語が '+found.size+' 件:'); for (const [k,v] of found) console.log('  ['+v+'] '+k); process.exit(1); }
console.log('[ok] 英語版の画面に日本語は残っていません（スマホ・PCで1回ずつ通し）');
process.exit(errs.length ? 1 : 0);
