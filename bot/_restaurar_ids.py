#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Restaura a coluna `id` do leads.csv (INCIDENTE 12/11/2026, 17:33).

Causa raiz: um script escreveu o leads.csv com BOM (encoding="utf-8-sig").
Os scripts do pipeline leem com encoding="utf-8" puro, então a primeira coluna
virou '\ufeffid' — ao regravar, os valores de `id` foram descartados (coluna
ficou vazia em TODAS as 464 linhas) e o BOM desapareceu, escondendo a pista.

Fonte dos ids: backup tirado imediatamente antes (mesmas 464 linhas, mesmos
emails). Casamento por email; sobra recebe id novo sequencial.

Uso: python _restaurar_ids.py --aplicar | --dry-run
"""
import argparse, csv, datetime, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
LEADS = os.path.join(BASE, "leads.csv")
BAK = os.path.join(BASE, "leads.csv.bak-20261112-093039-laticinios")
FIELDS = ["id", "nome", "empresa", "email", "tipo", "volume", "segmento", "cidade",
          "fonte", "status", "criado_em", "boas_vindas_em", "follow1_em", "follow2_em",
          "follow3_em", "apresentacao_em", "fp1_em", "fp2_em", "fp3_em",
          "apresentacao_msgid", "ultima_resposta", "respondido_em", "respondido_por"]


def rd(p):
    with open(p, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    cur, bak = rd(LEADS), rd(BAK)
    if len(cur) != len(bak):
        print("ABORTADO: linhas diferentes (atual %d x backup %d) — revisar antes."
              % (len(cur), len(bak)))
        return
    ids_por_email = {}
    for r in bak:
        e = (r.get("email") or "").strip().lower()
        if e and (r.get("id") or "").strip() and e not in ids_por_email:
            ids_por_email[e] = r["id"].strip()
    usados = set(ids_por_email.values())
    prox = max([int(i) for i in usados if i.isdigit()] or [0])
    restaurados, novos = 0, []
    for r in cur:
        if (r.get("id") or "").strip():
            continue
        e = (r.get("email") or "").strip().lower()
        if e in ids_por_email and ids_por_email[e] in usados:
            r["id"] = ids_por_email.pop(e)
            usados.discard(r["id"])
            restaurados += 1
        else:
            prox += 1
            r["id"] = str(prox)
            novos.append((r["id"], r.get("empresa", "")[:48]))

    print("restaurados do backup: %d | ids novos atribuidos: %d" % (restaurados, len(novos)))
    for i, emp in novos:
        print("   novo id %-12s %s" % (i, emp))
    dup = [i for i in [r["id"] for r in cur] if [x["id"] for x in cur].count(i) > 1]
    print("ids duplicados apos a correcao:", len(set(dup)), sorted(set(dup))[:5])
    print("ids vazios restantes:", sum(1 for r in cur if not (r.get("id") or "").strip()))

    if not args.aplicar:
        print("\n[DRY-RUN] nada gravado.")
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LEADS, LEADS + ".bak-%s-ids" % stamp)
    with open(LEADS, "w", newline="", encoding="utf-8") as f:   # SEM BOM: é o formato que o pipeline usa
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(cur)
    print("\nOK gravado (backup .bak-%s-ids)" % stamp)


if __name__ == "__main__":
    main()
