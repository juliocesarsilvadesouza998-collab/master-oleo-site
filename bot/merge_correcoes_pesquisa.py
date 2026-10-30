#!/usr/bin/env python3
"""Test candidates from correction files against queue/bounces/leads + MX check."""
import json, subprocess, os

candidates = {
    "sac@theoto.com.br": {"empresa": "Theoto S/A Industria e Comercio", "cidade": "Jundiai/SP", "segmento": "Industria alimenticia (sal, oleos e gorduras)"},
    "sac@selmi.com.br": {"empresa": "Pastificio Selmi S/A", "cidade": "Campinas/SP", "segmento": "Industria de massas alimenticias (fritura em volume)"},
    "televendas@selmi.com.br": {"empresa": "Pastificio Selmi S/A", "cidade": "Campinas/SP", "segmento": "Industria de massas alimenticias (fritura em volume)"},
    "contato@rosaves.com.br": {"empresa": "Rosaves Abatedouro de Aves", "cidade": "Sorocaba/SP", "segmento": "Abatedouro de aves (gordura animal)"},
    "avesideal@rosaves.com.br": {"empresa": "Abatedouro de Aves Ideal LTDA (Rosaves)", "cidade": "Sorocaba/SP", "segmento": "Abatedouro de aves (gordura animal)"},
    "faleconosco@beirariosm.com.br": {"empresa": "Supermercado Beira Rio", "cidade": "SP", "segmento": "Supermercado (fritura continua)"},
    "supermercado@infanger.com.br": {"empresa": "Supermercado Infanger", "cidade": "SP", "segmento": "Supermercado (fritura continua)"},
    "paulo@realdist.com.br": {"empresa": "Real Distribuidora", "cidade": "SP", "segmento": "Distribuidora de alimentos"},
    "marketing@ultrapan.com.br": {"empresa": "Ultrapan Industria e Comercio", "cidade": "SP", "segmento": "Industria de panificacao (fritura)"},
    "aquiarcor@arcor.com": {"empresa": "Arcor do Brasil (Bagley)", "cidade": "SP", "segmento": "Industria de balas e biscoitos (fritura)"},
    "sac@vigor.com.br": {"empresa": "Vigor Alimentos", "cidade": "Sao Paulo/SP", "segmento": "Laticinios e manteiga (grande)"},
    "atendimento@cowpig.com.br": {"empresa": "Frigorifico Cowpig", "cidade": "SP", "segmento": "Frigorifico (gordura animal)"},
}

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
for em, info in candidates.items():
    em = em.strip()
    eml = em.lower()
    if eml in known:
        print(f"JA CONHECIDO: {info['empresa']} <{em}>")
        continue
    dom = em.split('@')[1]
    if not has_mx(dom):
        print(f"SEM MX: {info['empresa']} <{em}> ({dom})")
        continue
    entry = {
        "nome": info["empresa"],
        "empresa": info["empresa"],
        "email": em,
        "cidade": info["cidade"],
        "segmento": info["segmento"],
    }
    data.append(entry)
    known.add(eml)
    added += 1
    print(f"ADICIONADO: {info['empresa']} <{em}> [{info['segmento']}]")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nAdicionados: {added}. Total fila: {len(data)}")