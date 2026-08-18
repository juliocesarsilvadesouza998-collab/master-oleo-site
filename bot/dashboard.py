#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Dashboard de Retorno (métricas de prospecção)
=============================================================
Mostra o que importa: quantos emails foram enviados, quantos responderam,
taxa de resposta, leads quentes e bounces. Rode a qualquer momento:

  python dashboard.py              # visão geral
  python dashboard.py --detalhe   # lista leads quentes + respondidos
"""
import argparse, csv, datetime, json, os, sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS_PATH = os.path.join(BASE, "leads.csv")

def fmt_data(iso):
    if not iso:
        return "—"
    try:
        return datetime.datetime.fromisoformat(iso).strftime("%d/%m")
    except Exception:
        return iso[:10]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--detalhe", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(LEADS_PATH):
        print("leads.csv não encontrado — rode sync_formspree.py primeiro.")
        return 1

    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        leads = list(csv.DictReader(f))

    # Separa prospecção (outbound) de inbound
    outbound = [l for l in leads if str(l.get("fonte","")).startswith("prospeccao")]
    inbound = [l for l in leads if not str(l.get("fonte","")).startswith("prospeccao")]

    enviados = [l for l in outbound if l.get("apresentacao_em")]
    respondidos = [l for l in outbound if l.get("status") == "respondido"]
    bounces = [l for l in outbound if l.get("status") == "bounce"]
    ativos = [l for l in outbound if l.get("status") not in ("bounce","respondido","encerrado")]

    taxa_resposta = (len(respondidos)/len(enviados)*100) if enviados else 0
    taxa_entrega = ((len(enviados)-len(bounces))/len(enviados)*100) if enviados else 0

    now = datetime.datetime.now().astimezone()
    print("="*62)
    print("  📊 DASHBOARD MASTER ÓLEO — retorno da prospecção")
    print(f"  Gerado em: {now.strftime('%d/%m/%Y %H:%M')}")
    print("="*62)
    print()
    print(f"  📨 Emails de apresentação enviados : {len(enviados)}")
    print(f"  ✅ Entregues (sem bounce)          : {len(enviados)-len(bounces)}")
    print(f"  ❌ Bounces                         : {len(bounces)}  ({100-taxa_entrega:.0f}%)")
    print(f"  💬 RESPOSTAS RECEBIDAS             : {len(respondidos)}")
    print(f"  📈 Taxa de resposta                : {taxa_resposta:.1f}%")
    print(f"  ⏳ Aguardando resposta/follow-up   : {len(ativos)}")
    print(f"  🧊 Inbound (formulário do site)    : {len(inbound)}")
    print()

    if args.detalhe:
        print("  --- LEADS QUE RESPONDERAM (quentes!) ---")
        for l in respondidos:
            print(f"    🔥 {l.get('empresa','')[:40]:<42} {l.get('email','')}")
            if l.get("ultima_resposta"):
                print(f"       💬 {l['ultima_resposta'][:110]}")
        if not respondidos:
            print("    (nenhum ainda)")
        print()
        print("  --- ÚLTIMOS ENVIADOS ---")
        for l in sorted(enviados, key=lambda x: x.get("apresentacao_em") or "", reverse=True)[:8]:
            print(f"    📤 {fmt_data(l.get('apresentacao_em'))} | {l.get('empresa','')[:38]:<40} {l.get('email','')}")
        print()

    # Tendência por dia
    dias = Counter()
    for l in enviados:
        d = fmt_data(l.get("apresentacao_em"))
        if d != "—":
            dias[d] += 1
    print("  --- ENVIOS POR DIA ---")
    for d in sorted(dias):
        barra = "█" * dias[d]
        print(f"    {d}  {barra} {dias[d]}")
    print()
    print("  💡 Meta: taxa de resposta > 3% e pelo menos 1 lead quente por semana.")
    print("     Próximos follow-ups: FP1 (dia 3), FP2 (dia 6), FP3 (dia 10).")
    return 0

if __name__ == "__main__":
    sys.exit(main())