#!/usr/bin/env python3
# Conta leads do CSV atual
import csv, os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "leads.csv")

total = 0
status = Counter()
fonte = Counter()
respondidos = []

with open(path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1
        status[row["status"]] += 1
        fonte[row["fonte"]] += 1
        if row["status"] == "respondido":
            respondidos.append(row.get("empresa", "?"))

print(f"Total: {total}")
print(f"Status: bounce={status.get('bounce',0)} novo={status.get('novo',0)} respondido={status.get('respondido',0)} descartado={status.get('descartado',0)} encerrado={status.get('encerrado',0)}")
print(f"Fonte: prospeccao={fonte.get('prospeccao',0)} prospeccao-lote={fonte.get('prospeccao-lote',0)} prospeccao-fritas-2026-09-25={fonte.get('prospeccao-fritas-2026-09-25',0)} prospeccao_desmoldante={fonte.get('prospeccao_desmoldante',0)} desmoldante={fonte.get('desmoldante',0)} formspree={fonte.get('formspree',0)} resposta_email={fonte.get('resposta_email',0)}")
print(f"Respondidos ({len(respondidos)}): {', '.join(respondidos)}")