#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspector: imprime estado da fila de prospeccao (base + extra) p/ evitar duplicatas."""
import json, csv, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

from prospecao import EMPRESAS as BASE_EMPRESAS

extra_path = os.path.join(BASE, "fila_prospeccao_extra.json")
extra = json.load(open(extra_path, encoding="utf-8"))

leads_path = os.path.join(BASE, "leads.csv")
contatados = set()
if os.path.exists(leads_path):
    with open(leads_path, newline="", encoding="utf-8") as f:
        contatados = {r.get("email", "").strip().lower() for r in csv.DictReader(f)}

bounces = set()
bounce_path = os.path.join(BASE, "bounces.json")
if os.path.exists(bounce_path):
    bounces = set(json.load(open(bounce_path, encoding="utf-8")))

print(f"Base prospecao.py EMPRESAS: {len(BASE_EMPRESAS)}")
print(f"Fila extra JSON: {len(extra)}")
print(f"leads.csv contatados: {len(contatados)}")
print(f"bounces.json: {len(bounces)}")

# segmentos na fila extra
from collections import Counter
segs = Counter(p.get("segmento", "?") for p in extra)
print("\nSegmentos na fila extra (top 15):")
for s, n in segs.most_common(15):
    print(f"  {n:3d}  {s}")

# dominios da fila extra
doms = Counter(p["email"].split("@")[-1].lower() for p in extra)
print(f"\nDomínios distintos na fila extra: {len(doms)}")

# candidatos ainda pendentes (não contatados, não bounce)
pend = [p for p in (list(BASE_EMPRESAS) + extra)
        if p["email"].strip().lower() not in contatados
        and p["email"].strip().lower() not in bounces]
print(f"\nPendentes (base+extra, sem filtro MX): {len(pend)}")
for p in pend[:10]:
    print(f"  {p['empresa']} <{p['email']}> [{p.get('segmento','')}]")

# todas as empresas conhecidas p/ conferir duplicata futura
print("\nEMPRESAS conhecidas (base+extra): ", len(BASE_EMPRESAS) + len(extra))