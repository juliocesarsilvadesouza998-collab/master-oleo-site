#!/usr/bin/env python3
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, 'equipe', 'ecossistema.json')

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

data['total_leads'] = 473
data['status_dist'] = {'bounce': 95, 'novo': 286, 'respondido': 24, 'descartado': 53, 'encerrado': 15}
data['respondidos'] = 24
data['taxa_resposta'] = '5.1%'
data['bounce_csv'] = 95
data['taxa_bounce_csv'] = '20.1%'
data['novos_para_enviar'] = 286
data['descartados'] = 53
data['bounce_cache'] = 130
data['dias_sem_resposta_humana'] = 62
data['ultima_resposta'] = 'Tauste 30/09/2026'
data['inbox_nao_lidas'] = 0
data['atualizado_em'] = '2026-11-17 11:34 (Atendente IA - cron - terça-feira)'

key = 'ciclo_2026_11_17_1134_cron_atendente_terca'
data[key] = {
    'timestamp': '2026-11-17 11:34 (Atendente IA - cron - terça-feira)',
    'acoes': [
        'sync_formspree.py — 133 bounces cache, 0 notificações Formspree novas (ok, 120s timeout)',
        'corrigir_emails.py — 0 bounces processados (todos os 130 já tentados; nenhum bounce novo)',
        'prospecao_followup.py — 2 FP3 enviados (Copacol, EcoTaua)',
        'bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)',
        'bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)',
        'proposta_contrato/relatorio_ESG — não acionados (sem lead com volume informado ou solicitação de relatório)'
    ],
    'diagnostico': {
        'total_leads_csv': 473,
        'status_csv': 'novo 286 | respondido 24 | bounce 95 (130 cache) | descartado 53 | encerrado 15',
        'bounce_cache_json': 130,
        'dias_sem_resposta_humana_fluxo_oleo': '62 (última: Tauste 30/09); 34 dias desde Pague Menos (14/10)',
        'respostas_reais': 0,
        'respostas_humanas_fluxo_oleo': 'Nenhuma — replies_pending.json vazio, INBOX sem novas',
        'respostas_auto': 0,
        'propostas_contrato_geradas': 0,
        'relatorios_esg_gerados': 0,
        'observacao': '62º dia sem respostas humanas. Sistema saudável SMTP/IMAP OK. 473 leads (286 ativos), 130 bounces cache, 53 descartados. 2 FP3 enviados (Copacol, EcoTaua). Pipeline bloqueado em ação humana (WhatsApp/telefone).'
    },
    'leads_quentes': [
        '🍀 Pastificio Selmi (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno',
        '🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 62+ dias sem ação humana.',
        '🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 34 dias sem retorno.',
        '🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada.',
        '🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br. 66+ dias.',
        '🔴🔴 BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local.',
        '🔴🔴 QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.',
        '🟡 SONDA (R$6,12bi) — (11) 2145-6200.',
        '🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09.',
        '🟡 SANOFI MEDLEY — Protocolo 03065348 (29/10).',
        '🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês.'
    ]
}

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print('ecossistema.json atualizado OK')