#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Backfill de `segmento`/`cidade` no leads.csv (12/11/2026).

Motivo: as 464 linhas do leads.csv estão com `segmento` VAZIO (o backfill
anterior rodou antes de a coluna existir / não pegou). Sem segmento, nenhum
relatório por segmento funciona e o filtro de alvo (filtros_oleo) só consegue
olhar o nome da empresa.

Fontes: prospecao.EMPRESAS + fila_prospeccao_extra.json (atual) + backup da fila
de 12/11/2026 (que ainda contém as empresas de laticínio removidas) — assim o
segmento real de quem está no leads.csv é recuperado.

Efeito colateral desejado: lead de laticínio com status 'novo' passa a
'descartado' (regra do Julio, 12/11/2026). Leads que JÁ responderam ficam como
'estão' (histórico preservado) — apenas deixam de aparecer como lead quente.

Uso: python _backfill_segmento.py --dry-run | --aplicar
"""
import argparse, csv, datetime, json, os, shutil, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import prospecao as P                      # noqa: E402
from filtros_oleo import motivo_exclusao   # noqa: E402

LEADS = os.path.join(BASE, "leads.csv")
FONTES = [os.path.join(BASE, "fila_prospeccao_extra.json"),
          os.path.join(BASE, "fila_prospeccao_extra.json.bak-20261112-093039-laticinios")]
FIELDS = ["id", "nome", "empresa", "email", "tipo", "volume", "segmento", "cidade",
          "fonte", "status", "criado_em", "boas_vindas_em", "follow1_em", "follow2_em",
          "follow3_em", "apresentacao_em", "fp1_em", "fp2_em", "fp3_em",
          "apresentacao_msgid", "ultima_resposta", "respondido_em", "respondido_por"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    por_email, por_empresa = {}, {}
    for f in FONTES:
        if not os.path.exists(f):
            continue
        for e in json.load(open(f, encoding="utf-8")):
            par = (e.get("segmento", ""), e.get("cidade", ""))
            por_email.setdefault(e["email"].strip().lower(), par)
            por_empresa.setdefault(e["empresa"].strip().lower(), par)
    for e in P.EMPRESAS:
        por_email.setdefault(e["email"].strip().lower(), (e.get("segmento", ""), e.get("cidade", "")))
        por_empresa.setdefault(e["empresa"].strip().lower(), (e.get("segmento", ""), e.get("cidade", "")))

    with open(LEADS, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    preenchidos, sem_info, novos_fora, ja_fora = 0, [], [], []
    for r in rows:
        em = (r.get("email") or "").strip().lower()
        seg, cid = por_email.get(em) or por_empresa.get((r.get("empresa") or "").strip().lower()) or ("", "")
        r["segmento"], r["cidade"] = seg, cid
        if seg:
            preenchidos += 1
        else:
            sem_info.append(r.get("empresa", "?"))
        motivo = motivo_exclusao(r.get("nome", ""), r.get("empresa", ""), seg)
        if motivo and r["status"] == "novo":
            novos_fora.append((r, motivo))
        elif motivo:
            ja_fora.append((r, motivo))

    print("leads.csv: %d linhas | segmento preenchido: %d | sem info: %d"
          % (len(rows), preenchidos, len(sem_info)))
    print("fora do alvo (laticínio) com status 'novo' -> 'descartado': %d" % len(novos_fora))
    for r, m in novos_fora:
        print("   #%-12s %-52s <- %s" % (r["id"], r["empresa"][:50], m))
    print("fora do alvo que já responderam/bounce (status preservado): %d" % len(ja_fora))
    for r, m in ja_fora:
        print("   #%-12s %-52s status=%s" % (r["id"], r["empresa"][:50], r["status"]))

    if not args.aplicar:
        print("\n[DRY-RUN] nada gravado.")
        return
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(LEADS, LEADS + ".bak-%s-segmento" % stamp)
    for r, _ in novos_fora:
        r["status"] = "descartado"
    with open(LEADS, "w", newline="", encoding="utf-8") as f:   # sem BOM (ver incidente 12/11/2026)
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print("\nOK gravado (backup .bak-%s-segmento)" % stamp)


if __name__ == "__main__":
    main()
