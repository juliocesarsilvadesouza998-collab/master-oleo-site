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
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em",
          "ultima_resposta","respondido_em","respondido_por"]

# Empresas com MX válido + email (corrigido onde houve bounce)
# Fontes: econodata rankings 2026 (Campinas, Indaiatuba, Itu, Sorocaba) + sites oficiais
EMPRESAS = [
    # --- Salto/região (base) ---
    {"nome": "Alimentare Servicos", "empresa": "Alimentare Servicos de Alimentacao LTDA", "email": "contato@alimentare.com.br", "cidade": "Salto/SP", "segmento": "Restaurantes e refeicoes coletivas"},
    {"nome": "Casa Alianca Gourmet", "empresa": "Casa Alianca - Padaria Gourmet", "email": "contato@padariaalianca.com.br", "cidade": "Salto/SP", "segmento": "Padaria e confeitaria"},
    {"nome": "Restaurante Scallet", "empresa": "Restaurante e Pizzaria Scallet", "email": "pedidos@scallet.com.br", "cidade": "Salto/SP", "segmento": "Restaurante"},
    {"nome": "Supermercados Dias", "empresa": "Supermercados Dias", "email": "contato@jvmsupermarket.com.br", "cidade": "Salto/SP", "segmento": "Supermercado"},
    {"nome": "Massima Alimentacao", "empresa": "Massima Alimentacao", "email": "contato@massimaalimentacao.com.br", "cidade": "Regiao", "segmento": "Refeicoes coletivas"},
    # --- Campinas (grandes) ---
    {"nome": "Sapore S.A.", "empresa": "Sapore S.A.", "email": "contato@sapore.com.br", "cidade": "Campinas/SP", "segmento": "Restaurantes (rede nacional)"},
    {"nome": "Kerry do Brasil", "empresa": "Kerry do Brasil LTDA", "email": "dpo.kerry@lbca.com.br", "cidade": "Campinas/SP", "segmento": "Industria de ingredientes"},
    {"nome": "Bagley do Brasil", "empresa": "Bagley do Brasil Alimentos LTDA", "email": "aquiarcor@arcor.com", "cidade": "Campinas/SP", "segmento": "Industria de alimentos (snacks)"},
    {"nome": "Alimentare Nutricao", "empresa": "Alimentare Nutricao e Servicos LTDA", "email": "contato@redealimentare.com.br", "cidade": "Campinas/SP", "segmento": "Refeicoes coletivas (1 mi refeicoes/mes)"},
    {"nome": "Higa Atacado", "empresa": "Higa Produtos Alimenticios LTDA", "email": "contato@higa.com.br", "cidade": "Campinas/SP", "segmento": "Atacado e varejo de alimentos"},
    # --- Indaiatuba (grandes) ---
    {"nome": "Kelco Pet Care", "empresa": "Kelco Industrial Produtos Animais LTDA", "email": "info@kelcopetcare.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de alimentos pet"},
    {"nome": "Palacios Brasil", "empresa": "Palacios Brasil Comercializacao de Alimentos LTDA", "email": "palacios@palaciosbrasil.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de embutidos e frios"},
    {"nome": "Crista Margarina", "empresa": "Crista Industria e Comercio LTDA", "email": "faleconosco@cristamargarina.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de gorduras e margarinas"},
    {"nome": "Sumerbol Supermercados", "empresa": "Sumerbol Supermercados LTDA", "email": "atendimento@sumerbol.com.br", "cidade": "Indaiatuba/SP", "segmento": "Supermercados (rede)"},
    # --- Itu (grandes) ---
    {"nome": "Monin Brasil", "empresa": "Monin Brasil Industria", "email": "faleconosco@monin.com", "cidade": "Itu/SP", "segmento": "Industria de xaropes e sabores"},
    # --- Sorocaba (grandes) ---
    {"nome": "Sorocaba Refrescos", "empresa": "Sorocaba Refrescos S.A.", "email": "last@sorocabarefrescos.com.br", "cidade": "Sorocaba/SP", "segmento": "Engarrafadora Coca-Cola"},
    {"nome": "Supermercado UNE", "empresa": "Supermercado UNE LTDA", "email": "rh@superune.com.br", "cidade": "Sorocaba/SP", "segmento": "Supermercados (rede)"},
    {"nome": "Shinoda Alimentos", "empresa": "Shinoda Alimentos LTDA", "email": "comercial.granja@shinoda.com.br", "cidade": "Sorocaba/SP", "segmento": "Industria de ovos e alimentos"},
    {"nome": "Rosaves Aves", "empresa": "Abatedouro de Aves Ideal LTDA (Rosaves)", "email": "contato@rosaves.com.br", "cidade": "Sorocaba/SP", "segmento": "Abatedouro e frigorifico de aves"},
    # --- Jundiaí (grandes) ---
    {"nome": "Fini Company Brasil", "empresa": "Sanchez Cano LTDA (Fini)", "email": "fini@rpmacomunicacao.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de balas e guloseimas"},
    {"nome": "Food Brands Kisabor", "empresa": "Food Brands Industria de Produtos Alimenticios S/A", "email": "sac@kisabor.ind.br", "cidade": "Jundiai/SP", "segmento": "Industria de condimentos e alimentos"},
    {"nome": "Castelo Alimentos", "empresa": "Castelo Alimentos S/A", "email": "sacc@casteloalimentos.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de biscoitos e massas"},
    {"nome": "CRS Brands", "empresa": "CRS Brands Industria e Comercio S/A", "email": "contato@crsbrands.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de bebidas e alimentos"},
    # --- Louveira (grandes) ---
    {"nome": "Prime Cater", "empresa": "Prime Cater Comercial de Produtos Alimenticios S/A", "email": "contato@pmct.com.br", "cidade": "Louveira/SP", "segmento": "Refeicoes coletivas e catering"},
    {"nome": "PGR Sao Paulo Refeicoes", "empresa": "P.G.R. Sao Paulo Refeicoes LTDA", "email": "marcia.mendes@somospremium.com.br", "cidade": "Louveira/SP", "segmento": "Restaurantes e refeicoes"},
    # --- Piracicaba (grandes) ---
    {"nome": "Bom Peixe", "empresa": "Bom Peixe Industria e Comercio LTDA", "email": "sac@bompeixe.com.br", "cidade": "Piracicaba/SP", "segmento": "Industria de pescados e conservas"},
    {"nome": "Laticinios Noiva da Colina", "empresa": "Laticinios Noiva da Colina LTDA", "email": "contato@vimilk.com.br", "cidade": "Piracicaba/SP", "segmento": "Industria de laticinios"},
    # --- Valinhos (grandes) ---
    {"nome": "Zarelli Supermercados", "empresa": "Zarelli Supermercados LTDA", "email": "contato@supermercadoszarelli.com.br", "cidade": "Valinhos/SP", "segmento": "Supermercados (rede)"},
    {"nome": "Chr Hansen Brasil", "empresa": "Chr Hansen Industria e Comercio LTDA", "email": "braco@chr-hansen.com", "cidade": "Valinhos/SP", "segmento": "Industria de culturas e ingredientes"},
    {"nome": "Pronutrition", "empresa": "Pronutrition do Brasil Industria de Suplementos", "email": "compras@pronutrition.com.br", "cidade": "Valinhos/SP", "segmento": "Industria de suplementos alimentares"},
    {"nome": "Ultrapan", "empresa": "Ultrapan Industria e Comercio LTDA", "email": "marketing@ultrapan.com.br", "cidade": "Valinhos/SP", "segmento": "Industria de produtos alimenticios"},
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
    """Template de email de apresentação B2B (prospecção fria — NÓS contatamos)."""
    g = cfg["empresa"]
    cidade = lead.get("cidade") or "região"
    segmento = (lead.get("segmento") or "alimentação").lower()
    return {
        "subject": f"Compra de óleo usado — Master Óleo ({cidade})",
        "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Sou da <b>{g['nome']}</b>, de {g['cidade']}, e estou entrando em contato porque a <b>{lead.get('empresa','')}</b> atua no segmento de {segmento} — setor que gera <b>óleo de cozinha usado e gordura vegetal</b> com frequência.</p>
<p>O mercado mudou: o óleo usado virou <b>"ouro líquido"</b>. O setor global de reciclagem de óleo de cozinha vale <b>US$ 11 bilhões</b> e cresce ~7% ao ano — a demanda por biodiesel e combustível de aviação disparou. E a <b>{g['nome']}</b> <b>compra esse material</b>, com coleta programada e certificado em toda retirada:</p>
<ul>
  <li><b>Pagamento pelo óleo e gordura vegetal usados</b> — valor negociado conforme a quantidade e a qualidade (referência de mercado: R$ 1,00 a R$ 2,50/litro)</li>
  <li><b>Certificado de destinação</b> em cada coleta (comprovação da PNRS, Lei 12.305/2010)</li>
  <li><b>Coleta programada</b> — semanal, quinzenal ou sob demanda, conforme o seu volume</li>
  <li><b>Bombonas e tambores</b> fornecidos, com troca cheia/vazia</li>
  <li><b>Relatório de impacto ambiental</b> — ideal para metas ESG e licenciamentos</li>
</ul>
<p>Se fizer sentido, me responda com a <b>quantidade aproximada</b> (litros ou kg por mês) e o <b>tipo de material</b> (óleo de fritura, gordura vegetal etc.) — com isso, alinho uma proposta de compra sem compromisso em até 24h.</p>
<p>Também estou à disposição pelo WhatsApp: <b>{g['telefone_whatsapp']}</b> (atendimento em horário comercial).</p>
<p>Atenciosamente,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {g['cidade']}<br>{g['telefone_whatsapp']} · {g.get('site','https://masteroleo.eco.br')}</p>
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
                        "volume": "", "segmento": lead_info.get("segmento",""),
                        "cidade": lead_info.get("cidade",""),
                        "fonte": "prospeccao", "status": "novo",
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