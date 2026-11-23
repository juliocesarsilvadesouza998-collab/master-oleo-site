#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o painel comercial HTML da Master Óleo (indicadores e leads)."""
import csv, datetime, json, os, sqlite3
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "crm_masteroleo.db")
OUT = os.path.join(BASE, "painel_comercial.html")

def gerar():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    com = con.cursor()

    total = com.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    por_status = dict(com.execute("SELECT status, COUNT(*) FROM empresas GROUP BY status").fetchall())
    por_pot = dict(com.execute("SELECT potencial, COUNT(*) FROM empresas GROUP BY potencial").fetchall())
    por_seg = dict(com.execute("SELECT COALESCE(NULLIF(segmento,''),'não-classificado'), COUNT(*) FROM empresas GROUP BY segmento ORDER BY COUNT(*) DESC LIMIT 10").fetchall())

    respondidos = com.execute("SELECT COUNT(*) FROM empresas WHERE status='respondido' OR status='negociando'").fetchone()[0]
    negociando = com.execute("SELECT COUNT(*) FROM empresas WHERE status='negociando'").fetchone()[0]
    em_contrato = com.execute("SELECT COUNT(*) FROM empresas WHERE status='contrato'").fetchone()[0]

    # leads quentes
    quentes = com.execute(
        """SELECT nome, cidade, status, potencial, notas, ultimo_contato, proximo_contato_em, proxima_acao
           FROM empresas WHERE status IN ('respondido','negociando') OR potencial='A'
           ORDER BY ultimo_contato DESC LIMIT 30""").fetchall()

    con.close()

    hoje = datetime.date.today().strftime("%d/%m/%Y")
    pct_resp = round(respondidos / total * 100, 1) if total else 0

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Painel Comercial — Master Óleo</title><style>
:root{{--green:#14532d;--amber:#f59e0b;--ink:#1c2a21;--muted:#5b6b60;--paper:#faf9f4;--line:#dce2d7}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Segoe UI",Arial,sans-serif;padding:28px}}
h1{{font-size:26px;color:var(--green);margin:0 0 4px}}h1 small{{color:var(--muted);font-size:13px;font-weight:400}}
.sub{{color:var(--muted);font-size:13px;margin-bottom:22px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:26px}}
.kpi{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px}}
.kpi .v{{font-size:28px;font-weight:800;color:var(--green)}}
.kpi .l{{font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.4px;margin-top:4px}}
.kpi.hot .v{{color:#b91c1c}}
h2{{font-size:17px;margin:22px 0 10px;color:var(--green)}}
table{{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;font-size:13px}}
th,td{{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line)}}
th{{background:var(--green);color:#fff;font-size:11.5px;text-transform:uppercase;letter-spacing:.5px}}
tr:last-child td{{border-bottom:none}}
.badge{{display:inline-block;padding:3px 10px;border-radius:999px;font-size:11px;font-weight:700}}
.b-A{{background:#e7f6ec;color:#14532d}}.b-B{{background:#fdf3e0;color:#92610f}}.b-C{{background:#f1f1f1;color:#58675e}}
.s-respondido{{background:#fde8e8;color:#b91c1c}}.s-negociando{{background:#fdf3e0;color:#92610f}}.s-novo{{background:#e7f6ec;color:#14532d}}.s-contrato{{background:#14532d;color:#fff}}
.seg-bar{{height:14px;border-radius:7px;background:var(--green);display:inline-block;vertical-align:middle;margin-right:8px}}
.footer{{margin-top:24px;color:var(--muted);font-size:11.5px;text-align:center}}
</style></head><body>
<h1>💼 Painel Comercial Master Óleo <small>· {hoje}</small></h1>
<div class="sub">Inteligência comercial · CRM {total} empresas · Backlog direto do banco de dados</div>

<div class="kpis">
  <div class="kpi"><div class="v">{total}</div><div class="l">Empresas no CRM</div></div>
  <div class="kpi"><div class="v">{por_pot.get('A',0)}</div><div class="l">Potencial alto</div></div>
  <div class="kpi"><div class="v">{por_pot.get('B',0)}</div><div class="l">Potencial médio</div></div>
  <div class="kpi hot"><div class="v">{respondidos}</div><div class="l">Leads quentes</div></div>
  <div class="kpi hot"><div class="v">{negociando}</div><div class="l">Em negociação</div></div>
  <div class="kpi"><div class="v">{em_contrato}</div><div class="l">Contratos</div></div>
  <div class="kpi"><div class="v">{pct_resp}%</div><div class="l">Taxa resposta</div></div>
</div>

<h2>📊 Leads quentes / potenciais prioritários</h2>
<table><tr><th>Empresa</th><th>Cidade</th><th>Status</th><th>Pot</th><th>Próximo contato</th><th>Ação</th><th>Nota</th></tr>
"""
    for r in quentes:
        nome = (r["nome"] or "")[:36]
        cidade = (r["cidade"] or "—")[:22]
        st = r["status"] or ""
        pot = r["potencial"] or "B"
        prox = (r["proximo_contato_em"] or "—")[:10]
        acao = (r["proxima_acao"] or "follow-up")[:14]
        nota = (r["notas"] or "").replace("\n", " ")[:70]
        html += f"""<tr><td><b>{nome}</b></td><td>{cidade}</td>
<td><span class="badge s-{st}">{st}</span></td>
<td><span class="badge b-{pot}">{pot}</span></td><td>{prox}</td><td>{acao}</td><td style="color:var(--muted)">{nota}</td></tr>"""
    html += "</table>"

    html += f"""
<h2>🏭 Segmentos na base</h2>
<table><tr><th>Segmento</th><th>Empresas</th><th></th></tr>"""
    max_seg = max(por_seg.values()) if por_seg else 1
    for seg, n in por_seg.items():
        w = int(n / max_seg * 100)
        html += f"""<tr><td>{seg[:42]}</td><td>{n}</td><td><span class="seg-bar" style="width:{w}%"></span>{w}%</td></tr>"""
    html += "</table>"

    html += """
<div class="footer">Gerado automaticamente pelo CRM Master Óleo · python painel_comercial.py</div>
</body></html>"""

    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Painel gerado: {OUT}")


if __name__ == "__main__":
    gerar()
