#!/usr/bin/env python3
"""Quick cron stats for Master Oleo."""
import csv, json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
leads_path = os.path.join(BASE, "leads.csv")
eco_path = os.path.join(BASE, "ecossistema.json")

with open(leads_path, newline="", encoding="utf-8-sig") as f:
    leads = list(csv.DictReader(f))

total = len(leads)
ativos = sum(1 for l in leads if l["status"] in ("novo","respondido"))
bounce = sum(1 for l in leads if l["status"] == "bounce")
encerrados = sum(1 for l in leads if l["status"] == "encerrado")
respondidos = sum(1 for l in leads if l["status"] == "respondido")
descartados = sum(1 for l in leads if l["status"] == "descartado")
novo = sum(1 for l in leads if l["status"] == "novo")

print(f"total={total} novo={novo} respondido={respondidos} bounce={bounce} descartado={descartados} encerrado={encerrados} ativos={ativos}")

# Lead quentes com ultima_resposta
for l in leads:
    ur = (l.get("ultima_resposta") or "").strip()
    if ur:
        print(f"  QUENTE: {l.get('empresa','')[:40]} | {l.get('email','')} | {ur[:100]}")