#!/usr/bin/env python3
"""Check bounces.json and see which new bounces from inbox are not yet cached"""
import json, os, imaplib, ssl, email

BASE = r'C:\Users\julio\master-oleo-site\bot'

with open(os.path.join(BASE,'bounces.json'), encoding='utf-8') as f:
    cached = set(json.load(f))

print(f"Bounces já em cache: {len(cached)}")

with open(os.path.join(BASE,'config.json'), encoding='utf-8') as f:
    cfg = json.load(f)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

mail = imaplib.IMAP4_SSL(cfg['email']['imap_host'], cfg['email']['imap_port'], ssl_context=ctx)
mail.login(cfg['email']['usuario'], cfg['email']['senha_app'])
mail.select("INBOX")

# Search for delivery failure notifications
result, data = mail.search(None, '(FROM "mailer-daemon@googlemail.com")')
if data[0]:
    bmsg_ids = data[0].split()
    print(f"Mailer-Daemon messages in inbox: {len(bmsg_ids)}")
    new_bounces = []
    for mid in bmsg_ids[-20:]:
        result, msg_data = mail.fetch(mid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')[:2000]
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')[:2000]
        # Extract the target email
        import re
        emails_bounced = re.findall(r'[\w.+-]+@[\w-]+\.[\w.+-]+', body)
        for e in emails_bounced:
            if 'google.com' not in e and 'googlemail.com' not in e and e not in cached:
                if e not in new_bounces:
                    new_bounces.append(e)
                    print(f"🆕 Novo bounce: {e}")
    if not new_bounces:
        print("Nenhum bounce novo não-cacheado encontrado.")
    # Print also the last bounce email addresses
    for mid in bmsg_ids[-5:]:
        result, msg_data = mail.fetch(mid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)
        subj = msg.get('Subject', '')
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
        print(f"\n--- Last bounce: {subj[:80]}")
        print(f"Body excerpt: {body[:300]}")
else:
    print("Nenhum mailer-daemon encontrado na caixa.")

mail.logout()