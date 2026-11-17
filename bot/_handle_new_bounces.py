#!/usr/bin/env python3
"""Add new bounces to cache and update leads.csv"""
import csv, json, os

BASE = r'C:\Users\julio\master-oleo-site\bot'

# Load current bounces
with open(os.path.join(BASE,'bounces.json'), encoding='utf-8') as f:
    bounces = set(json.load(f))

# New bounces discovered from mailer-daemon
new_ones = [
    'orcamento@rmartefatosdeconcreto.com.br',
    'sac@extra.com.br',
    'atendimento@frigorificoverdi.com.br',
    'sac@polenghi.com.br',
    'sac@farmoquimica.com.br',
    'cassolsp@cassol.ind.br',
    'premoldados@civil.com.br',
    'protendit@protendit.com.br',
    'saviski@saviski.com.br',
    'proaco@proaco.in.br',
    'relacionamento@padariareal.com.br',
    'sac@restaurantesabordivino.com.br',
]

added = []
for e in new_ones:
    e_clean = e.rstrip('.')
    if e_clean not in bounces:
        bounces.add(e_clean)
        added.append(e_clean)

# Save updated bounces
with open(os.path.join(BASE,'bounces.json'), 'w', encoding='utf-8') as f:
    json.dump(sorted(bounces), f, ensure_ascii=False, indent=2)
print(f"Bounces adicionados ao cache: {len(added)}")

# Update leads.csv - mark these leads as bounce
if added:
    with open(os.path.join(BASE,'leads.csv'), newline='', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
    fields = list(reader[0].keys()) if reader else []
    
    updated = 0
    for row in reader:
        email_field = row.get('email','').strip().lower()
        if email_field in [a.lower() for a in added]:
            old_status = row.get('status','')
            if old_status != 'bounce':
                row['status'] = 'bounce'
                updated += 1
                print(f"  Marcado bounce: {row.get('empresa','?')} <{email_field}> (era {old_status})")
    
    if updated:
        with open(os.path.join(BASE,'leads.csv'), 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(reader)
        print(f"Total leads atualizados: {updated}")
    else:
        print("Nenhum lead correspondente encontrado para marcar como bounce.")
else:
    print("Nenhum bounce novo para adicionar.")