#!/usr/bin/env python3
"""Update ecossistema.json with current cycle data."""
import json

with open('ecossistema.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

entry = {
    'timestamp': '2026-10-24 19:03 (Atendente IA - cron tick #3 - sábado)',
    'acoes': [
        '✅ sync_formspree.py — 97 bounces cache, 0 notificações Formspree novas',
        '✅ corrigir_emails.py — 0 processados (todos os 97 já tentados anteriormente)',
        '✅ prospecao_followup.py — 0 follow-ups processados (nada pendente)',
        '✅ send_sequence — sequência processada (nada a enviar)',
        '✅ check-replies — 0 respostas (replies_pending.json vazio)',
        'ℹ️ proposta_contrato.py / relatorio_esg.py — não executados (sem leads com volume novo nem solicitação ESG)'
    ],
    'diagnostico': {
        'total_leads_watchdog': 337,
        'ativos_watchdog': 235,
        'bounce_cache_json': 97,
        'fila_total': 382,
        'fila_contatados': 324,
        'fila_bounce': 78,
        'fila_pendentes_validas': 1,
        'watchdog': 'exit 0 — saudável',
        'dashboard': '283 enviados | 211 entregues | 72 bounces (25%) | 19 respostas (6,7%) | 235 aguardando',
        'respostas_reais': 0,
        'respostas_humanas': '10 dias sem respostas humanas (última: Pague Menos 14/10; última real: Tauste 30/09 — 24 dias)',
        'observacao': 'Tick 19:03 — sistema saudável, 0 respostas novas, 0 follow-ups, 0 bounces. Mesmo cenário: 10 dias sem respostas humanas, pipeline de fechamento parado. 1 pendente na fila (Unialimentar com MX). Nenhuma demanda de proposta ou ESG.'
    },
    'dias_sem_resposta_humana': 10,
    'ultimo_lead_quente': 'Pague Menos (14/10)'
}

key = 'ciclo_2026_10_24_cron_atendente_tick_19h'
data[key] = entry
data['atualizado_em'] = '2026-10-24 19:03 (Atendente IA - cron tick #3)'

with open('ecossistema.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ ecossistema.json atualizado')