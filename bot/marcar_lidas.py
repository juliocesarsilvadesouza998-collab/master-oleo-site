#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marca como lidas (\\Seen) mensagens da INBOX vindas de remetentes específicos.
Uso: python marcar_lidas.py <email1> [email2 ...]
Lê credenciais de config.json (nunca imprime senha)."""
import imaplib, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, "config.json"), encoding="utf-8") as f:
    cfg = json.load(f)
e = cfg["email"]

alvos = [a.lower() for a in sys.argv[1:]]
if not alvos:
    sys.exit("informe ao menos um remetente alvo")

m = imaplib.IMAP4_SSL(e["imap_host"], e["imap_port"])
m.login(e["usuario"], e["senha_app"])
m.select("INBOX")
total = 0
for alvo in alvos:
    typ, data = m.search(None, 'UNSEEN FROM "%s"' % alvo)
    if typ != "OK" or not data[0]:
        continue
    ids = data[0].split()
    if ids:
        m.store(b",".join(ids), "+FLAGS", "\\Seen")
        total += len(ids)
        print(f"{len(ids)} mensagem(ns) de {alvo} marcada(s) como lida(s)")
m.logout()
print(f"Total: {total}")
