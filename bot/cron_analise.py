#!/usr/bin/env python3
"""Script de análise para o analista de qualidade (cron job)."""
import csv
from collections import Counter

c = Counter()
bounce_com_boas_vindas = []

with open('leads.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        status = row['status']
        c[status] += 1
        if status == 'bounce' and row.get('boas_vindas_em', '').strip():
            bounce_com_boas_vindas.append((row.get('id',''), row.get('email',''), row.get('boas_vindas_em','')))

print('=== LEADS POR STATUS ===')
for s, n in sorted(c.items()):
    print(f'  {s}: {n}')
print(f'  TOTAL: {sum(c.values())}')

if bounce_com_boas_vindas:
    print('\n=== BOUNCE COM BOAS_VINDAS_EM PREENCHIDO ===')
    for item in bounce_com_boas_vindas:
        print(f'  ID {item[0]} - {item[1]} - boas_vindas_em={item[2]}')
else:
    print('\nNenhum bounce com boas_vindas_em preenchido.')

# Verificar sync: emails em bounces.json que não estão como bounce no csv
import json
with open('bounces.json') as f:
    bounces_cache = json.load(f)

bounce_emails = set(bounces_cache.keys()) if isinstance(bounces_cache, dict) else set(bounces_cache)

csv_bounce = set()
csv_todos = {}
with open('leads.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        csv_todos[row.get('id','')] = row
        if row['status'] == 'bounce':
            csv_bounce.add(row['email'])

nao_marcados = bounce_emails - csv_bounce
if nao_marcados:
    print(f'\nEmails em bounces.json NÃO marcados como bounce no CSV ({len(nao_marcados)}):')
    for e in sorted(nao_marcados):
        print(f'  {e}')
else:
    print('\nTodos os bounces.json estão corretamente marcados como bounce no CSV.')

# Verificar bounces.json que sumiram do csv
csv_emails = set(r['email'] for r in csv_todos.values())
bounce_fora_csv = bounce_emails - csv_emails
if bounce_fora_csv:
    print(f'\nEmails em bounces.json que não existem mais no CSV ({len(bounce_fora_csv)}):')
    for e in sorted(bounce_fora_csv):
        print(f'  {e}')
