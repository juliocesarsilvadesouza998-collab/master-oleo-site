#!/usr/bin/env python3
"""Quick cron stats for Master Oleo."""
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
leads_path = os.path.join(BASE, "leads.csv")

with open(leads_path, newline="", encoding="utf-8-sig") as f:
    leads = list(csv.DictReader(f))

total = len(leads)
novo = sum(1 for l in leads if l["status"] == "novo")
respondido = sum(1 for l in leads if l["status"] == "respondido")
bounce = sum(1 for l in leads if l["status"] == "bounce")
descartado = sum(1 for l in leads if l["status"] == "descartado")
encerrado = sum(1 for l in leads if l["status"] == "encerrado")
ativos = novo + respondido

print(f"total={total} novo={novo} respondido={respondido} bounce={bounce} descartado={descartado} encerrado={encerrado} ativos={ativos}")

for l in leads:
    ur = (l.get("ultima_resposta") or "").strip()
    if ur:
        empresa = l.get('empresa','')[:40]
        email = l.get('email','')
        print(f"  QUENTE: {empresa} | {email} | {ur[:120]}")