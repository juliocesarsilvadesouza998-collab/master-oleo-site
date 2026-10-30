#!/usr/bin/env python3
"""Merge validated leads from nicho3/nicho4/vencidos files into the queue."""
import json, os

with open('fila_prospeccao_extra.json') as f:
    data = json.load(f)

existing_emails = set()
for e in data:
    if isinstance(e, dict) and 'email' in e:
        existing_emails.add(e['email'].strip().lower())

# Check bounces too
try:
    with open('bounces.json') as f:
        bounces = json.load(f)
    bounce_emails = set()
    if isinstance(bounces, list):
        for b in bounces:
            if isinstance(b, dict) and 'email' in b:
                bounce_emails.add(b['email'].strip().lower())
            elif isinstance(b, str):
                bounce_emails.add(b.strip().lower())
    print(f"Bounces carregados: {len(bounce_emails)}")
except Exception as ex:
    bounce_emails = set()
    print(f"Erro lendo bounces: {ex}")

# Check leads.csv too
lead_emails = set()
try:
    with open('leads.csv', encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) > 3 and '@' in parts[3]:
                lead_emails.add(parts[3].strip().lower())
    print(f"Emails em leads.csv: {len(lead_emails)}")
except Exception as ex:
    print(f"Erro lendo leads.csv: {ex}")

files_to_merge = ['nicho3_validas.json', 'nicho4_validas.json', 'vencidos_validas.json']
added = 0
skipped = 0
for fn in files_to_merge:
    if not os.path.exists(fn):
        continue
    with open(fn) as f:
        entries = json.load(f)
    for entry in entries:
        em = entry.get('email', '').strip().lower()
        if not em or '@' not in em:
            skipped += 1
            continue
        motivo = None
        if em in existing_emails:
            motivo = 'ja na fila'
        elif em in bounce_emails:
            motivo = 'bounce'
        elif em in lead_emails:
            motivo = 'ja contatado (leads.csv)'
        if motivo:
            print(f"SKIP [{motivo}] {entry.get('empresa','?')} <{entry['email']}>")
            skipped += 1
            continue
        data.append(entry)
        existing_emails.add(em)
        added += 1
        print(f"ADICIONADO: {entry.get('empresa','?')} <{entry['email']}> [{entry.get('segmento','')} - {entry.get('cidade','')}]")

with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nResumo: {added} adicionados, {skipped} ignorados. Total fila: {len(data)}")