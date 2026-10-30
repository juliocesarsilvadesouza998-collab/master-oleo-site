#!/usr/bin/env python3
"""Merge valid corrections (correcoes_validas.json) into the queue with MX+dedup."""
import json, subprocess

# Load corrected emails
with open('correcoes_validas.json') as f:
    corr = json.load(f)

with open('fila_prospeccao_extra.json') as f:
    data = json.load(f)

known = set()
for e in data:
    if isinstance(e, dict) and 'email' in e:
        known.add(e['email'].strip().lower())

try:
    with open('bounces.json') as f:
        b = json.load(f)
    for x in b:
        if isinstance(x, dict) and 'email' in x:
            known.add(x['email'].strip().lower())
        elif isinstance(x, str):
            known.add(x.strip().lower())
except Exception:
    pass

with open('leads.csv', encoding='utf-8', errors='ignore') as f:
    for line in f:
        parts = line.strip().split(',')
        if len(parts) > 3 and '@' in parts[3]:
            known.add(parts[3].strip().lower())

def has_mx(domain):
    try:
        r = subprocess.run(['nslookup', '-type=MX', domain],
                           capture_output=True, text=True, timeout=20)
        out = (r.stdout + r.stderr).lower()
        return 'mail exchanger' in out
    except Exception:
        return False

added = 0
for empresa, em in corr.items():
    em = em.strip()
    if not em or '@' not in em:
        continue
    if em.lower() in known:
        print(f"SKIP ja conhecido: {empresa} <{em}>")
        continue
    domain = em.split('@')[1]
    if not has_mx(domain):
        print(f"SKIP sem MX: {empresa} <{em}> ({domain})")
        continue
    entry = {
        "nome": empresa,
        "empresa": empresa,
        "email": em,
        "cidade": "SP",
        "segmento": "Alimentos",
    }
    data.append(entry)
    known.add(em.lower())
    added += 1
    print(f"ADICIONADO: {empresa} <{em}>")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAdicionados: {added}. Total fila: {len(data)}")