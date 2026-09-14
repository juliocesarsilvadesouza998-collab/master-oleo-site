#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arquiva leads cujo canal SAC respondeu apenas com auto-resposta (Mars/Nestle).
Auto-respostas de SAC corporativo NAO sao resposta comercial -> status encerrado.
"""
import csv, datetime, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
          "ultima_resposta","respondido_em","respondido_por"]

ALVO = {
    "189": "2026-09-14T12:43:44+00:00",   # Mars Brasil (noreply@br.mars.com — "NÃO A RESPONDA")
    "193": "2026-09-14T12:44:32+00:00",   # Nestlé (falecom@nestle.com.br — confirmação genérica)
    "194": "2026-09-14T12:49:47+00:00",   # Vitafor (sac@ — Freshdesk ticket 510438, notificação automática)
}

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

shutil.copy(LEADS_PATH, LEADS_PATH + ".bak-20260914-sac")
leads = []
with open(LEADS_PATH, newline="", encoding="utf-8") as f:
    leads = list(csv.DictReader(f))

alterados = 0
for r in leads:
    if r.get("id") in ALVO and r.get("status") not in ("encerrado",):
        r["status"] = "encerrado"
        r["ultima_resposta"] = ALVO[r["id"]]
        r["respondido_em"] = now_iso()
        r["respondido_por"] = "atendente_ia (auto-resposta SAC)"
        alterados += 1
        print(f"Arquivado lead {r['id']} {r['empresa']} -> encerrado (auto-resposta SAC)")

with open(LEADS_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    for r in leads:
        w.writerow({k: r.get(k, "") for k in FIELDS})

print(f"{alterados} lead(s) arquivado(s). Backup: leads.csv.bak-20260914-sac")
