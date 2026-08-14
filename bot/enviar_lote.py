#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Envio de Prospecção em Lote
===========================================
Envia emails de apresentação B2B respeitando limite diário, sem duplicar
leads já contatados e sem reenviar para endereços com bounce.

Uso:
  python enviar_lote.py --max 15          # envia até 15 emails novos hoje
  python enviar_lote.py --max 15 --dry-run  # simula
  python enviar_lote.py --status          # mostra fila: enviados/pendentes/bounces
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, sys, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
BOUNCE_CACHE = os.path.join(BASE, "bounces.json")
FIELDS = ["id","nome","empresa","email","tipo","volume","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "ultima_resposta","respondido_em","respondido_por"]

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def load_bounces():
    if os.path.exists(BOUNCE_CACHE):
        try:
            return set(json.load(open(BOUNCE_CACHE, encoding="utf-8")))
        except Exception:
            return set()
    return set()

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_leads(leads):
    with open(LEADS_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(leads)

def smtp_send(cfg, e, to_addr, subject, html):
    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    smtp.login(e["usuario"], e["senha_app"].replace(" ",""))
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    msg.attach(MIMEText(re.sub(r"<[^>]+>", "", html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    smtp.sendmail(e["usuario"], [to_addr], msg.as_string())
    smtp.quit()

def tpl_apresentacao(cfg, lead):
    g = cfg["empresa"]
    return {
        "subject": f"Compramos óleo usado em {lead['cidade']} — Master Óleo",
        "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Meu nome é <b>{g['nome']}</b> e atuamos na <b>compra de óleo de cozinha usado e gordura vegetal usada</b> em {g['cidade']} e região.</p>
<p>Sabemos que empresas como a <b>{lead['empresa']}</b> ({lead['segmento']}) geram óleo de fritura e gordura vegetal saturados com frequência — e o descarte correto é <b>obrigação legal</b> (PNRS, Lei 12.305/2010), além de uma questão ambiental importante.</p>
<p>E aqui vai a boa notícia: <b>nós compramos esse material</b>. Gostaria de apresentar o que fazemos:</p>
<ul>
  <li><b>Pagamos pelo óleo e gordura vegetal usados</b> — valor negociado conforme a quantidade e a qualidade</li>
  <li><b>Coleta programada</b> — semanal, quinzenal ou sob demanda, conforme o seu volume</li>
  <li><b>Certificado de destinação</b> emitido em <b>toda coleta</b> (comprovação legal)</li>
  <li><b>Bombonas e tambores</b> fornecidos, com troca cheia/vazia</li>
</ul>
<p>Atendemos em {g['cidade']} e região. Gostaria de saber qual a <b>quantidade aproximada</b> (litros ou kg por mês) e o <b>tipo de material</b> que a {lead['empresa']} gera? Com isso, alinho a melhor proposta de compra sem compromisso.</p>
<p>Se preferir, estou disponível pelo WhatsApp: <b>{g['telefone_whatsapp']}</b> — resposta rápida em horário comercial.</p>
<p>Atenciosamente,<br><b>{g['nome']}</b><br>Compra de óleo de cozinha usado · {g['cidade']}<br>WhatsApp: {g['telefone_whatsapp']}</p>
</div>"""}

def main():
    ap = argparse.ArgumentParser(description="Envio de prospecção em lote")
    ap.add_argument("--max", type=int, default=15, help="max de emails por execução")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    e = cfg["email"]
    bounces = load_bounces()
    leads = read_leads()
    contatados = {l.get("email","").strip().lower() for l in leads}

    if args.status:
        novos = [p for p in EMPRESAS if p["email"].strip().lower() not in contatados and p["email"].strip().lower() not in bounces]
        print(f"Fila de prospecção: {len(EMPRESAS)} empresas")
        print(f"  já contatados: {len(contatados & {p['email'].strip().lower() for p in EMPRESAS})}")
        print(f"  com bounce:    {len({p['email'].strip().lower() for p in EMPRESAS} & bounces)}")
        print(f"  pendentes:     {len(novos)}")
        for p in novos[:50]:
            print(f"    ⬜ {p['empresa']} <{p['email']}>")
        return

    # Fila: empresas com email não contatado e sem bounce
    fila = []
    for p in EMPRESAS:
        em = p["email"].strip().lower()
        if em in contatados or em in bounces:
            continue
        fila.append(p)
    fila = fila[:args.max]

    if not fila:
        print("Nenhum email pendente. Use --status para ver a fila.")
        return

    if args.dry_run:
        print(f"[DRY-RUN] Enviaria {len(fila)} email(s):")
        for p in fila:
            print(f"  {p['empresa']} <{p['email']}>")
        return

    enviados = 0
    for p in fila:
        try:
            tpl = tpl_apresentacao(cfg, p)
            smtp_send(cfg, e, p["email"], tpl["subject"], tpl["html"])
            leads.append({"id": str(len(leads)+1), "nome": p["nome"], "empresa": p["empresa"],
                          "email": p["email"], "tipo": "industria" if "industria" in p["segmento"].lower() else "outro",
                          "volume": "", "fonte": "prospeccao-lote", "status": "novo",
                          "criado_em": now_iso(), "boas_vindas_em": "",
                          "follow1_em": "", "follow2_em": "", "follow3_em": "",
                          "ultima_resposta": "", "respondido_em": "", "respondido_por": ""})
            contatados.add(p["email"].strip().lower())
            enviados += 1
            print(f"✅ {p['empresa']} <{p['email']}>")
            time.sleep(6)
        except Exception as ex:
            print(f"❌ {p['empresa']} — {str(ex)[:100]}")
    write_leads(leads)
    print(f"\n{enviados} email(s) enviados neste lote. Próximo lote: novos pendentes.")

# Lista compartilhada com prospecao.py (mantida em prospecao.py)
from prospecao import EMPRESAS

# Fila extra: empresas descobertas pelo Prospector IA (JSON, adicionado via cron)
FILA_EXTRA = os.path.join(BASE, "fila_prospeccao_extra.json")

def load_fila_extra():
    if os.path.exists(FILA_EXTRA):
        try:
            with open(FILA_EXTRA, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_fila_extra(fila):
    with open(FILA_EXTRA, "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=2)

# EMPRESAS efetivas = base + fila extra do Prospector
_EXTRA = load_fila_extra()
EMPRESAS = EMPRESAS + _EXTRA

if __name__ == "__main__":
    main()