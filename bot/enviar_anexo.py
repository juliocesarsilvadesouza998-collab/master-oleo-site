#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Envia email COM ANEXO via SMTP (Gmail).
Uso:
  python enviar_anexo.py --to email@x.com --subject "..." --body-arquivo corpo.html \
      --anexo bot/proposta-contrato-x-2026-10-14.html [--cc cc@x.com] [--in-reply-to ID]
"""
import argparse, os, ssl, smtplib, sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

def load_config():
    import json
    with open(os.path.join(BASE, "config.json"), encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True)
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body-arquivo", required=True, help="arquivo com corpo HTML")
    ap.add_argument("--anexo", required=True, help="arquivo a anexar")
    ap.add_argument("--cc", default=None)
    ap.add_argument("--in-reply-to", default=None)
    args = ap.parse_args()

    cfg = load_config()
    e = cfg["email"]
    with open(args.body_arquivo, encoding="utf-8") as f:
        corpo_html = f.read()

    ctx = ssl.create_default_context()
    msg = MIMEMultipart("mixed")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = args.to
    if args.cc:
        msg["Cc"] = args.cc
    msg["Subject"] = Header(args.subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    if args.in_reply_to:
        msg["In-Reply-To"] = args.in_reply_to
        msg["References"] = args.in_reply_to

    # corpo
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(corpo_html.replace("<br>", "\n").replace("</p>", "\n\n").replace("<li>", "- "), "plain", "utf-8"))
    alt.attach(MIMEText(corpo_html, "html", "utf-8"))
    msg.attach(alt)

    # anexo
    nome_anexo = os.path.basename(args.anexo)
    with open(args.anexo, "rb") as f:
        part = MIMEApplication(f.read(), Name=nome_anexo)
    part["Content-Disposition"] = f'attachment; filename="{nome_anexo}"'
    msg.attach(part)

    dests = [args.to] + ([args.cc] if args.cc else [])
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"].replace(" ", ""))
        s.sendmail(e["usuario"], dests, msg.as_string())
    print(f"Enviado com anexo {nome_anexo} para {args.to} (cc={args.cc})")

if __name__ == "__main__":
    main()