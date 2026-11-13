#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Migração: leitura do leads.csv tolerante a BOM (INCIDENTE 12/11/2026).

Um script gravou o leads.csv com BOM (utf-8-sig). Como os leitores do pipeline
abriam com encoding="utf-8" puro, a primeira coluna virou '\\ufeffid' e, ao
regravar, TODOS os ids foram perdidos (coluna vazia nas 464 linhas), sem erro
nenhum na tela.

Correção: todo LEITOR de leads.csv passa a abrir com encoding="utf-8-sig", que
funciona tanto com BOM quanto sem. Os gravadores continuam em "utf-8" puro
(arquivo segue sem BOM, que é o formato que todos esperam).

Uso: python _migrar_leitura_utf8sigs.py --dry-run | --aplicar
"""
import argparse, io, os, re, shutil, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# Somente linhas de LEITURA do leads.csv (sem modo de escrita)
RX = re.compile(r'^(\s*.*open\((?P<alvo>[^)]*?(LEADS|LEADS_PATH|path)[^)]*?),'
                r'\s*[^)]*encoding=)"utf-8"(.+)$')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    mudados = []
    for nome in sorted(os.listdir(BASE)):
        if not nome.endswith(".py") or nome.startswith("_"):
            continue
        p = os.path.join(BASE, nome)
        with open(p, encoding="utf-8") as f:
            linhas = f.readlines()
        novo, alterou = [], False
        for ln in linhas:
            m = RX.match(ln)
            if m and ("\"w\"" not in ln and "'w'" not in ln and "\"a\"" not in ln and "'a'" not in ln):
                novo.append(ln.replace('encoding="utf-8"', 'encoding="utf-8-sig"'))
                alterou = True
                mudados.append("%s: %s" % (nome, ln.strip()[:88]))
            else:
                novo.append(ln)
        if alterou and args.aplicar:
            shutil.copy2(p, p + ".bak-%s-utf8sig" % datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
            with open(p, "w", encoding="utf-8", newline="") as f:
                f.writelines(novo)
    print("linhas de leitura convertidas para utf-8-sig: %d" % len(mudados))
    for m in mudados:
        print("  -", m)
    if not args.aplicar:
        print("\n[DRY-RUN] nada gravado.")


if __name__ == "__main__":
    main()
