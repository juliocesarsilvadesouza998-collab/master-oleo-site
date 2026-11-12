#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Descartar leads de LATICINIOS (decisao do Julio, 12/11/2026).

Motivo: laticinio nao gera material oleoso separavel (o residuo e' soro/queijo,
nao oleo) e o ticket e' baixo => fora do alvo comercial da Master Oleo.

O que faz:
  1) leads.csv        -> leads de laticinio com status 'novo' viram 'descartado'
  2) fila_prospeccao_extra.json -> remove entradas de laticinio da fila de entrada
  3) backfill_segmento.py / prospectar_novos.py: o filtro permanente fica em
     `filtros_oleo.py` (segmento_excluido), importado pelos scripts de captacao.

Uso: python _descartar_laticinios.py --dry-run    (so mostra)
     python _descartar_laticinios.py --aplicar    (grava, com backup)
"""
import argparse, csv, json, os, re, shutil, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from filtros_oleo import motivo_exclusao  # noqa: E402

LEADS = os.path.join(BASE, "leads.csv")
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")
FIELDS = ["id", "nome", "empresa", "email", "tipo", "volume", "segmento", "cidade",
          "fonte", "status", "criado_em", "boas_vindas_em", "follow1_em", "follow2_em",
          "follow3_em", "apresentacao_em", "fp1_em", "fp2_em", "fp3_em",
          "apresentacao_msgid", "ultima_resposta", "respondido_em", "respondido_por"]


def read_leads():
    with open(LEADS, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_leads(leads):
    with open(LEADS, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for l in leads:
            w.writerow(l)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    aplicar = args.aplicar and not args.dry_run

    leads = read_leads()
    marcados, mantidos_borda = [], []
    for l in leads:
        m = motivo_exclusao(l.get("nome", ""), l.get("empresa", ""), l.get("segmento", ""))
        if not m:
            continue
        if l["status"] in ("respondido", "bounce", "descartado"):
            mantidos_borda.append((l, m, "mantido: %s" % l["status"]))
            continue
        marcados.append((l, m))

    fila = json.load(open(FILA, encoding="utf-8"))
    fila_ok, fila_fora = [], []
    for e in fila:
        m = motivo_exclusao(e.get("nome", ""), e.get("empresa", ""), e.get("segmento", ""))
        (fila_fora if m else fila_ok).append((e, m))

    print("== leads.csv: %d marcados p/ 'descartado' de %d ==" % (len(marcados), len(leads)))
    for l, m in marcados:
        print("  #%-12s %-8s %-58s <- %s" % (l["id"], l["status"], l.get("empresa", "")[:56], m))
    print("\n== leads.csv: laticinio ja respondido/descartado (nao mexo) ==")
    for l, m, why in mantidos_borda:
        print("  #%-12s %-58s %s" % (l["id"], l.get("empresa", "")[:56], why))
    print("\n== fila_prospeccao_extra.json: %d fora de %d ==" % (len(fila_fora), len(fila)))
    for e, m in fila_fora:
        print("  - %-58s <- %s" % (e.get("empresa", "")[:56], m))

    if not aplicar:
        print("\n[DRY-RUN] nada foi gravado. Rode com --aplicar para efetivar.")
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LEADS, LEADS + ".bak-%s-laticinios" % stamp)
    shutil.copy2(FILA, FILA + ".bak-%s-laticinios" % stamp)
    for l, m in marcados:
        l["status"] = "descartado"
    write_leads(leads)
    json.dump([e for e, _ in fila_ok], open(FILA, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print("\nOK: %d leads -> 'descartado'; fila %d -> %d (backup .bak-%s-laticinios)"
          % (len(marcados), len(fila), len(fila_ok), stamp))


if __name__ == "__main__":
    main()
