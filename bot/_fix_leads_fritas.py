#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Corrige metadados dos 11 fabricantes de fritas/snacks importados sem `fonte`.

Contexto (12/11/2026): 11 empresas de fritas/chips (Rick's Fritas, Art Fritas,
Point Chips, Fritamaz, Mega Chips, Tostally, Quetti, União Fritas, Mantiqueira)
entraram em 25/09/2026 SEM `empresa`, SEM `segmento` e SEM `fonte`. Consequência:
- a régua de boas-vindas (para quem nos procurou) rodou EM CIMA da apresentação
  outbound => cada uma levou 5 emails (apresentação + boas-vindas + 3 follow-ups);
- o dashboard contava as 11 como "inbound (formulário do site)".

Corrige: empresa=nome, segmento=indústria de fritura, fonte=prospeccao-fritas-2026-09-25.
Status permanece 'encerrado' (a régua já terminou — nenhum email é disparado).

Uso: python _fix_leads_fritas.py --aplicar | --dry-run
"""
import argparse, csv, datetime, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(BASE, "leads.csv")
SEG = "Industria de snacks/fritas (fritura industrial continua - oleo usado em volume)"
FONTE = "prospeccao-fritas-2026-09-25"
FIELDS = ["id", "nome", "empresa", "email", "tipo", "volume", "segmento", "cidade",
          "fonte", "status", "criado_em", "boas_vindas_em", "follow1_em", "follow2_em",
          "follow3_em", "apresentacao_em", "fp1_em", "fp2_em", "fp3_em",
          "apresentacao_msgid", "ultima_resposta", "respondido_em", "respondido_por"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    with open(LEADS, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    alvo = [r for r in rows if not (r.get("fonte") or "").strip()]
    print("linhas sem `fonte` (prospeccao sem rotulo): %d" % len(alvo))
    for r in alvo:
        print("   #%-12s %-30s criado %s | status=%s | apres=%s"
              % (r["id"], (r.get("nome") or "")[:28], r["criado_em"][:10], r["status"],
                 (r.get("apresentacao_em") or "-")[:10]))
        if args.aplicar:
            r["empresa"] = r.get("empresa") or r.get("nome", "")
            r["segmento"] = r.get("segmento") or SEG
            r["fonte"] = FONTE
    if not args.aplicar:
        print("\n[DRY-RUN] nada gravado.")
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LEADS, LEADS + ".bak-%s-fritas" % stamp)
    with open(LEADS, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("\nOK gravado (backup .bak-%s-fritas)" % stamp)


if __name__ == "__main__":
    main()
