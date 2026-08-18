#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Gerador de Relatório de Impacto Ambiental (PDF)
==============================================================
Gera o relatório ESG prometido nos emails de prospecção: litros coletados,
água preservada, CO₂ evitada e certificado de destinação — com a marca do
cliente. Uso:

  python relatorio_esg.py --empresa "Rede Boa" --litros 550 --mes 8 --ano 2026
  python relatorio_esg.py --empresa "Catalent" --litros 1200 --periodo "ago/2026"
  python relatorio_esg.py --empresa "Teste" --litros 100 --pdf "C:/Users/julio/Desktop/relatorio.pdf"
"""
import argparse, datetime, os, sys

# 25 mil litros de água por litro de óleo (fonte SABESP, usada por JBS/Óleo Verde)
AGUA_POR_LITRO = 25000
# ~2,5 kg CO₂ evitada por litro de UCO destinado a biodiesel (referência setorial)
CO2_POR_LITRO = 2.5

def gerar_pdf(empresa, litros, periodo, cliente_nome, destino=None):
    """Gera o relatório em PDF (simples, sem dependências externas)."""
    agua = litros * AGUA_POR_LITRO
    co2 = litros * CO2_POR_LITRO
    hoje = datetime.date.today().strftime("%d/%m/%Y")

    # Tenta reportlab; se não houver, gera HTML que pode ser aberto no navegador
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        return _gerar_reportlab(empresa, litros, periodo, cliente_nome, agua, co2, hoje, destino)
    except ImportError:
        html = _gerar_html(empresa, litros, periodo, cliente_nome, agua, co2, hoje)
        if not destino:
            destino = os.path.join(os.path.expanduser("~"), "relatorio-esg-master-oleo.html")
        with open(destino, "w", encoding="utf-8") as f:
            f.write(html)
        return destino

def _gerar_reportlab(empresa, litros, periodo, cliente, agua, co2, hoje, destino):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas
    if not destino:
        destino = f"relatorio-esg-{empresa.lower().replace(' ','-')}-{datetime.date.today().isoformat()}.pdf"
    c = canvas.Canvas(destino, pagesize=A4)
    w, h = A4
    # Cabeçalho
    c.setFillColorRGB(0.08, 0.32, 0.18)
    c.rect(0, h-28*mm, w, 28*mm, fill=1, stroke=0)
    c.setFillColorRGB(1,1,1)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, h-15*mm, "Master Óleo — Relatório de Impacto Ambiental")
    c.setFont("Helvetica", 10)
    c.drawString(20*mm, h-21*mm, "Coleta e destinação de óleo e gordura vegetal usados · Salto/SP")
    # Corpo
    c.setFillColorRGB(0.15,0.15,0.15)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(20*mm, h-45*mm, f"Cliente: {empresa}")
    c.setFont("Helvetica", 11)
    c.drawString(20*mm, h-52*mm, f"Período: {periodo} · Emissão: {hoje}")
    c.drawString(20*mm, h-58*mm, f"Responsável pela coleta: {cliente or 'Master Óleo'}")
    # Indicadores
    y = h-72*mm
    itens = [
        ("Óleo/gordura coletados", f"{litros:,}".replace(",", ".") + " litros"),
        ("Água preservada", f"{agua:,}".replace(",", ".") + " litros (equiv. 1L óleo contamina até 25.000L água)"),
        ("CO₂ evitada", f"{co2:,.1f}".replace(",", ".") + " kg (destino: biodiesel)"),
    ]
    for titulo, valor in itens:
        c.setFillColorRGB(0.08, 0.32, 0.18)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20*mm, y, titulo)
        c.setFillColorRGB(0.15,0.15,0.15)
        c.setFont("Helvetica", 11)
        c.drawString(20*mm, y-7*mm, valor)
        y -= 22*mm
    # Conformidade
    y -= 8*mm
    c.setFillColorRGB(0.08, 0.32, 0.18)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y, "Conformidade")
    c.setFillColorRGB(0.15,0.15,0.15)
    c.setFont("Helvetica", 10)
    confs = [
        "Certificado de destinação emitido em cada coleta (PNRS, Lei 12.305/2010)",
        "MTR (Manifesto de Transporte de Resíduos) conforme Portaria MMA 280/2020",
        "Material destinado à produção de biodiesel — economia circular",
    ]
    for i, t in enumerate(confs):
        c.drawString(20*mm, y - 7*mm - i*6*mm, f"• {t}")
    # Rodapé
    c.setFont("Helvetica", 8)
    c.setFillColorRGB(0.5,0.5,0.5)
    c.drawString(20*mm, 12*mm, "Master Óleo · (11) 96785-9631 · https://masteroleo.eco.br")
    c.save()
    return destino

def _gerar_html(empresa, litros, periodo, cliente, agua, co2, hoje):
    return f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<title>Relatório de Impacto — {empresa}</title>
<style>
 body{{font-family:Segoe UI,Arial,sans-serif;max-width:700px;margin:40px auto;color:#1c2a21;padding:0 20px}}
 header{{background:#14532d;color:#fff;padding:26px 30px;border-radius:14px}}
 h1{{margin:0;font-size:22px}} header p{{margin:6px 0 0;opacity:.85;font-size:13px}}
 .card{{border:1px solid #e4e9e2;border-radius:14px;padding:24px 30px;margin-top:18px}}
 .kpi{{display:flex;gap:16px;flex-wrap:wrap}} .kpi div{{flex:1;min-width:180px;background:#f7f5ef;border-radius:12px;padding:16px}}
 .kpi b{{display:block;font-size:20px;color:#14532d}} .kpi span{{font-size:12px;color:#5b6b60}}
 h2{{font-size:16px;color:#14532d}} .ok{{color:#14532d;font-weight:600}}
 footer{{margin-top:24px;font-size:12px;color:#5b6b60;text-align:center}}
</style></head><body>
<header><h1>Master Óleo — Relatório de Impacto Ambiental</h1>
<p>Coleta e destinação de óleo e gordura vegetal usados · Salto/SP</p></header>
<div class="card"><h2>Cliente: {empresa}</h2>
<p>Período: <b>{periodo}</b> · Emissão: {hoje} · Responsável: {cliente or 'Master Óleo'}</p></div>
<div class="card"><h2>Indicadores do período</h2>
<div class="kpi">
 <div><b>{litros:,}</b><span>litros de óleo/gordura coletados</span></div>
 <div><b>{agua:,}</b><span>litros de água preservada (1L de óleo contamina até 25.000L)</span></div>
 <div><b>{co2:,.1f} kg</b><span>CO₂ evitada (destino: biodiesel)</span></div>
</div></div>
<div class="card"><h2>Conformidade</h2>
<p class="ok">✔ Certificado de destinação em cada coleta (PNRS, Lei 12.305/2010)</p>
<p class="ok">✔ MTR — Manifesto de Transporte de Resíduos (Portaria MMA 280/2020)</p>
<p class="ok">✔ Material destinado à produção de biodiesel — economia circular</p></div>
<footer>Master Óleo · (11) 96785-9631 · https://masteroleo.eco.br</footer>
</body></html>"""

def main():
    ap = argparse.ArgumentParser(description="Relatório de impacto ambiental Master Óleo")
    ap.add_argument("--empresa", required=True, help="Nome do cliente (empresa)")
    ap.add_argument("--litros", required=True, type=float, help="Litros coletados no período")
    ap.add_argument("--periodo", default=None, help='Período (ex.: "ago/2026")')
    ap.add_argument("--cliente", default="Master Óleo", help="Responsável pela coleta")
    ap.add_argument("--pdf", default=None, help="Caminho do arquivo de saída (opcional)")
    args = ap.parse_args()

    periodo = args.periodo or datetime.date.today().strftime("%m/%Y")
    out = gerar_pdf(args.empresa, args.litros, periodo, args.cliente, args.pdf)
    print(f"✅ Relatório gerado: {out}")
    print(f"   {args.litros:,.0f} L coletados → {args.litros*AGUA_POR_LITRO:,.0f} L de água preservada")
    return 0

if __name__ == "__main__":
    sys.exit(main())