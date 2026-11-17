#!/usr/bin/env python3
import csv, json, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, 'leads.csv'), newline='', encoding='utf-8-sig') as f:
    reader = list(csv.DictReader(f))
total = len(reader)
status = Counter(r['status'] for r in reader)
respostas = sum(1 for r in reader if r['respondido_em'])
quentes = [r for r in reader if r['status'] == 'respondido' and r['respondido_por'] and r['respondido_por'].strip()]
print(json.dumps({
    'total': total,
    'status': dict(status),
    'respostas': respostas,
    'respondidos_com_interesse': len(quentes),
    'respondidos_por': [{'empresa': r['empresa'], 'email': r['email'], 'respondido_em': r['respondido_em'], 'respondido_por': r['respondido_por'], 'volume': r['volume']} for r in quentes]
}, ensure_ascii=False, indent=2))