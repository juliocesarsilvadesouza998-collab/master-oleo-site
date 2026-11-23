#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — CRM COMERCIAL PROFISSIONAL
=========================================
Substitui o CSV simples por um CRM com classificação de potencial,
histórico de conversas, próximo acompanhamento e indicadores.

Uso:
  python crm.py status               # resumo geral
  python crm.py leads --potencial A  # leads por potencial
  python crm.py pipeline             # funil de vendas por status
  python crm.py proximos             # próximos acompanhamentos agendados
  python crm.py quentes              # leads quentes (respondidos/negociação)
  python crm.py migrar               # migra leads.csv para o banco
  python crm.py registro <id> --nota "texto"   # adiciona nota no histórico
  python crm.py próximo <id> --data 2026-12-01 --acao "ligar"  # agenda follow-up
"""
import argparse, csv, datetime, json, os, sqlite3, sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "crm_masteroleo.db")
LEADS_CSV = os.path.join(BASE, "leads.csv")

SCHEMA = """
CREATE TABLE IF NOT EXISTS empresas (
    id TEXT PRIMARY KEY,
    nome TEXT,
    razao_social TEXT,
    email TEXT,
    telefone TEXT,
    whatsapp TEXT,
    cidade TEXT,
    uf TEXT,
    endereco TEXT,
    segmento TEXT,
    subsegmento TEXT,
    fonte TEXT,
    material TEXT,
    volume_estimado TEXT,
    potencial TEXT DEFAULT 'B',   -- A (alto), B (médio), C (baixo)
    status TEXT DEFAULT 'novo',   -- novo/contatado/respondido/negociando/contrato/encerrado
    preco_negociado TEXT,
    frequencia_coleta TEXT,
    criado_em TEXT,
    ultimo_contato TEXT,
    proxima_acao TEXT,
    proximo_contato_em TEXT,
    notas TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS historico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id TEXT,
    data TEXT,
    tipo TEXT,        -- email/whatsapp/telefone/nota/visita
    conteudo TEXT,
    FOREIGN KEY (empresa_id) REFERENCES empresas(id)
);

CREATE INDEX IF NOT EXISTS idx_emp_status ON empresas(status);
CREATE INDEX IF NOT EXISTS idx_emp_potencial ON empresas(potencial);
CREATE INDEX IF NOT EXISTS idx_hist_emp ON historico(empresa_id);
"""


def conectar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def migrar():
    """Migra leads.csv para o CRM (idempotente: não duplica)."""
    if not os.path.exists(LEADS_CSV):
        print("leads.csv não encontrado.")
        return 0
    con = conectar()
    com = con.cursor()
    com.execute("SELECT COUNT(*) FROM empresas")
    existentes = com.fetchone()[0]
    print(f"CRM já tem {existentes} registros")

    added = 0
    with open(LEADS_CSV, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        lid = r.get("id") or str(abs(hash(r.get("email", ""))) % 10**10)
        com.execute("SELECT id FROM empresas WHERE id=?", (lid,))
        if com.fetchone():
            continue
        com.execute(
            """INSERT INTO empresas (id, nome, email, cidade, segmento, fonte,
               status, criado_em, ultimo_contato, volume_estimado, potencial)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (lid, r.get("empresa") or r.get("nome", ""), r.get("email", ""),
             r.get("cidade", ""), r.get("segmento", ""), r.get("fonte", ""),
             r.get("status", "novo"), r.get("criado_em", ""),
             r.get("respondido_em") or r.get("apresentacao_em", ""),
             r.get("volume", ""), "B")
        )
        # Histórico: apresentação enviada
        if r.get("apresentacao_em"):
            com.execute(
                "INSERT INTO historico (empresa_id, data, tipo, conteudo) VALUES (?,?,?,?)",
                (lid, r.get("apresentacao_em"), "email", "Apresentação enviada"))
        if r.get("respondido_em"):
            com.execute(
                "INSERT INTO historico (empresa_id, data, tipo, conteudo) VALUES (?,?,?,?)",
                (lid, r.get("respondido_em"), "email", "Lead respondeu: " +
                 (r.get("ultima_resposta", "") or "")[:200]))
        added += 1
    con.commit()
    total = com.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    con.close()
    print(f"Migrados: {added} novos | Total no CRM: {total}")
    return added


def status():
    con = conectar()
    com = con.cursor()
    total = com.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    por_status = dict(com.execute(
        "SELECT status, COUNT(*) FROM empresas GROUP BY status").fetchall())
    por_potencial = dict(com.execute(
        "SELECT potencial, COUNT(*) FROM empresas GROUP BY potencial").fetchall())
    con.close()
    print(f"=== CRM MASTER ÓLEO ===")
    print(f"Total empresas: {total}")
    print(f"\nPor status:")
    for k, v in sorted(por_status.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")
    print(f"\nPor potencial:")
    for k in "ABC":
        print(f"  {k}: {por_potencial.get(k, 0)}")


def pipeline():
    con = conectar()
    com = con.cursor()
    etapas = ["novo", "contatado", "respondido", "negociando", "contrato", "encerrado"]
    print("=== FUNIL DE VENDAS ===")
    for e in etapas:
        n = com.execute("SELECT COUNT(*) FROM empresas WHERE status=?", (e,)).fetchone()[0]
        bar = "#" * min(n, 30)
        print(f"  {e:12s} {n:4d} {bar}")
    total = com.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    print(f"\n  Total: {total}")
    con.close()


def quentes():
    con = conectar()
    com = con.cursor()
    rows = com.execute(
        """SELECT * FROM empresas WHERE status IN ('respondido','negociando')
           OR potencial='A' ORDER BY ultimo_contato DESC LIMIT 25""").fetchall()
    print("=== LEADS QUENTES ===")
    for r in rows:
        print(f"  [{r['potencial']}] {r['nome'][:40]:40s} | {r['status']:10s} | "
              f"{r['cidade'] or '-'} | {r['email'] or '-'}")
    con.close()


def proximos():
    con = conectar()
    com = con.cursor()
    hoje = datetime.date.today().isoformat()
    rows = com.execute(
        """SELECT * FROM empresas WHERE proximo_contato_em IS NOT NULL
           AND proximo_contato_em <= ? AND status NOT IN ('encerrado','contrato')
           ORDER BY proximo_contato_em LIMIT 25""", (hoje,)).fetchall()
    print(f"=== PRÓXIMOS ACOMPANHAMENTOS (vencidos até {hoje}) ===")
    for r in rows:
        print(f"  {r['proximo_contato_em']} | {r['proxima_acao'] or 'follow-up'} | {r['nome'][:40]}")
    con.close()


def leads(potencial=None):
    con = conectar()
    com = con.cursor()
    q = "SELECT * FROM empresas"
    args = ()
    if potencial:
        q += " WHERE potencial=?"
        args = (potencial,)
    rows = com.execute(q + " ORDER BY criado_em DESC LIMIT 50", args).fetchall()
    print(f"=== LEADS {'potencial ' + potencial if potencial else ''} ===")
    for r in rows:
        print(f"  {r['criado_em'][:10] if r['criado_em'] else '—'} | "
              f"{r['nome'][:38]:38s} | {r['segmento'][:22]:22s} | {r['cidade'] or '—'}")
    con.close()


def registrar_nota(empresa_id, nota):
    con = conectar()
    com = con.cursor()
    agora = datetime.datetime.now().isoformat()
    com.execute("INSERT INTO historico (empresa_id, data, tipo, conteudo) VALUES (?,?,?,?)",
                (empresa_id, agora, "nota", nota))
    com.execute("UPDATE empresas SET notas = notas || ? WHERE id=?",
                (nota + "\n", empresa_id))
    con.commit()
    con.close()
    print(f"Nota registrada para {empresa_id}")


def agendar(empresa_id, data, acao):
    con = conectar()
    com = con.cursor()
    com.execute("UPDATE empresas SET proximo_contato_em=?, proxima_acao=? WHERE id=?",
                (data, acao, empresa_id))
    con.commit()
    con.close()
    print(f"Agendado: {acao} em {data} para {empresa_id}")


def buscar(termo):
    con = conectar()
    com = con.cursor()
    rows = com.execute(
        "SELECT * FROM empresas WHERE nome LIKE ? OR email LIKE ? OR cidade LIKE ? OR segmento LIKE ? LIMIT 20",
        (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")).fetchall()
    print(f"=== BUSCA: {termo} ===")
    for r in rows:
        print(f"  [{r['potencial']}] {r['nome'][:40]:40s} | {r['status']:10s} | "
              f"{r['cidade'] or '-'} | {r['email'] or '-'}")
        if r["proximo_contato_em"]:
            print(f"      → próximo: {r['proximo_contato_em']} ({r['proxima_acao']})")
    if not rows:
        print("  Nada encontrado.")
    con.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("comando", choices=["status", "migrar", "pipeline", "quentes",
                                        "proximos", "leads", "registro", "proximo", "buscar"])
    ap.add_argument("arg", nargs="*")
    ap.add_argument("--potencial", default=None)
    ap.add_argument("--nota", default=None)
    ap.add_argument("--data", default=None)
    ap.add_argument("--acao", default="follow-up")
    args = ap.parse_args()

    if args.comando == "migrar":
        migrar()
    elif args.comando == "status":
        status()
    elif args.comando == "pipeline":
        pipeline()
    elif args.comando == "quentes":
        quentes()
    elif args.comando == "proximos":
        proximos()
    elif args.comando == "leads":
        leads(args.potencial)
    elif args.comando == "registro":
        registrar_nota(args.arg[0], args.nota or "")
    elif args.comando == "proximo":
        agendar(args.arg[0], args.data or datetime.date.today().isoformat(), args.acao)
    elif args.comando == "buscar":
        buscar(" ".join(args.arg))


if __name__ == "__main__":
    main()
