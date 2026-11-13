#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Corrige email do lead Pague Menos (id 44): josiane@ bloqueado por regra de fluxo -> volta ao canal SAC que funciona."""
import csv, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "leads.csv")

rows = list(csv.DictReader(open(path, encoding="utf-8")))
email_final = "falecom@supermercadospaguemenos.com.br"
achou = 0
for r in rows:
    if r["id"] == "44":
        r["email"] = email_final
        r["status"] = "respondido"
        for k in list(r.keys()):
            if r[k] is None:
                del r[k]
        achou += 1

with open(path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"leads.csv: {achou} lead id=44 email -> {email_final} (SAC funcional; josiane@ bloqueia externos)")