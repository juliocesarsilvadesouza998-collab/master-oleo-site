#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Bot de Email com Atendente IA
============================================
Gerencia leads, envia sequência de emails e lê/responde conversas.

Uso:
  python bot_oleo.py add-lead --nome "Ana" --empresa "Alimentos X" --email ana@x.com [--tipo industria] [--volume 500]
  python bot_oleo.py send-sequence            # envia boas-vindas + follow-ups devidos
  python bot_oleo.py check-replies            # lista respostas de leads não respondidas (JSON)
  python bot_oleo.py reply --to email@x.com --subject "..." --body "..." [--in-reply-to ID]
  python bot_oleo.py leads                    # lista leads
  python bot_oleo.py test-email               # testa SMTP/IMAP com as credenciais
"""
import argparse, csv, datetime, email, imaplib, json, os, smtplib, ssl, sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid, parsedate_to_datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
REPLIES_PATH = os.path.join(BASE, "replies_pending.json")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em",
          "ultima_resposta","respondido_em","respondido_por"]

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def cfg_email(cfg):
    e = cfg["email"]
    if "COLOQUE" in str(e.get("usuario","")) or "COLOQUE" in str(e.get("senha_app","")):
        sys.exit("ERRO: configure bot/config.json com seu email e senha de app (Gmail). Veja README.")
    return e

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

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

def find_lead(leads, email):
    for l in leads:
        if l.get("email","").strip().lower() == email.strip().lower():
            return l
    return None

def smtp_send(cfg, e, to, subject, body_html, body_text=None, in_reply_to=None, references=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = references or in_reply_to
    msg.attach(MIMEText(body_text or _plain_from_html(body_html), "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html", "utf-8"))
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"])
        s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def _plain_from_html(html):
    import re
    t = re.sub(r"<br\s*/?>", "\n", html)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.strip()

def imap_connect(e):
    m = imaplib.IMAP4_SSL(e["imap_host"], e["imap_port"])
    m.login(e["usuario"], e["senha_app"])
    return m

def fetch_thread_messages(m, msg_ids):
    """Busca mensagens de um thread e devolve (msg_id, data, from, subject, body)."""
    out = []
    for i in msg_ids:
        typ, data = m.fetch(i, "(RFC822)")
        if typ != "OK" or not data or not data[0]:
            continue
        raw = data[0][1]
        msg = email.message_from_bytes(raw)
        mid = msg.get("Message-ID","").strip()
        frm = msg.get("From","")
        subj = msg.get("Subject","")
        date = msg.get("Date","")
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                    try: body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                    except Exception: pass
                    break
            if not body:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        try: body = part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", "replace")
                        except Exception: pass
                        break
        else:
            try: body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", "replace")
            except Exception: body = msg.get_payload() or ""
        out.append({"id": i.decode(), "message_id": mid, "from": frm, "subject": subj,
                    "date": date, "body": body[:4000]})
    return out

def add_lead(args):
    leads = read_leads()
    if find_lead(leads, args.email):
        print(f"Lead já existe: {args.email}")
        return
    leads.append({"id": str(len(leads)+1), "nome": args.nome, "empresa": args.empresa,
                  "email": args.email, "tipo": args.tipo, "volume": args.volume,
                  "fonte": args.fonte, "status": "novo", "criado_em": now_iso(),
                  "boas_vindas_em": "", "follow1_em": "", "follow2_em": "", "follow3_em": "",
                  "ultima_resposta": "", "respondido_em": "", "respondido_por": ""})
    write_leads(leads)
    print(f"Lead adicionado: {args.nome} <{args.email}>")

# ---------- TEMPLATES DE EMAIL ----------
def tpl_boas_vindas(cfg, lead):
    g = cfg["empresa"]
    return {
        "subject": "Compramos seu óleo de cozinha usado — Master Óleo",
        "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Obrigado pelo seu interesse na <b>{g['nome']}</b>. Segue o guia gratuito que você solicitou:</p>
<p style="text-align:center;margin:24px 0">
  <a href="{g['link_guia']}" style="background:#f59e0b;color:#3b2600;padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:bold">📘 Baixar Guia de Descarte</a>
</p>
<p>Nele você encontra o que a lei exige (PNRS), o checklist para escolher um coletor confiável e as boas práticas de acondicionamento para grandes volumes.</p>
<p><b>E uma boa notícia:</b> além de coletar com certificado de destinação, <b>compramos o óleo de cozinha usado e a gordura vegetal usada</b> — o valor é negociado conforme a quantidade e a qualidade do material.</p>
<p>Para alinhar a melhor proposta, me conta:</p>
<ul>
  <li>Qual a <b>quantidade aproximada</b> de óleo/gordura por mês (litros ou kg)?</li>
  <li>Qual o <b>tipo de material</b> (óleo de fritura, gordura vegetal, etc.)?</li>
</ul>
<p>Atendemos {g['cidade']} e região, com certificado de destinação em toda coleta.</p>
<p>Atenciosamente,<br><b>{g['nome']}</b><br>WhatsApp: {g['telefone_whatsapp']}</p>
</div>"""}

def tpl_follow(cfg, lead, n):
    g = cfg["empresa"]
    if n == 1:
        subj, html = "Seu óleo usado vale dinheiro. Vamos negociar?", f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Espero que o guia tenha sido útil. E se eu te disser que o seu óleo usado pode virar <b>dinheiro na conta</b>?</p>
<p>A {g['nome']} <b>compra óleo de cozinha usado e gordura vegetal usada</b> — o valor é negociado conforme a quantidade e a qualidade do material, com coleta programada e certificado em cada retirada.</p>
<p>Quer que eu prepare uma <b>proposta de compra sem compromisso</b>? Me responda com a quantidade aproximada (litros ou kg por mês) e o tipo de material (óleo de fritura, gordura vegetal, etc.).</p>
<p>WhatsApp: {g['telefone_whatsapp']} — resposta rápida em horário comercial.</p>
<p>Abraço,<br><b>{g['nome']}</b></p>
</div>"""
    elif n == 2:
        subj, html = "Quanto vale o óleo que a sua operação descarta?", f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Pensando na sua operação, montei um resumo de como funciona a parceria com a {g['nome']}:</p>
<ul>
  <li><b>Pagamos pelo óleo e gordura vegetal usados</b> — valor negociado por quantidade</li>
  <li><b>Coleta programada</b> (diária, semanal ou quinzenal)</li>
  <li><b>Certificado de destinação</b> emitido a cada retirada</li>
  <li><b>Bombonas</b> fornecidas com troca cheia/vazia</li>
  <li><b>Contrato simples</b>, sem fidelidade e sem burocracia</li>
</ul>
<p>Posso agendar uma conversa rápida de <b>10 minutos</b> para entender a sua quantidade e alinhar o valor? É só responder este e-mail com o melhor horário.</p>
<p>Um abraço,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    else:
        subj, html = "Último lembrete: vendemos o seu óleo usado por um bom valor", f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Este é nosso último e-mail sobre o assunto — não quero ser chato. 😊</p>
<p>Se ainda faz sentido para a sua empresa <b>vender o óleo e a gordura vegetal usados</b> com certificado em toda coleta, a proposta continua de pé: <b>negociação de valor conforme a quantidade, sem compromisso</b>.</p>
<p>É só responder este e-mail ou chamar no WhatsApp {g['telefone_whatsapp']}. Se preferir, fico à disposição para quando o momento for melhor.</p>
<p>Obrigado pela atenção!<br><b>{g['nome']}</b></p>
</div>"""
    return {"subject": subj, "html": html}

# ---------- SEQUÊNCIA ----------
def send_sequence(args):
    cfg = load_config()
    e = cfg_email(cfg)
    leads = read_leads()
    if not leads:
        print("Nenhum lead cadastrado.")
        return
    now = datetime.datetime.now().astimezone()
    env = cfg["sequencia"]
    for l in leads:
        if l["status"] in ("respondido", "bounce", "encerrado"):
            continue
        # Leads de prospecção (outbound) têm fluxo próprio (apresentação + follow-ups),
        # NÃO a sequência de boas-vindas do guia (que é para quem nos procurou).
        if str(l.get("fonte","")).startswith("prospeccao"):
            continue
        try:
            criado = datetime.datetime.fromisoformat(l["criado_em"])
        except Exception:
            continue
        dias = (now - criado).days
        # Boas-vindas (dia 0)
        if not l["boas_vindas_em"] and dias >= env["boas_vindas_dias"]:
            t = tpl_boas_vindas(cfg, l)
            mid = smtp_send(cfg, e, l["email"], t["subject"], t["html"])
            l["boas_vindas_em"] = now_iso()
            l["status"] = "sequencia"
            print(f"[{now:%d/%m %H:%M}] Boas-vindas → {l['email']}")
        # Follow-ups
        plan = [(env["follow_1_dias"], "follow1_em", 1), (env["follow_2_dias"], "follow2_em", 2), (env["follow_3_dias"], "follow3_em", 3)]
        for dia_limite, campo, n in plan:
            if l["boas_vindas_em"] and not l[campo] and dias >= dia_limite:
                t = tpl_follow(cfg, l, n)
                mid = smtp_send(cfg, e, l["email"], t["subject"], t["html"])
                l[campo] = now_iso()
                print(f"[{now:%d/%m %H:%M}] Follow-up {n} → {l['email']}")
        # Encerrar após todos os follows
        if l["boas_vindas_em"] and l["follow3_em"] and l["status"] == "sequencia":
            l["status"] = "encerrado"
    write_leads(leads)
    print("Sequência processada.")

# ---------- RESPOSTAS ----------
def check_replies(args):
    cfg = load_config()
    e = cfg_email(cfg)
    leads = read_leads()
    m = imap_connect(e)
    try:
        m.select("INBOX")
        # Busca respostas para nossos emails (qualquer email enviado por leads p/ nossa caixa, não spam, recente)
        typ, data = m.search(None, '(UNSEEN SINCE "1-Jan-2026")')
        ids = data[0].split() if typ == "OK" and data[0] else []
        msgs = fetch_thread_messages(m, ids)
    finally:
        m.logout()
    pendentes = []
    for msg in msgs:
        frm = msg["from"].lower()
        if e["usuario"].lower() in frm:
            continue  # é o próprio bot
        # extrai email do remetente
        import re
        rem = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", msg["from"])
        if not rem:
            continue
        rem_email = rem.group(0)
        lead = find_lead(leads, rem_email)
        if not lead:
            continue  # só conversamos com leads cadastrados
        pendentes.append({"to_email": rem_email, "lead_nome": lead["nome"], "lead_empresa": lead["empresa"],
                          "message_id": msg["message_id"], "subject": msg["subject"],
                          "date": msg["date"], "body": msg["body"]})
    with open(REPLIES_PATH, "w", encoding="utf-8") as f:
        json.dump(pendentes, f, ensure_ascii=False, indent=2)
    print(f"{len(pendentes)} resposta(s) de lead(s) aguardando atendimento (ver replies_pending.json)")
    for p in pendentes:
        print(f"  - {p['to_email']} | {p['subject']} | {p['date']}")

def reply(args):
    cfg = load_config()
    e = cfg_email(cfg)
    mid = smtp_send(cfg, e, args.to, args.subject, args.body.replace("\n", "<br>"),
                    in_reply_to=args.in_reply_to)
    # marca lead como respondido
    leads = read_leads()
    lead = find_lead(leads, args.to)
    if lead:
        lead["status"] = "respondido"
        lead["respondido_em"] = now_iso()
        lead["respondido_por"] = "atendente_ia"
        write_leads(leads)
    print(f"Resposta enviada para {args.to} (Message-ID: {mid})")

def test_email(args):
    cfg = load_config()
    e = cfg_email(cfg)
    print(f"Testando SMTP {e['smtp_host']}:{e['smtp_port']} com {e['usuario']}...")
    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"])
        print("SMTP OK — autenticado.")
    print("Testando IMAP...")
    m = imap_connect(e)
    m.logout()
    print("IMAP OK — conexão e login funcionando.")

def list_leads(args):
    leads = read_leads()
    if not leads:
        print("Nenhum lead.")
        return
    print(f"{'ID':<4}{'Nome':<18}{'Empresa':<22}{'Email':<30}{'Status':<12}")
    for l in leads:
        print(f"{l['id']:<4}{l['nome'][:17]:<18}{l['empresa'][:21]:<22}{l['email'][:29]:<30}{l['status']:<12}")

def main():
    p = argparse.ArgumentParser(description="Bot Master Óleo")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add-lead"); a.add_argument("--nome", required=True); a.add_argument("--empresa", required=True)
    a.add_argument("--email", required=True); a.add_argument("--tipo", default=""); a.add_argument("--volume", default=""); a.add_argument("--fonte", default="site")
    a.set_defaults(func=add_lead)
    sub.add_parser("send-sequence").set_defaults(func=send_sequence)
    sub.add_parser("check-replies").set_defaults(func=check_replies)
    r = sub.add_parser("reply"); r.add_argument("--to", required=True); r.add_argument("--subject", required=True)
    r.add_argument("--body", required=True); r.add_argument("--in-reply-to", default=None)
    r.set_defaults(func=reply)
    sub.add_parser("test-email").set_defaults(func=test_email)
    sub.add_parser("leads").set_defaults(func=list_leads)
    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
