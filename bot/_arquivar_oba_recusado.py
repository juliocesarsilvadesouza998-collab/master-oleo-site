#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arquiva leads Oba cujo caso foi RECUSADO pelo sistema SAC (30/10/2026).
Notificacao 'Seu caso foi recusado!' (Salesforce) = auto-resposta SAC -> status encerrado.
Politica: arquivar_sac_auto.py (precedente Mars/Nestle/Vitafor)."""
import csv, datetime, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS_PATH = os.path.join(BASE, "leads.csv")
RP_PATH = os.path.join(BASE, "replies_pending.json")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
          "ultima_resposta","respondido_em","respondido_por"]

ALVO = {"9672890930", "41"}  # Grupo Oba (atendimento@) e Oba Hortifruti SA (ouvidoria@)

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

shutil.copy(LEADS_PATH, LEADS_PATH + ".bak-20261030-oba-recusado")
leads = []
with open(LEADS_PATH, newline="", encoding="utf-8") as f:
    leads = list(csv.DictReader(f))

alterados = 0
for r in leads:
    if r.get("id") in ALVO and r.get("status") != "encerrado":
        r["status"] = "encerrado"
        r["ultima_resposta"] = now_iso()
        r["respondido_em"] = now_iso()
        r["respondido_por"] = "atendente_ia (auto-resposta SAC: caso recusado 30/10)"
        alterados += 1
        print(f"Arquivado lead {r['id']} {r['empresa']} ({r['email']}) -> encerrado (caso recusado SAC)")

with open(LEADS_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in leads:
        w.writerow({k: r.get(k, "") for k in FIELDS})

# limpa pendencias
if os.path.exists(RP_PATH):
    import json
    with open(RP_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("replies_pending.json limpo (0 pendentes)")

print(f"{alterados} lead(s) arquivado(s). Backup: leads.csv.bak-20261030-oba-recusado")