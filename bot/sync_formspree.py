#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Sync Formspree → leads.csv
=========================================
Lê as notificações de "New submission" do Formspree na caixa do bot,
extrai os campos do formulário e adiciona cada lead novo ao leads.csv
(para a sequência automática do bot_oleo.py).

Uso:
  python sync_formspree.py            # processa notificações não lidas
  python sync_formspree.py --all      # processa também notificações já lidas
  python sync_formspree.py --dry-run  # mostra o que faria sem alterar nada
"""
import argparse, csv, datetime, imaplib, json, os, re, ssl, sys, email

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em",
          "ultima_resposta","respondido_em","respondido_por"]
FROM_FILTER = "noreply@formspree.io"
SUBJECT_FILTER = "New submission"

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

# Bounces detectados automaticamente (emails que o Gmail devolveu como inválidos)
BOUNCE_CACHE = os.path.join(BASE, "bounces.json")

def load_bounces():
    if os.path.exists(BOUNCE_CACHE):
        try:
            with open(BOUNCE_CACHE, encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()

def save_bounces(bounces):
    with open(BOUNCE_CACHE, "w", encoding="utf-8") as f:
        json.dump(sorted(bounces), f, ensure_ascii=False, indent=2)

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

def find_lead(leads, email_addr):
    for l in leads:
        if l.get("email","").strip().lower() == email_addr.strip().lower():
            return l
    return None

def parse_body(body):
    """Extrai campos 'campo:\nvalor' do corpo da notificação do Formspree."""
    out = {}
    # Formato: linha com o nome do campo, depois linha(s) com o valor
    lines = [l.rstrip() for l in body.splitlines()]
    current = None
    for line in lines:
        line = line.strip()
        # rodapé da notificação do Formspree — encerra a captura
        if re.match(r"^Submitted\s", line, re.I) or "You are receiving this because" in line:
            break
        if not line:
            continue
        m = re.match(r"^([a-z_]+):$", line, re.I)
        if m:
            current = m.group(1).lower()
            out.setdefault(current, "")
            continue
        if current:
            if out.get(current):
                out[current] += "\n" + line
            else:
                out[current] = line
            # continua acumulando até o próximo campo
            continue
    return out

def process_notifications(args):
    cfg = load_config()
    e = cfg["email"]
    if "COLOQUE" in str(e.get("usuario","")):
        sys.exit("ERRO: configure bot/config.json com email e senha de app (Gmail).")
    leads = read_leads()
    existing = {l.get("email","").strip().lower() for l in leads}
    bounces = load_bounces()

    ctx = ssl.create_default_context()
    m = imaplib.IMAP4_SSL(e["imap_host"], e["imap_port"], ssl_context=ctx, timeout=30)
    m.login(e["usuario"], e["senha_app"].replace(" ",""))
    try:
        # 1) Detectar bounces: emails que o Gmail devolveu como inválidos
        m.select("INBOX")
        typ, data = m.search(None, '(FROM "mailer-daemon@googlemail.com")')
        bounce_ids = data[0].split() if typ == "OK" and data[0] else []
        for i in bounce_ids:
            typ2, msg_data = m.fetch(i, "(BODY.PEEK[TEXT])")
            if typ2 != "OK" or not msg_data or not msg_data[0]:
                continue
            body = msg_data[0][1].decode("utf-8","replace")
            for em in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", body):
                el = em.lower().strip()
                # Normaliza lixo de parsing: remove ponto final/espacos capturados
                # pelo regex (ex.: 'contato@x.com.br.' vira 'contato@x.com.br')
                while el.endswith("."):
                    el = el[:-1]
                el = el.strip()
                if "masteroleo" not in el and "gmail.com" not in el and "@" in el:
                    bounces.add(el)
        if bounces:
            save_bounces(bounces)
            # marca leads existentes com email que deu bounce
            mudou = False
            for l in leads:
                if l.get("email","").strip().lower() in bounces and l.get("status") != "bounce":
                    l["status"] = "bounce"
                    l["ultima_resposta"] = "EMAIL INVÁLIDO (bounce) — não reenviar"
                    mudou = True
            if mudou:
                write_leads(leads)
            print(f"{len(bounces)} email(s) em bounce cache (leads marcados como bounce).")

        # 2) Processar notificações do Formspree
        m.select("INBOX")
        search_cmd = '(UNSEEN FROM "%s")' % FROM_FILTER
        if args.all:
            search_cmd = '(FROM "%s")' % FROM_FILTER
        typ, data = m.search(None, search_cmd)
        ids = data[0].split() if typ == "OK" and data[0] else []
        added = 0
        for i in ids:
            typ2, msg_data = m.fetch(i, "(RFC822)")
            if typ2 != "OK" or not msg_data or not msg_data[0]:
                continue
            msg = email.message_from_bytes(msg_data[0][1])
            subj = msg.get("Subject","") or ""
            if SUBJECT_FILTER not in subj:
                continue
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8","replace")
                        except Exception:
                            body = ""
                        break
            else:
                try:
                    body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8","replace")
                except Exception:
                    body = msg.get_payload() or ""
            fields = parse_body(body)
            lead_email = (fields.get("email") or "").strip()
            if not lead_email or "@" not in lead_email:
                continue
            if lead_email.lower() in existing:
                # já cadastrado — marca como lida para não reprocessar
                if not args.dry_run:
                    m.store(i, "+FLAGS", "\\Seen")
                continue
            nome = (fields.get("nome") or fields.get("name") or "").strip() or "Cliente"
            empresa = (fields.get("empresa") or fields.get("company") or "").strip()
            tipo = (fields.get("tipo") or "").strip()
            volume = (fields.get("volume") or "").strip()
            msg_extra = (fields.get("msg") or fields.get("message") or "").strip()
            # inferir tipo a partir da mensagem se o campo não veio
            if not tipo:
                t = msg_extra.lower()
                if "indústria" in t or "industria" in t or "fabrica" in t or "fábrica" in t:
                    tipo = "industria"
                elif "restaurante" in t:
                    tipo = "restaurante"
                elif "padaria" in t:
                    tipo = "padaria"
                elif "mercado" in t or "supermercado" in t:
                    tipo = "mercado"
                else:
                    tipo = "outro"
            new_lead = {"id": str(len(leads)+1), "nome": nome, "empresa": empresa,
                        "email": lead_email, "tipo": tipo, "volume": volume,
                        "fonte": "formspree", "status": "novo", "criado_em": now_iso(),
                        "boas_vindas_em": "", "follow1_em": "", "follow2_em": "", "follow3_em": "",
                        "ultima_resposta": "", "respondido_em": "", "respondido_por": ""}
            if args.dry_run:
                print(f"[DRY-RUN] adicionaria: {nome} <{lead_email}> | {tipo} | vol: {volume} | msg: {msg_extra[:60]}")
            else:
                leads.append(new_lead)
                existing.add(lead_email.lower())
                m.store(i, "+FLAGS", "\\Seen")
                print(f"Lead adicionado do Formspree: {nome} <{lead_email}> ({tipo})")
            added += 1
        if not args.dry_run and added > 0:
            write_leads(leads)
        print(f"{added} notificação(ões) processada(s) do Formspree.")
    finally:
        m.logout()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Sync Formspree → leads.csv")
    ap.add_argument("--all", action="store_true", help="processa também notificações já lidas")
    ap.add_argument("--dry-run", action="store_true", help="mostra o que faria sem alterar nada")
    args = ap.parse_args()
    process_notifications(args)
