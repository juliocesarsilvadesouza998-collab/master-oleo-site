#!/usr/bin/env python3
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, 'leads.csv'), newline='', encoding='utf-8-sig') as f:
    reader = list(csv.DictReader(f))

hot = [r for r in reader if r.get('respondido_em','') or r.get('status','') in ['respondido','quente','negociacao']]
print(f'Total leads: {len(reader)}')
print(f'Respondidos/quentes: {len(hot)}')
for h in sorted(hot, key=lambda x: x.get('respondido_em','') or x.get('ultima_resposta','') or '', reverse=True)[:20]:
    print(f"{h.get('id','?')} | {str(h.get('empresa','?'))[:50]:50s} | {str(h.get('contato',''))[:30]:30s} | status={str(h.get('status','')):15s} | resp={h.get('respondido_em','') or '-'} | ult_resp={str(h.get('ultima_resposta',''))[:25] or '-'}")