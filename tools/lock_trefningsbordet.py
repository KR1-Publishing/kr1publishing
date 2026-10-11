#!/usr/bin/env python3
"""Lås Trefningsbordet bak et passord, uten server.

Bruk:  python3 tools/lock_trefningsbordet.py <kildefil.html> <utfil.html> <passord>

Hele appen krypteres med AES-256-GCM. Nøkkelen avledes fra passordet med
PBKDF2 (SHA-256, 200 000 runder). Utfila er én selvstendig HTML-side med et
passordfelt. Uten passordet er innholdet ubrukelig, også for den som leser
kildekoden. Passordet deles i BackerKit-meldingen til følgere.
"""
import sys, os, base64, json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

src, out, pw = sys.argv[1], sys.argv[2], sys.argv[3]
plain = open(src, 'rb').read()
salt, iv = os.urandom(16), os.urandom(12)
key = PBKDF2HMAC(hashes.SHA256(), 32, salt, 200000).derive(pw.encode('utf-8'))
ct = AESGCM(key).encrypt(iv, plain, None)
b64 = lambda b: base64.b64encode(b).decode()
payload = json.dumps({'salt': b64(salt), 'iv': b64(iv), 'ct': b64(ct)})

page = r'''<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Trefningsbordet · De Dødes Bok</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=IM+Fell+English+SC&display=swap">
<style>
  :root{--night:#0d0c0b;--bone:#e9e2d2;--gold:#e8c96f;--blood:#a8201a;--blood-soft:#d8453b;--ink:#1e1c18}
  *{box-sizing:border-box;margin:0;padding:0}
  body{min-height:100vh;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at 50% 0%,rgba(168,32,26,.28),transparent 55%),var(--night);color:var(--bone);font-family:'EB Garamond',Georgia,serif;font-size:18px;line-height:1.5;padding:24px}
  .gate{max-width:460px;width:100%;text-align:center}
  h1{font-family:'IM Fell English SC',Georgia,serif;font-weight:400;font-size:34px;letter-spacing:.04em;color:#fff;margin-bottom:8px}
  .kicker{font-family:system-ui,sans-serif;font-size:12.5px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);font-weight:700;margin-bottom:14px}
  p{color:#d5cdbd}
  form{display:flex;gap:10px;margin-top:26px}
  input{flex:1;min-width:0;padding:15px 18px;border-radius:32px;border:1px solid #4a4038;background:#120f0d;color:#fff;font-size:16px;font-family:system-ui,sans-serif;letter-spacing:.08em}
  input::placeholder{color:#7d7466;letter-spacing:0}
  button{background:var(--blood);color:#fff;border:0;border-radius:32px;padding:15px 26px;font-family:system-ui,sans-serif;font-weight:700;font-size:16px;cursor:pointer;white-space:nowrap}
  button:hover{background:var(--blood-soft)}
  .err{color:var(--blood-soft);margin-top:14px;min-height:1.5em;font-style:italic}
  .small{font-family:system-ui,sans-serif;font-size:13px;color:#8f8878;margin-top:26px}
  .small a{color:var(--gold)}
  @media(max-width:480px){form{flex-direction:column}}
</style>
</head>
<body>
<div class="gate">
  <div class="kicker">De Dødes Bok</div>
  <h1>Trefningsbordet</h1>
  <p>Bordet er låst. Koden får du når du følger De Dødes Bok på BackerKit.</p>
  <form id="f"><input id="pw" type="password" placeholder="Kode fra BackerKit" autocomplete="off" autofocus><button type="submit">Åpne bordet</button></form>
  <div class="err" id="err"></div>
  <p class="small">Har du ikke koden? <a href="https://www.backerkit.com/c/projects/kr1-publishing/de-dodes-bok/pre-launch" target="_blank" rel="noopener">Følg De Dødes Bok på BackerKit</a>, så får du den.</p>
</div>
<script id="payload" type="application/json">__PAYLOAD__</script>
<script>
const P=JSON.parse(document.getElementById('payload').textContent);
const b=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
async function open(pw){
  const km=await crypto.subtle.importKey('raw',new TextEncoder().encode(pw),'PBKDF2',false,['deriveKey']);
  const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt:b(P.salt),iterations:200000,hash:'SHA-256'},km,{name:'AES-GCM',length:256},false,['decrypt']);
  const plain=await crypto.subtle.decrypt({name:'AES-GCM',iv:b(P.iv)},key,b(P.ct));
  const html=new TextDecoder().decode(plain);
  document.open(); document.write(html); document.close();
}
document.getElementById('f').addEventListener('submit',async e=>{
  e.preventDefault(); const err=document.getElementById('err'); err.textContent='Låser opp ...';
  const pw=document.getElementById('pw').value.trim();
  try{ await open(pw); try{localStorage.setItem('ddb-bord-kode',pw);}catch(_){} }
  catch(_){ err.textContent='Feil kode. Prøv igjen.'; }
});
try{ const s=localStorage.getItem('ddb-bord-kode'); if(s){ open(s).catch(()=>{}); } }catch(_){}
</script>
</body>
</html>
'''
open(out, 'w', encoding='utf-8').write(page.replace('__PAYLOAD__', payload))
print(out, len(ct) // 1024, 'KB kryptert')
