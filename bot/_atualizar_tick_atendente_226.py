#!/usr/bin/env python3
"""Atualiza ecossistema.json e insights.md com este ciclo."""
import json, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now().astimezone()
dia_pt = {
    'Monday': 'segunda-feira', 'Tuesday': 'terça-feira', 'Wednesday': 'quarta-feira',
    'Thursday': 'quinta-feira', 'Friday': 'sexta-feira', 'Saturday': 'sábado', 'Sunday': 'domingo'
}
dia = dia_pt.get(now.strftime('%A'), now.strftime('%A'))
tick_num = 226  # next tick number after #224

ts = now.strftime("%Y-%m-%d %H:%M") + f" (Atendente IA - cron tick #{tick_num} - {dia})"

# Dados do ciclo
novo_ciclo = {
    "timestamp": ts,
    "acoes": [
        "sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas (OK)",
        "corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)",
        "prospecao_followup.py — 0 follow-ups atrasados (fila zerada)",
        "bot_oleo.py send_sequence — sequência processada, nada a enviar",
        "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
        "_miniscan_inbox.py — INBOX: 0 não lidas",
        "watchdog.py — exit 1: 469 leads, 283 ativos, 129 bounces, 2 FP atrasados (status skip), 1 bounce sem correção (já tentado). SMTP OK · IMAP OK",
        "proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação de relatório)"
    ],
    "diagnostico": {
        "total_leads_csv": 469,
        "status_csv": "novo 283 | bounce 94 | descartado 53 | respondido 24 | encerrado 15",
        "bounce_cache_json": 129,
        "watchdog": "exit 1 — 469 leads, 283 ativos, 129 bounces, 2 FP atrasados (status skip — leads já respondidos ou descartados), 1 bounce sem correção (já registrado). SMTP OK · IMAP OK",
        "dias_sem_resposta_humana_fluxo_oleo": "45 (última: Tauste 30/09); 30 dias desde Pague Menos (14/10)",
        "respostas_reais": 0,
        "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX limpa",
        "respostas_auto": 0,
        "propostas_contrato_geradas": 0,
        "relatorios_esg_gerados": 0,
        "observacao": "45º dia sem respostas humanas no fluxo de COMPRA de óleo. Sistema saudável SMTP/IMAP OK. 469 leads (283 ativos), 129 bounces, 53 descartados (laticínios/fora do alvo). Fila zerada. Nenhuma resposta, volume ou solicitação de relatório ESG/proposta de contrato. Pipeline bloqueado em ação humana (WhatsApp/telefone)."
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

# Atualiza o ecossistema.json principal (bot/equipe/ecossistema.json)
ecopath1 = os.path.join(BASE, "equipe", "ecossistema.json")
with open(ecopath1, "r", encoding="utf-8-sig") as f:
    eco = json.load(f)
eco["atualizado_em"] = ts
key = f"ciclo_{now.strftime('%Y_%m_%d_%H%M')}_cron_atendente_{tick_num}"
eco[key] = novo_ciclo
with open(ecopath1, "w", encoding="utf-8", newline="\n") as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)
print("bot/equipe/ecossistema.json atualizado.")

# Atualiza também o raiz se existir e for diferente
ecopath2 = os.path.join(BASE, "..", "equipe", "ecossistema.json")
ecopath2 = os.path.normpath(ecopath2)
if os.path.exists(ecopath2) and os.path.abspath(ecopath2) != os.path.abspath(ecopath1):
    with open(ecopath2, "r", encoding="utf-8-sig") as f:
        eco2 = json.load(f)
    eco2["atualizado_em"] = ts
    eco2[key] = novo_ciclo
    with open(ecopath2, "w", encoding="utf-8", newline="\n") as f:
        json.dump(eco2, f, ensure_ascii=False, indent=1)
    print("equipe/ecossistema.json (raiz) atualizado.")
else:
    print("equipe/ecossistema.json (raiz) é o mesmo arquivo ou não existe.")

# Atualiza insights.md
insight = f"""

## {now.strftime('%Y-%m-%d %H:%M')} (Atendente IA - cron tick #{tick_num} - {dia})

### Diagnóstico do ciclo
- ✅ sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)
- ✅ prospecao_followup.py — 0 follow-ups atrasados (fila zerada)
- ✅ bot_oleo.py send_sequence — sequência processada, nada a enviar
- ✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)
- ✅ _miniscan_inbox.py — INBOX: 0 não lidas
- ✅ watchdog.py — exit 1: 469 leads, 283 ativos, 129 bounces. SMTP OK · IMAP OK
- ⏭️ proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação)
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

"""

for inspath_candidate in [
    os.path.join(BASE, "equipe", "insights.md"),
    os.path.join(os.path.normpath(os.path.join(BASE, "..")), "equipe", "insights.md")
]:
    inspath = os.path.normpath(inspath_candidate)
    if os.path.exists(inspath):
        with open(inspath, "a", encoding="utf-8", newline="\n") as f:
            f.write(insight)
        print(f"insights.md atualizado: {inspath}")

print("Concluído.")