#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Backfill one-off: adiciona colunas segmento/cidade ao leads.csv
para leads de prospeccao, usando prospecao.EMPRESAS + fila_prospeccao_extra.json.
"""
import csv, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import prospecao as P

EXTRA = json.load(open(os.path.join(BASE, "fila_prospeccao_extra.json"), encoding="utf-8"))

seg_by_email = {}
seg_by_empresa = {}
for e in P.EMPRESAS + EXTRA:
    seg_by_email[e["email"].strip().lower()] = (e.get("segmento", ""), e.get("cidade", ""))
    seg_by_empresa[e["empresa"].strip().lower()] = (e.get("segmento", ""), e.get("cidade", ""))

LEADS = os.path.join(BASE, "leads.csv")
with open(LEADS, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

header = list(rows[0].keys()) if rows else []
if "segmento" not in header:
    header.insert(header.index("volume") + 1 if "volume" in header else len(header), "segmento")
if "cidade" not in header:
    header.insert(header.index("segmento") + 1, "cidade")

preenchidos = 0
sem_info = []
for r in rows:
    if not str(r.get("fonte", "")).startswith("prospeccao"):
        continue
    em = (r.get("email") or "").strip().lower()
    seg, cid = "", ""
    if em in seg_by_email:
        seg, cid = seg_by_email[em]
    else:
        key = (r.get("empresa") or "").strip().lower()
        if key in seg_by_empresa:
            seg, cid = seg_by_empresa[key]
    r["segmento"] = seg
    r["cidade"] = cid
    if seg:
        preenchidos += 1
    else:
        sem_info.append(r.get("empresa", "?"))

with open(LEADS, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=header)
    w.writeheader()
    w.writerows(rows)

print(f"Leads de prospeccao com segmento preenchido: {preenchidos}")
print(f"Sem segmento (usarao fallback 'alimentacao'): {len(sem_info)}")
for s in sem_info:
    print("  -", s)
print("Colunas finais:", header)
