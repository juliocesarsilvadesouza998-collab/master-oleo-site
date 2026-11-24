#!/usr/bin/env python3
"""Atualiza ecossistema.json com tick #255 (Atendente IA cron)."""
import json, os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
now = datetime.now().astimezone()
ts = now.strftime('%Y-%m-%d %H:%M') + ' (Atendente IA - cron tick #255 - terça-feira)'

novo_ciclo = {
    'timestamp': ts,
    'acoes': [
        '✅ sync_formspree.py — 138 bounces cache, 0 notificações Formspree novas (OK)',
        '✅ corrigir_emails.py — 0 bounces novos (todos os 98 já tentados; nenhum bounce novo)',
        '✅ prospecao_followup.py — 0 follow-ups (fila zerada)',
        '✅ bot_oleo.py send_sequence — 0 envios novos',
        '✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)',
        '⏭️ proposta_contrato.py — não acionado (0 leads com volume novo)',
        '⏭️ relatorio_esg.py — não acionado (sem solicitação de relatório)'
    ],
    'diagnostico': {
        'total_leads_csv': 503,
        'status_csv': 'novo 311 | bounce 100 | respondido 24 | encerrado 15 | descartado 53',
        'bounce_cache_json': 138,
        'dias_sem_resposta_humana_fluxo_oleo': '56 (última: Tauste 30/09; 42 dias desde Pague Menos 14/10)',
        'fila_prospeccao': '0 pendentes MX-válido (fila zerada)',
        'propostas_contrato_geradas': 0,
        'relatorios_esg_gerados': 0,
        'novas_respostas_humanas': 0
    }
}

# Update ecossistema.json
ecopath = os.path.join(BASE, 'equipe', 'ecossistema.json')
with open(ecopath, 'r', encoding='utf-8-sig') as f:
    eco = json.load(f)

key = 'ciclo_2026_11_24_' + now.strftime('%H%M') + '_cron_atendente_255'
eco['atualizado_em'] = ts
eco['_ultimo_check'] = ts
eco['_ultimo_tick'] = ts
eco[key] = novo_ciclo

with open(ecopath, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)

# Append to insights.md
insight = f"""

## 2026-11-24 (terça-feira) — {now.strftime('%H:%M')} (Atendente IA - cron tick #255)

### Diagnóstico do ciclo
- ✅ sync_formspree: 138 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails: 0 bounces novos (todos os 98 já tentados)
- ✅ prospecao_followup: 0 follow-ups (fila zerada)
- ✅ send_sequence: 0 envios novos
- ✅ check-replies: 0 respostas (replies_pending.json vazio)
- ⏭️ proposta_contrato: não acionado (0 leads com volume novo)
- ⏭️ relatorio_esg: não acionado (sem solicitação)

### Estado do pipeline
- **56º dia sem resposta humana real** (Tauste 30/09; 42 desde Pague Menos 14/10)
- **503 leads**: 311 novo, 100 bounce, 24 respondido, 15 encerrado, 53 descartado
- **138 bounces** em cache
- **Fila de prospecção: 0 pendentes** — totalmente drenada
- **Sistema SMTP/IMAP OK** — todos os scripts executados sem erro

### Leads QUENTES (inalterados — aguardando ação humana)
| Prioridade | Lead | Próximo passo |
|:----------:|------|---------------|
| 🔴🔴🔴 | **SAVEGNAGO** (R$7,98bi) | WhatsApp (11) 96785-9631 — 56+ dias |
| 🔴🔴🔴 | **PAGUE MENOS** (R$4,33bi) | Ticket 407470 (Josiane Marinho) — 42 dias |
| 🔴🔴🔴 | **REDE CONFIANÇA** (Sorocaba) | Proposta 2.500 L/mês enviada |
| 🔴🔴🔴 | **COVABRA** | Cadastro fornecedor isac.ivrim.com.br |
| 🔴🔴 | **BRASFRIGO** (Salto/SP) | Coleta-teste a agendar |
| 🔴🔴 | **QUEIJOS ITUPEVA** | Coleta-teste a agendar |
| 🟡 | **SONDA** (R$6,12bi) | (11) 2145-6200 |
| 🟡 | **TAUSTE** | (15) 3324-4680 |
| 🟡 | **SANOFI MEDLEY** | Protocolo 03065348 (29/10) |
| 🟡 | **NAGUMO** | Caso 00143542, proposta 5.000 L/mês |
| 🟡 | **PASTIFÍCIO SELMI** | compras@selmi.com.br, proposta 800 L/mês |
| 🟡 | **DU PORTO** | sac@duporto.com.br (04/11) |

### Observações
Mais um tick de manutenção limpo: sistema saudável, fila zerada, sem respostas novas. **56º dia sem resposta humana real.** O pipeline de fechamento continua travado em ação humana — WhatsApp/telefone nos leads quentes. Sem reposição da fila de prospecção (listas CNPJ pagas), o cold email permanece inativo.

"""

inspath = os.path.join(BASE, 'equipe', 'insights.md')
with open(inspath, 'a', encoding='utf-8', newline='\n') as f:
    f.write(insight)

print('ecossistema.json + insights.md atualizados (tick #255)')