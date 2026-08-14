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
FIELDS = ["id","nome","empresa","email","tipo","volume","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em",
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
    with open(LEADS_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(leads)

def smtp_send(cfg, e, to, subject, html, in_reply_to=None):
    ctx = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    msg.attach(MIMEText(re.sub(r"<[^>]+>", "", html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"].replace(" ",""))
        s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def tpl_fp(cfg, lead, n):
    """Templates de follow-up de prospecção (n=1,2,3). Todos reforçam a compra."""
    g = cfg["empresa"]
    if n == 1:
        subj = f"Master Óleo — proposta de compra do óleo da {lead['empresa']}"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Semana passada apresentei a <b>{g['nome']}</b> para a {lead['empresa']} — a proposta de <b>compra do óleo de cozinha usado e da gordura vegetal</b> gerados na operação de vocês.</p>
<p>Sei que a rotina de uma empresa do segmento de {lead['segmento'].lower()} é corrida, então deixo aqui o resumo do que isso significa na prática:</p>
<ul>
  <li><b>Renda com um resíduo</b>: o óleo usado passa a gerar receita, com valor negociado por quantidade</li>
  <li><b>Conformidade</b>: certificado de destinação em cada coleta (PNRS, Lei 12.305/2010)</li>
  <li><b>Zero preocupação logística</b>: coleta programada + bombonas fornecidas</li>
</ul>
<p>Para alinharmos o valor, só preciso de duas informações: <b>quantos litros (ou kg) por mês</b> e o <b>tipo de material</b>. Me responde por aqui ou no WhatsApp {g['telefone_whatsapp']}?</p>
<p>Atenciosamente,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    elif n == 2:
        subj = f"Re: compra de óleo usado — {lead['empresa']} × Master Óleo"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Entendo que o momento pode não ser o ideal, mas reforço que a proposta segue disponível: <b>compramos o óleo e a gordura vegetal usados</b> da {lead['empresa']} com coleta programada e certificado em toda retirada.</p>
<p>Para empresas que geram <b>mais de 500 litros por mês</b>, além do pagamento pelo material, a coleta e a logística são totalmente por nossa conta — a sua equipe não precisa se preocupar com nada.</p>
<p>Vale uma conversa rápida? Posso te passar uma estimativa de valor em poucos minutos se você me disser a quantidade mensal aproximada. WhatsApp: {g['telefone_whatsapp']}.</p>
<p>Atenciosamente,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    else:
        subj = f"Último contato sobre a compra do óleo — {g['nome']}"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Este é nosso último e-mail sobre a proposta de <b>compra do óleo usado</b> da {lead['empresa']} — não quero ocupar sua caixa de entrada sem necessidade.</p>
<p>Se o tema for relevante em algum momento, a porta continua aberta: <b>pagamos pelo óleo e gordura vegetal usados</b>, com certificado de destinação e coleta programada. Basta chamar no WhatsApp {g['telefone_whatsapp']} ou responder este e-mail.</p>
<p>Obrigado pela atenção.<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
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
                        mid = smtp_send(cfg, e, l["email"], tpl["subject"], tpl["html"])
                        l[campo] = now_iso()
                        print(f"✅ FP{i} → {l['email']} ({l.get('empresa','')})")
                    except Exception as ex:
                        print(f"❌ FP{i} → {l['email']} — {str(ex)[:100]}")
                enviados += 1
                break  # um follow-up por lead por execução
    if not args.dry_run:
        write_leads(leads)
    print(f"\n{enviados} follow-up(s) processado(s).")

if __name__ == "__main__":
    main()