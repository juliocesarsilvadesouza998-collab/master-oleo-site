#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Follow-ups de Prospecção
========================================
Envia follow-ups automáticos para leads de prospecção que não responderam
à apresentação inicial. Sequência: apresentação (dia 0) → FP1 (dia 3) →
FP2 (dia 6) → FP3 (dia 10, último). Para assim que o lead responder.

Uso:
  python prospecao_followup.py            # envia follow-ups devidos
  python prospecao_followup.py --dry-run  # simula
  python prospecao_followup.py --status   # mostra onde cada lead está
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, sys
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
          "ultima_resposta","respondido_em","respondido_por"]

# Dias para cada follow-up após a apresentação
FP_DIAS = [3, 6, 10]

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
    normal = []
    for r in leads:
        normal.append({k: r.get(k, "") if r.get(k) is not None else "" for k in FIELDS})
    tmp = LEADS_PATH + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(normal)
    os.replace(tmp, LEADS_PATH)  # atômico: nunca deixa o arquivo truncado

def smtp_send(cfg, e, to, subject, html, in_reply_to=None):
    ctx = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
        msg["References"] = in_reply_to
    msg.attach(MIMEText(_plain_from_html(html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"].replace(" ",""))
        s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def _plain_from_html(html):
    """Converte HTML em texto puro com quebras de linha preservadas."""
    import re
    t = re.sub(r"<br\s*/?>", "\n", html)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.strip()

def tpl_fp(cfg, lead, n):
    """Templates de follow-up de prospecção (n=1,2,3). Todos reforçam a compra."""
    g = cfg["empresa"]
    if n == 1:
        subj = f"Re: óleo usado da {lead['empresa']} vale dinheiro"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Te escrevi há poucos dias sobre a <b>compra do óleo usado da {lead['empresa']}</b> — como sei que a caixa de entrada enche, deixo aqui o essencial:</p>
<p>Pagamos de <b>R$ 1,00 a R$ 2,50/litro</b>, com certificado de destinação (PNRS) em toda coleta e bombonas fornecidas. Para ter ideia: um estabelecimento que gera <b>600 L/mês</b> recebe cerca de <b>R$ 14 mil por ano</b> só com o resíduo que hoje é descartado — sem nenhum custo de logística.</p>
<p>E não é só: o Brasil acaba de liberar <b>exportação de óleo usado para os EUA</b> (1,4 mi t importadas em 2023) e a <b>Portaria Interministerial MME/MMA nº 3/2026</b> (11/05/2026) torna obrigatório o uso de ≥1% de óleo residual no biodiesel a partir de <b>01/01/2028</b> — voluntário em 2026-2027, obrigatório em 2028 (fonte: gov.br). O mundo está disputando essa matéria-prima — fechar contrato agora garante preço e prioridade antes da disputa.</p>
<p>Para eu te passar o valor exato da sua operação: <b>quanto vocês geram por mês (litros ou kg)?</b> Me responde esse número que eu te mando a estimativa ainda esta semana.</p>
<p>Alternativa rápida: WhatsApp {g['telefone_whatsapp']}.</p>
<p>Abraço,<br><b>{g['nome']}</b></p>
</div>"""
    elif n == 2:
        subj = f"Re: oleo usado da {lead['empresa']} — 3 motivos para tratar isso este ano"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Ola, {lead['nome']}.</p>
<p>Sei que esta ocupado, entao vou direto aos <b>3 fatos</b> que tornam a destinacao do oleo usado da <b>{lead['empresa']}</b> urgente:</p>
<p><b>1</b> A <b>Portaria MME/MMA no 3/2026</b> torna <b>OBRIGATORIO >=1%</b> de oleo residual no biodiesel a partir de <b>jan/2028</b> (fonte: gov.br). Quem ja tiver contrato assinado tera prioridade antes da corrida.</p>
<p><b>2</b> O <b>Grupo Madero</b> (270 restaurantes) ja vende 55 mil L/mes para biodiesel — rede grande <b>ja trata como receita</b>, nao como descarte.</p>
<p><b>3</b> Se o coletor nao emitir <b>MTR + certificado de destinacao</b>, o passivo ambiental fica no CNPJ da {lead['empresa']} (Lei 12.305/2010). Nos emitimos em toda coleta.</p>
<p>Para {lead['empresa']}: <b>coleta programada semanal</b>, bombonas fornecidas, logistica por nossa conta e <b>pagamento a vista (PIX) na coleta</b>. Cada litro vira biodiesel certificado.</p>
<p><b>Quantos litros a {lead['empresa']} gera por mes?</b> Responda este numero que envio a avaliacao em 24h. WhatsApp: {g['telefone_whatsapp']}.</p>
<p>Abraco,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    else:
            subj = f"Encerrando contato — {lead['empresa']} × {g['nome']}"
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
    <p>Olá, {lead['nome']}.</p>
    <p>Só mais esta — prometo que é a última sobre a <b>compra do óleo usado da {lead['empresa']}</b>.</p>
    <p>O mercado global UCO vale <b>US$ 11 bi</b> e a demanda mundial já supera a coleta — Europa consome 8× mais do que coleta, e a partir de <b>jan/2028</b> o biodiesel brasileiro é obrigado a usar ≥1% de óleo residual (Portaria MME/MMA nº 3/2026). Quem tiver contrato assinado antes estará na dianteira.</p>
    <p>Não precisa de nada agora? Sem problema — é só ignorar e não receberá mais mensagens sobre isso. Se no futuro fizer sentido, chama no WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
    <p>Obrigado pela atenção e sucesso com a {lead['empresa']}.<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
    </div>"""
    return {"subject": subj, "html": html}

def main():
    ap = argparse.ArgumentParser(description="Follow-ups de prospecção")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    cfg = load_config()
    e = cfg["email"]
    leads = read_leads()
    now = datetime.datetime.now().astimezone()

    if args.status:
        print(f"{'Lead':<40} {'apresentacao':<20} {'FP1':<20} {'FP2':<20} {'FP3':<20} {'status'}")
        for l in leads:
            if not str(l.get("fonte","")).startswith("prospeccao"):
                continue
            print(f"{l.get('empresa','')[:38]:<40} {(l.get('apresentacao_em') or '—')[:18]:<20} "
                  f"{(l.get('fp1_em') or '—')[:18]:<20} {(l.get('fp2_em') or '—')[:18]:<20} "
                  f"{(l.get('fp3_em') or '—')[:18]:<20} {l.get('status','')}")
        return

    enviados = 0
    for l in leads:
        if not str(l.get("fonte","")).startswith("prospeccao"):
            continue
        if l.get("status") in ("respondido", "bounce", "encerrado"):
            continue
        ap_em = l.get("apresentacao_em") or l.get("criado_em")
        try:
            ap_dt = datetime.datetime.fromisoformat(ap_em)
        except Exception:
            continue
        dias = (now - ap_dt).days
        for i, campo in enumerate(["fp1_em", "fp2_em", "fp3_em"], start=1):
            if not l.get(campo) and dias >= FP_DIAS[i-1]:
                tpl = tpl_fp(cfg, l, i)
                if args.dry_run:
                    print(f"[DRY-RUN] FP{i} → {l['email']} ({l.get('empresa','')})")
                else:
                    try:
                        mid = smtp_send(cfg, e, l["email"], tpl["subject"], tpl["html"],
                                        in_reply_to=l.get("apresentacao_msgid") or None)
                        l[campo] = now_iso()
                        print(f"✅ FP{i} → {l['email']} ({l.get('empresa','')})" + (" [thread]" if l.get("apresentacao_msgid") else ""))
                    except Exception as ex:
                        print(f"❌ FP{i} → {l['email']} — {str(ex)[:100]}")
                enviados += 1
                break  # um follow-up por lead por execução
    if not args.dry_run:
        write_leads(leads)
    print(f"\n{enviados} follow-up(s) processado(s).")

if __name__ == "__main__":
    main()