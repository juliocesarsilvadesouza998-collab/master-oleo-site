#!/usr/bin/env python3
"""Check Gmail inbox for lead replies (last 20 emails from non-bot addresses)"""
import imaplib, email, json, os, ssl
from email.header import decode_header

BASE = r'C:\Users\julio\master-oleo-site\bot'

with open(os.path.join(BASE,'config.json'), encoding='utf-8') as f:
    cfg = json.load(f)

email_user = cfg['email']['usuario']
email_pass = cfg['email']['senha_app']

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

mail = imaplib.IMAP4_SSL(cfg['email']['imap_host'], cfg['email']['imap_port'], ssl_context=ctx)
mail.login(email_user, email_pass)
mail.select("INBOX")

result, data = mail.search(None, "UNSEEN")
unseen_ids = data[0].split() if data[0] else []
print(f"UNSEEN emails: {len(unseen_ids)}")

# Also get recent seen emails (last 10)
result, data = mail.search(None, "SEEN")
all_seen = data[0].split() if data[0] else []
recent_ids = all_seen[-15:] if len(all_seen) > 15 else all_seen

# Check unseen first
for mid in unseen_ids[-10:]:
    result, msg_data = mail.fetch(mid, "(RFC822)")
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)
    frm = msg.get('From', '')
    subj = msg.get('Subject', '')
    # Skip our own sent messages and formspree
    if email_user.split('@')[0].lower() in frm.lower() or 'formspree.io' in frm:
        continue
    print(f"\n📩 UNSEEN From: {frm}")
    print(f"   Subject: {subj}")
    # Get body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='replace')[:500]
    print(f"   Body preview: {body[:300]}")

# Check recent seen for potential replies we missed
print("\n--- RECENT SEEN ---")
for mid in reversed(recent_ids):
    result, msg_data = mail.fetch(mid, "(RFC822)")
    raw = msg_data[0][1]
    msg = email.message_from_bytes(raw)
    frm = msg.get('From', '')
    subj = msg.get('Subject', '')
    if email_user.split('@')[0].lower() in frm.lower() or 'formspree.io' in frm:
        continue
    # Get date
    dt = msg.get('Date', '')
    # Get body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', errors='replace')[:300]
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='replace')[:300]
    print(f"\n📨 From: {frm}")
    print(f"   Date: {dt}")
    print(f"   Subject: {subj}")
    print(f"   Body: {body[:200] if body else '(empty)'}")

mail.logout()