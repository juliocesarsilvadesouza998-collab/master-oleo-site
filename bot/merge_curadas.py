#!/usr/bin/env python3
"""Remove auto-scanned noisy entries, then re-add curated high-value list with MX+dedup."""
import json, subprocess

with open('fila_prospeccao_extra.json') as f:
    data = json.load(f)

# 1. Remove all auto-added by scanners (tagged segment)
auto_tag = ('Prospeccao automatica (script)', 'Prospeccao automatica (projeto)')
before = len(data)
data = [e for e in data if e.get('segmento') not in auto_tag]
removed = before - len(data)
print(f"Removidos ruido automatico: {removed}")

# 2. Known set rebuild
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

# 3. Curated high-value list (real-site emails, priority niches)
curadas = [
    # LATICINIOS/GORDURAS (nicho 1)
    {"empresa": "Laticinios Uniao do Brasil", "email": "gerentecomercial@laticiniosuniaodobrasil.com.br",
     "cidade": "SP", "segmento": "Industria de laticinios (manteiga, cremes)"},
    {"empresa": "Schreiber Foods Brasil", "email": "portofeliz@schreiberfoods.com",
     "cidade": "Porto Feliz/SP", "segmento": "Laticinios e queijos (vencidos >40% gordura)"},
    {"empresa": "Lider Alimentos", "email": "marketing.gold@lideralimentos.com.br",
     "cidade": "SP", "segmento": "Industria alimenticia (gorduras)"},
    {"empresa": "Confeitaria Dama", "email": "marketing@confeitariadama.com.br",
     "cidade": "SP", "segmento": "Confeitaria industrial (manteiga, cremes)"},
    {"empresa": "FS Alimentos", "email": "contato@fsalimentos.com.br",
     "cidade": "SP", "segmento": "Industria alimenticia"},
    {"empresa": "Goldy Alimentos", "email": "administrativo@goldy.com.br",
     "cidade": "SP", "segmento": "Alimentos (gordura vegetal)"},
    # FARMACEUTICAS/ENCAPSULADOS (nicho 2)
    {"empresa": "Infinity Pharma", "email": "farmaceutica@infinitypharma.com.br",
     "cidade": "SP", "segmento": "Industria farmaceutica (oleo vegetal limpeza maquinas)"},
    {"empresa": "Veridi Nutrition", "email": "contato@veridinutrition.com.br",
     "cidade": "SP", "segmento": "Nutraceuticos e encapsulados"},
    {"empresa": "Blis Farma", "email": "comercial@blisfarma.com.br",
     "cidade": "SP", "segmento": "Industria farmaceutica"},
    {"empresa": "Farmaviva", "email": "contato@farmaviva.com.br",
     "cidade": "SP", "segmento": "Farmacia e manipulados"},
    {"empresa": "IndCaps", "email": "edilson.silva@indcaps.com.br",
     "cidade": "SP", "segmento": "Fabricante de capsulas oleosas (softgel)"},
    # SUPERMERCADOS/REDES (nicho 4)
    {"empresa": "Grupo Oba Hortifruti", "email": "atendimento@redeoba.com.br",
     "cidade": "SP", "segmento": "Rede de hortifrutis (vencidos de prateleira)"},
    {"empresa": "Savegnago Supermercados", "email": "comercial@savegnago.com.br",
     "cidade": "SP", "segmento": "Supermercados (rede - fritura e vencidos)"},
    {"empresa": "Supermercados Natario", "email": "contato@natario.com.br",
     "cidade": "Jundiai/SP", "segmento": "Supermercados (rede regional)"},
    {"empresa": "Supermercados Extra", "email": "sac@extra.com.br",
     "cidade": "SP", "segmento": "Supermercados (rede nacional)"},
    {"empresa": "Supermercado Confianca", "email": "sac@confianca.com.br",
     "cidade": "SP", "segmento": "Supermercados (fritura continua)"},
    {"empresa": "Supermercados SM Boa", "email": "produtos.novos@smboa.com.br",
     "cidade": "SP", "segmento": "Supermercados (fritura continua)"},
    {"empresa": "Supermercados Frisa", "email": "frisaeco@frisa.com.br",
     "cidade": "SP", "segmento": "Supermercados (fritura e vencidos)"},
    # FRIGORIFICOS (gordura animal com separacao)
    {"empresa": "Frigorifico Verdi", "email": "atendimento@frigorificoverdi.com.br",
     "cidade": "SP", "segmento": "Frigorifico (gordura animal)"},
    {"empresa": "Frigorifico do Sul", "email": "comercial@frigorificodosul.com.br",
     "cidade": "SP", "segmento": "Frigorifico (gordura animal)"},
    {"empresa": "Frigorifico 3R", "email": "contato@frigorifico3r.com.br",
     "cidade": "SP", "segmento": "Frigorifico (gordura animal)"},
    {"empresa": "Maxxi Ovos", "email": "contato@maxxiovos.com.br",
     "cidade": "SP", "segmento": "Granja de ovos (frituras e gorduras)"},
]

def has_mx(domain):
    try:
        r = subprocess.run(['nslookup', '-type=MX', domain],
                           capture_output=True, timeout=20)
        out = (r.stdout + r.stderr).decode('latin-1', 'replace').lower()
        return 'mail exchanger' in out
    except Exception:
        return False

added = 0
for c in curadas:
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
    print(f"ADICIONADO: {c['empresa']} <{em}>")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nCuradas adicionadas: {added}. Total fila: {len(data)}")