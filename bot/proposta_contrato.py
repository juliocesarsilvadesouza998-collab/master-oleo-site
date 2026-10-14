#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Gerador de PROPOSTA DE CONTRATO (PDF/HTML)
==========================================================
Gera proposta formal de coleta com PREÇOS ESCALONADOS POR VOLUME —
estratégia para buscar CONTRATOS e COLETAS MAIORES:

  * Quanto maior o volume, maior o valor/L (o gerador consolida tudo
    num contrato só em vez de vender para vários coletores)
  * Bônus de consolidação e exclusividade
  * Valores de mercado: R$ 1,00–2,50/L (óleo) — os escalões abaixo são
    referência configurável; o fechamento final é negociado.

Uso:
  python proposta_contrato.py --empresa "Savegnago" --cidade "Sertãozinho/SP" \
      --volume 3000 --periodo "out/2026" --email "atendimento@savegnago.com.br"
  python proposta_contrato.py --empresa "X" --volume 800 --pdf "C:/Users/julio/Desktop/proposta.pdf"

Gera: proposta-contrato-<empresa>-<data>.pdf (ou .html sem reportlab).
"""
import argparse, datetime, os

# Referência de mercado (R$ por litro) — escalões crescentes por volume
# para incentivar consolidação em UM contrato grande
TABELA_PRECOS = [
    (200,   1.20),   # 200–499 L/mês
    (500,   1.40),   # 500–999 L/mês
    (1000,  1.60),   # 1.000–1.999 L/mês
    (2000,  1.80),   # 2.000–4.999 L/mês
    (5000,  2.00),   # 5.000–9.999 L/mês
    (10000, 2.20),   # 10.000+ L/mês (redes/indústrias)
]

BONUS_EXCLUSIVIDADE = 0.10   # +R$ 0,10/L se fechar exclusivo
BONUS_CONSOLIDACAO = 0.05    # +R$ 0,05/L se consolidar todas as lojas/unidades


def preco_por_litro(volume):
    """Retorna (preco, faixa_desc) — o escalão é o MAIOR limiar <= volume."""
    if volume < TABELA_PRECOS[0][0]:
        return TABELA_PRECOS[0][1], f"até {TABELA_PRECOS[0][0]-1} L/mês"
    preco, faixa = TABELA_PRECOS[0]
    for lim, val in TABELA_PRECOS:
        if volume >= lim:
            preco, faixa = val, f"{lim}+ L/mês"
    # ajusta a faixa para o intervalo real
    vols = [v for v, _ in TABELA_PRECOS]
    for i, (lim, val) in enumerate(TABELA_PRECOS):
        if preco == val and volume >= lim and (i == len(TABELA_PRECOS)-1 or volume < TABELA_PRECOS[i+1][0]):
            faixa = (f"até {lim-1} L/mês" if i == 0 else f"{vols[i-1]}–{lim-1} L/mês") if i < len(TABELA_PRECOS)-1 else f"{lim}+ L/mês"
            if i == 0 and volume >= lim:
                faixa = f"{lim}–{TABELA_PRECOS[1][0]-1} L/mês"
            break
    return preco, faixa


def alinhar_escaloes(volume):
    """Retorna a linha da tabela inteira para exibição com destaque."""
    linhas = []
    vols = [v for v, _ in TABELA_PRECOS]
    for i, (lim, val) in enumerate(TABELA_PRECOS):
        faixa = (str(lim) if i == 0 else str(vols[i-1])) + "–" + str(lim-1) + (" L/mês" if lim < 10000 else " L/mês")
        if i == len(TABELA_PRECOS) - 1:
            faixa = f"{lim}+ L/mês"
        destaque = volume >= lim and (i == len(TABELA_PRECOS)-1 or volume < TABELA_PRECOS[i+1][0])
        linhas.append((faixa, val, destaque))
    return linhas


def ganho_anual(volume, preco):
    return volume * preco * 12


def gerar_html(empresa, cidade, volume, periodo, email, preco, faixa, linhas):
    ganho_mes = volume * preco
    ganho_ano = ganho_mes * 12
    hoje = datetime.date.today().strftime("%d/%m/%Y")
    validade = (datetime.date.today() + datetime.timedelta(days=15)).strftime("%d/%m/%Y")
    exclusivo = preco + BONUS_EXCLUSIVIDADE
    consolidado = preco + BONUS_CONSOLIDACAO

    rows = ""
    for f, v, dest in linhas:
        estilo = ' style="background:#e8f5e9;font-weight:700"' if dest else ""
        rows += f"<tr{estilo}><td>{f}</td><td align='center'>R$ {v:.2f}/L</td><td align='center'>R$ {volume*v:.0f}/mês</td><td align='center'>R$ {volume*v*12:.0f}/ano</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<title>Proposta de Coleta — Master Óleo × {empresa}</title>
<style>
body{{font-family:Segoe UI,Arial,sans-serif;max-width:700px;margin:30px auto;color:#1c2a21;line-height:1.6}}
h1{{color:#14532d;font-size:24px;margin-bottom:4px}}
h2{{color:#14532d;font-size:17px;margin-top:26px;border-bottom:2px solid #22a058;padding-bottom:4px}}
table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:14px}}
th{{background:#14532d;color:#fff;padding:8px;text-align:left}}
td{{padding:8px;border-bottom:1px solid #e4e9e2}}
.box{{background:#f7f5ef;border:1px solid #e4e9e2;border-radius:10px;padding:16px;margin:12px 0}}
.footer{{margin-top:30px;font-size:12px;color:#5b6b60;border-top:1px solid #e4e9e2;padding-top:12px}}
</style></head><body>

<h1>Proposta de Coleta de Óleo Usado</h1>
<p><b>Master Óleo</b> → <b>{empresa}</b> ({cidade}) · {periodo}<br>
Emitida em {hoje} · Válida até {validade}</p>

<h2>1. Volume estimado</h2>
<div class="box"><b>{volume} L/mês</b> — faixa <b>{faixa}</b><br>
Receita estimada: <b>R$ {ganho_mes:,.0f}/mês</b> · <b>R$ {ganho_ano:,.0f}/ano</b></div>

<h2>2. Tabela de valores por volume (escalonada)</h2>
<table>
<tr><th>Faixa (L/mês)</th><th>Valor/L</th><th>Receita/mês</th><th>Receita/ano</th></tr>
{rows}
</table>
<p style="font-size:13px;color:#5b6b60">Sua faixa destacada em verde. O valor final é confirmado após a 1ª pesagem.</p>

<h2>3. Bônus por compromisso</h2>
<table>
<tr><th>Condição</th><th>Bônus</th><th>Efeito no seu valor</th></tr>
<tr><td>Contrato de exclusividade (1 ano)</td><td>+R$ 0,10/L</td><td>R$ {exclusivo:.2f}/L → <b>R$ {volume*exclusivo:,.0f}/mês</b></td></tr>
<tr><td>Consolidar todas as lojas/unidades</td><td>+R$ 0,05/L</td><td>R$ {consolidado:.2f}/L → <b>R$ {volume*consolidado:,.0f}/mês</b></td></tr>
</table>

<h2>4. O que está incluído (sem custo)</h2>
<ul>
<li>Coleta programada (semana fixa) — logística por nossa conta</li>
<li>Bombonas com trava fornecidas (troca cheia/vazia)</li>
<li>Certificado de destinação (PNRS) + <b>MTR</b> a cada coleta</li>
<li><b>Relatório de Impacto Ambiental mensal</b> (água preservada + CO₂ evitada) — argumento ESG para seu relatório anual</li>
<li>Descaracterização completa de vencidos com &gt;40% de gordura (cortesia)</li>
<li>Pagamento por PIX em até 48h após cada coleta</li>
</ul>

<h2>5. Próximos passos</h2>
<ol>
<li>Confirmar o volume mensal consolidado (ou agendar <b>coleta-teste</b> de 1 mês)</li>
<li>Enviar contrato de 12 meses (renovável) com preço tabelado</li>
<li>1ª coleta em até 7 dias após assinatura</li>
</ol>

<div class="box" style="text-align:center">
<b>WhatsApp (11) 96785-9631</b> · masteroleo.eco.br<br>
Responda a este e-mail ou chame no WhatsApp para fechar a coleta-teste.
</div>

<div class="footer">Master Óleo · Compra de óleo de cozinha usado, gordura vegetal e vencidos &gt;40% para biodiesel · Salto/SP · {email}</div>
</body></html>"""


def gerar_pdf(empresa, cidade, volume, periodo, email, preco, faixa, linhas, destino=None):
    html = gerar_html(empresa, cidade, volume, periodo, email, preco, faixa, linhas)
    if not destino:
        destino = f"proposta-contrato-{empresa.lower().replace(' ','-')}-{datetime.date.today().isoformat()}.pdf"
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        c = canvas.Canvas(destino, pagesize=A4)
        w, h = A4
        c.setFillColorRGB(0.08, 0.32, 0.18)
        c.rect(0, h-25*mm, w, 25*mm, fill=1, stroke=0)
        c.setFillColorRGB(1,1,1)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(20*mm, h-13*mm, "Proposta de Coleta de Óleo Usado")
        c.setFont("Helvetica", 10)
        c.drawString(20*mm, h-19*mm, f"Master Óleo → {empresa} ({cidade}) · {periodo}")
        c.setFillColorRGB(0.15,0.15,0.15)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, h-35*mm, f"Volume: {volume} L/mês · Receita: R$ {volume*preco:,.0f}/mês (R$ {volume*preco*12:,.0f}/ano)")
        y = h-50*mm
        c.setFont("Helvetica-Bold", 11)
        c.drawString(20*mm, y, "Tabela de valores escalonada:")
        y -= 8*mm
        for f, v, dest in linhas:
            c.setFont("Helvetica-Bold" if dest else "Helvetica", 10)
            c.drawString(24*mm, y, f"{f}  →  R$ {v:.2f}/L")
            y -= 7*mm
        c.setFont("Helvetica", 10)
        c.drawString(20*mm, y-3*mm, "Inclui: coleta programada, bombonas, certificado PNRS+MTR,")
        c.drawString(20*mm, y-9*mm, "relatório ESG mensal, descaracterização cortesia, PIX 48h.")
        c.drawString(20*mm, y-18*mm, "WhatsApp (11) 96785-9631 · masteroleo.eco.br")
        c.save()
        return destino
    except ImportError:
        html_path = destino.replace(".pdf", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        return html_path


def main():
    ap = argparse.ArgumentParser(description="Proposta de contrato Master Óleo")
    ap.add_argument("--empresa", required=True)
    ap.add_argument("--cidade", default="Salto/SP")
    ap.add_argument("--volume", type=int, required=True, help="L/mês estimados")
    ap.add_argument("--periodo", default=datetime.date.today().strftime("%b/%Y"))
    ap.add_argument("--email", default="masteroleo.eco@gmail.com")
    ap.add_argument("--pdf", default=None)
    args = ap.parse_args()

    preco, faixa = preco_por_litro(args.volume)
    linhas = alinhar_escaloes(args.volume)
    destino = gerar_pdf(args.empresa, args.cidade, args.volume, args.periodo, args.email,
                        preco, faixa, linhas, args.pdf)
    print(f"Proposta gerada: {destino}")
    print(f"Volume {args.volume} L/mês → R$ {preco:.2f}/L | R$ {args.volume*preco:,.0f}/mês | R$ {args.volume*preco*12:,.0f}/ano")


if __name__ == "__main__":
    main()