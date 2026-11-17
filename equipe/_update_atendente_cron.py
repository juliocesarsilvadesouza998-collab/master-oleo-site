#!/usr/bin/env python3
"""Update equipe/ecossistema.json with current Atendente IA cycle."""
import json, os, datetime
from collections import OrderedDict

BASE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE, 'ecossistema.json')

now = datetime.datetime.now()
ts = now.strftime('%Y-%m-%d %H:%M')
dow = now.strftime('%A')
dias_semana = {'Monday':'segunda-feira','Tuesday':'terça-feira','Wednesday':'quarta-feira',
               'Thursday':'quinta-feira','Friday':'sexta-feira','Saturday':'sábado','Sunday':'domingo'}
dow_pt = dias_semana.get(dow, dow)

key = f'ciclo_{now.strftime("%Y_%m_%d_%H%M")}_cron_atendente_{dow_pt}'

entry = {
    "timestamp": f"{ts} (Atendente IA - cron - {dow_pt})",
    "acoes": [
        "sync_formspree.py — 130 bounces cache, 0 notificações Formspree novas (OK)",
        "corrigir_emails.py — 0 bounces processados (todos os 130 já tentados; nenhum bounce novo)",
        "prospecao_followup.py — 0 follow-ups atrasados (fila zerada)",
        "bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)",
        "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
        "proposta_contrato/relatorio_ESG — não acionados (sem lead com volume informado ou solicitação de relatório)"
    ],
    "diagnostico": {
        "total_leads_csv": 472,
        "status_csv": "novo 285 | respondido 24 | bounce 95 (130 cache) | descartado 53 | encerrado 15",
        "bounce_cache_json": 130,
        "dias_sem_resposta_humana_fluxo_oleo": "57 (última: Tauste 30/09); 33 dias desde Pague Menos (14/10)",
        "respostas_reais": 0,
        "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX sem novas",
        "respostas_auto": 0,
        "propostas_contrato_geradas": 0,
        "relatorios_esg_gerados": 0,
        "observacao": "57º dia sem respostas humanas no fluxo de COMPRA de óleo. 472 leads (285 ativos), 95 bounces CSV (130 em cache), 53 descartados, 15 encerrados, 24 respondidos (todos SAC/comercial — nenhum com volume informado). Sistema saudável. Fila de prospecção zerada — sem fonte de busca gratuita para repor. Nenhuma resposta para processar. Pipeline bloqueado em ação humana (WhatsApp/telefone)."
    },
    "leads_quentes": [
        "🍀 Pastificio Selmi (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno",
        "🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 57+ dias sem ação humana.",
        "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 33 dias sem retorno.",
        "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada.",
        "🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br. 63+ dias.",
        "🔴🔴 BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local.",
        "🔴🔴 QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.",
        "🟡 SONDA (R$6,12bi) — (11) 2145-6200.",
        "🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09 (57 dias).",
        "🟡 SANOFI MEDLEY — Protocolo 03065348 (29/10).",
        "🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês."
    ]
}

with open(PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = OrderedDict()
new_data[key] = entry
for k, v in data.items():
    new_data[k] = v
new_data['atualizado_em'] = f'{ts} (Atendente IA - cron - {dow_pt})'

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f'✅ equipe/ecossistema.json atualizado com {key}')