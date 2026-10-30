#!/usr/bin/env python3
"""Validate fila_prioritaria entries with MX and dedup, add to main queue."""
import json, subprocess, re

# Load targets
with open('fila_prioritaria.json') as f:
    targets = json.load(f)

# Known emails (queue + leads + bounces)
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
        r = subprocess.run(['nslookup', '-type=MX', domain], capture_output=True, text=True, timeout=20)
        out = r.stdout + r.stderr
        return 'mail exchanger' in out.lower() or 'MX preference' in out
    except Exception:
        return False

added = 0
for t in targets:
    em = t.get('email', '').strip().lower()
    if not em or '@' not in em:
        print(f"SKIP sem email: {t.get('nome')}")
        continue
    if em in known:
        print(f"SKIP ja conhecido: {t.get('nome')} <{t['email']}>")
        continue
    domain = em.split('@')[1]
    if not has_mx(domain):
        print(f"SKIP sem MX: {t.get('nome')} <{t['email']}> ({domain})")
        continue
    entry = {
        "nome": t.get("nome"),
        "empresa": t.get("empresa"),
        "email": t["email"],
        "cidade": t.get("cidade"),
        "segmento": t.get("segmento"),
    }
    data.append(entry)
    known.add(em)
    added += 1
    print(f"ADICIONADO: {t.get('empresa')} <{t['email']}> [{t.get('segmento')} - {t.get('cidade')}]")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAdicionados da fila_prioritaria: {added}. Total fila: {len(data)}")