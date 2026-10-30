#!/usr/bin/env python3
"""Add high-value candidates from insights.md (spreadsheet of meltdown/food niche) with MX+dedup."""
import json, subprocess

candidates = [
    {"empresa": "FullCaps Encapsulados", "email": "comercial@fullcaps.com.br", "cidade": "SP", "segmento": "Encapsulados e suplementos"},
    {"empresa": "Americpan", "email": "atendimento@ameripan.com.br", "cidade": "SP", "segmento": "Industria de panificacao e massas (fritura)"},
    {"empresa": "AVEC Jundiai", "email": "contato.fornecedor@avecjundiai.com.br", "cidade": "Jundiai/SP", "segmento": "Abatedouro de aves (gordura animal)"},
    {"empresa": "Organ Alimentos", "email": "contato@organalimentos.com.br", "cidade": "SP", "segmento": "Industria alimenticia"},
    {"empresa": "Rocha Distribuidora", "email": "contato@rochadist.com.br", "cidade": "SP", "segmento": "Distribuidora de alimentos (vencidos de prateleira)"},
    {"empresa": "Bauducco", "email": "sac@bauducco.com.br", "cidade": "SP", "segmento": "Industria alimenticia (biscoitos, fritura)"},
    {"empresa": "Assai Atacadista", "email": "sac@assai.com.br", "cidade": "SP", "segmento": "Atacadista (fritura continua, vencidos)"},
    {"empresa": "Atacadao", "email": "sac@atacadao.com.br", "cidade": "SP", "segmento": "Atacadista (fritura continua, vencidos)"},
    {"empresa": "Camil Alimentos", "email": "comercial@camil.com.br", "cidade": "SP", "segmento": "Industria alimenticia (graos, oleos)"},
    {"empresa": "Supermercado Confianca", "email": "social@confianca.com.br", "cidade": "SP", "segmento": "Supermercados (fritura continua)"},
]

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
                           capture_output=True, timeout=20)
        out = (r.stdout + r.stderr).decode('latin-1', 'replace').lower()
        return 'mail exchanger' in out
    except Exception:
        return False

added = 0
for c in candidates:
    em = c['email'].strip()
    eml = em.lower()
    if eml in known:
        print(f"JA CONHECIDO: {c['empresa']} <{em}>")
        continue
    dom = em.split('@')[1]
    if not has_mx(dom):
        print(f"SEM MX: {c['empresa']} <{em}> ({dom})")
        continue
    entry = {"nome": c["empresa"], "empresa": c["empresa"], "email": em,
             "cidade": c["cidade"], "segmento": c["segmento"]}
    data.append(entry)
    known.add(eml)
    added += 1
    print(f"ADICIONADO: {c['empresa']} <{em}> [{c['segmento']}]")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAdicionados: {added}. Total fila: {len(data)}")