#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza lead Supermercados Nagumo (id 289) apos envio de proposta ao canal que abriu o caso 00143542."""
import csv, json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, "leads.csv")
now = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")

rows = list(csv.DictReader(open(path, encoding="utf-8")))
achou = 0
for r in rows:
    if r["id"] == "289":
        r["status"] = "respondido"
        r["respondido_em"] = now
        r["respondido_por"] = "atendente_ia"
        r["ultima_resposta"] = ("SAC Nagumo registrou caso Salesforce 00143542 em 14/10/2026 "
                                "(auto-ack: 'recebemos seu caso'). Proposta de contrato enviada anexada "
                                "para relacionamento@nagumo.com.br (rede regional; 5.000 L/mês est. = R$ 120k/ano). "
                                "Aguardando retorno da equipe Nagumo. Follow-up humano em 3 dias via WhatsApp.")
        # limpa colunas extra vazias que o DictReader pode ter criado
        for k in list(r.keys()):
            if r[k] is None:
                del r[k]
        achou += 1

with open(path, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"leads.csv: {achou} lead id=289 atualizado -> status respondido (caso 00143542, proposta enviada)")

# limpa replies_pending.json
rp = os.path.join(BASE, "replies_pending.json")
with open(rp, "w", encoding="utf-8") as f:
    json.dump([], f)
print("replies_pending.json limpo (0 pendentes)")