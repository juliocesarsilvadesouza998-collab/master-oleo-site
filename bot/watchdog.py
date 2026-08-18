#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Watchdog de Follow-ups e Bounces
================================================
Detecta problemas na operação de email e reporta para correção:

1. Follow-ups ATRASADOS: leads de prospecção com apresentação enviada há
   mais de X dias sem FP correspondente (sinal de que algo travou)
2. Bounces NOVOS: emails em bounces.json que ainda não foram tentados corrigir
3. Leads parados: leads 'novo' sem apresentacao_em (nunca receberam email)

Uso:
  python watchdog.py               # verifica e reporta (exit 0 = ok, 1 = problemas)
  python watchdog.py --detalhado   # mostra lista completa
"""
import argparse, csv, datetime, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS_PATH = os.path.join(BASE, "leads.csv")
BOUNCE_CACHE = os.path.join(BASE, "bounces.json")
CORRIGIDOS_LOG = os.path.join(BASE, "correcoes_emails.json")

# Limites
FP_LIMITES = {"fp1_em": 3, "fp2_em": 6, "fp3_em": 10}

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_bounces():
    if os.path.exists(BOUNCE_CACHE):
        try:
            return set(json.load(open(BOUNCE_CACHE, encoding="utf-8")))
        except Exception:
            return set()
    return set()

def load_corrigidos():
    """Emails que já passaram por tentativa de correção (qualquer resultado)."""
    if os.path.exists(CORRIGIDOS_LOG):
        try:
            return {e.get("email_antigo","").lower() for e in json.load(open(CORRIGIDOS_LOG, encoding="utf-8"))}
        except Exception:
            return set()
    return set()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--detalhado", action="store_true")
    args = ap.parse_args()

    leads = read_leads()
    bounces = load_bounces()
    corrigidos = load_corrigidos()
    now = datetime.datetime.now().astimezone()
    problemas = []

    # 1) Follow-ups atrasados
    atrasados = []
    for l in leads:
        if not str(l.get("fonte","")).startswith("prospeccao"):
            continue
        if l.get("status") in ("respondido","bounce","encerrado"):
            continue
        ap = l.get("apresentacao_em")
        if not ap:
            continue
        try:
            dias = (now - datetime.datetime.fromisoformat(ap)).days
        except Exception:
            continue
        for campo, limite in FP_LIMITES.items():
            if dias >= limite and not l.get(campo):
                atrasados.append((l.get("empresa",""), l.get("email",""), campo, dias))
                break
    if atrasados:
        problemas.append(f"{len(atrasados)} follow-up(s) ATRASADO(S) (aguardando prospecao_followup.py)")
        if args.detalhado:
            for emp, em, campo, dias in atrasados[:15]:
                print(f"  ⏰ {emp[:38]:<40} {em:<40} {campo} há {dias}d")

    # 2) Bounces sem tentativa de correção (cruza com leads.csv: só conta se o
    #    email do bounce AINDA estiver em uso como lead com status bounce)
    emails_ativos = {l.get("email","").strip().lower() for l in leads if l.get("status") == "bounce"}
    bounces_atuais = {b.lower() for b in bounces if b.lower() in emails_ativos}
    sem_correcao = bounces_atuais - corrigidos
    if sem_correcao:
        problemas.append(f"{len(sem_correcao)} bounce(s) sem tentativa de correção (aguardando corrigir_emails.py)")
        if args.detalhado:
            for em in sorted(sem_correcao)[:10]:
                print(f"  ❌ {em}")

    # 3) Leads parados sem apresentação
    parados = [l for l in leads if l.get("status") == "novo" and not l.get("apresentacao_em") and not l.get("boas_vindas_em")]
    if parados:
        problemas.append(f"{len(parados)} lead(s) 'novo' SEM apresentação enviada")
        if args.detalhado:
            for l in parados[:10]:
                print(f"  ⚠️  {l.get('empresa','')[:38]:<40} {l.get('email','')}")

    # 4) Resumo saudável
    ativos = [l for l in leads if l.get("status") in ("novo","sequencia")]
    print(f"=== WATCHDOG Master Óleo — {now.strftime('%d/%m/%Y %H:%M')} ===")
    print(f"Leads: {len(leads)} | ativos: {len(ativos)} | bounces: {len(bounces)}")
    if problemas:
        print(f"\n⚠️  {len(problemas)} problema(s) detectado(s):")
        for p in problemas:
            print(f"  • {p}")
        return 1
    print("\n✅ Tudo saudável — nenhum follow-up atrasado, bounces corrigidos ou leads parados.")
    return 0

if __name__ == "__main__":
    sys.exit(main())