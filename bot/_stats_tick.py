#!/usr/bin/env python3
"""Quick stats for the leads.csv"""
import csv, os, json
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "leads.csv"), newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    stats = Counter()
    bounce_fontes = Counter()
    bounce_empresas = []
    for row in reader:
        s = row.get("status", "").strip()
        stats[s] += 1
        if s == "bounce":
            bounce_fontes[row.get("fonte", "")] += 1
            bounce_empresas.append(row.get("empresa", "")[:50])

print("=== STATUS DISTRIBUTION ===")
for k, v in stats.most_common():
    print(f"  {k}: {v}")
total = sum(stats.values())
print(f"\nTotal: {total}")
print(f"Ativos (novo+sequencia): {stats.get('novo',0) + stats.get('sequencia',0)}")
print(f"Respondidos: {stats.get('respondido',0)}")
print(f"Bounces: {stats.get('bounce',0)}")
print(f"Encerrados: {stats.get('encerrado',0)}")

# Count bounces.json
bounce_path = os.path.join(BASE, "bounces.json")
if os.path.exists(bounce_path):
    bj = json.load(open(bounce_path, encoding="utf-8"))
    print(f"\nBounces cache (bounces.json): {len(bj)}")

# Count fila
print(f"\n=== FILA ===")
for fn in ["fila_prospeccao_extra.json", "fila_prospeccao_prioritaria.json"]:
    fp = os.path.join(BASE, fn)
    if os.path.exists(fp):
        data = json.load(open(fp, encoding="utf-8"))
        total_f = len(data)
        contatados = sum(1 for e in data if e.get("contatado"))
        bounce = sum(1 for e in data if e.get("bounce"))
        pendentes = total_f - contatados - bounce
        print(f"  {fn}: total={total_f} contatados={contatados} bounce={bounce} pendentes={pendentes}")