#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera preview HTML dos templates de email."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from email_templates import tpl_apresentacao_oleo, tpl_desmoldante, tpl_followup, tpl_proposta_oleo

a = tpl_apresentacao_oleo("João", "Supermercados ABC", "Campinas")
d = tpl_desmoldante("Sr. Valdir", "Tegofort")
p = tpl_proposta_oleo("Supermercados ABC", "600", 2.00)
f = tpl_followup("João", "Supermercados ABC", 3)

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Master Óleo — Templates</title>
<style>
body{{background:#f7f5ef;font-family:Segoe UI,sans-serif;padding:20px;display:flex;flex-wrap:wrap;gap:20px}}
.card{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);width:620px}}
.card h2{{padding:16px 20px;margin:0;font-size:14px;color:#14532d;background:#e7f6ec;border-bottom:1px solid #e4e9e2}}
.card iframe{{width:100%;height:750px;border:none}}
</style></head><body>
<div class="card"><h2>📧 Apresentação — Compra de Óleo</h2><iframe srcdoc=\"{a.replace('"','&quot;')}\"></iframe></div>
<div class="card"><h2>📧 Desmoldante Concentrado</h2><iframe srcdoc=\"{d.replace('"','&quot;')}\"></iframe></div>
<div class="card"><h2>📧 Proposta Comercial</h2><iframe srcdoc=\"{p.replace('"','&quot;')}\"></iframe></div>
<div class="card"><h2>📧 Follow-up</h2><iframe srcdoc=\"{f.replace('"','&quot;')}\"></iframe></div>
</body></html>"""

out = os.path.join(os.path.dirname(__file__), "templates_preview.html")
with open(out, "w", encoding="utf-8") as o:
    o.write(html)
print(f"✅ {out}")