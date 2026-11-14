#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 13/11/2026 18:33 — registra tick #233 no ecossistema.json e insights.md."""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now().astimezone()
dia_pt = {0:'segunda-feira',1:'terça-feira',2:'quarta-feira',3:'quinta-feira',4:'sexta-feira',5:'sábado',6:'domingo'}
dia = dia_pt[now.weekday()]
tick_num = 233

ts = now.strftime("%Y-%m-%d %H:%M") + f" (Atendente IA - cron tick #{tick_num} - {dia})"

novo_ciclo = {
    "timestamp": ts,
    "acoes": [
        "sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas (OK)",
        "corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)",
        "prospecao_followup.py — 2 FP1 enviados: Nutrisanti (sac@nutrisanti.com.br) e Diffucap (sac@diffucap.com.br)",
        "bot_oleo.py send_sequence — sequência processada, nada a enviar",
        "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
        "_miniscan_inbox.py — INBOX: 0 não lidas",
        "watchdog.py — exit 1: 469 leads, 283 ativos, 129 bounces. SMTP OK · IMAP OK",
        "proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação de relatório)"
    ],
    "diagnostico": {
        "total_leads_csv": 469,
        "status_csv": "novo ~283 | bounce 94 | descartado 53 | respondido 24 | encerrado 15",
        "bounce_cache_json": 129,
        "watchdog": "exit 1 — 469 leads, 283 ativos, 129 bounces, 4 FP atrasados (status skip). SMTP OK · IMAP OK",
        "dias_sem_resposta_humana_fluxo_oleo": "45 (última: Tauste 30/09); 30 dias desde Pague Menos (14/10)",
        "respostas_reais": 0,
        "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX limpa",
        "respostas_auto": 0,
        "propostas_contrato_geradas": 0,
        "relatorios_esg_gerados": 0,
        "observacao": "45º dia sem respostas humanas no fluxo de COMPRA de óleo. Sistema saudável SMTP/IMAP OK. 469 leads (283 ativos), 129 bounces, 53 descartados. Fila zerada. Nenhuma resposta, volume ou solicitação de relatório ESG/proposta de contrato. Pipeline bloqueado em ação humana (WhatsApp/telefone)."
    },
    "leads_quentes": [
        "🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 45+ dias sem ação humana.",
        "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 30 dias sem retorno.",
        "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada.",
        "🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br. 52+ dias.",
        "🔴🔴 BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local.",
        "🔴🔴 QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.",
        "🟡 SONDA (R$6,12bi) — (11) 2145-6200.",
        "🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09.",
        "🟡 SANOFI MEDLEY — Protocolo 03065348 (29/10).",
        "🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês."
    ]
}

# Atualiza ecossistema.json
key = f"ciclo_{now.strftime('%Y_%m_%d_%H%M')}_cron_atendente_{tick_num}"
for ecopath_candidate in [
    os.path.join(BASE, "equipe", "ecossistema.json"),
    os.path.join(os.path.normpath(os.path.join(BASE, "..")), "equipe", "ecossistema.json")
]:
    ecopath = os.path.normpath(ecopath_candidate)
    if os.path.exists(ecopath):
        with open(ecopath, "r", encoding="utf-8-sig") as f:
            eco = json.load(f)
        eco["atualizado_em"] = ts
        eco[key] = novo_ciclo
        with open(ecopath, "w", encoding="utf-8", newline="\n") as f:
            json.dump(eco, f, ensure_ascii=False, indent=1)
        print(f"ecossistema.json atualizado: {ecopath}")

# Atualiza insights.md
insight = f"""

## {now.strftime('%Y-%m-%d %H:%M')} (Atendente IA - cron tick #{tick_num} - {dia})

### Diagnóstico do ciclo
- ✅ sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)
- ✅ prospecao_followup.py — 2 FP1 enviados (Nutrisanti, Diffucap)
- ✅ bot_oleo.py send_sequence — sequência processada, nada a enviar
- ✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)
- ✅ _miniscan_inbox.py — INBOX: 0 não lidas
- ✅ watchdog.py — exit 1: 469 leads, 283 ativos, 129 bounces. SMTP OK · IMAP OK
- ⏭️ proposta_contrato/relatorio_ESG — não acionados (0 leads com volume ou solicitação)
- 🔴 **45º dia sem respostas humanas no fluxo de COMPRA de óleo**
- 🔴 Fila de prospecção zerada — sem fonte de busca gratuita para repor

### Leads QUENTES (fechamento depende de ação humana)
1. 🔴🔴🔴 **SAVEGNAGO** (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 45+ dias sem ação.
2. 🔴🔴🔴 **PAGUE MENOS** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 30 dias sem retorno.
3. 🔴🔴🔴 **REDE CONFIANÇA** (Sorocaba) — Proposta 2.500 L/mês enviada.
4. 🔴🔴🔴 **COVABRA** — **AÇÃO HUMANA: cadastro fornecedor** isac.ivrim.com.br. 52+ dias.
5. 🔴🔴 **BRASFRIGO** (Salto/SP) — Agendar coleta-teste. Local.
6. 🔴🔴 **QUEIJOS ITUPEVA** (Rafael) — Agendar coleta-teste.
7. 🟡 **SONDA** (R$6,12bi) — (11) 2145-6200.
8. 🟡 **TAUSTE** — (15) 3324-4680. Respondeu 30/09 (45 dias).
9. 🟡 **SANOFI MEDLEY** — Protocolo 03065348 (29/10).
10. 🟡 **NAGUMO** — Caso 00143542, proposta 5.000 L/mês.

### Observações
- **45 dias sem resposta humana nova** (última: Tauste 30/09). Após 469 leads trabalhados, o canal de email atingiu o teto.
- **Pipeline de fechamento 100% parado** em ação humana — sem scripts que liguem ou enviem WhatsApp.
- **Nenhum bounce novo**, nenhuma resposta pendente, nenhuma notificação Formspree.
- Sistema saudável — SMTP/IMAP OK, watchdog funcional.

---

"""

for inspath_candidate in [
    os.path.join(BASE, "equipe", "insights.md"),
    os.path.join(os.path.normpath(os.path.join(BASE, "..")), "equipe", "insights.md")
]:
    inspath = os.path.normpath(inspath_candidate)
    if os.path.exists(inspath):
        atual = open(inspath, "r", encoding="utf-8").read()
        with open(inspath, "w", encoding="utf-8", newline="\n") as f:
            f.write(insight + atual)
        print(f"insights.md atualizado: {inspath}")

print("Concluído.")