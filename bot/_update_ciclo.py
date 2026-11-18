#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza ecossistema.json e insights.md com o ciclo atual"""
import json, datetime, os, sys

BOT_DIR = os.path.dirname(os.path.abspath(__file__))
ECO_FILE = os.path.join(BOT_DIR, 'ecossistema.json')
INSIGHTS_FILE = os.path.join(BOT_DIR, 'equipe', 'insights.md')

now = datetime.datetime.now()
dia_semana = ['segunda','terca','quarta','quinta','sexta','sabado','domingo'][now.weekday()]
ts = now.strftime(f'%Y-%m-%d %H:%M')
ts_br = now.strftime(f'%d/%m/%Y %H:%M')

# Dados do ciclo
acoes = [
    "sync_formspree.py — 133 bounces cache, 0 notificações Formspree novas (OK)",
    "corrigir_emails.py — 0 bounces processados (todos os 133 já tentados; nenhum bounce novo)",
    "prospecao_followup.py — 0 follow-ups atrasados (fila zerada)",
    "bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)",
    "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
    "proposta_contrato/relatorio_ESG — não acionados (sem lead com volume informado ou solicitação de relatório)"
]

diagnostico = {
    "total_leads_csv": 473,
    "status_csv": "novo ~286 | respondido 24 | bounce 94 (133 cache) | descartado 53 | encerrado 15",
    "bounce_cache_json": 133,
    "dias_sem_resposta_humana_fluxo_oleo": "48 (última: Tauste 30/09); 34 dias desde Pague Menos (14/10)",
    "respostas_reais": 0,
    "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX sem novas",
    "respostas_auto": 0,
    "propostas_contrato_geradas": 0,
    "relatorios_esg_gerados": 0,
    "observacao": f"48º dia sem respostas humanas. 473 leads (~286 ativos), 133 bounces. 6º tick do dia ({ts_br}) — mesmo cenário dos ticks anteriores. Sistema saudável. Nenhuma resposta para processar. Pipeline bloqueado em ação humana (WhatsApp/telefone)."
}

leads_quentes = [
    "🍀 Pastificio Selmi (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno",
    "🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 48+ dias sem ação humana.",
    "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 34 dias sem retorno.",
    "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada.",
    "🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br. 66+ dias.",
    "🔴🔴 BRASFRIGO (Salto/SP) — Coleta-teste a agendar. Local.",
    "🔴🔴 QUEIJOS ITUPEVA (Rafael) — Coleta-teste a agendar.",
    "🟡 SONDA (R$6,12bi) — (11) 2145-6200.",
    "🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09 (48 dias).",
    "🟡 SANOFI MEDLEY — Protocolo 03065348 (29/10).",
    "🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês."
]

ciclo_key = f"ciclo_{ts.replace(':','-').replace(' ','_')}_cron_atendente_6o_tick"
ciclo_entry = {
    "timestamp": f"{ts} (Atendente IA - cron - {dia_semana}-feira - 6º tick)",
    "acoes": acoes,
    "diagnostico": diagnostico,
    "leads_quentes": leads_quentes
}

# Carregar ecossistema existente
try:
    with open(ECO_FILE, 'r', encoding='utf-8') as f:
        eco = json.load(f)
except:
    eco = {}

# Atualizar
eco["atualizado_em"] = f"{ts} (Atendente IA - cron - {dia_semana}-feira - 6o tick)"
eco[ciclo_key] = ciclo_entry

# Salvar (manter só últimos 15 ciclos para não explodir)
keys = sorted([k for k in eco.keys() if k.startswith('ciclo_')], reverse=True)
for k in keys[15:]:
    del eco[k]

with open(ECO_FILE, 'w', encoding='utf-8') as f:
    json.dump(eco, f, indent=2, ensure_ascii=False, sort_keys=False)

print(f"✅ ecossistema.json atualizado ({len(acoes)} açoes)")

# --- insights.md ---
insight_entry = f"""
## {ts} (Atendente IA - cron - 6º tick - {dia_semana}-feira)

### Diagnóstico do ciclo
- ✅ sync_formspree.py — 133 bounces cache, 0 notificações Formspree novas (OK)
- ✅ corrigir_emails.py — 0 bounces processados (todos os 133 já tentados; nenhum bounce novo)
- ✅ prospecao_followup.py — 0 follow-ups atrasados (fila zerada)
- ✅ bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)
- ✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)
- ⏭️ proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação de relatório)
- 🔴 **48º dia sem respostas humanas no fluxo de COMPRA de óleo** (última: Tauste 30/09)
- 🔴 Fila de prospecção zerada — sem fonte de busca gratuita para repor leads

### Leads QUENTES (fechamento depende de ação humana)
1. 🍀 **PASTIFICIO SELMI** — proposta 800 L/mês (03/11), aguardando retorno compras.
2. 🔴🔴🔴 **SAVEGNAGO** (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 48+ dias sem ação.
3. 🔴🔴🔴 **PAGUE MENOS** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 34 dias sem retorno.
4. 🔴🔴🔴 **REDE CONFIANÇA** (Sorocaba) — Proposta 2.500 L/mês enviada.
5. 🔴🔴🔴 **COVABRA** — **AÇÃO HUMANA: cadastro fornecedor** isac.ivrim.com.br. 66+ dias.
6. 🔴🔴 **BRASFRIGO** (Salto/SP) — Coleta-teste a agendar. Local.
7. 🔴🔴 **QUEIJOS ITUPEVA** (Rafael) — Coleta-teste a agendar.
8. 🟡 **SONDA** (R$6,12bi) — (11) 2145-6200.
9. 🟡 **TAUSTE** — (15) 3324-4680. Respondeu 30/09 (48 dias).
10. 🟡 **SANOFI MEDLEY** — Protocolo 03065348 (29/10).
11. 🟡 **NAGUMO** — Caso 00143542, proposta 5.000 L/mês.

### Observações
- **48 dias sem resposta humana nova** (última: Tauste 30/09). 473 leads trabalhados, canal email no teto.
- **Pipeline de fechamento 100% parado** em ação humana — sem scripts que liguem ou enviem WhatsApp.
- **Nenhum bounce novo**, nenhuma resposta pendente, nenhuma notificação Formspree.
- **Nenhum lead informou volume** para gerar proposta de contrato ou relatório ESG.
- Sistema saudável — SMTP/IMAP OK.
- Ação humana necessária: **enviar WhatsApp para Savegnago** (script no persona.md) e **preencher cadastro Covabra** (isac.ivrim.com.br).

---
"""

# Append to insights.md
try:
    with open(INSIGHTS_FILE, 'a', encoding='utf-8') as f:
        f.write(insight_entry)
    print(f"✅ insights.md atualizado")
except Exception as e:
    print(f"⚠️ insights.md: {e}")

print("Ciclo completo.")