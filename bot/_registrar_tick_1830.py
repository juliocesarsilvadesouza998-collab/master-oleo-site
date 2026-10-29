#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 28/10 18:30 (tick #15): registra ciclo."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
# path pro equipe/
EQUIPE = os.path.join(BASE, "..", "equipe")
ECOSSISTEMA = os.path.join(EQUIPE, "ecossistema.json")
INSIGHTS = os.path.join(EQUIPE, "insights.md")

tick = {
    "ciclo_2026_10_28_atendente_tick_1830": {
        "timestamp": "2026-10-28 18:30 (Atendente IA - cron quarta-feira - tick diurno #15)",
        "acoes": [
            "✅ sync_formspree.py — 112 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 processados (todos os 112 bounces já tentados anteriormente)",
            "✅ prospecao_followup.py — 0 follow-ups (nada atrasado)",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json vazio)",
            "✅ scan_inbox.py --tudo --dias 3 — varredura completa: 26 mensagens na caixa (bounces + respostas já processadas + spam). Nenhum lead não atendido.",
            "✅ watchdog.py — IMAP timeout transiente na 1ª tentativa, OK nas retentativas (SMTP/IMAP saudável)",
            "✅ enviar_lote.py --status — fila 430 / 370 contatados / 89 bounce / 0 pendentes (inalterado)",
            "⏭️ proposta_contrato.py — não executado (nenhum lead com volume novo)",
            "⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG)",
            "⏭️ prospecção manual — não executado (free web scraping esgotado per persona.md; recomendação Leadjet pendente de compra)"
        ],
        "diagnostico": {
            "fila_total": 430,
            "fila_contatados": 370,
            "fila_bounce": 89,
            "fila_pendentes": 0,
            "respostas_total": 22,
            "respondidos_hoje": [
                "ICT Farmacêutica 09:33 (respondido_atendente)",
                "Artema Pre Moldados 14:43 (desmoldante, respondido_atendente)"
            ],
            "caixa_nao_lidas": 0,
            "dias_sem_resposta_humana": "30 (última: Pague Menos 14/10; última real: Tauste 30/09)",
            "observacao": "Tick #15 — 15º ciclo consecutivo sem novas respostas. Pipeline 100% drenado (0 pendentes, fila parada aguardando reposição). IMAP timeout transiente na 1ª tentativa resolvido com retry — não crítico, mas indicador de latência de rede. Mesmo estado do tick #14 (18:03). Reabastecimento da fila depende de listas CNPJ pagas (Leadjet) recomendadas pelo Estrategista."
        },
        "leads_quentes": [
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 30+ dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 15 dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês enviada; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste (Salto/região).",
            "🟡 SONDA (ligar 11-2145-6200) / TAUSTE (ligar 15-3324-4680) / ICT FARMACÊUTICA (SAC 1173).",
            "🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada 28/10 15:3x; vigiar resposta."
        ]
    }
}

# Atualizar ecossistema.json (prepend)
with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

# Atualizar insights.md (prepend)
entrada = f"""## 2026-10-28 18:30 (Atendente IA - cron quarta-feira - tick diurno #15)

### Diagnóstico do ciclo
- ✅ **Watchdog** — 392 leads, caixa sem não-lidas (scan 3d), SMTP/IMAP OK (timeout transiente no 1º teste, OK nos 2 seguintes)
- ✅ **Fila** — 430 / 370 contatados / 89 bounce / **0 pendentes** (inalterado desde 15:30)
- ✅ **Caixa de entrada** — varredura completa (tudo, 3 dias): 26 mensagens = 20 bounces Gmail + 2 respostas já processadas (ICT/Artema) + 4 spam/irrelevant. **Nenhum lead não atendido**
- ✅ **Sequência/replies** — 0 follow-ups, 0 respostas pendentes (15º tick consecutivo sem novos contatos)

### Observações
- **Pipeline 100% drenado há 3h.** Mesmo estado do tick #14 (18:03). A única alavanca restante é a compra de listas CNPJ (Leadjet) para reabastecer a fila.
- **Gargalo**: 30 dias sem ação humana nos leads quentes (Savegnago, Pague Menos, Covabra, Rede Confiança). Sem isso ou novos leads, o pipeline para.
- **Leads QUENTES** — inalterado desde o tick #14.

| Prioridade | Lead | Status |
|:----------:|------|--------|
| 🔴🔴🔴 | SAVEGNAGO (R$7,98bi) | 30+ dias, WhatsApp pendente |
| 🔴🔴🔴 | PAGUE MENOS (R$4,33bi) | Ticket 407470, 15 dias |
| 🔴🔴🔴 | REDE CONFIANÇA (Sorocaba) | Proposta 2.500 L/mês enviada |
| 🔴🔴🔴 | COVABRA | Cadastro Ivrim pendente |
| 🔴🔴 | BRASFRIGO / QUEIJOS ITUPEVA | Coleta-teste a agendar |
| 🟡 | SONDA / TAUSTE / ICT FARM. | Ligar/acompanhar |
| 🟢 | UNIÃO SUPERMERCADOS | Apresentação enviada hoje |

---
"""

import re
with open(INSIGHTS, encoding="utf-8") as f:
    current = f.read()
# Use regex to find the start of the first ## entry (the most recent one) and insert before it
# The current top is the 18:03 entry; we'll just prepend
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + current)

print("ecossistema.json + insights.md atualizados (tick #15 registrado)")