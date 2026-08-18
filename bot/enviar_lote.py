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
import argparse, csv, datetime, json, os, re, ssl, smtplib, subprocess, sys, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

# Reutiliza o template otimizado do prospecao.py (fonte única de verdade)
from prospecao import tpl_apresentacao as tpl_apresentacao_novo, _plain_from_html

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
BOUNCE_CACHE = os.path.join(BASE, "bounces.json")
FIELDS = ["id","nome","empresa","email","tipo","volume","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","fp1_em","fp2_em","fp3_em","apresentacao_msgid",
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

# Cache de MX por domínio (evita nslookup repetido dentro da mesma execução)
_MX_CACHE = {}

def tem_mx(dominio):
    """Valida registro MX de um domínio via nslookup (mesma lógica de corrigir_emails.py).
    Retorna True apenas se houver 'mail exchanger' no retorno. Sem MX = email quase
    certamente vai dar bounce (ex.: 8 bounces de 18/08 vieram de domínios sem MX)."""
    if dominio in _MX_CACHE:
        return _MX_CACHE[dominio]
    try:
        r = subprocess.run(["nslookup", "-type=MX", dominio], capture_output=True, timeout=25)
        out = (r.stdout + r.stderr).decode("latin-1", "replace")
        ok = bool(re.findall(r"mail exchanger = (\S+)", out, re.I))
    except Exception:
        ok = False
    _MX_CACHE[dominio] = ok
    return ok

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_leads(leads):
    # Normaliza: garante que todas as linhas tenham exatamente os campos de FIELDS
    # (evita ValueError/truncamento se algum dict tiver chaves extras ou faltantes)
    normal = []
    for r in leads:
        normal.append({k: r.get(k, "") if r.get(k) is not None else "" for k in FIELDS})
    tmp = LEADS_PATH + ".tmp"
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(normal)
    os.replace(tmp, LEADS_PATH)  # atômico: nunca deixa o arquivo truncado

# --- Lock de arquivo: evita perder linhas em escrita concorrente de leads.csv ---
# (Prospector, Atendente e Estrategista rodam em paralelo; sem lock, o último
#  que grava sobrescreve as linhas dos outros — 5 leads já foram perdidos assim)
def _acquire_lock(path, timeout=20):
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return True
        except FileExistsError:
            if time.time() > deadline:
                return False
            time.sleep(0.3)
        except OSError:
            return False

def _release_lock(path):
    try:
        os.remove(path)
    except OSError:
        pass

def merge_write_leads(novos_em_memoria):
    """Grava leads.csv com lock, mesclando com o que estiver em disco.
    Deduplica por email e renumera ids sequencialmente. `novos_em_memoria`
    é a lista completa (snapshot antigo + novos) que o agente montou."""
    lock = LEADS_PATH + ".lock"
    if _acquire_lock(lock):
        try:
            atuais = read_leads()
            existentes = {l.get("email", "").strip().lower() for l in atuais}
            a_adicionar = []
            for l in novos_em_memoria:
                if l.get("email", "").strip().lower() not in existentes:
                    a_adicionar.append(l)
            base_id = max((int(l.get("id") or 0) for l in atuais), default=0)
            for i, l in enumerate(a_adicionar, start=base_id + 1):
                l["id"] = str(i)
            write_leads(atuais + a_adicionar)
            return len(a_adicionar)
        finally:
            _release_lock(lock)
    # Falha ao obter lock: grava direto mesmo assim (melhor que perder o lote)
    write_leads(novos_em_memoria)
    return len(novos_em_memoria) - 0

def smtp_send(cfg, e, to_addr, subject, html):
    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    smtp.login(e["usuario"], e["senha_app"].replace(" ",""))
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
    msg["To"] = to_addr
    msg["Subject"] = Header(subject, "utf-8")
    msg["Message-ID"] = make_msgid()
    msg.attach(MIMEText(_plain_from_html(html).strip(), "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    smtp.sendmail(e["usuario"], [to_addr], msg.as_string())
    smtp.quit()
    return msg["Message-ID"]

def tpl_apresentacao(cfg, lead):
    """Template de apresentação — delega ao otimizado do prospecao.py (fonte única)."""
    return tpl_apresentacao_novo(cfg, lead)

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

    # Fila: empresas com email não contatado, sem bounce e com MX válido
    fila = []
    sem_mx = []
    for p in EMPRESAS:
        em = p["email"].strip().lower()
        if em in contatados or em in bounces:
            continue
        if not tem_mx(em.split("@")[-1]):
            sem_mx.append(p)
            print(f"⚠️  Sem MX: {p['empresa']} <{em}> — pulando (evita bounce)")
            continue
        fila.append(p)
    fila = fila[:args.max]

    if sem_mx and not fila:
        print(f"{len(sem_mx)} empresa(s) pendente(s) sem MX válido — nada a enviar.")
        return

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
            mid = smtp_send(cfg, e, p["email"], tpl["subject"], tpl["html"])
            leads.append({"id": str(len(leads)+1), "nome": p["nome"], "empresa": p["empresa"],
                          "email": p["email"], "tipo": "industria" if "industria" in p["segmento"].lower() else "outro",
                          "volume": "", "fonte": "prospeccao-lote", "status": "novo",
                          "criado_em": now_iso(), "boas_vindas_em": "",
                          "follow1_em": "", "follow2_em": "", "follow3_em": "",
                          "apresentacao_em": now_iso(), "fp1_em": "", "fp2_em": "", "fp3_em": "",
                          "apresentacao_msgid": mid,
                          "ultima_resposta": "", "respondido_em": "", "respondido_por": ""})
            contatados.add(p["email"].strip().lower())
            enviados += 1
            print(f"✅ {p['empresa']} <{p['email']}>")
            time.sleep(6)
        except Exception as ex:
            print(f"❌ {p['empresa']} — {str(ex)[:100]}")
    gravados = merge_write_leads(leads) if enviados > 0 else 0
    print(f"\n{enviados} email(s) enviados; {gravados} registrado(s) no leads.csv (merge com lock). Próximo lote: novos pendentes.")

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