#!/usr/bin/env python3
"""Etter lock_trefningsbordet.py: gjør porten til DDBverksted.html om fra demo-tekst til verkstedtekst."""
import sys
p=sys.argv[1]; s=open(p).read()
s=s.replace('<title>Trefningsbordet · De Dødes Bok</title>','<title>Verkstedet · De Dødes Bok</title>').replace('<h1>Trefningsbordet</h1>','<h1>Verkstedet</h1>')
s=s.replace('<p>Bordet er låst. Koden får du når du følger De Dødes Bok på BackerKit.</p>','<p>Arbeidsbordet til Henrik og Karl Otto. Reglene testes her før de havner i manuset.</p>')
s=s.replace('<p class="small">Har du ikke koden? <a href="https://www.backerkit.com/c/projects/kr1-publishing/de-dodes-bok/pre-launch" target="_blank" rel="noopener">Følg De Dødes Bok på BackerKit</a>, så får du den.</p>','<p class="small">Leter du etter demoen? <a href="/DDBkirkegarden">Kirkegården</a> er der.</p>')
s=s.replace("'ddb-bord-kode'","'ddb-verksted-kode'")
open(p,'w').write(s)
