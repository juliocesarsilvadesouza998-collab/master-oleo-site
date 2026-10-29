#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspeção de estado do pipeline Master Óleo — atendente IA (tick 18:30)."""
import csv, json, os, datetime, collections

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(BASE, "leads.csv")

def read_leads():
    with open(LEADS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

leads = read_leads()
hoje = datetime.date.today().isoformat()
agora = datetime.datetime.now().astimezone()

print(f"LEADS TOTAIS: {len(leads)}")

st = collections.Counter(l.get("status", "") for l in leads)
print("STATUS:", dict(st.most_common()))

fonte = collections.Counter(
    ("prospeccao" if str(l.get("fonte", "")).startswith("prospeccao") else l.get("fonte", ""))
    for l in leads
)
print("FONTE:", dict(fonte.most_common(10)))

# campos de data relevantes
campos = ["boas_vindas_em", "follow1_em", "follow2_em", "follow3_em", "apresentacao_em",
          "fp1_em", "fp2_em", "fp3_em", "respondido_em", "ultima_resposta"]
for c in campos:
    n = sum(1 for l in leads if l.get(c))
    h = sum(1 for l in leads if str(l.get(c, "")).startswith(hoje))
    print(f"  {c:20s} preenchidos={n:4d}  hoje={h}")

# enviados hoje (qualquer campo de data)
hoje_sends = 0
for l in leads:
    if any(str(l.get(c, "")).startswith(hoje) for c in campos):
        hoje_sends += 1
print(f"LEADS COM ATIVIDADE HOJE: {hoje_sends}")

print("\nULTIMOS 12 LEADS COM ENVIO (por apresentacao_em):")
com_env = [l for l in leads if l.get("apresentacao_em")]
com_env.sort(key=lambda l: l["apresentacao_em"], reverse=True)
for l in com_env[:12]:
    print(f"  {l['apresentacao_em'][:16]} | {l['empresa'][:45]:45s} | {l['cidade'] if 'cidade' in l else ''} | {l['email']}")

print("\nRESPONDIDOS (respondido_em preenchido):")
resp = [l for l in leads if l.get("respondido_em")]
resp.sort(key=lambda l: l["respondido_em"], reverse=True)
for l in resp[:15]:
    print(f"  {l['respondido_em'][:16]} | {l['empresa'][:45]:45s} | status={l['status']} | {l.get('respondido_por','')}")

# itens de fila extra não contactados
for fn in ("fila_prospeccao_extra.json", "fila_prioritaria.json"):
    p = os.path.join(BASE, fn)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        emails_leads = {l["email"].strip().lower() for l in leads}
        novos = [x for x in d if str(x.get("email", "")).strip().lower() not in emails_leads]
        print(f"\n{fn}: total={len(d)} | ainda nao em leads.csv={len(novos)}")
        for x in novos[:10]:
            print(f"   - {x.get('empresa','')[:50]} | {x.get('email','')}")

# bounces
p = os.path.join(BASE, "bounces.json")
if os.path.exists(p):
    with open(p, encoding="utf-8") as f:
        b = json.load(f)
    print(f"\nbounces.json: {len(b) if isinstance(b,(list,dict)) else '?'} entradas")
print(f"\nHORA: {agora:%Y-%m-%d %H:%M %z}")
