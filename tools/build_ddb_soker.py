#!/usr/bin/env python3
"""Bygger /ddb/soker (Hvilken Søker er du?) og delingssidene /ddb/soker/<profesjon>.
Kjør fra repo-rota: python3 tools/build_ddb_soker.py"""
import json, os

BK = "https://www.backerkit.com/c/projects/kr1-publishing/de-dodes-bok/pre-launch"
MC = "https://kr1publishing.us13.list-manage.com/subscribe/post?u=9b8e99b826134f12e16a15a13&amp;id=1eeadea463&amp;f_id=007c7de9f0"

P = {
 "leiesoldat": {"n":"Leiesoldat","lag":"Overflaten","L":8,"F":2,"tag":"Står lengst.",
   "d":"Du er den de andre stiller seg bak når det smeller, og du har for lengst sluttet å spørre hvorfor det alltid er deg. Når noe går galt, er det deg de ser etter.",
   "spill":"I spillet tåler du mest av alle, og du får fordel hver gang du presser på. Det er sinnet ditt som slites først.","pitch":"Som Leiesoldat er du den gruppa lener seg på når det går galt, og i De Dødes Bok går det ofte galt."},
 "duelist": {"n":"Duelist","lag":"Overflaten","L":6,"F":4,"tag":"Står først.",
   "d":"Du ser åpningen før de andre har skjønt at kampen har begynt, og ett presist hugg er som regel nok.",
   "spill":"I spillet gjør du kort prosess med enkeltmål, og du velger selv når du slår. Du er farligst når du venter.","pitch":"Som Duelist får du øyeblikkene der alt står på ett hugg, og det er du som bestemmer når det kommer."},
 "akademiker": {"n":"Akademiker","lag":"Overflaten","L":4,"F":6,"tag":"Vet hva det er.",
   "d":"Du skriver ned alt du ser og hører, og det er notatene dine som holder de andre i live når de står overfor noe ingen har sett før.",
   "spill":"I spillet er det du som vet hva noe tåler og hva det frykter. Du blander miksturer og leser det de andre bare ser.","pitch":"Som Akademiker er det kunnskapen din som holder de andre i live, og i De Dødes Bok er det kunnskap som avgjør hvem som kommer hjem."},
 "dusorjeger": {"n":"Dusørjeger","lag":"Underverdenen","L":6,"F":4,"tag":"Vet hvor det er.",
   "d":"Du finner hvem som helst, så lenge prisen er riktig, og noen ganger betaler folk mer for at du skal glemme hvor de er.",
   "spill":"I spillet merker du byttet, og du vet alltid hvor det er. Med sølv og en bue er du farlig på avstand.","pitch":"Som Dusørjeger er du den som finner sporet når alle andre har gitt opp, og i De Dødes Bok er det alltid noe som må finnes."},
 "hundetrener": {"n":"Hundetrener","lag":"Underverdenen","L":6,"F":4,"tag":"Finner veien.",
   "d":"Hunden din har aldri tatt feil om hvem som kan stoles på, og du har lært deg å lytte når den knurrer.",
   "spill":"I spillet er dere to. Hunden biter, sporer og hjelper de andre, og den merker det som ikke er levende.","pitch":"Som Hundetrener har du alltid en venn ved siden av deg, og i De Dødes Bok er det ofte hunden som merker faren før noen av dere."},
 "artist": {"n":"Artist","lag":"Eterisk","L":4,"F":6,"tag":"Får folk til å snakke.",
   "d":"Du har en maske for hver dør, og du vet hvilke ord som får folk til å si mer enn de burde. Noen av maskene er ikke laget for mennesker.",
   "spill":"I spillet åpner du dører med ord, og masken din får selv de døde til å nøle.","pitch":"Som Artist løser du med ord det andre må løse med våpen, og i De Dødes Bok kan en god samtale redde flere liv enn et sverd."},
 "okkultist": {"n":"Okkultist","lag":"Kosmisk","L":3,"F":7,"tag":"Leser det ingen tør.",
   "d":"Du vet at et tegn bare er en dør, og at det farlige er det som venter på den andre siden. Likevel åpner du den, fordi noen må.",
   "spill":"I spillet bærer du agimater som brenner gjennom både rustning og sølv, men hver agimat du bryter, koster deg noe.","pitch":"Som Okkultist bruker du kreftene alle andre er redde for, og i De Dødes Bok har hver av dem en pris du selv må betale."},
 "konstruktor": {"n":"Konstruktør","lag":"Kosmisk","L":4,"F":6,"tag":"Bygger det som trengs.",
   "d":"Du har alltid en liten figur i lomma, og den våkner når du trenger den. Den lever ikke, men den gjør jobben bedre enn de fleste.",
   "spill":"I spillet gir du gruppa en ekstra kropp. Du lager dukkene selv, og de kan brukes til kamp, vakt eller verre ting.","pitch":"Som Konstruktør har du alltid noe du har bygget selv, og i De Dødes Bok er det ofte det som får gruppa gjennom."},
}
LAGC = {"Overflaten":"#b08a3e","Underverdenen":"#6e8c5a","Eterisk":"#7d8fb3","Kosmisk":"#9b6cb0"}

Q = [
 ("Natten før ekspedisjonen. Hva gjør du?", [
   ("Sliper våpenet og legger meg tidlig", ["leiesoldat","duelist"]),
   ("Leser alt som finnes om stedet", ["akademiker","okkultist"]),
   ("Går ut og hører hva folk i landsbyen sier", ["artist","dusorjeger"]),
   ("Gjør klart utstyret, og vier ekstra oppmerksomhet til følgesvennen din", ["hundetrener","konstruktor"])]),
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
 "exp": {"aldri":["Du trenger ikke ha spilt rollespill før. Du kaster fem terninger og teller de tre i midten, og resten lærer du ved bordet sammen med de andre.",
                  "Du trenger ingen forkunnskaper for å begynne. Én regel styrer alt, og allerede første kveld vet du hvordan den virker."],
         "noen":["Når du spiller av og til, er det godt å slippe å lese seg opp hver gang. Én regel gjelder alt, så dere kan sette dere ned og begynne med en gang.",
                 "Reglene sitter etter det første kastet, også når det har gått en måned siden forrige spillkveld."],
         "fast":["Med en fast gruppe har dere nok å gjøre lenge. Trettiseks tapte kapitler ligger gjemt rundt om i Unara, og hvert kapittel dere finner, endrer hva Søkerne kan gjøre.",
                 "Med en fast gruppe får dere se Søkerne vokse av det de finner. Etter et halvt år ved bordet er de ikke de samme som gikk inn porten første gang."],
         "gm":["Som spilleder slipper du å bla i tabeller. Én stige gjelder alt fra sverdhugg til samtaler, og du får mer tid til det som skjer ved bordet.",
               "Som spilleder får du fiender som er enkle å styre, og terningene sier fra når verden slår tilbake. Du bestemmer bare hvordan."]},
 "sys": {"dnd":["Du som kommer fra D&D, kjenner gleden av å bli sterkere. Her vokser Søkerne av det de finner og forstår, i tillegg til det de overlever.",
                "Du som kommer fra D&D, kjenner kampene og eventyrene. Her er døden nærmere, og derfor kjennes hver seier større."],
         "coc":["Du som liker Call of Cthulhu, kjenner redselen for det ukjente. Forskjellen er at Søkerne kan slå tilbake, men all magi har en pris.",
                "Du som liker skrekk, får mer enn blod. Fatningen er det som holder deg hel, og den går fortere enn du tror."],
         "osr":["Du som kommer fra OSR, vet at døden kan vente bak neste dør. Her kalles den Banesår. Du tåler to, og det tredje tar deg.",
                "Du som kommer fra OSR, får et spill som er farlig med vilje. Hvert Banesår blir værende, og du kjenner det på hvert kast etterpå."],
         "iron":["Du som kommer fra Ironsworn, kjenner kastet som avgjør alt. Her kaster du fem terninger, og med ett blikk ser du hvordan det gikk.",
                 "Du som liker små grupper, får regler som er så enkle at to spillere holder, og kastet driver historien videre."],
         "norsk":["Du som liker norske rollespill, får et spill skrevet på norsk fra første side, med folketro, skrekk og gamle myter du kjenner igjen.",
                  "Du som vil spille på norsk, får et spill der ingenting er oversatt. Mare, gjenganger og vardøger hører hjemme her, og det merkes."],
         "ingen":["Du trenger ikke kjenne andre spill. Alt står i boken, og terningene forklarer resten.",
                  "Siden du ikke har spilt noe av dette, har du heller ingenting å lære om igjen. Du starter blankt, akkurat som Søkerne."]},
 "vil": {"spenning":["Vil du ha spenning, får du det på hvert kast. Hver 1'er som teller, gir verden et trekk mot deg, og hele bordet holder pusten.",
                     "Vil du kjenne at det står om noe, er dette spillet for deg. Ett dårlig kast kan koste dyrt, og ett godt kast kan snu hele kvelden."],
         "mysterier":["Liker du gåter, har du trettiseks av dem foran deg. Hvert kapittel er gjemt et sted, og ingen av dem ligger der du venter.",
                      "Vil du vite hva som egentlig skjedde, finner du en historie bak hver grav og hver lukket dør, og den vil helst ikke bli funnet."],
         "samtaler":["Liker du rollespill og samtaler, får du spille et vanlig menneske med et hjemland, minner og noe du har mistet.",
                     "Liker du å snakke deg ut av problemer, kan ord vinne der våpen taper, og selv de døde har noe å si."],
         "taktikk":["Liker du å tenke ut neste trekk, får du et valg hver runde. Skal du angripe først eller vente, og skal du ta skaden på kroppen eller på sinnet?",
                    "Liker du å legge planer, bestemmer dere sammen hvem som går først, hvem som venter og hvem som hjelper, og gode valg merkes på terningene."]},
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
  a.btn[href*="backerkit.com"]{{background:#FFD200!important;color:#111!important;border:2px solid #FFD200!important}}
  a.btn[href*="backerkit.com"]:hover{{background:#FFE14D!important;border-color:#FFE14D!important}}
  @media(max-width:420px){{nav .back .bl{{display:none}}}}
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
  .sharebox{{margin:16px 0 6px;display:flex;flex-direction:column;gap:6px;align-items:flex-start}}.sharebox .sharenote{{font-size:13.5px;color:var(--mut,#a99f8e)}}
  @media(max-width:640px){{.sharebox{{align-items:center}}}}
  .res p{{margin-top:12px;color:#d5cdbd}}
  .res .lf{{font-family:system-ui,sans-serif;font-size:13px;color:var(--muted);margin-top:12px;letter-spacing:.5px}}
  .fit{{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--blood);border-radius:10px;padding:16px 18px;margin-top:26px}}
  .fit.top{{margin-top:26px;border-left-color:var(--gold)}}
  .fit .pitch{{font-size:21px;line-height:1.4;color:var(--bone,#ece3d3);margin:6px 0 14px}}
  .fit .tryk{{margin-top:14px;padding-top:12px;border-top:1px solid var(--line)}}
  .fit.top .cta{{margin-top:14px;justify-content:flex-start}}
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
<nav><div class="in"><a class="logo" href="/"><img src="/img/kr1-hex.png" alt="" width="80" height="90">KR1 PUBLISHING</a><a class="back" href="/ddb">&larr; <span class="bl">Tilbake til </span>De Dødes Bok</a></div></nav>
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
  const bi=Math.max(0,ORDER.indexOf(k)); const sh={{exp:0,sys:1,vil:2}}; const pk=(g,v)=>{{const L=FIT[g][v]; return L?L[((bi>>sh[g])&1)%L.length]:'';}}; const fit=[pk('exp',about.exp),pk('sys',about.sys),pk('vil',about.vil)].filter(Boolean);
  const track=['ddb-soker',k,about.exp||'',about.sys||'',about.vil||''].join('-');
  r.innerHTML=`<div class="fit top"><div class="kicker">Derfor passer De Dødes Bok for deg</div><p class="pitch">${{esc(p.pitch)}}</p>${{fit.map(t=>`<p>${{esc(t)}}</p>`).join('')}}
    <p class="tryk"><b>Klar til å prøve?</b> I Kirkegården spiller du kampreglene fra boken, tre rom rett i nettleseren. Følg De Dødes Bok på BackerKit, så får du koden og kan gå inn porten i kveld.</p>
    <div class="cta"><a class="btn blood" href="{BK}" target="_blank" rel="noopener">Følg og få koden</a><a class="btn ghost" href="/DDBkirkegarden">Jeg har koden</a></div></div>
  <div class="hero" style="padding-bottom:0"><div class="kicker">Din Søker</div></div>
  <div class="res"><img src="/img/ddb/fig-${{k}}.jpg" alt="${{esc(p.n)}}"><div>
    <h2>${{esc(p.n)}}</h2><div class="tag">${{esc(p.tag)}}</div>
    <div class="sharebox"><button class="btn blood" id="copyres">Del svaret ditt</button><span class="sharenote" id="sharenote">Kopierer en kort tekst og lenke du kan lime inn hvor du vil.</span></div>
    <p>${{esc(p.d)}}</p><p>${{esc(p.spill)}}</p><div class="lf">Legeme ${{p.L}} · Fatning ${{p.F}}</div>
    <div class="cta"><a class="btn blood" href="{BK}" target="_blank" rel="noopener">Følg De Dødes Bok</a><button class="btn ghost" id="share">Del via telefonen</button></div>
  </div></div>
  <div class="mail"><p>Vil du heller ha beskjed på e-post når kampanjen starter?</p>
    <form action="{MC}" method="post" target="_blank"><input type="email" name="EMAIL" placeholder="din@epost.no" required><input type="hidden" name="TRACK" value="${{esc(track)}}"><button class="btn ghost" type="submit">Gi meg beskjed</button></form></div>
  <div class="again"><a href="/ddb/soker" id="again">Ta testen på nytt</a> · <a href="/ddb">Om De Dødes Bok</a></div>`;
  document.getElementById('share').onclick=()=>share(k); document.getElementById('copyres').onclick=()=>copyRes(k); if(!navigator.share) document.getElementById('share').style.display='none';
  document.getElementById('again').onclick=e=>{{e.preventDefault(); location.href='/ddb/soker';}};
  history.replaceState(null,'','/ddb/soker?r='+k); window.scrollTo({{top:0,behavior:'smooth'}}); }}
function shareText(k){{ const p=P[k]; return `Jeg ble ${{p.n}} i De Dødes Bok! ${{p.tag}} Hvilken Søker er du? https://www.kr1publishing.com/ddb/soker/${{k}}`; }}
function copyRes(k){{ const t=shareText(k); const done=()=>{{const b=document.getElementById('copyres'); b.textContent='Kopiert!'; document.getElementById('sharenote').textContent='Lim inn i Messenger, Discord, SMS eller hvor du vil.'; setTimeout(()=>b.textContent='Del svaret ditt',2500);}};
  if(navigator.clipboard&&window.isSecureContext) navigator.clipboard.writeText(t).then(done).catch(()=>fallbackCopy(t,done)); else fallbackCopy(t,done); }}
function fallbackCopy(t,done){{ const a=document.createElement('textarea'); a.value=t; a.style.position='fixed'; a.style.opacity='0'; document.body.appendChild(a); a.select(); try{{document.execCommand('copy'); done();}}catch(e){{ prompt('Kopier teksten:',t); }} a.remove(); }}
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
