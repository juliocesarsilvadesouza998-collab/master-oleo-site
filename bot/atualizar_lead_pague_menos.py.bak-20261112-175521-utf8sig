#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza lead Pague Menos (id 44) apos envio de proposta ao canal comercial."""
import csv, json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "leads.csv")
now = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

rows = list(csv.DictReader(open(path, encoding="utf-8")))
novo_email = "josiane.marinho@supermercadospaguemenos.com.br"
achou = 0
for r in rows:
    if r["id"] == "44":
        r["email"] = novo_email
        r["status"] = "respondido"
        r["respondido_em"] = now
        r["respondido_por"] = "atendente_ia"
        # limpa colunas extra vazias que o DictReader pode ter criado
        for k in list(r.keys()):
            if r[k] is None:
                del r[k]
        achou += 1

with open(path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"leads.csv: {achou} lead id=44 atualizado -> {novo_email} (status respondido)")

# limpa replies_pending.json
rp = os.path.join(BASE, "replies_pending.json")
with open(rp, "w", encoding="utf-8") as f:
    json.dump([], f)
print("replies_pending.json limpo (0 pendentes)")