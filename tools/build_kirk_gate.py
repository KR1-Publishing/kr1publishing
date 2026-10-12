#!/usr/bin/env python3
"""Etter lock_trefningsbordet.py: gjør porten til DDBkirkegarden.html om til Kirkegården."""
import sys
p=sys.argv[1]; s=open(p).read()
s=s.replace('<title>Trefningsbordet · De Dødes Bok</title>','<title>Kirkegården · De Dødes Bok</title>').replace('<h1>Trefningsbordet</h1>','<h1>Kirkegården</h1>')
s=s.replace('<p>Bordet er låst. Koden får du når du følger De Dødes Bok på BackerKit.</p>','<p>Kirkegården er låst. Koden får du når du følger De Dødes Bok på BackerKit.</p>')
s=s.replace('placeholder="Kode fra BackerKit"','placeholder="Kode fra BackerKit"').replace('>Åpne bordet<','>Gå inn porten<')
open(p,'w').write(s)
