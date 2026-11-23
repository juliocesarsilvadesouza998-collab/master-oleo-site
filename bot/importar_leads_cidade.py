#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Importa leads descobertos (fora do prospector automatico) para o pipeline.

Contexto (23/11/2026): o Julio pediu coleta de oleo usado em ITU e INDAIATUBA com teto de
compra ate R$ 3,00/L. O prospector do projeto (prospectar_novos.py) depende do Bing e
devolveu ZERO lead nesses dois municipios (15 sites sem email, 1 fora da cidade) — a
descoberta foi feita com as ferramentas web do agente. Este script FAZ A ENTRADA controlada:

  1. deduplica contra leads.csv (quem ja foi contatado), bounces.json e a fila;
  2. valida MX do email (regra do projeto: sem MX nao entra);
  3. grava os emails validos na fila (fonte prospeccao-<slug>-<data>) para o robô de email;
  4. gera uma FOLHA DE LIGACOES/WHATSAPP em markdown com todos (inclusive os que nao tem
     email), porque em Itu/Indaiatuba o telefone e' a rota que fura a concorrencia.

Uso:
  python importar_leads_cidade.py --json <arquivo.json> --slug itu-indaiatuba \
      --callsheet ../leads/folha-itu-indaiatuba.md [--dry-run]

Formato do JSON de entrada: lista de objetos com nome, segmento, cidade, telefone,
email, site, fonte_url, evidencia (os campos vazios sao aceitos).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime
import json
import os
import re
import shutil
import sys
import unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from prospectar_novos import tem_mx  # noqa: E402

LEADS = os.path.join(BASE, "leads.csv")
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")
BOUNCES = os.path.join(BASE, "bounces.json")


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"\b(ltda|me|eireli|sa|s/a|s\.a)\b", " ", s.lower())
    return " ".join(re.findall(r"[a-z0-9]+", s))


def so_digitos(t: str) -> str:
    return re.sub(r"\D", "", t or "")


def classifica_telefone(t: str) -> tuple[str, str]:
    """Devolve (tipo, numero_e164_sem_mais). tipo: celular|fixo|invalido."""
    d = so_digitos(t)
    if not d:
        return "invalido", ""
    if len(d) in (10, 11):
        d = "55" + d
    if len(d) == 13 and d[4] == "9":
        return "celular", d
    if len(d) == 12:
        return "fixo", d
    if len(d) == 13:
        return "celular", d
    return "invalido", d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", required=True)
    ap.add_argument("--slug", required=True, help="rotulo da fonte, ex.: itu-indaiatuba")
    ap.add_argument("--callsheet", default="")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    with open(args.json, encoding="utf-8") as f:
        dados = json.load(f)
    if isinstance(dados, dict):
        dados = dados.get("leads", [])

    with open(LEADS, encoding="utf-8-sig", newline="") as f:
        leads = list(csv.DictReader(f))
    emails_conhecidos = {(l.get("email") or "").strip().lower() for l in leads}
    nomes_conhecidos = {norm(l.get("empresa") or l.get("nome") or "") for l in leads}
    bounces = set()
    if os.path.exists(BOUNCES):
        bounces = {e.strip().lower() for e in json.load(open(BOUNCES, encoding="utf-8"))}
    fila = json.load(open(FILA, encoding="utf-8"))
    emails_fila = {(e.get("email") or "").strip().lower() for e in fila}
    nomes_fila = {norm(e.get("empresa") or e.get("nome") or "") for e in fila}

    aprovados_email, telefones, duplicados, sem_mx, sem_contato = [], [], [], [], []
    fonte = "prospeccao-%s-%s" % (args.slug, datetime.date.today().strftime("%Y%m%d"))

    for d in dados:
        nome = (d.get("nome") or "").strip()
        emp = (d.get("empresa") or nome).strip()
        em = (d.get("email") or "").strip().lower()
        tel = (d.get("telefone") or "").strip()
        cidade = (d.get("cidade") or "").strip()
        seg = (d.get("segmento") or "").strip()
        nn = norm(emp)
        if not nome and not tel:
            continue
        ja = (em and (em in emails_conhecidos or em in emails_fila or em in bounces)) or \
             any(nn and (nn == x or (len(nn) > 8 and (nn in x or x in nn))) for x in nomes_conhecidos | nomes_fila)
        if ja:
            duplicados.append(emp or nome)
            continue
        if tel:
            tipo, num = classifica_telefone(tel)
            telefones.append((nome or emp, seg, cidade, tel, tipo, num, em))
        if not em:
            if not tel:
                sem_contato.append(emp or nome)
            continue
        ok, mx = tem_mx(em.split("@")[-1])
        if not ok:
            sem_mx.append("%s <%s> (%s)" % (emp or nome, em, mx or "sem MX"))
            continue
        aprovados_email.append({
            "nome": nome or emp, "empresa": emp, "email": em, "cidade": cidade, "segmento": seg,
            "fonte": fonte, "site": (d.get("site") or "").strip(),
            "telefone": tel, "evidencia": (d.get("evidencia") or "").strip(),
            "fonte_url": (d.get("fonte_url") or "").strip(),
        })

    print("entrada: %d | duplicados (ja na base/fila): %d | sem MX: %d | sem contato: %d"
          % (len(dados), len(duplicados), len(sem_mx), len(sem_contato)))
    print("emails aprovados: %d | com telefone: %d" % (len(aprovados_email), len(telefones)))
    for d in duplicados:
        print("   dup  %s" % d[:60])
    for s in sem_mx:
        print("   sem MX: %s" % s[:70])

    # folha de ligacoes/whatsapp (todos, com ou sem email)
    if args.callsheet and telefones:
        linhas = ["# Folha de contato — oleo usado (%s) — %s" % (args.slug, datetime.date.today().strftime("%d/%m/%Y")),
                  "",
                  "%d empresas. Celular = link direto do WhatsApp (mensagem ja preenchida). Fixo = ligar." % len(telefones),
                  "Regra: **nunca falar preco no primeiro contato**. Pergunte primeiro quem leva o oleo hoje e quanto ele recebe.",
                  "Teto de compra nesta praca: **ate R$ 3,00/L**.", ""]
        for nome, seg, cidade, tel, tipo, num, em in sorted(telefones, key=lambda x: (x[2], x[0])):
            linhas.append("## %s — %s" % (nome, cidade or "?"))
            linhas.append("- Segmento: %s" % (seg or "-"))
            linhas.append("- Telefone: %s (%s)" % (tel, "celular/WhatsApp" if tipo == "celular" else ("fixo — ligar" if tipo == "fixo" else "invalido")))
            if tipo == "celular":
                msg = ("Ola! Falo com quem cuida da cozinha? Sou o Julio, da Master Oleo (Salto/SP). "
                       "A gente compra oleo de cozinha usado e faz a coleta aqui na regiao. "
                       "Posso te perguntar uma coisa: quem leva o oleo usado de voces hoje?")
                import urllib.parse
                linhas.append("- WhatsApp: https://wa.me/%s?text=%s" % (num, urllib.parse.quote(msg)))
            linhas.append("- E-mail: %s" % (em or "-"))
            if em:
                linhas.append("- CRM: entra na fila com fonte `%s`" % fonte)
            linhas.append("")
        caminho = args.callsheet if os.path.isabs(args.callsheet) else os.path.join(BASE, args.callsheet)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        if not args.dry_run:
            with open(caminho, "w", encoding="utf-8") as f:
                f.write("\n".join(linhas))
            print("folha de contato: %s" % caminho)
        else:
            print("[DRY-RUN] folha de contato seria escrita em %s (%d linhas)" % (caminho, len(linhas)))

    if not aprovados_email:
        print("nada novo com email valido — fila nao foi alterada.")
        return 0
    if args.dry_run:
        print("[DRY-RUN] fila ficaria com %d registros (+%d)." % (len(fila) + len(aprovados_email), len(aprovados_email)))
        for a in aprovados_email:
            print("   + %-42s <%s> %s" % (a["empresa"][:42], a["email"], a["cidade"]))
        return 0
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    shutil.copy2(FILA, FILA + ".bak-%s-import" % stamp)
    fila.extend(aprovados_email)
    with open(FILA, "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=2)
    print("fila: %d registros (+%d, fonte %s) | backup .bak-%s-import"
          % (len(fila), len(aprovados_email), fonte, stamp))
    return 0


if __name__ == "__main__":
    sys.exit(main())
