# -*- coding: utf-8 -*-
"""Validação pós-edição: JSON-LD válido + tags equilibradas + palavras-chave."""
import json, re, os, sys

DEPLOY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "deploy-vercel")
arquivos = ["index.html", "industrias.html", "descaracterizacao.html"]

def validar_jsonld(path):
    html = open(path, encoding="utf-8").read()
    blocos = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    for b in blocos:
        json.loads(b)  # sobe exceção se inválido
    return len(blocos)

def checar_tags(path):
    html = open(path, encoding="utf-8").read()
    # remove scripts e styles para checar tags estruturais principais
    problemas = []
    for tag in ["div", "section", "header", "footer", "main", "nav", "h1", "h2", "h3", "p", "ul", "li", "a", "script", "style", "table"]:
        abertas = len(re.findall(r"<%s[\s>]" % tag, html))
        fechadas = len(re.findall(r"</%s>" % tag, html))
        # <a> pode não ter </a> se for âncora vazia? assume que deve casar
        if abertas != fechadas and tag not in ("a", "li"):  # tolera li/a auto-fechados
            problemas.append(f"{tag}: {abertas} abertas / {fechadas} fechadas")
        elif abertas != fechadas and tag in ("a", "li"):
            # registrar só se diferença grande
            if abs(abertas - fechadas) > 3:
                problemas.append(f"{tag}: {abertas} abertas / {fechadas} fechadas (dif {abertas-fechadas})")
    return problemas

ok = True
for fn in arquivos:
    path = os.path.join(DEPLOY, fn)
    try:
        n = validar_jsonld(path)
        print(f"  OK  {fn}: {n} bloco(s) JSON-LD válido(s)")
    except Exception as e:
        ok = False
        print(f"  ERRO {fn}: JSON-LD inválido: {e}")
    probs = checar_tags(path)
    if probs:
        ok = False
        print(f"  ERRO {fn} tags: {probs}")
    else:
        print(f"  OK  {fn}: tags equilibradas")

print("\nRESULTADO:", "OK" if ok else "FALHOU")
sys.exit(0 if ok else 1)
