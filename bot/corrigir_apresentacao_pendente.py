#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correção pontual: envia apresentação inicial para leads 'novo' que
receberam FP1 sem apresentação (bug de fallback criado_em)."""
import csv, datetime, json, os, ssl, smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from prospecao import tpl_apresentacao, _plain_from_html

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
          "ultima_resposta","respondido_em","respondido_por"]

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def smtp_send(cfg, e, to, subject, html):
    ctx = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    msg.attach(MIMEText(_plain_from_html(html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"].replace(" ",""))
        s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def main():
    cfg = json.load(open(CONFIG_PATH, encoding="utf-8"))
    e = cfg["email"]
    leads = list(csv.DictReader(open(LEADS_PATH, newline="", encoding="utf-8")))
    alvos = [l for l in leads if l.get("status") == "novo" and not l.get("apresentacao_em") and not l.get("boas_vindas_em")]
    if not alvos:
        print("Nenhum lead parado.")
        return
    for l in alvos:
        try:
            tpl = tpl_apresentacao(cfg, l)
            mid = smtp_send(cfg, e, l["email"], tpl["subject"], tpl["html"])
            l["apresentacao_em"] = now_iso()
            l["apresentacao_msgid"] = mid
            # FP1 enviado antes da apresentação (fallback criado_em) — reseta p/ contar da apresentação real
            if l.get("fp1_em") and l.get("criado_em") and l.get("apresentacao_em"):
                l["fp1_em"] = ""
            print(f"✅ Apresentação → {l['email']} ({l.get('empresa','')}) msgid={mid}")
        except Exception as ex:
            print(f"❌ {l['email']} — {str(ex)[:120]}")
    tmp = LEADS_PATH + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(leads)
    os.replace(tmp, LEADS_PATH)
    print("leads.csv atualizado.")

if __name__ == "__main__":
    main()
