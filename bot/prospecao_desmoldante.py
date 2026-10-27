#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master EcoDesmold — PROSPECÇÃO DE DESMOLDANTE
=============================================
Envia emails de desmoldante para fábricas de concreto pré-moldado e
artefatos de cimento, usando o remetente masterecodesmold@gmail.com
(conta SEPARADA da masteroleo — regra do usuário).

Uso:
  python prospecao_desmoldante.py                 # envia a fila inteira
  python prospecao_desmoldante.py --max 5         # envia no máximo 5
  python prospecao_desmoldante.py --list          # lista a fila

Config (preenchida quando o usuário passar a senha de app):
  bot/config_desmoldante.json
"""
import argparse, csv, json, os, ssl, smtplib, sys, time
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

ROOT = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(ROOT, "fila_desmoldante.json")
CONFIG = os.path.join(ROOT, "config_desmoldante.json")
LEADS = os.path.join(ROOT, "leads_desmoldante.csv")

TEMPLATE = """Prezados, boa tarde!

Meu nome é {nome}, representante da {marca} (Salto/SP).

Produzimos um DESMOLDANTE à base de óleo vegetal para a produção de concreto pré-moldado, artefatos de cimento e formas metálicas — ideal para blocos, tubos, lajes, mourões, manilhas, postes e peças em geral.

Vantagens do produto:
- Base vegetal: renovável e de menor impacto ambiental
- Alto rendimento: cobertura eficiente com baixo consumo por peça
- Acabamento superior: peças limpas, sem manchas ou porosidades
- Proteção das formas: reduz oxidação e desgaste das formas metálicas
- Fácil aplicação: trincha, pano, pistola ou sistema automático

Apresentação:
- Galão de 50 litros
- Quantidade mínima: 4 galões (200 litros)
- Amostra grátis: enviamos para avaliação em todo o Brasil, sem compromisso
- Entrega: todo o território nacional, via transportadora

Gostaria de enviar uma amostra para avaliação na sua empresa. Podemos conversar?

Atenciosamente,
{nome}
{marca} · Salto/SP
WhatsApp: {whatsapp}
{site}
"""


def carregar_config():
    if not os.path.exists(CONFIG):
        raise SystemExit(f"❌ Falta {CONFIG} — preencher com usuario/senha_app do masterecodesmold@gmail.com")
    return json.load(open(CONFIG, encoding="utf-8"))


def enviar(destino, empresa):
    cfg = carregar_config()
    email = cfg["email"]
    marca = cfg["empresa"]

    msg = MIMEText(TEMPLATE.format(
        nome=marca["nome"], marca=marca["marca"],
        whatsapp=marca["whatsapp"], site=marca["site"]
    ), "plain", "utf-8")
    msg["From"] = formataddr((str(Header(marca["nome"], "utf-8")), email["usuario"]))
    msg["To"] = destino
    msg["Subject"] = str(Header("Desmoldante vegetal para concreto pré-moldado — " + marca["marca"], "utf-8"))
    msg["Message-ID"] = make_msgid()

    ctx = ssl.create_default_context()
    s = smtplib.SMTP_SSL(email["smtp_host"], email["smtp_port"], context=ctx, timeout=30)
    s.login(email["usuario"], email["senha_app"])
    s.sendmail(email["usuario"], [destino], msg.as_string())
    s.quit()
    return True


def registrar_lead(empresa, email_destino, status="enviado"):
    agora = datetime.now().isoformat()
    novo = not os.path.exists(LEADS)
    with open(LEADS, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if novo:
            w.writerow(["empresa", "email", "status", "data"])
        w.writerow([empresa, email_destino, status, agora])


def main():
    ap = argparse.ArgumentParser(description="Prospecção de desmoldante")
    ap.add_argument("--max", type=int, default=0)
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    fila = json.load(open(FILA, encoding="utf-8"))
    if args.list:
        for item in fila:
            print(f"  {item['empresa']} <{item['email']}>")
        return

    enviados = 0
    for item in fila:
        if args.max and enviados >= args.max:
            break
        try:
            enviar(item["email"], item["empresa"])
            registrar_lead(item["empresa"], item["email"])
            print(f"✅ {item['empresa']} <{item['email']}>")
            enviados += 1
        except Exception as ex:
            registrar_lead(item["empresa"], item["email"], status=f"erro: {str(ex)[:40]}")
            print(f"❌ {item['empresa']}: {str(ex)[:50]}")
        time.sleep(3)

    print(f"\n✅ Enviados: {enviados}/{len(fila)}")


if __name__ == "__main__":
    main()