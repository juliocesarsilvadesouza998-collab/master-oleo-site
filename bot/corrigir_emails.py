#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Auto-correção de Emails com Bounce
==================================================
Quando um email de prospecção dá bounce, este script:
1. Identifica o lead com bounce (status=bounce, fonte=prospeccao*)
2. Busca na web o email CORRETO da empresa (site oficial / página de contato)
3. Valida MX do domínio do novo email
4. Atualiza o lead no leads.csv com o email correto (status volta a "novo")
5. Reenvia a apresentação para o email correto
6. Mantém o email antigo no bounces.json (nunca mais reenviar)

Uso:
  python corrigir_emails.py --dry-run   # mostra o que faria (busca na web, sem enviar)
  python corrigir_emails.py             # busca, corrige e reenvia
  python corrigir_emails.py --status    # mostra bounces pendentes de correção
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, subprocess, sys, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
BOUNCE_CACHE = os.path.join(BASE, "bounces.json")
CORRIGIDOS_LOG = os.path.join(BASE, "correcoes_emails.json")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em",
          "ultima_resposta","respondido_em","respondido_por"]

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
    os.replace(tmp, LEADS_PATH)

def load_bounces():
    if os.path.exists(BOUNCE_CACHE):
        try:
            return set(json.load(open(BOUNCE_CACHE, encoding="utf-8")))
        except Exception:
            return set()
    return set()

def save_bounces(b):
    with open(BOUNCE_CACHE, "w", encoding="utf-8") as f:
        json.dump(sorted(b), f, ensure_ascii=False, indent=2)

def load_log():
    if os.path.exists(CORRIGIDOS_LOG):
        try:
            return json.load(open(CORRIGIDOS_LOG, encoding="utf-8"))
        except Exception:
            return []
    return []

def save_log(log):
    with open(CORRIGIDOS_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def tem_mx(dominio):
    """Valida registro MX de um domínio (nslookup)."""
    try:
        r = subprocess.run(["nslookup", "-type=MX", dominio], capture_output=True, timeout=25)
        out = (r.stdout + r.stderr).decode("latin-1", "replace")
        return bool(re.findall(r"mail exchanger = (\S+)", out, re.I))
    except Exception:
        return False

def email_valido_plausivel(em):
    em = em.strip().lower()
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", em):
        return False
    if any(x in em for x in ["example", "sentry", "wixpress", ".png", ".jpg", "domain", "schema", "@2x", "@1x", "gov.br", "jusbrasil", "duckduckgo", "error-lite", "w3.org"]):
        return False
    return True

def smtp_send(cfg, e, to, subject, html):
    ctx = ssl.create_default_context()
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    msg.attach(MIMEText(re.sub(r"<[^>]+>", "", html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    with smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30) as s:
        s.login(e["usuario"], e["senha_app"].replace(" ",""))
        s.sendmail(e["usuario"], [to], msg.as_string())
    return msg["Message-ID"]

def tpl_apresentacao(cfg, lead):
    g = cfg["empresa"]
    cidade = lead.get("cidade") or "região"
    segmento = (lead.get("segmento") or "alimentação").lower()
    return {
        "subject": f"Compra de óleo usado — Master Óleo ({cidade})",
        "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Sou da <b>{g['nome']}</b>, de {g['cidade']}, e estou entrando em contato porque a <b>{lead.get('empresa','')}</b> atua no segmento de {segmento} — setor que gera <b>óleo de cozinha usado e gordura vegetal</b> com frequência.</p>
<p>A <b>{g['nome']}</b> <b>compra esse material</b> com coleta programada e certificado de destinação em toda retirada. Na prática, o que oferecemos à sua empresa:</p>
<ul>
  <li><b>Pagamento pelo óleo e gordura vegetal usados</b> — valor negociado conforme a quantidade e a qualidade</li>
  <li><b>Certificado de destinação</b> em cada coleta (comprovação da PNRS, Lei 12.305/2010)</li>
  <li><b>Coleta programada</b> — semanal, quinzenal ou sob demanda, conforme o seu volume</li>
  <li><b>Bombonas e tambores</b> fornecidos, com troca cheia/vazia</li>
</ul>
<p>Se fizer sentido, me responda com a <b>quantidade aproximada</b> (litros ou kg por mês) e o <b>tipo de material</b> (óleo de fritura, gordura vegetal etc.) — com isso, alinho uma proposta de compra sem compromisso em até 24h.</p>
<p>Também estou à disposição pelo WhatsApp: <b>{g['telefone_whatsapp']}</b> (atendimento em horário comercial).</p>
<p>Atenciosamente,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {g['cidade']}<br>{g['telefone_whatsapp']} · {g.get('site','https://masteroleo.eco.br')}</p>
</div>"""}

def buscar_email_web(empresa, cidade):
    """Busca email de contato da empresa na web (via pesquisa). Retorna lista de candidatos."""
    # 1) Correções manuais validadas (prioridade máxima — pesquisadas e MX confirmado)
    MANUAIS = {
        "Kelco Industrial Produtos Animais LTDA": "comercial@kelcopetcare.com.br",
        "Abatedouro de Aves Ideal LTDA (Rosaves)": "avesideal@rosaves.com.br",
        "Beira Rio Comercio, Exportacao e Importacao de Produtos Alimenticios LTDA": "faleconosco@beirariosm.com.br",
        "Infanger & Cia LTDA": "supermercado@infanger.com.br",
        "Real Distribuidora de Alimentos LTDA": "paulo@realdist.com.br",
        "Pastificio Selmi S/A": "sac@selmi.com.br",
        "Industria Moageira Nova Odessa LTDA": "contato@moinhopotenza.com.br",
    }
    for nome_emp, email_certo in MANUAIS.items():
        if nome_emp.lower() in empresa.lower():
            return [email_certo]
    candidatos = []
    queries = [
        f'"{empresa}" contato email',
        f'"{empresa}" {cidade} fale conosco',
    ]
    try:
        import urllib.parse, urllib.request
        for q in queries:
            url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                html = resp.read().decode("utf-8", "replace")
            for m in re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", html):
                if email_valido_plausivel(m) and m not in candidatos:
                    candidatos.append(m.lower())
            time.sleep(2)
    except Exception:
        pass
    return candidatos

def main():
    ap = argparse.ArgumentParser(description="Auto-correção de emails com bounce")
    ap.add_argument("--dry-run", action="store_true", help="busca na web mas NÃO envia")
    ap.add_argument("--status", action="store_true", help="mostra bounces pendentes")
    args = ap.parse_args()

    leads = read_leads()
    bounces = load_bounces()
    log = load_log()
    # evita reprocessar correções já feitas
    ja_tentados = {e.get("email_antigo","").lower() for e in log}

    if args.status:
        pendentes = [l for l in leads if l["status"] == "bounce" and str(l.get("fonte","")).startswith("prospeccao")]
        print(f"Bounces de prospecção: {len(pendentes)} | já tentados corrigir: {len(ja_tentados)}")
        for l in pendentes:
            status_c = "🔁 já tentado" if l["email"].lower() in ja_tentados else "⬜ pendente"
            print(f"  {status_c} | {l['empresa'][:40]:<42} | {l['email']}")
        return

    cfg = load_config()
    e = cfg["email"]
    pendentes = [l for l in leads if l["status"] == "bounce" and str(l.get("fonte","")).startswith("prospeccao")]
    corrigidos = 0
    for l in pendentes:
        email_antigo = l["email"].strip().lower()
        if email_antigo in ja_tentados:
            print(f"⏭️  Já tentado: {l['empresa']} <{email_antigo}>")
            continue
        print(f"\n🔍 Buscando email correto para: {l['empresa']} ({email_antigo})")
        candidatos = buscar_email_web(l["empresa"], l.get("cidade",""))
        # filtra: descarta o próprio email que deu bounce, mantém domínios com MX
        novo = None
        for c in candidatos:
            if c == email_antigo:
                continue
            if c in bounces:
                continue
            dominio = c.split("@")[1]
            if not tem_mx(dominio):
                continue
            novo = c
            break
        if not novo:
            msg = "nenhum email alternativo válido encontrado"
            print(f"  ❌ {msg}")
            log.append({"email_antigo": email_antigo, "empresa": l["empresa"], "novo_email": None,
                        "status": "nao_encontrado", "quando": now_iso()})
            save_log(log)
            ja_tentados.add(email_antigo)
            continue
        print(f"  ✅ Email correto encontrado: {novo}")
        # Proteção anti-duplicata: se o novo email já existe como lead, o antigo
        # é apenas arquivado (o lead novo já está sendo atendido)
        ja_existe = any(x.get("email","").strip().lower() == novo for x in leads if x is not l)
        if ja_existe:
            print(f"  ℹ️  {novo} já existe como lead — arquivando bounce {email_antigo} sem duplicar")
            log.append({"email_antigo": email_antigo, "empresa": l["empresa"], "novo_email": novo,
                        "status": "ja_existia", "quando": now_iso()})
            save_log(log)
            ja_tentados.add(email_antigo)
            continue
        if args.dry_run:
            print(f"  [DRY-RUN] Atualizaria lead e enviaria apresentação para {novo}")
            log.append({"email_antigo": email_antigo, "empresa": l["empresa"], "novo_email": novo,
                        "status": "dry_run", "quando": now_iso()})
            save_log(log)
            ja_tentados.add(email_antigo)
            corrigidos += 1
            continue
        # Atualiza o lead com o email correto
        l["email"] = novo
        l["status"] = "novo"
        l["apresentacao_em"] = now_iso()
        l["ultima_resposta"] = f"corrigido de {email_antigo} (bounce)"
        # Envia a apresentação para o email correto
        try:
            tpl = tpl_apresentacao(cfg, l)
            smtp_send(cfg, e, novo, tpl["subject"], tpl["html"])
            print(f"  📤 Apresentação reenviada para {novo}")
            log.append({"email_antigo": email_antigo, "empresa": l["empresa"], "novo_email": novo,
                        "status": "corrigido_e_enviado", "quando": now_iso()})
            corrigidos += 1
        except Exception as ex:
            print(f"  ❌ Falha ao enviar para {novo}: {str(ex)[:100]}")
            log.append({"email_antigo": email_antigo, "empresa": l["empresa"], "novo_email": novo,
                        "status": "erro_envio", "quando": now_iso(), "erro": str(ex)[:100]})
        ja_tentados.add(email_antigo)
        time.sleep(4)
    write_leads(leads)
    save_log(log)
    print(f"\n{corrigidos} bounce(s) processados. Ver correcoes_emails.json para o histórico.")

if __name__ == "__main__":
    main()