#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mini-scan IMAP da INBOX (sem pasta Sent, que trava) — Atendente IA.

scan_inbox.py trava na varredura da pasta Sent (caixa grande). Este script
verifica apenas a INBOX (não lidas) em segundos. Uso: python _miniscan_inbox.py
"""
import imaplib, json, os, sys, email
from email.header import decode_header

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "config.json"), encoding="utf-8") as f:
    cfg = json.load(f)

host = cfg.get("email", {}).get("imap_host", "imap.gmail.com")
user = cfg.get("email", {}).get("usuario")
pw = cfg.get("email", {}).get("senha_app")

if not (user and pw):
    print("ERRO: config.json sem credenciais IMAP"); sys.exit(1)

M = imaplib.IMAP4_SSL(host)
M.login(user, pw)
M.select("INBOX")
typ, data = M.search(None, "(UNSEEN)")
ids = data[0].split()
print(f"INBOX: {len(ids)} não lida(s)")

for i in ids[-15:]:
    t, d = M.fetch(i, "(RFC822)")
    if t != "OK" or not d or not d[0]:
        continue
    msg = email.message_from_bytes(d[0][1])
    frm = msg.get("From", "?")
    subj = str(email.header.make_header(email.header.decode_header(msg.get("Subject", "?"))))
    date = msg.get("Date", "?")
    print(f"- [{i.decode()}] {date} | {frm} | {subj[:90]}")

M.logout()