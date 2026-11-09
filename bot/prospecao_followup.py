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

def smtp_send(cfg, e, to, subject, html, in_reply_to=None, conn=None):
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
    if conn:
        conn.sendmail(e["usuario"], [to], msg.as_string())
    else:
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
    """Templates de follow-up de prospecção (n=1,2,3). Versão compacta — 3 parágrafos cada."""
    g = cfg["empresa"]
    if n == 1:
        subj = f"Re: óleo usado da {lead['empresa']} vale dinheiro"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p><b>💰 Pagamos de R$ 1,00 a R$ 2,50/litro</b> (PIX na coleta) — óleo usado, gordura vegetal, vencidos. Mercado UCO global <b>US$ 15 bilhões</b> (cresceu 87% em 1 ano). <b>200 L/mês = R$ 4.080/ano; 1.000 L/mês = R$ 20.400/ano</b> — de resíduo a receita.</p>
<p><b>🏆 3 maiores do interior SP já negociam:</b> <b>Savegnago</b> (R$7,98 bi, #1), <b>Pague Menos</b> (R$4,33 bi, #2) e <b>Tauste</b> (#3). JBS comprou +154% de UCO em 2024. Se os líderes contratam, sua empresa também pode.</p>
<p><b>📊 Quanto vocês geram por mês?</b> Me responda o volume (litros ou kg) que eu te mando a estimativa. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    elif n == 2:
        subj = f"Re: oleo usado da {lead['empresa']} — urgencia 2028"
        html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p><b>⚖️ FALTAM 14 MESES para a obrigatoriedade:</b> a Portaria MME/MMA nº 3/2026 exige ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b>. Mercado UCO global <b>US$ 15 bilhões</b> — o Brasil coleta só 180M L/ano, mas o potencial é 600M L. <b>70% inexplorado.</b> Quem contratar agora define o território.</p>
<p><b>💰 Quanto a {lead['empresa']} gera por mês?</b> Pagamos de <b>R$ 1,00 a R$ 2,50/L</b> (PIX na coleta). <b>200 L/mês = R$ 4.080/ano; 1.000 L/mês = R$ 20.400/ano</b> — dinheiro que hoje sai como resíduo. Coleta com crachá, bombona com trava, MTR e certificado — <b>sem passivo no seu CNPJ.</b></p>
<p><b>📊 Me responda com o volume mensal</b> (litros ou kg) de óleo de cozinha, gordura vegetal ou vencidos que a {lead['empresa']} gera, e envio a proposta em <b>24h</b>. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
</div>"""
    else:
            subj = f"Último contato — {lead['empresa']} perde R$ 14,4 mil/ano se não responder"
            html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
    <p>Olá, {lead['nome']}.</p>
    <p><b>⚠️ Última mensagem — não enviaremos mais sobre este assunto.</b></p>
    <p><b>💰 R$ 1,00 a R$ 2,50/L pagos à vista (PIX)</b> na coleta. Mercado UCO global <b>US$ 15 bilhões</b> e subindo (era US$ 8 bi em 2025). <b>200 L/mês = R$ 4.080/ano</b> de renda extra; <b>1.000 L/mês = R$ 20.400/ano</b> — dinheiro que hoje sai como resíduo.</p>
    <p><b>🏆 Seus concorrentes estão fechando:</b> as 3 maiores redes do interior SP (<b>Savegnago</b> R$7,98bi, <b>Pague Menos</b> R$4,33bi, <b>Tauste</b>) já estão conosco. A JBS coletou 36 milhões de litros em 8 anos (+154% em 2024). Madero vende 55 mil L/mês como commodity para biodiesel. Quem não contratar até 2027 vai pagar caro para descartar — ou ter o passivo no CNPJ (Lei 12.305/2010).</p>
    <p><b>⏰ Responda este email com o volume mensal</b> (litros ou kg) + seu WhatsApp, e envio a proposta em 24h. Ou chame direto: <b>{g['telefone_whatsapp']}</b>.</p>
    <p>Atenciosamente,<br><b>{g['nome']}</b> · {g['telefone_whatsapp']}</p>
    </div>"""
    return {"subject": subj, "html": html}

def fonte_elegivel(l):
    """Só leads do fluxo de COMPRA de óleo recebem follow-up de prospecção.
    `prospeccao_desmoldante` é de OUTRO negócio (Master EcoDesmold) e tem oferta
    diferente — recebeu em 02/11/2026 um FP2 de óleo usado por engano, porque o
    fallback usava `criado_em` mesmo sem apresentação registrada."""
    f = str(l.get("fonte", ""))
    return f in ("prospeccao", "prospeccao-lote")

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
            if not fonte_elegivel(l):
                continue
            print(f"{l.get('empresa','')[:38]:<40} {(l.get('apresentacao_em') or '—')[:18]:<20} "
                  f"{(l.get('fp1_em') or '—')[:18]:<20} {(l.get('fp2_em') or '—')[:18]:<20} "
                  f"{(l.get('fp3_em') or '—')[:18]:<20} {l.get('status','')}")
        return

    enviados = 0
    ctx = ssl.create_default_context()
    conn = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    conn.login(e["usuario"], e["senha_app"].replace(" ",""))
    for l in leads:
        if not fonte_elegivel(l):
            continue
        if l.get("status") in ("respondido", "bounce", "encerrado"):
            continue
        ap_em = l.get("apresentacao_em") or l.get("criado_em")
        try:
            ap_dt = datetime.datetime.fromisoformat(ap_em)
            if ap_dt.tzinfo is None:
                ap_dt = ap_dt.replace(tzinfo=now.tzinfo)
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
                                        in_reply_to=l.get("apresentacao_msgid") or None, conn=conn)
                        l[campo] = now_iso()
                        print(f"✅ FP{i} → {l['email']} ({l.get('empresa','')})" + (" [thread]" if l.get("apresentacao_msgid") else ""))
                    except Exception as ex:
                        print(f"❌ FP{i} → {l['email']} — {str(ex)[:100]}")
                enviados += 1
                break  # um follow-up por lead por execução
    conn.quit()
    if not args.dry_run:
        write_leads(leads)
    print(f"\n{enviados} follow-up(s) processado(s).")

if __name__ == "__main__":
    main()