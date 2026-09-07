#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Varredura manual da caixa de entrada — Master Óleo
==================================================
Lista mensagens NÃO LIDAS da INBOX (e, opcionalmente, as últimas N de todas)
e tenta correlacionar com leads por:
  1) remetente == email do lead  (filtro padrão do check-replies)
  2) References / In-Reply-To batendo com Message-ID enviado (apresentacao_msgid
     em leads.csv ou qualquer msgid de mensagens enviadas na pasta Sent)
  3) assunto contendo nome da empresa do lead

Uso: python scan_inbox.py [--tudo] [--dias 30]
"""
import argparse, csv, datetime, email, imaplib, json, os, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def fetch_msgs(m, ids):
    out = []
    for i in ids:
        typ, data = m.fetch(i, "(RFC822)")
        if typ != "OK" or not data or not data[0]:
            continue
        msg = email.message_from_bytes(data[0][1])
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    try:
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                    except Exception:
                        pass
                    break
            if not body:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        try:
                            body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                        except Exception:
                            pass
                        break
        else:
            try:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")
            except Exception:
                body = msg.get_payload() or ""
        out.append({
            "uid": i.decode(),
            "message_id": (msg.get("Message-ID") or "").strip(),
            "from": msg.get("From", ""),
            "to": msg.get("To", ""),
            "subject": msg.get("Subject", ""),
            "date": msg.get("Date", ""),
            "in_reply_to": (msg.get("In-Reply-To") or "").strip(),
            "references": (msg.get("References") or "").strip(),
            "body": re.sub(r"\s+", " ", body)[:1500],
        })
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tudo", action="store_true", help="varrer todas as mensagens (não só não lidas)")
    ap.add_argument("--dias", type=int, default=45)
    args = ap.parse_args()

    cfg = load_config()
    e = cfg["email"]
    leads = read_leads()
    leads_by_email = {l["email"].strip().lower(): l for l in leads}
    sent_msgids = set()
    for l in leads:
        if l.get("apresentacao_msgid"):
            sent_msgids.add(l["apresentacao_msgid"].strip().lower())

    m = imaplib.IMAP4_SSL(e["imap_host"], e["imap_port"])
    m.login(e["usuario"], e["senha_app"])
    try:
        m.select("INBOX")
        since = (datetime.date.today() - datetime.timedelta(days=args.dias)).strftime("%d-%b-%Y")
        if args.tudo:
            typ, data = m.search(None, f'(SINCE "{since}")')
        else:
            typ, data = m.search(None, f'(UNSEEN SINCE "{since}")')
        ids = data[0].split() if typ == "OK" and data[0] else []
        msgs = fetch_msgs(m, ids)
        # também busca msgids enviados na pasta Sent para correlação de thread
        try:
            typf, folders = m.list()
            sent_folder = None
            for f in (folders or []):
                fl = f.decode("utf-8", "replace").lower()
                for cand in ('"[gmail]/sent mail"', '"[gmail]/enviados"', 'sent', 'enviados'):
                    if cand in fl:
                        sent_folder = f.decode("utf-8", "replace").split(' "/" ')[-1].strip('"')
                        break
                if sent_folder:
                    break
            if sent_folder:
                m.select(sent_folder)
                typ, sdata = m.search(None, f'(SINCE "{since}")')
                sids = sdata[0].split() if typ == "OK" and sdata[0] else []
                for sm in fetch_msgs(m, sids):
                    if sm["message_id"]:
                        sent_msgids.add(sm["message_id"].strip().lower())
            else:
                print("(aviso: pasta Sent/Enviados não encontrada)")
        except Exception as exc:
            print(f"(aviso: não foi possível ler Sent Mail: {exc})")
        m.select("INBOX")
    finally:
        m.logout()

    print(f"== Caixa: {len(msgs)} mensagem(ns) não lida(s)/recente(s) | {len(leads)} leads | {len(sent_msgids)} msgids enviados ==")
    print()
    for msg in msgs:
        frm = msg["from"]
        rem = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", frm)
        rem_email = rem.group(0).lower() if rem else ""
        is_self = e["usuario"].lower() in frm.lower()
        # correlação 1: remetente == lead
        lead = leads_by_email.get(rem_email)
        # correlação 2: thread bate com msgid enviado
        refs = (msg["references"] + " " + msg["in_reply_to"]).lower()
        thread_hit = any(mid in refs for mid in sent_msgids if mid)
        # correlação 3: assunto menciona empresa do lead
        subj_hit = None
        for l in leads:
            emp = l.get("empresa", "")
            if emp and emp.lower() in msg["subject"].lower():
                subj_hit = l
                break
        status = []
        if is_self:
            status.append("ENVIADO PELO PRÓPRIO BOT")
        else:
            if lead:
                status.append(f"LEAD DIRETO: {lead['empresa']}")
            if thread_hit:
                status.append("THREAD BATE COM MSG ENVIADA")
            if subj_hit:
                status.append(f"ASSUNTO CITA EMPRESA: {subj_hit['empresa']}")
            if not status:
                status.append("SEM CORRELAÇÃO")
        print(f"--- [{msg['date']}] {frm}")
        print(f"    Assunto: {msg['subject']}")
        print(f"    In-Reply-To: {msg['in_reply_to'][:80]}")
        print(f"    References: {msg['references'][:120]}")
        print(f"    => {'; '.join(status)}")
        if not is_self:
            print(f"    Corpo: {msg['body'][:300]}")
        print()

if __name__ == "__main__":
    main()
