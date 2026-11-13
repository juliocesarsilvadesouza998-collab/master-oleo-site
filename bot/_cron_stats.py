#!/usr/bin/env python3
"""Quick stats for cron tick"""
import csv, os
from collections import Counter

os.chdir(os.path.dirname(__file__) or '.')
with open('leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Total leads: {len(rows)}")
stats = Counter(r.get('status','') for r in rows)
for k in sorted(stats):
    print(f"  {k}: {stats[k]}")

# Hot leads status
hots = ['savegnago','pague menos','rede confianca','covabra','brasfrigo','sonda','tauste','nagumo','sanofi']
for r in rows:
    emp = (r.get('empresa','') + ' ' + r.get('email','')).lower()
    for h in hots:
        if h in emp:
            print(f"HOT|{r.get('status','')}|{r.get('empresa','')}|{r.get('email','')}|resp_em={r.get('respondido_em','')}")
            break