#!/usr/bin/env python3
"""Bygger /ddb/soker (Hvilken Søker er du?) og delingssidene /ddb/soker/<profesjon>.
Kjør fra repo-rota: python3 tools/build_ddb_soker.py"""
import json, os

BK = "https://www.backerkit.com/c/projects/kr1-publishing/de-dodes-bok/pre-launch"
MC = "https://kr1publishing.us13.list-manage.com/subscribe/post?u=9b8e99b826134f12e16a15a13&amp;id=1eeadea463&amp;f_id=007c7de9f0"

P = {
 "leiesoldat": {"n":"Leiesoldat","lag":"Overflaten","L":8,"F":2,"tag":"Står lengst.",
   "d":"Du er veggen de andre står bak, og du har aldri lurt på hvorfor det er du som står fremst. Når det smeller, er det deg de ser etter.",
   "spill":"I spillet tåler du mest av alle og har fordel hver gang du presser. Sinnet ditt er det som slites først."},
 "duelist": {"n":"Duelist","lag":"Overflaten","L":6,"F":4,"tag":"Står først.",
   "d":"Du ser åpningen før de andre ser kampen. Ett presist hugg er nok, og du har sjelden bruk for et nummer to.",
   "spill":"I spillet avslutter du enkeltmål og velger selv når du slår. Du er farligst når du venter."},
 "akademiker": {"n":"Akademiker","lag":"Overflaten","L":4,"F":6,"tag":"Vet hva det er.",
   "d":"Hvis det ikke er skrevet ned, er det ikke viktig. Du skriver ned alt, og det er derfor de andre lever.",
   "spill":"I spillet er du den som vet hva noe tåler og hva det frykter. Du blander miksturer og leser det andre bare ser."},
 "dusorjeger": {"n":"Dusørjeger","lag":"Underverdenen","L":6,"F":4,"tag":"Vet hvor det er.",
   "d":"Du finner alle. Spørsmålet er bare hva de betaler for at du skal glemme hvor.",
   "spill":"I spillet merker du byttet og vet alltid hvor det er. Sølv og en bue gjør deg farlig på avstand."},
 "hundetrener": {"n":"Hundetrener","lag":"Underverdenen","L":6,"F":4,"tag":"Finner veien.",
   "d":"Det er ikke en ulv. Det er en hund. Og den har aldri tatt feil om hvem som kan stoles på.",
   "spill":"I spillet er dere to. Hunden biter, sporer og hjelper de andre, og den merker det som ikke er levende."},
 "artist": {"n":"Artist","lag":"Eterisk","L":4,"F":6,"tag":"Får folk til å snakke.",
   "d":"Du har en maske for hver dør, og noen av dem er ikke laget for mennesker.",
   "spill":"I spillet åpner du dører med ord, og masken får selv de døde til å nøle."},
 "okkultist": {"n":"Okkultist","lag":"Kosmisk","L":3,"F":7,"tag":"Leser det ingen tør.",
   "d":"Tegnet er ikke farlig. Tegnet er en dør. Det som er farlig, er det som venter bak.",
   "spill":"I spillet bærer du ladede tegn som brenner gjennom rustning og sølv. Hvert av dem koster deg noe."},
 "konstruktor": {"n":"Konstruktør","lag":"Kosmisk","L":4,"F":6,"tag":"Bygger det som trengs.",
   "d":"Den er ikke levende. Den er bedre. Du har alltid en liten figur i lomma, og den våkner når du trenger den.",
   "spill":"I spillet gir du gruppa en ekstra kropp: dukker du lager selv, til kamp, vakt eller verre ting."},
}
LAGC = {"Overflaten":"#b08a3e","Underverdenen":"#6e8c5a","Eterisk":"#7d8fb3","Kosmisk":"#9b6cb0"}

Q = [
 ("Natten før ekspedisjonen. Hva gjør du?", [
   ("Sliper våpenet og legger meg tidlig", ["leiesoldat","duelist"]),
   ("Leser alt som finnes om stedet", ["akademiker","okkultist"]),
   ("Går ut og hører hva folk i landsbyen sier", ["artist","dusorjeger"]),
   ("Gjør klart utstyret, og hunden", ["hundetrener","konstruktor"])]),
 ("Gruppa står foran en dør som ikke vil åpne seg.", [
   ("Den åpner seg om den får en skulder", ["leiesoldat"]),
   ("Jeg leser tegnene i treverket", ["okkultist","akademiker"]),
   ("Jeg ser hvem som gikk her sist, og hvor de gikk i stedet", ["dusorjeger","hundetrener"]),
   ("Jeg har et verktøy, eller en venn på innsiden", ["konstruktor","artist"])]),
 ("Noe kommer mot dere i mørket.", [
   ("Jeg stiller meg foran de andre", ["leiesoldat"]),
   ("Jeg venter til jeg ser åpningen", ["duelist","dusorjeger"]),
   ("Jeg sender noe annet først", ["hundetrener","konstruktor"]),
   ("Jeg vet allerede hva det er, og hva det tåler", ["akademiker","okkultist"]),
   ("Jeg snakker til det", ["artist"])]),
 ("Hva vil du helst ha med hjem fra en ruin?", [
   ("En bok ingen andre har lest", ["akademiker","okkultist"]),
   ("Dusøren, og ryktet", ["dusorjeger","leiesoldat"]),
   ("En mekanisme ingen forstår ennå", ["konstruktor"]),
   ("En historie folk vil betale for å høre", ["artist","duelist"])]),
 ("Hva gjør deg farlig?", [
   ("Jeg gir meg ikke", ["leiesoldat","hundetrener"]),
   ("Jeg treffer der jeg sikter", ["duelist","dusorjeger"]),
   ("Jeg vet ting andre ikke vet", ["akademiker","okkultist"]),
   ("Folk undervurderer meg", ["artist","konstruktor"])]),
 ("Hvem stoler du på?", [
   ("Hunden", ["hundetrener"]),
   ("Det jeg har bygget selv", ["konstruktor"]),
   ("Den som betaler", ["leiesoldat","dusorjeger"]),
   ("Det som står skrevet", ["akademiker","okkultist"]),
   ("Ingen, men jeg later som", ["artist","duelist"])]),
 ("Det er noe bak sløret. Hva kjenner du?", [
   ("Nysgjerrighet", ["akademiker","konstruktor"]),
   ("Sult", ["okkultist"]),
   ("Ingenting, det er en jobb", ["leiesoldat","dusorjeger"]),
   ("At noen må hente de andre trygt hjem", ["hundetrener","artist","duelist"])]),
]
ABOUT = [
 ("exp","Hvor mye har du spilt rollespill?", [
   ("aldri","Aldri, men jeg er nysgjerrig"),("noen","Noen ganger"),("fast","Jeg har en fast gruppe"),("gm","Jeg er spilleder")]),
 ("sys","Hva har du spilt mest av?", [
   ("dnd","D&D eller Pathfinder"),("coc","Call of Cthulhu eller annen skrekk"),("osr","OSR, Mörk Borg og lignende"),
   ("iron","Ironsworn eller solo"),("norsk","Norske rollespill"),("ingen","Ingen av disse")]),
 ("vil","Hva vil du ha mest ut av en spillkveld?", [
   ("spenning","Spenning og fare"),("mysterier","Mysterier å løse"),("samtaler","Rollespill og samtaler"),("taktikk","Taktikk og terninger")]),
]
FIT = {
 "exp": {"aldri":"Har du aldri spilt? Da er Kirkegården stedet å begynne. Tre rom, og hvert kast forklarer seg selv.",
         "noen":"Spiller du av og til? De Dødes Bok har én regel for alt: fem terninger, tell de tre i midten.",
         "fast":"Har du en fast gruppe? De Dødes Bok er laget for kampanjer som varer, med 36 kapitler å jakte på.",
         "gm":"Er du spilleder? Én stige for alt betyr ingen egne tabeller for hver ferdighet, og mer tid til historien."},
 "sys": {"dnd":"Fra D&D kjenner du klassene. Her heter de profesjoner, og du vokser av det du utforsker og finner, ikke bare det du beseirer.",
         "coc":"Fra Call of Cthulhu kjenner du sinnet som slites. Her har Søkerne en sjanse til å slå tilbake, og magien koster Fatning.",
         "osr":"Fra OSR kjenner du døden bak neste dør. Her heter den Banesår, og du kan tåle to før den tredje.",
         "iron":"Fra Ironsworn kjenner du kastet som avgjør alt. Her er det fem terninger og én stige for alt du gjør.",
         "norsk":"Liker du norske rollespill? De Dødes Bok er skrevet på norsk, med gotisk skrekk, folketro og eldgamle myter.",
         "ingen":""},
 "vil": {"spenning":"Vil du ha spenning? Med hver 1'er som teller, handler verden mot deg.",
         "mysterier":"Vil du ha mysterier? 36 kapitler ligger spredt over Unara, og hvert av dem er en gåte.",
         "samtaler":"Vil du ha rollespill? Søkerne er vanlige folk, med nasjoner, minner og noe de har mistet.",
         "taktikk":"Vil du ha taktikk? Presse eller Avvente, Legeme eller Fatning. Hver runde er et valg."},
}

def esc(s): return (s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;"))

qhtml=""
for i,(q,opts) in enumerate(Q):
    qhtml+=f'<div class="qcard" data-q="{i}"><div class="qn">{i+1} av {len(Q)}</div><h3>{esc(q)}</h3><div class="opts">'
    for t,ps in opts: qhtml+=f'<button class="opt" data-p="{",".join(ps)}">{esc(t)}</button>'
    qhtml+='</div></div>\n'
ahtml=""
for k,q,opts in ABOUT:
    ahtml+=f'<div class="qcard about" data-a="{k}"><div class="qn">Om deg</div><h3>{esc(q)}</h3><div class="opts">'
    for v,t in opts: ahtml+=f'<button class="opt" data-v="{v}">{esc(t)}</button>'
    ahtml+='</div></div>\n'

page=f'''<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hvilken Søker er du? | De Dødes Bok</title>
<meta name="description" content="Sju spørsmål om hvordan du møter det ukjente. Én av åtte Søkere fra De Dødes Bok, Henrik Grimsheis norske fantasyrollespill.">
<link rel="canonical" href="https://www.kr1publishing.com/ddb/soker">
<meta property="og:type" content="website">
<meta property="og:site_name" content="KR1 Publishing">
<meta property="og:title" content="Hvilken Søker er du? De Dødes Bok">
<meta property="og:description" content="Sju spørsmål om hvordan du møter det ukjente. Én av åtte Søkere.">
<meta property="og:image" content="https://www.kr1publishing.com/img/ddb/og-soker.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="https://www.kr1publishing.com/ddb/soker">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://www.kr1publishing.com/img/ddb/og-soker.jpg">
<meta name="theme-color" content="#0d0c0b">
<link rel="icon" href="/img/ddb/kr1-hex.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=IM+Fell+English+SC&display=swap">
<style>
  /* HVILKEN SØKER ER DU (okt 2026). Bygges av tools/build_ddb_soker.py. Skjemaet poster til Mailchimp med TRACK=ddb-soker-... */
  :root{{--gold:#e8c96f;--gold-dark:#b8863b;--blood:#a8201a;--blood-soft:#d8453b;--bone:#e9e2d2;--night:#0d0c0b;--dark:#191713;--card:#1b1814;--line:#2e2922;--muted:#8f8878}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{font-family:'EB Garamond',Georgia,serif;color:var(--bone);background:var(--night);line-height:1.55;font-size:19px;-webkit-font-smoothing:antialiased}}
  a{{color:var(--gold)}}
  .in{{max-width:860px;margin:0 auto;padding:0 20px}}
  nav{{background:var(--dark);border-bottom:1px solid var(--line)}}
  nav .in{{display:flex;align-items:center;justify-content:space-between;height:58px;gap:12px;max-width:1120px}}
  nav .logo{{font-family:system-ui,sans-serif;font-weight:700;letter-spacing:2px;font-size:14px;color:var(--gold);text-decoration:none;display:inline-flex;align-items:center;gap:10px;white-space:nowrap}}
  nav .logo img{{height:30px;width:auto}}
  nav .back{{font-family:system-ui,sans-serif;font-size:14px;color:#b9ab95;text-decoration:none;white-space:nowrap}}
  nav .back:hover{{color:var(--gold)}}
  .hero{{text-align:center;padding:46px 0 18px;background:radial-gradient(ellipse at 50% 0%,rgba(168,32,26,.28),transparent 60%)}}
  .kicker{{font-family:system-ui,sans-serif;font-size:12.5px;letter-spacing:2.4px;text-transform:uppercase;color:var(--gold);font-weight:700}}
  h1{{font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:clamp(38px,6vw,56px);line-height:1.05;color:#fff;margin:10px 0 12px;letter-spacing:.02em}}
  h1 em{{font-style:normal;color:var(--blood-soft)}}
  .lead{{font-size:20px;color:#d5cdbd;max-width:600px;margin:0 auto}}
  .strip{{display:flex;justify-content:center;gap:6px;margin:26px auto 0;max-width:640px}}
  .strip img{{width:12%;aspect-ratio:346/800;object-fit:cover;border-radius:6px;opacity:.85;filter:drop-shadow(0 10px 14px rgba(0,0,0,.6))}}
  .qcard{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px 20px 18px;margin-top:14px}}
  .qcard.about{{border-style:dashed}}
  .qn{{font-family:system-ui,sans-serif;font-size:11.5px;letter-spacing:1.6px;text-transform:uppercase;color:var(--muted);font-weight:700}}
  .qcard h3{{font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:24px;color:#fff;margin:4px 0 12px;line-height:1.2}}
  .opts{{display:grid;gap:8px}}
  .opt{{all:unset;cursor:pointer;display:block;padding:11px 16px;border-radius:10px;border:1.5px solid #3d352c;color:#d5cdbd;font-size:17.5px;line-height:1.35;transition:border-color .12s,background .12s}}
  .opt:hover{{border-color:var(--gold-dark)}}
  .opt.on{{background:var(--bone);color:#1a1612;border-color:var(--bone)}}
  .sep{{text-align:center;margin:30px 0 4px}}
  .sep p{{color:var(--muted);font-size:16px}}
  .go{{text-align:center;margin:26px 0 60px}}
  .btn{{display:inline-block;background:var(--gold);color:#1a1612;text-decoration:none;font-family:system-ui,sans-serif;font-size:16px;font-weight:700;padding:16px 36px;border-radius:32px;border:0;cursor:pointer}}
  .btn.blood{{background:var(--blood);color:#fff}}
  .btn.ghost{{background:transparent;border:1.5px solid #4a4038;color:var(--bone);font-weight:600}}
  .btn:disabled{{opacity:.35;cursor:default}}
  .count{{font-family:system-ui,sans-serif;font-size:13px;color:var(--muted);margin-top:10px}}
  .hidden{{display:none}}
  .res{{display:grid;grid-template-columns:240px minmax(0,1fr);gap:28px;align-items:start;margin-top:22px}}
  .res img{{width:100%;aspect-ratio:346/800;object-fit:cover;border-radius:12px;filter:drop-shadow(0 20px 30px rgba(0,0,0,.7))}}
  .res .lag{{font-family:system-ui,sans-serif;font-size:12px;letter-spacing:1.6px;text-transform:uppercase;font-weight:700}}
  .res h2{{font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:46px;color:#fff;line-height:1;margin:6px 0 4px}}
  .res .tag{{font-style:italic;font-size:22px;color:var(--gold)}}
  .res p{{margin-top:12px;color:#d5cdbd}}
  .res .lf{{font-family:system-ui,sans-serif;font-size:13px;color:var(--muted);margin-top:12px;letter-spacing:.5px}}
  .fit{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--blood);border-radius:10px;padding:16px 18px;margin-top:26px}}
  .fit .kicker{{margin-bottom:6px}}
  .fit p{{margin-top:6px;color:#d5cdbd}}
  .cta{{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}}
  .mail{{margin-top:26px;padding-top:20px;border-top:1px solid var(--line)}}
  .mail p{{font-size:16px;color:var(--muted)}}
  .mail form{{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}}
  .mail input[type=email]{{flex:1;min-width:200px;padding:14px 16px;border-radius:30px;border:1px solid #4a4038;background:#120f0d;color:#fff;font-size:16px;font-family:system-ui,sans-serif}}
  .again{{text-align:center;margin:30px 0 60px;font-family:system-ui,sans-serif;font-size:14px}}
  @media(max-width:640px){{.res{{grid-template-columns:1fr}}.res img{{max-width:200px;margin:0 auto;display:block}}.res{{text-align:center}}.cta{{justify-content:center}}.strip img{{width:11%}}}}
  .opt,.lead,.res p,.fit p{{text-wrap:pretty}}
</style>
</head>
<body>
<nav><div class="in"><a class="logo" href="/"><img src="/img/kr1-hex.png" alt="" width="80" height="90">KR1 PUBLISHING</a><a class="back" href="/ddb">&larr; Tilbake til De Dødes Bok</a></div></nav>
<div id="quizbox">
<div class="hero"><div class="in">
  <div class="kicker">De Dødes Bok</div>
  <h1>Hvilken <em>Søker</em> er du?</h1>
  <p class="lead">Sju spørsmål om hvordan du møter det ukjente. Svaret er én av åtte profesjoner fra boka.</p>
  <div class="strip">{"".join(f'<img src="/img/ddb/fig-{k}.jpg" alt="">' for k in P)}</div>
</div></div>
<div class="in">
{qhtml}
<div class="sep"><div class="kicker">Tre til, om deg</div><p>Disse teller ikke på svaret, men de hjelper oss å lage et bedre spill.</p></div>
{ahtml}
<div class="go"><button class="btn blood" id="go" disabled>Vis meg Søkeren min</button><div class="count" id="count">0 av {len(Q)} besvart</div></div>
</div>
</div>
<div class="in hidden" id="resbox"></div>
<script>
const P={json.dumps(P,ensure_ascii=False)};
const LAGC={json.dumps(LAGC)};
const FIT={json.dumps(FIT,ensure_ascii=False)};
const ORDER={json.dumps(list(P.keys()))};
const NQ={len(Q)}; const ans={{}}, about={{}};
const W={{}}; ORDER.forEach(k=>W[k]=0); document.querySelectorAll('.qcard[data-q]').forEach(c=>{{ const os=[...c.querySelectorAll('.opt')]; os.forEach(o=>{{ const ps=o.dataset.p.split(','); ps.forEach(k=>W[k]+=1/ps.length/os.length); }}); }});
document.querySelectorAll('.qcard').forEach(c=>c.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{{
  c.querySelectorAll('.opt').forEach(x=>x.classList.remove('on')); b.classList.add('on');
  if(c.dataset.q!==undefined) ans[c.dataset.q]=b.dataset.p.split(','); else about[c.dataset.a]=b.dataset.v;
  const n=Object.keys(ans).length; document.getElementById('count').textContent=n+' av '+NQ+' besvart';
  document.getElementById('go').disabled=n<NQ;
  const nx=c.nextElementSibling; if(nx&&nx.classList.contains('qcard')&&!nx.querySelector('.on')) setTimeout(()=>nx.scrollIntoView({{behavior:'smooth',block:'center'}}),180);
}}));
function pick(){{ const s={{}}; ORDER.forEach(k=>s[k]=0);
  Object.values(ans).forEach(ps=>ps.forEach(k=>s[k]+=1/ps.length)); ORDER.forEach(k=>s[k]/=W[k]);
  let best=ORDER[0]; ORDER.forEach(k=>{{ if(s[k]>s[best]+1e-9) best=k; }});
  const tie=ORDER.filter(k=>Math.abs(s[k]-s[best])<1e-9); if(tie.length>1&&ans[2]){{ const t=ans[2].find(k=>tie.includes(k)); if(t) best=t; }}
  return best; }}
function esc(t){{return String(t).replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]))}}
function show(k){{ const p=P[k]; const r=document.getElementById('resbox');
  document.getElementById('quizbox').classList.add('hidden'); r.classList.remove('hidden');
  const fit=[FIT.exp[about.exp],FIT.sys[about.sys],FIT.vil[about.vil]].filter(Boolean);
  const track=['ddb-soker',k,about.exp||'',about.sys||'',about.vil||''].join('-');
  r.innerHTML=`<div class="hero" style="padding-bottom:0"><div class="kicker">Din Søker</div></div>
  <div class="res"><img src="/img/ddb/fig-${{k}}.jpg" alt="${{esc(p.n)}}"><div>
    <div class="lag" style="color:${{LAGC[p.lag]}}">${{esc(p.lag)}}</div><h2>${{esc(p.n)}}</h2><div class="tag">${{esc(p.tag)}}</div>
    <p>${{esc(p.d)}}</p><p>${{esc(p.spill)}}</p><div class="lf">Legeme ${{p.L}} · Fatning ${{p.F}}</div>
    <div class="cta"><a class="btn blood" href="{BK}" target="_blank" rel="noopener">Følg De Dødes Bok</a><button class="btn ghost" id="share">Del resultatet</button></div>
  </div></div>
  ${{fit.length?`<div class="fit"><div class="kicker">Slik passer De Dødes Bok for deg</div>${{fit.map(t=>`<p>${{esc(t)}}</p>`).join('')}}</div>`:''}}
  <div class="fit" style="border-left-color:var(--gold)"><div class="kicker">Prøv kampreglene</div><p>Følgere på BackerKit får koden til Kirkegården, et ferdig scenario i tre rom. Spill det i nettleseren før alle andre.</p><div class="cta"><a class="btn" href="{BK}" target="_blank" rel="noopener">Følg og få koden</a><a class="btn ghost" href="/DDBkirkegarden">Jeg har koden</a></div></div>
  <div class="mail"><p>Vil du heller ha beskjed på e-post når kampanjen starter?</p>
    <form action="{MC}" method="post" target="_blank"><input type="email" name="EMAIL" placeholder="din@epost.no" required><input type="hidden" name="TRACK" value="${{esc(track)}}"><button class="btn ghost" type="submit">Gi meg beskjed</button></form></div>
  <div class="again"><a href="/ddb/soker" id="again">Ta testen på nytt</a> · <a href="/ddb">Om De Dødes Bok</a></div>`;
  document.getElementById('share').onclick=()=>share(k);
  document.getElementById('again').onclick=e=>{{e.preventDefault(); location.href='/ddb/soker';}};
  history.replaceState(null,'','/ddb/soker?r='+k); window.scrollTo({{top:0,behavior:'smooth'}}); }}
function share(k){{ const p=P[k]; const url='https://www.kr1publishing.com/ddb/soker/'+k; const text=`Jeg er ${{p.n}}. ${{p.tag}} Hvilken Søker er du?`;
  if(navigator.share) navigator.share({{title:'Hvilken Søker er du?',text,url}}).catch(()=>{{}});
  else if(navigator.clipboard) navigator.clipboard.writeText(text+' '+url).then(()=>{{const b=document.getElementById('share'); b.textContent='Lenken er kopiert';}}); }}
document.getElementById('go').onclick=()=>show(pick());
const q=new URLSearchParams(location.search).get('r'); if(q&&P[q]) show(q);
</script>
</body>
</html>
'''
os.makedirs('ddb/soker',exist_ok=True)
open('ddb/soker.html','w').write(page)
for k,p in P.items():
    t=f'Jeg er {p["n"]}. Hvilken Søker er du?'
    open(f'ddb/soker/{k}.html','w').write(f'''<!DOCTYPE html><html lang="no"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t)} | De Dødes Bok</title><meta name="robots" content="noindex">
<meta property="og:type" content="website"><meta property="og:site_name" content="KR1 Publishing">
<meta property="og:title" content="{esc(t)}"><meta property="og:description" content="{esc(p["tag"]+" "+p["d"])}">
<meta property="og:image" content="https://www.kr1publishing.com/img/ddb/og-soker-{k}.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="https://www.kr1publishing.com/ddb/soker/{k}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://www.kr1publishing.com/img/ddb/og-soker-{k}.jpg">
<meta http-equiv="refresh" content="0;url=/ddb/soker?r={k}">
<style>body{{background:#0d0c0b;color:#e9e2d2;font-family:Georgia,serif;text-align:center;padding:60px 20px}}a{{color:#e8c96f}}</style></head>
<body><p>{esc(p["n"])}. {esc(p["tag"])}</p><p><a href="/ddb/soker?r={k}">Se Søkeren</a> · <a href="/ddb/soker">Ta testen</a></p>
<script>location.replace('/ddb/soker?r={k}')</script></body></html>''')
json.dump({"P":P,"LAGC":LAGC},open('/tmp/claude-0/sh/soker_data.json','w'),ensure_ascii=False)
print('ok')
