#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Melhorador Continuo 28/10/2026 — Reabastece fila_prospeccao_extra.json
1) Corrige Unialimentar (email publicado no proprio site, domínio atual sem MX)
2) Remove NUF Farmaceutica (dominio sem MX, email inenviavel, segmento fora do core)
3) Adiciona 9 empresas novas da regiao (lista oficial prefeitura Tiete + sites oficiais)
4) Valida MX de todos os novos por nslookup antes de gravar
"""
import json, os, re, subprocess, sys, csv

BASE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")

novas = [
    {"nome": "Supermercado Stabile", "empresa": "Supermercado Stabile Ltda",
     "email": "supermercadostabile@gmail.com", "cidade": "Tiete/SP",
     "segmento": "Supermercado local (padaria/rotisserie/acougue - fritura continua, oleo vencido de prateleira)"},
    {"nome": "Supermercado M&M", "empresa": "Supermercado M M Ltda",
     "email": "contato@mmsupermercado.com.br", "cidade": "Tiete/SP",
     "segmento": "Supermercado local (padaria/rotisserie - fritura continua)"},
    {"nome": "Supermercado Tiaozinho", "empresa": "Supermercado Elias Moreira Ltda",
     "email": "cartoes@supermercadostiaozinho.com.br", "cidade": "Tiete/SP",
     "segmento": "Supermercado local (padaria/rotisserie - fritura continua)"},
    {"nome": "Supermercado Tiba", "empresa": "Supermercados Tiba Ltda",
     "email": "suptiba@yahoo.com.br", "cidade": "Tiete/SP",
     "segmento": "Supermercado local (padaria/rotisserie - fritura continua)"},
    {"nome": "Mercado Potiguara", "empresa": "Mercado Potiguara",
     "email": "mercado.potiguara@bol.com.br", "cidade": "Tiete/SP",
     "segmento": "Mercado local (rotisserie - fritura continua)"},
    {"nome": "Mercado Ponto Certo", "empresa": "Mercado Ponto Certo",
     "email": "mercado.pontocertotiete@gmail.com", "cidade": "Tiete/SP",
     "segmento": "Mercado local (rotisserie - fritura continua)"},
    {"nome": "TBS Minimercado", "empresa": "TBS Minimercado Ltda",
     "email": "tbminimercado@gmail.com", "cidade": "Tiete/SP",
     "segmento": "Minimercado local (rotisserie - fritura)"},
    {"nome": "Mercado Atual", "empresa": "Mercado Atual Ltda",
     "email": "atualsupermercado@gmail.com", "cidade": "Itu/SP",
     "segmento": "Supermercado local (padaria/rotisserie - fritura continua, oleo vencido de prateleira)"},
    {"nome": "Boi na Brasa Sorocaba", "empresa": "Churrascaria Boi na Brasa Sorocaba",
     "email": "reserva@boinabrasasorocaba.com.br", "cidade": "Sorocaba/SP",
     "segmento": "Churrascaria (fritura alto volume - batata frita, pasteis, coxinhas, mandioca frita)"},
    {"nome": "Uniao Supermercados", "empresa": "Uniao Supermercados (14 lojas, 30+ anos)",
     "email": "sac@uniaosupermercados.com", "cidade": "Itu/SP",
     "segmento": "Supermercados (rede 14+ lojas - padaria/rotisserie/acougue, fritura continua, oleo vencido)"},
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

print("== REMOVER / CORRIGIR ==")
nova_fila = []
for e in fila:
    em = e.get("email", "").strip().lower()
    if em == "suporte@nuffarmaceutica.com.br":
        print(f"REMOVER: {e.get('empresa')} <{em}> (dominio sem MX, inenviavel)")
        continue
    if em == "comercial@unialimentar.com.br":
        print(f"FIX Unialimentar: {em} -> unialimentar@gmail.com (email publicado no site unialimentar.com.br)")
        e["email"] = "unialimentar@gmail.com"
        e["segmento"] = e.get("segmento", "") + " (email corrigido 28/10 via site oficial)"
    nova_fila.append(e)

print("\n== MX CHECK + ADICIONAR ==")
adicionadas = 0
for n in novas:
    em = n["email"].strip().lower()
    dom = em.split("@")[-1]
    if em in conhecidos:
        print(f"JA EXISTE: {n['empresa']} <{em}>")
        continue
    if em in bounces:
        print(f"BOUNCE ANTERIOR: {n['empresa']} <{em}> — pulando")
        continue
    if not tem_mx(dom):
        print(f"SEM MX: {n['empresa']} <{em}> ({dom}) — pulando")
        continue
    nova_fila.append(n)
    conhecidos.add(em)
    adicionadas += 1
    print(f"ADICIONADA (MX ok): {n['empresa']} <{em}>")

with open(FILA, "w", encoding="utf-8") as f:
    json.dump(nova_fila, f, ensure_ascii=False, indent=2)

print(f"\nTotal na fila agora: {len(nova_fila)} (era {len(fila)}) | adicionadas: {adicionadas}")