#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Melhorador 14/11/2026 — Adiciona novas empresas à fila_prospeccao_extra.json
com MX validation. Empresas encontradas via pesquisa web: Padaria Real (Sorocaba),
Supermercados Sao Vicente (Nova Odessa/Itu/Indaiatuba), e outras.
"""
import json, os, re, subprocess, sys, csv

BASE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")

novas = [
    {
        "nome": "Padaria Real Conveniencia",
        "empresa": "Padaria Real Conveniencia Ltda",
        "email": "relacionamento@padariareal.com.br",
        "cidade": "Sorocaba/SP",
        "segmento": "Padaria e restaurante (rede 7+ lojas - fritura continua, restaurante, pizzaria - 500+ funcionarios)"
    },
    {
        "nome": "Supermercados Sao Vicente",
        "empresa": "Supermercados Cavicchiolli Ltda",
        "email": "atendimento@svicente.com.br",
        "cidade": "Nova Odessa/SP",
        "segmento": "Supermercados (rede multi-cidades: Itu, Indaiatuba, Campinas, Sorocaba - padaria/rotisserie/acougue)"
    },
    {
        "nome": "Supermercados Sao Vicente Online",
        "empresa": "Supermercados Cavicchiolli Ltda",
        "email": "online@svicente.com.br",
        "cidade": "Nova Odessa/SP",
        "segmento": "Supermercados (rede - canal de vendas online, padaria/rotisserie)"
    },
    {
        "nome": "Tenda Atacado Salto",
        "empresa": "Tenda Atacado SA",
        "email": "sac@tendaatacado.com.br",
        "cidade": "Salto/SP",
        "segmento": "Atacarejo (padaria/rotisserie - alto volume de fritura, loja em Salto/SP)"
    },
]

def tem_mx(dominio):
    try:
        r = subprocess.run(["nslookup", "-type=MX", dominio], capture_output=True, timeout=25)
        out = (r.stdout + r.stderr).decode("latin-1", "replace")
        return bool(re.findall(r"mail exchanger = (\S+)", out, re.I))
    except Exception:
        return False

# --- estado atual ---
fila = json.load(open(FILA, encoding="utf-8"))
leads_emails = set()
if os.path.exists(os.path.join(BASE, "leads.csv")):
    with open(os.path.join(BASE, "leads.csv"), newline="", encoding="utf-8") as f:
        leads_emails = {r.get("email", "").strip().lower() for r in csv.DictReader(f)}
bounces = set()
if os.path.exists(os.path.join(BASE, "bounces.json")):
    bounces = set(json.load(open(os.path.join(BASE, "bounces.json"), encoding="utf-8")))

conhecidos = {e.get("email", "").strip().lower() for e in fila if isinstance(e, dict)}
conhecidos |= leads_emails

print(f"Fila atual: {len(fila)} | Leads: {len(leads_emails)} | Bounces: {len(bounces)}")

adicionadas = 0
for n in novas:
    em = n["email"].strip().lower()
    dom = em.split("@")[-1]
    if em in conhecidos:
        print(f"JA EXISTE: {n['empresa']} <{em}>")
        continue
    if em in bounces:
        print(f"BOUNCE: {n['empresa']} <{em}>")
        continue
    if not tem_mx(dom):
        print(f"SEM MX: {n['empresa']} <{em}> ({dom})")
        continue
    fila.append(n)
    conhecidos.add(em)
    adicionadas += 1
    print(f"ADICIONADA (MX ok): {n['empresa']} <{em}>")

with open(FILA, "w", encoding="utf-8") as f:
    json.dump(fila, f, ensure_ascii=False, indent=2)

print(f"\nTotal na fila: {len(fila)} | adicionadas: {adicionadas}")