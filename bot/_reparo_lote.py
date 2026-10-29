#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reparo pós-crash do enviar_lote (28/10 15:3x): o batch enviou 11 emails novos
mas quebrou ao gravar (id nao numerico 'ARTEMA20261028' em leads.csv), entao
nenhum registro foi persistido. Este script:
  1) confere na pasta Sent do Gmail quais das 11 empresas receberam email hoje
     (prova de envio real) e captura o Message-ID de cada um;
  2) registra esses leads em leads.csv (via merge_write_leads com lock),
     marcando apresentacao_em e o msgid, para o proximo lote nao reenviar.
"""
import csv, datetime, email, imaplib, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from enviar_lote import load_config, merge_write_leads, read_leads, now_iso

ALVOS = [
    ("Unialimentar Comercio e Servicos de Alimentos Ltda", "unialimentar@gmail.com"),
    ("Supermercado Stabile Ltda", "supermercadostabile@gmail.com"),
    ("Supermercado M M Ltda", "contato@mmsupermercado.com.br"),
    ("Supermercado Elias Moreira Ltda", "cartoes@supermercadostiaozinho.com.br"),
    ("Supermercados Tiba Ltda", "suptiba@yahoo.com.br"),
    ("Mercado Potiguara", "mercado.potiguara@bol.com.br"),
    ("Mercado Ponto Certo", "mercado.pontocertotiete@gmail.com"),
    ("TBS Minimercado Ltda", "tbminimercado@gmail.com"),
    ("Mercado Atual Ltda", "atualsupermercado@gmail.com"),
    ("Churrascaria Boi na Brasa Sorocaba", "reserva@boinabrasasorocaba.com.br"),
    ("Uniao Supermercados (14 lojas, 30+ anos)", "sac@uniaosupermercados.com"),
]

cfg = load_config()
e = cfg["email"]

# --- 1) Ler msgids reais da pasta Sent (prova de envio) ---
sent_by_to = {}  # to_lower -> message_id
m = imaplib.IMAP4_SSL(e["imap_host"], e["imap_port"])
m.login(e["usuario"], e["senha_app"])
try:
    # localiza pasta Sent/Enviados
    typ, folders = m.list()
    sent_folder = None
    for f in (folders or []):
        fl = f.decode("utf-8", "replace").lower()
        for cand in ('"[gmail]/sent mail"', '"[gmail]/enviados"', "sent", "enviados"):
            if cand in fl:
                sent_folder = f.decode("utf-8", "replace").split(' "/" ')[-1].strip('"')
                break
        if sent_folder:
            break
    if not sent_folder:
        print("ERRO: pasta Sent nao encontrada"); sys.exit(1)
    m.select(sent_folder)
    since = (datetime.date.today()).strftime("%d-%b-%Y")
    typ, data = m.search(None, f'(SINCE "{since}")')
    ids = data[0].split() if typ == "OK" and data[0] else []
    print(f"{len(ids)} mensagens enviadas hoje na pasta Sent")
    for i in ids:
        typ, d = m.fetch(i, "(RFC822)")
        if typ != "OK" or not d or not d[0]:
            continue
        msg = email.message_from_bytes(d[0][1])
        to = (msg.get("To") or "").lower()
        mid = (msg.get("Message-ID") or "").strip()
        # extrai o endereco do To
        mt = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", to)
        if mt:
            sent_by_to[mt.group(0)] = mid
finally:
    m.logout()

# --- 2) Registrar os que de fato foram enviados ---
leads = read_leads()
existentes = {l.get("email", "").strip().lower() for l in leads}
novos = []
for nome, eml in ALVOS:
    em = eml.lower()
    if em in existentes:
        print(f"ja estava na base: {em}")
        continue
    mid = sent_by_to.get(em, "")
    if not mid:
        print(f"!! NAO ENCONTRADO na Sent (possivel nao enviado): {em}")
        continue
    novos.append({
        "nome": nome.split(" (")[0], "empresa": nome, "email": eml.strip(),
        "tipo": "outro", "volume": "", "fonte": "prospeccao-lote", "status": "novo",
        "criado_em": now_iso(), "boas_vindas_em": "", "follow1_em": "", "follow2_em": "",
        "follow3_em": "", "apresentacao_em": now_iso(), "fp1_em": "", "fp2_em": "", "fp3_em": "",
        "apresentacao_msgid": mid, "ultima_resposta": "", "respondido_em": "", "respondido_por": "",
    })
    print(f"OK {nome} <{eml}> msgid={mid[:40]}...")

if novos:
    n = merge_write_leads(novos)
    print(f"\n{n} lead(s) registrado(s) no leads.csv")
else:
    print("\nnada a registrar")