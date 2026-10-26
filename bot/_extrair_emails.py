# -*- coding: utf-8 -*-
"""Extrai todos os emails ja existentes na fila + leads.csv para evitar duplicatas."""
import json, csv, re, os

emails = set()

# fila_prospeccao_extra.json
p_fila = os.path.join(os.path.dirname(__file__), 'fila_prospeccao_extra.json')
with open(p_fila, encoding='utf-8') as f:
    data = json.load(f)

def walk(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ('email', 'emails') and isinstance(v, str):
                for e in re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', v.lower()):
                    emails.add(e)
            else:
                walk(v)
    elif isinstance(obj, list):
        for v in obj:
            walk(v)
    elif isinstance(obj, str):
        for e in re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', obj.lower()):
            emails.add(e)

walk(data)

# leads.csv
p_leads = os.path.join(os.path.dirname(__file__), '..', 'leads.csv')
if os.path.exists(p_leads):
    with open(p_leads, encoding='utf-8', errors='replace') as f:
        text = f.read()
    for e in re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text.lower()):
        emails.add(e)

# bounces.json
p_b = os.path.join(os.path.dirname(__file__), 'bounces.json')
if os.path.exists(p_b):
    with open(p_b, encoding='utf-8') as f:
        bdata = json.load(f)
    walk(bdata)

out = os.path.join(os.path.dirname(__file__), 'emails_existentes.txt')
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sorted(emails)))
print('emails unicos existentes:', len(emails))
print('arquivo:', out)