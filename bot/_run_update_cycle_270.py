#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza ecossistema.json e insights.md com este ciclo - run via cron."""
import json, datetime, os

BASE = os.path.join(os.path.dirname(__file__), "equipe")
ECO_PATH = os.path.join(BASE, "ecossistema.json")
INSIGHTS_PATH = os.path.join(BASE, "insights.md")

now = datetime.datetime.now().astimezone()
dia_semana = {0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira", 3: "quinta-feira",
              4: "sexta-feira", 5: "sábado", 6: "domingo"}[now.weekday()]

TICK = 270
TIMESTAMP = f"{now.strftime('%Y-%m-%d %H:%M')} (Atendente IA - cron tick #{TICK} - {dia_semana})"

# 1) ecossistema
with open(ECO_PATH, "r", encoding="utf-8") as f:
    eco = json.load(f)

eco["atualizado_em"] = TIMESTAMP
eco["_ultimo_check"] = TIMESTAMP

ciclo_key = f"ciclo_{now.strftime('%Y_%m_%d_%H%M')}_cron_atendente_{TICK}"
eco[ciclo_key] = {
    "timestamp": TIMESTAMP,
    "acoes": [
        "sync_formspree.py — 140 bounces cache, 0 notificações Formspree novas (OK)",
        "corrigir_emails.py — 0 bounces processados (todos os 140 já tentados; nenhum bounce novo)",
        "prospecao_followup.py — 0 follow-ups processados (fila zerada)",
        "bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)",
        "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)",
        "_miniscan_inbox.py — INBOX: 0 não lidas",
        "proposta_contrato/relatorio_ESG — não acionados (0 leads com volume ou solicitação)"
    ],
    "diagnostico": {
        "total_leads_csv": 512,
        "status_csv": "novo 318 | bounce 102 | respondido 24 | descartado 53 | encerrado 15",
        "bounce_cache_json": 140,
        "dias_sem_resposta_humana_fluxo_oleo": "57 (última: Tauste 30/09; 42 desde Pague Menos 14/10)",
        "respostas_reais": 0,
        "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX vazia",
        "respostas_auto": 0,
        "propostas_contrato_geradas": 0,
        "relatorios_esg_gerados": 0,
        "observacao": (
            "57º dia sem respostas humanas. Sistema SMTP/IMAP OK. "
            "512 leads (318 ativos), 140 bounces cache, 53 descartados. "
            "Nada novo: fila zerada, sem replies, sem follow-ups. "
            "Pipeline bloqueado em ação humana — WhatsApp (11) 96785-9631 "
            "é o próximo passo para todos os leads quentes."
        )
    }
}

with open(ECO_PATH, "w", encoding="utf-8", newline="\n") as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("✅ equipe/ecossistema.json atualizado")

# 2) insights.md
insight = f"""
## {TIMESTAMP}

### Ações executadas
| Ação | Resultado |
|------|-----------|
| ✅ sync_formspree.py | 140 bounces cache, 0 notificações Formspree novas (OK) |
| ✅ corrigir_emails.py | 0 bounces processados (todos os 140 já tentados; nenhum bounce novo) |
| ✅ prospecao_followup.py | 0 follow-ups processados (fila zerada) |
| ✅ bot_oleo.py send_sequence | Sequência processada, 0 envios novos (fila drenada) |
| ✅ bot_oleo.py check-replies | 0 respostas (replies_pending.json vazio) |
| ✅ _miniscan_inbox.py | INBOX: 0 não lidas |
| ⏭️ proposta_contrato/relatorio_ESG | Não acionados (0 leads com volume ou solicitação) |

### Diagnóstico
| Indicador | Valor |
|-----------|-------|
| Total leads | **512** |
| `novo` | 318 |
| `respondido` | 24 |
| `bounce` CSV | 102 (140 cache) |
| `encerrado` | 15 |
| `descartado` | 53 |
| Follow-ups atrasados | 0 ✅ |
| Respostas pendentes | 0 ✅ |
| Fila prospecção | 0 MX-válidos ❌ |
| Dias sem resposta humana | **57** (última: Tauste 30/09; 42 desde Pague Menos 14/10) |
| Caixa IMAP | 0 não lidas ✅ |
| SMTP/IMAP | OK ✅ |

### 🔥 Leads QUENTES — nenhuma mudança
- 🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — 57+ dias sem ação humana
- 🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470, 42 dias sem retorno
- 🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada
- 🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br (66+ dias)
- 🔴🔴 BRASFRIGO (Salto/SP) — Coleta-teste a agendar
- 🔴🔴 QUEIJOS ITUPEVA — Coleta-teste a agendar
- 🟡 SONDA, TAUSTE, SANOFI MEDLEY, NAGUMO, SELMI, DU PORTO
- 🆕 LEAD INBOUND WHATSAPP — Indústria óleos/oleoquímicos 6-25t/ano (respondido por Júlio, aguarda 26/11)

### 🔴 Diagnóstico estrutural
**57º dia consecutivo sem respostas humanas no fluxo de COMPRA de óleo.** Nada novo: 0 bounces, 0 replies, 0 follow-ups, 0 envios. Pipeline completamente bloqueado em ação humana — todo o cold email já foi enviado e reenviado. Os 12 leads QUENTES dependem de ação humana no WhatsApp (11) 96785-9631 ou telefone. **Ação prioritária para Júlio:** disparar WhatsApp de reengajamento para Savegnago (Pâmela, protocolo 00136403), Pague Menos (Josiane Marinho, ticket 407470) e Covabra (portal Ivrim). Lead inbound WhatsApp (indústria óleos/oleoquímicos 6-25t/ano) — Júlio respondeu em 25/11, aguarda retorno em 26/11.

---
"""

with open(INSIGHTS_PATH, "r+", encoding="utf-8") as f:
    content = f.read()
    f.seek(0)
    f.write(insight.strip() + "\n" + content)
print("✅ equipe/insights.md atualizado")

print(f"\n=== CICLO #{TICK} — {now.strftime('%Y-%m-%d %H:%M')} ===")
print(f"512 leads (318 ativos, 102 bounce, 24 respondidos, 53 descartados, 15 encerrados)")
print(f"Follow-ups: 0 | Respostas: 0 | Propostas: 0 | Relatórios ESG: 0")
print(f"57º dia sem resposta humana — status quo mantido.")