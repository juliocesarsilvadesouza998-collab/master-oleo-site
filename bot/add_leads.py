#!/usr/bin/env python3
"""Add new companies to the prospection queue."""
import json

with open('fila_prospeccao_extra.json') as f:
    data = json.load(f)

existing_emails = set()
for e in data:
    if isinstance(e, dict) and 'email' in e:
        existing_emails.add(e['email'].strip().lower())

new_entries = [
    {
        "nome": "Crista Industria e Comercio LTDA",
        "empresa": "Crista Industria e Comercio LTDA",
        "email": "faleconosco@cristamargarina.com.br",
        "cidade": "Indaiatuba/SP",
        "segmento": "Industria de margarina e gorduras vegetais"
    },
    {
        "nome": "Festpan Alimentos LTDA",
        "empresa": "Festpan Alimentos LTDA",
        "email": "ecommerce@festpan.com.br",
        "cidade": "Maua/SP",
        "segmento": "Comercio de margarinas e produtos de panificacao"
    },
]

added = 0
for entry in new_entries:
    if entry['email'].strip().lower() not in existing_emails:
        data.append(entry)
        existing_emails.add(entry['email'].strip().lower())
        added += 1
        print(f"ADICIONADO: {entry['empresa']} <{entry['email']}> [{entry['segmento']}]")
    else:
        print(f"JA EXISTE: {entry['email']}")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nTotal agora: {len(data)} empresas na fila")
print(f"Adicionados: {added}")