#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Correção manual dos 2 bounces do nicho farmacêutica/cosméticos (fonte vazia,
fora do filtro do corrigir_emails.py que só pega fonte=prospeccao*).

- Arese Farmaceutica: contato@arese.com.br deu bounce; site oficial lista
  sac@arese.com.br (mesmo domínio, MX Outlook válido) -> corrige + reenvia.
- HRT Cosmeticos: contato@hrtcosmeticos.com.br deu bounce; site oficial só
  tem esse email -> registra como nao_encontrado (watchdog limpa).
"""
import csv, datetime, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

import corrigir_emails as ce
import prospecao as pr

LEADS_PATH = ce.LEADS_PATH

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def main():
    cfg = ce.load_config()
    e = cfg["email"]
    leads = ce.read_leads()
    log = ce.load_log()
    ja_tentados = {x.get("email_antigo", "").lower() for x in log}

    alvo_arese = "contato@arese.com.br"
    alvo_hrt = "contato@hrtcosmeticos.com.br"

    for l in leads:
        em = l.get("email", "").strip().lower()

        # ---------- ARESE: corrigir para sac@arese.com.br + reenviar ----------
        if em == alvo_arese:
            if em in ja_tentados:
                print(f"⏭️  Arese já tentado: {em}")
                continue
            novo = "sac@arese.com.br"
            # valida MX do domínio (outlook) antes de usar
            if not ce.tem_mx(novo.split("@")[1]):
                print(f"❌ Arese: MX inválido para {novo} — registrando nao_encontrado")
                log.append({"email_antigo": em, "empresa": l.get("nome",""),
                            "novo_email": None, "status": "nao_encontrado",
                            "quando": now_iso()})
                ja_tentados.add(em)
                continue
            l["email"] = novo
            l["status"] = "novo"
            l["apresentacao_em"] = now_iso()
            l["ultima_resposta"] = f"corrigido de {em} (bounce) para {novo}"
            # template do nicho farmacêutica (V5 Catalent/MTR/Anvisa)
            tpl = pr.tpl_apresentacao(cfg, l)
            try:
                msgid = ce.smtp_send(cfg, e, novo, tpl["subject"], tpl["html"])
                l["apresentacao_msgid"] = msgid
                print(f"✅ Arese: apresentação reenviada para {novo}")
                log.append({"email_antigo": em, "empresa": l.get("nome",""),
                            "novo_email": novo, "status": "corrigido_e_enviado",
                            "quando": now_iso()})
            except Exception as ex:
                print(f"❌ Arese: falha ao enviar para {novo}: {str(ex)[:120]}")
                log.append({"email_antigo": em, "empresa": l.get("nome",""),
                            "novo_email": novo, "status": "erro_envio",
                            "quando": now_iso(), "erro": str(ex)[:100]})
            ja_tentados.add(em)

        # ---------- HRT: sem alternativa -> registra tentativa ----------
        elif em == alvo_hrt:
            if em in ja_tentados:
                print(f"⏭️  HRT já tentado: {em}")
                continue
            print(f"⚠️  HRT: nenhum email alternativo válido encontrado — registrando nao_encontrado")
            log.append({"email_antigo": em, "empresa": l.get("nome",""),
                        "novo_email": None, "status": "nao_encontrado",
                        "quando": now_iso()})
            ja_tentados.add(em)

    ce.write_leads(leads)
    ce.save_log(log)
    print("\nConcluído. correcoes_emails.json atualizado.")

if __name__ == "__main__":
    main()
