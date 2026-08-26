# -*- coding: utf-8 -*-
"""Análise do HTML publicado AO VIVO (o que o Google realmente indexa)."""
import os, re, glob

DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_seo_tmp")
KWS = [
    "coleta de óleo usado salto sp",
    "coleta de óleo de cozinha usado salto",
    "compra de óleo usado",
    "descaracterização de alimentos vencidos",
    "margarina vencida",
    "manteiga vencida",
    "maionese vencida",
    "compra de gordura vegetal usada",
    "óleo usado biodiesel",
    "descarte de óleo de cozinha salto",
]

textos = {}
for fn in glob.glob(os.path.join(DIR, "*.html")):
    nome = os.path.basename(fn)
    with open(fn, encoding="utf-8", errors="replace") as f:
        textos[nome] = f.read()

print("=== PALAVRAS-CHAVE NO SITE PUBLICADO ===")
for kw in KWS:
    locais = [n for n, h in textos.items() if kw.lower() in h.lower()]
    print(f"  {'OK ' if locais else 'X  '} {kw}: {locais or 'AUSENTE'}")

print("\n=== SEO TÉCNICO (publicado) ===")
for nome, html in textos.items():
    probs = []
    if "<title>" not in html or "</title>" not in html: probs.append("sem <title>")
    if 'name="description"' not in html: probs.append("sem meta description")
    if 'rel="canonical"' not in html: probs.append("sem canonical")
    if "application/ld+json" not in html: probs.append("sem JSON-LD")
    # links internos entre as 3 paginas
    for alvo in ["industrias.html", "descaracterizacao.html", "index.html"]:
        if alvo in html: probs.append(f"link->{alvo}")
    print(f"  {nome}: {probs if probs else 'OK'}")

print("\n=== TITLES ===")
for nome, html in textos.items():
    m = re.search(r"<title>([^<]*)</title>", html, re.I)
    print(f"  {nome}: {m.group(1) if m else 'SEM TITLE'}")

print("\n=== META DESCRIPTION ===")
for nome, html in textos.items():
    m = re.search(r'name="description"\s+content="([^"]*)"', html, re.I)
    print(f"  {nome}: {m.group(1)[:120] if m else 'SEM'}")
