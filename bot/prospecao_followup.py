#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Follow-ups de Prospecção
========================================
Envia follow-ups automáticos para leads de prospecção que não responderam
à apresentação inicial. Sequência: apresentação (dia 0) → FP1 (dia 3) →
FP2 (dia 6) → FP3 (dia 10, último). Para assim que o lead responder.

Uso:
  python prospecao_followup.py            # envia follow-ups devidos
  python prospecao_followup.py --dry-run  # simula
  python prospecao_followup.py --status   # mostra onde cada lead está
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
          "ultima_resposta","respondido_em","respondido_por"]

# Dias para cada follow-up após a apresentação
FP_DIAS = [3, 6, 10]

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_leads(leads):
    normal = []
    for r in leads:
        normal.append({k: r.get(k, "") if r.get(k) is not None else "" for k in FIELDS})
    tmp = LEADS_PATH + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(normal)
    os.replace(tmp, LEADS_PATH)  # atômico: nunca deixa o arquivo truncado

def smtp_send(cfg, e, to, subject, html, in_reply_to=None, conn=None):
    ctx = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    msg.attach(MIMEText(_plain_from_html(html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    if conn:
        conn.sendmail(e["usuario"], [to], msg.as_string())
    else:
        with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
            s.login(e["usuario"], e["senha_app"].replace(" ",""))
            s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def _plain_from_html(html):
    """Converte HTML em texto puro com quebras de linha preservadas."""
    import re
    t = re.sub(r"<br\s*/?>", "\n", html)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.strip()

def tpl_fp(cfg, lead, n):
    """Templates de follow-up de prospecção (n=1,2,3). Todos reforçam a compra."""
    g = cfg["empresa"]
    if n == 1:
        subj = f"Re: óleo usado da {lead['empresa']} vale dinheiro"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Te escrevi sobre a <b>compra do óleo usado da {lead['empresa']}</b> — direto ao ponto:</p>
<p><b>💰 Pagamos de R$ 1,00 a R$ 2,50/litro</b>, com certificado de destinação (PNRS) em cada coleta e bombonas fornecidas. 600 L/mês = R$ 14 mil/ano de renda extra, sem custo de logística. <b>Ambiental Santos já paga R$ 3/L</b> — o mercado está aquecido e o gerador pode negociar.</p>
<p><b>🏆 Prova social — Top 3 do interior SP no pipeline:</b> A <b>Savegnago</b> (#1 do interior SP, R$ 7,98 bi), o <b>Pague Menos</b> (R$ 4,33 bi — #2) e o <b>Tauste</b> (#3) — as três maiores redes do interior estão em negociação conosco (ABRAS 2026).</p>
<p><b>🍟 Gigantes já fecham contratos de coleta:</b> O <b>McDonald's</b> fechou parceria com a Recoleo para reciclar todo óleo de suas lojas em MG, ES e DF — destinado exclusivamente a biodiesel. Rede contrata coletor, não coleta por conta própria. Se o McDonald's terceiriza, sua empresa também pode.</p>
<p><b>⚖️ PNRS obriga contrato:</b> pela Lei 12.305/2010, estabelecimentos são obrigados a contratar empresa certificada para destinação — sem contrato, sem alvará. 1 bilhão de litros/ano vão para o ralo no Brasil. Quem coleta sem certificado deixa o passivo no seu CNPJ.</p>
<p><b>⚖️ Urgência regulatória:</b> A Portaria MME/MMA nº 3/2026 obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b> — o mundo está disputando essa matéria-prima e quem fecha contrato agora garante preço e prioridade.</p>
<p><b>🏭 Mercado em ebulição:</b> A Petrobras está investindo <b>R$ 23 milhões na coleta de OGR</b> em SP e BA (2026). O diesel brasileiro já é <b>B16</b> (16% biodiesel) desde março/2026. O Brasil coleta só <b>180 milhões de litros de UCO/ano</b> — mas o potencial é de <b>600 milhões</b>. 70% do mercado está inexplorado. Quem fechar contrato agora sai na frente.</p>
<p><b>📊 Quanto vocês geram por mês (litros ou kg)?</b> Me responda esse número que eu te mando a estimativa. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    elif n == 2:
        subj = f"Re: oleo usado da {lead['empresa']} — valor de mercado R$ 1-2,50/L + urgencia 2028"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Para {lead['empresa']} transformar o óleo de fritura em renda: <b>pagamos R$ 1,00 a R$ 2,50 por litro</b> conforme qualidade e volume — valor de mercado validado pela Óleo Verde (1.200+ clientes). <b>A Ambiental Santos já paga R$ 3/L</b> — mercado em alta.</p>
<p><b>🏆 Prova social — Top 3 do interior SP no pipeline:</b>
<br><b>1º Savegnago</b> (R$ 7,98 bi — #1 interior SP, ABRAS 2026) — canal aberto conosco
<br><b>2º Pague Menos</b> (R$ 4,33 bi) — em negociação
<br><b>3º Tauste</b> — encaminhou call comercial
<br><b>Grupo Madero</b> (270 restaurantes) — 55 mil L/mês vendidos como commodity
<br><b>🍟 McDonald's</b> fechou com a Recoleo para reciclar óleo de todas as lojas em MG, ES e DF — prova de que até gigantes terceirizam a coleta.</p>
<p><b>⚖️ PNRS obriga contrato:</b> pela Lei 12.305/2010, sem contrato com coletor certificado, sem alvará. 1 bilhão de L/ano vão para o ralo. O passivo fica no seu CNPJ se o coletor não emitir certificado.</p>
<p><b>⚖️ Portaria MME/MMA nº 3/2026</b> obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b>. Quem fechar hoje garante preço antes da corrida pela matéria-prima.</p>
<p><b>🔒 Sem MTR + certificado, o passivo fica no CNPJ.</b> Nossa coleta é anti-furto: crachá, pesagem, bombona travada.</p>
<p>Para {lead['empresa']}: coleta programada, bombonas fornecidas, pagamento à vista (PIX). Um supermercado com 5 lojas gera 2.000-3.000 L/mês = R$ 48-72 mil/ano de receita extra.</p>
<p><b>Quantos litros a rede gera por mês?</b> WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    else:
            subj = f"Último contato — {lead['empresa']} pode estar gerando R$ 14,4 mil/ano em óleo"
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
    <p>Olá, {lead['nome']}.</p>
    <p><b>Última mensagem automática sobre este assunto</b> — resumo de 3 motivos para agir agora:</p>
    <p><b>💰 1. Renda extra imediata</b> — R$ 1,00 a R$ 2,50/L, pago <b>à vista (PIX)</b> na coleta. 200 L/mês = R$ 4.080/ano. 1.000 L/mês = R$ 24.000/ano. Rede de 10 supermercados dá R$ 100-150 mil/ano. <b>Ambiental Santos paga R$ 3/L — mercado aquecido. O óleo usado virou commodity de U$ 11 bi.</p>
    <p><b>⚖️ 0. PNRS obriga contrato</b> — pela Lei 12.305/2010, todo estabelecimento é OBRIGADO a contratar coletor certificado. Sem contrato sem alvará. 1 bilhão de L vão para o ralo/ano. O passivo fica no seu CNPJ.</p>
    <p><b>🏆 2. Prova social que dispensa apresentação</b> — As <b>3 maiores redes do interior</b> (Savegnago R$7,98bi, Pague Menos R$4,33bi, Tauste — ABRAS 2026) em negociação conosco. <b>GR Madero</b> vende 55 mil L/mês. McDonald's fechou com Recoleo. O Catalent confia na coleta de óleo industrial.</p>
    <p><b>⚖️ 3. jan/2028 muda o jogo</b> — A Portaria MME/MMA nº 3/2026 obriga ≥1% de óleo residual no biodiesel. O Brasil exportou 1,4 milhão de toneladas de UCO para os EUA em 2023. A <b>Petrobras está investindo R$ 23 milhões na coleta de OGR</b> em SP e BA. O diesel brasileiro subiu para <b>B16</b> em 2026. O Brasil coleta 180 milhões de litros de UCO/ano mas o potencial é 600 milhões — 70% inexplorado. Quem não tiver contrato de coleta em 2027 vai pagar caro para descartar — ou ter o passivo no CNPJ (Lei 12.305/2010).</p>
    <p><b>🔒 Anti-furto incluso:</b> coleta com crachá, bombona lacrada com trava, pesagem na hora, comprovante. Sem risco de reuso ilegal.</p>
    <p><b>Quanto a {lead['empresa']} gera por mês?</b> Responda este email com o volume aproximado (litros ou kg) + seu WhatsApp que envio a <b>proposta em até 24h</b>. Se preferir, chame direto: <b>{g['telefone_whatsapp']}</b>.</p>
    <p>Sucesso,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
    </div>"""
    return {"subject": subj, "html": html}

def main():
    ap = argparse.ArgumentParser(description="Follow-ups de prospecção")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    e = cfg["email"]
    leads = read_leads()
    now = datetime.datetime.now().astimezone()

    if args.status:
        print(f"{'Lead':<40} {'apresentacao':<20} {'FP1':<20} {'FP2':<20} {'FP3':<20} {'status'}")
        for l in leads:
            if not str(l.get("fonte","")).startswith("prospeccao"):
                continue
            print(f"{l.get('empresa','')[:38]:<40} {(l.get('apresentacao_em') or '—')[:18]:<20} "
                  f"{(l.get('fp1_em') or '—')[:18]:<20} {(l.get('fp2_em') or '—')[:18]:<20} "
                  f"{(l.get('fp3_em') or '—')[:18]:<20} {l.get('status','')}")
        return

    enviados = 0
    ctx = ssl.create_default_context()
    conn = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    conn.login(e["usuario"], e["senha_app"].replace(" ",""))
    for l in leads:
        if not str(l.get("fonte","")).startswith("prospeccao"):
            continue
        if l.get("status") in ("respondido", "bounce", "encerrado"):
            continue
        ap_em = l.get("apresentacao_em") or l.get("criado_em")
        try:
            ap_dt = datetime.datetime.fromisoformat(ap_em)
        except Exception:
            continue
        dias = (now - ap_dt).days
        for i, campo in enumerate(["fp1_em", "fp2_em", "fp3_em"], start=1):
            if not l.get(campo) and dias >= FP_DIAS[i-1]:
                tpl = tpl_fp(cfg, l, i)
                if args.dry_run:
                    print(f"[DRY-RUN] FP{i} → {l['email']} ({l.get('empresa','')})")
                else:
                    try:
                        mid = smtp_send(cfg, e, l["email"], tpl["subject"], tpl["html"],
                                        in_reply_to=l.get("apresentacao_msgid") or None, conn=conn)
                        l[campo] = now_iso()
                        print(f"✅ FP{i} → {l['email']} ({l.get('empresa','')})" + (" [thread]" if l.get("apresentacao_msgid") else ""))
                    except Exception as ex:
                        print(f"❌ FP{i} → {l['email']} — {str(ex)[:100]}")
                enviados += 1
                break  # um follow-up por lead por execução
    conn.quit()
    if not args.dry_run:
        write_leads(leads)
    print(f"\n{enviados} follow-up(s) processado(s).")

if __name__ == "__main__":
    main()