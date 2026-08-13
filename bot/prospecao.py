#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Prospecção Ativa
================================
Envia emails de apresentação B2B para empresas alimentícias 
e registra os leads no leads.csv para follow-up automático.

Uso:
  python prospecao.py                    # envia para a lista (rate limit 5s)
  python prospecao.py --dry-run          # mostra o que faria sem enviar
  python prospecao.py --list             # lista empresas e emails candidatos
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, sys, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "ultima_resposta","respondido_em","respondido_por"]

# Empresas com MX válido + email padrão contato@dominio
EMPRESAS = [
    {"nome": "Alimentare Servicos", "empresa": "Alimentare Servicos de Alimentacao LTDA", "email": "contato@alimentare.com.br", "cidade": "Salto/SP", "segmento": "Restaurantes e refeicoes coletivas"},
    {"nome": "Casa Alianca Gourmet", "empresa": "Casa Alianca - Padaria Gourmet", "email": "contato@padariaalianca.com.br", "cidade": "Salto/SP", "segmento": "Padaria e confeitaria"},
    {"nome": "Restaurante Scallet", "empresa": "Restaurante e Pizzaria Scallet", "email": "contato@scallet.com.br", "cidade": "Salto/SP", "segmento": "Restaurante"},
    {"nome": "Supermercados Dias", "empresa": "Supermercados Dias", "email": "contato@jvmsupermarket.com.br", "cidade": "Salto/SP", "segmento": "Supermercado"},
    {"nome": "Sapore S.A.", "empresa": "Sapore S.A.", "email": "contato@sapore.com.br", "cidade": "Campinas/SP", "segmento": "Restaurantes (rede nacional)"},
    {"nome": "Kerry do Brasil", "empresa": "Kerry do Brasil LTDA", "email": "contato@kerry.com", "cidade": "Campinas/SP", "segmento": "Industria de ingredientes"},
    {"nome": "Bagley do Brasil", "empresa": "Bagley do Brasil Alimentos LTDA", "email": "contato@arcor.com", "cidade": "Campinas/SP", "segmento": "Industria de alimentos (snacks)"},
    {"nome": "Massima Alimentacao", "empresa": "Massima Alimentacao", "email": "contato@massimaalimentacao.com.br", "cidade": "Regiao", "segmento": "Refeicoes coletivas"},
]

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

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

def find_lead(leads, email_addr):
    for l in leads:
        if l.get("email","").strip().lower() == email_addr.strip().lower():
            return l
    return None

def tpl_apresentacao(cfg, lead):
    """Template de email de apresentação B2B (prospecção fria)."""
    g = cfg["empresa"]
    return {
        "subject": f"Coleta de óleo em {lead['cidade']} — Master Óleo",
        "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, <b>{lead['nome']}</b>!</p>
<p>Meu nome é <b>{g['nome']}</b> e atuamos na <b>coleta de óleo de cozinha usado</b> em {g['cidade']} e região.</p>
<p>Sabemos que empresas como a <b>{lead['empresa']}</b> ({lead['segmento']}) geram óleo de cozinha saturado com frequência — e o descarte correto é <b>obrigação legal</b> (PNRS, Lei 12.305/2010), além de uma questão ambiental importante.</p>
<p>Gostaria de apresentar o que fazemos:</p>
<ul>
  <li><b>Coleta programada</b> — semanal, quinzenal ou sob demanda, conforme o seu volume</li>
  <li><b>Certificado de destinação</b> emitido em <b>toda coleta</b> (comprovação legal)</li>
  <li><b>Bombonas e tambores</b> fornecidos, com troca cheia/vazia</li>
  <li><b>Para bom volume, a coleta é gratuita</b> — o valor está no destino sustentável do óleo (biodiesel)</li>
</ul>
<p>Atendemos em {g['cidade']} e região. Gostaria de saber qual o <b>volume aproximado de óleo</b> que a {lead['empresa']} gera por mês? Posso preparar uma proposta sem compromisso.</p>
<p>Se preferir, estou disponível pelo WhatsApp: <b>{g['telefone_whatsapp']}</b> — resposta rápida em horário comercial.</p>
<p>Atenciosamente,<br><b>{g['nome']}</b><br>Coleta de óleo de cozinha usado · {g['cidade']}<br>WhatsApp: {g['telefone_whatsapp']}</p>
</div>"""}

def prospecao(args):
    cfg = load_config()
    e = cfg["email"]
    if "COLOQUE" in str(e.get("usuario","")):
        sys.exit("ERRO: configure bot/config.json com email e senha de app (Gmail).")
    
    leads = read_leads()
    existing = {l.get("email","").strip().lower() for l in leads}
    
    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    smtp.login(e["usuario"], e["senha_app"].replace(" ",""))
    
    enviados = 0
    for lead_info in EMPRESAS:
        email_addr = lead_info["email"].strip().lower()
        if args.list:
            status = "✅ já cadastrado" if email_addr in existing else "⬜ novo"
            print(f"{status} | {lead_info['empresa']:40s} | {email_addr:35s} | {lead_info['cidade']}")
            continue
        
        if email_addr in existing and not args.force:
            # verifica se o lead existente deu bounce — não reenviar para inválidos
            existente = find_lead(leads, email_addr)
            if existente and existente.get("status") == "bounce":
                print(f"⏭️  Bounce anterior: {lead_info['empresa']} <{email_addr}> — pulando")
            else:
                print(f"⏭️  Já existe: {lead_info['empresa']} <{email_addr}>")
            continue
        
        if args.dry_run:
            print(f"[DRY-RUN] Enviaria para {lead_info['empresa']} <{email_addr}>")
            enviados += 1
            continue
        
        # Envia email
        tpl = tpl_apresentacao(cfg, lead_info)
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
        msg["To"] = email_addr
        msg["Subject"] = Header(tpl["subject"], "utf-8")
        msg["Message-ID"] = make_msgid()
        msg.attach(MIMEText(re.sub(r"<[^>]+>", "", tpl["html"]).strip(), "plain", "utf-8"))
        msg.attach(MIMEText(tpl["html"], "html", "utf-8"))
        
        try:
            smtp.sendmail(e["usuario"], [email_addr], msg.as_string())
            print(f"✅ Enviado: {lead_info['empresa']} <{email_addr}>")
            
            # Adiciona ao leads.csv
            new_lead = {"id": str(len(leads)+1), "nome": lead_info["nome"],
                        "empresa": lead_info["empresa"], "email": email_addr,
                        "tipo": "industria" if "industria" in lead_info["segmento"].lower() else "outro",
                        "volume": "", "fonte": "prospeccao", "status": "novo",
                        "criado_em": now_iso(), "boas_vindas_em": "",
                        "follow1_em": "", "follow2_em": "", "follow3_em": "",
                        "ultima_resposta": "", "respondido_em": "", "respondido_por": ""}
            leads.append(new_lead)
            existing.add(email_addr)
            enviados += 1
            time.sleep(5)  # rate limit
        except Exception as ex:
            print(f"❌ Falha: {lead_info['empresa']} <{email_addr}> — {str(ex)[:120]}")
    
    if not args.dry_run and not args.list and enviados > 0:
        write_leads(leads)
        print(f"\n{enviados} email(s) enviado(s) e registrado(s) no leads.csv.")
    elif args.dry_run:
        print(f"\nDRY-RUN — {enviados} envio(s) simulado(s) (nada foi enviado).")
    
    smtp.quit()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prospecção ativa Master Óleo")
    ap.add_argument("--dry-run", action="store_true", help="simula sem enviar")
    ap.add_argument("--list", action="store_true", help="lista empresas e emails candidatos")
    ap.add_argument("--force", action="store_true", help="reenvia mesmo se já cadastrado")
    args = ap.parse_args()
    prospecao(args)