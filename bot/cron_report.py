#!/usr/bin/env python3
"""Quick lead stats for cron report."""
import csv, json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(BASE, 'leads.csv')
ECO = os.path.join(BASE, '..', 'equipe', 'ecossistema.json')

with open(LEADS, encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

total = len(rows)
status = Counter(r['status'] for r in rows)
respondidos = [r for r in rows if r['status'] == 'respondido']
quentes = []
for r in respondidos:
    vol = r.get('volume','').strip()
    emp = r.get('empresa','').strip()
    email = r.get('email','').strip()
    if emp:
        quentes.append(f'{emp} <{email}> vol={vol}')

print(f'LEADS_TOTAL={total}')
for k,v in sorted(status.items(), key=lambda x:-x[1]):
    print(f'STATUS_{k}={v}')
print(f'QTD_RESPONDIDOS={len(quentes)}')
for q in quentes:
    print(f'RESPONDIDO: {q}')