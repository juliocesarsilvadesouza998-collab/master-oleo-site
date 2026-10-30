#!/usr/bin/env python3
"""Atualiza ecossistema.json com o ciclo atual (Atendente IA cron #137, 30/10/2026)."""
import json
from collections import OrderedDict

PATH = 'ecossistema.json'

with open(PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

entry = {
    'timestamp': '2026-10-30 12:32 (Atendente IA - cron #137 - sexta-feira)',
    'acoes': [
        '✅ sync_formspree.py — 118 bounces cache, 0 notificações Formspree novas',
        '✅ corrigir_emails.py — 0 bounces processados (todos já tentados anteriormente)',
        '✅ prospecao_followup.py — 0 follow-ups atrasados',
        '✅ send_sequence — sequência processada (nada a enviar)',
        '✅ check-replies — 0 respostas pendentes (replies_pending.json vazio)',
        '✅ scan_inbox.py --dias 2 — 0 mensagens não lidas/recentes na caixa (424 leads, 271 msgids)',
        '✅ watchdog.py — exit 0: 424 leads, 299 ativos, 118 bounces, SMTP/IMAP OK',
        '✅ enviar_lote.py --status — fila 466 / 398 contatados / 92 bounce / 7 pendentes MX-válidos',
        '⏭️ proposta_contrato.py — não executado (nenhum lead respondeu com volume novo)',
        '⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG/certificado)'
    ],
    'diagnostico': {
        'total_leads': 424,
        'status_leads': {
            'novo': 299,
            'bounce': 89,
            'respondido': 22,
            'encerrado': 14
        },
        'fila_total': 466,
        'fila_contatados': 398,
        'fila_bounce': 92,
        'fila_pendentes': 7,
        'followups_enviados_hoje': 0,
        'respostas_processadas': 0,
        'propostas_contrato_geradas': 0,
        'relatorios_esg_gerados': 0,
        'bounce_cache': 118,
        'bounce_rate': '~21% (92/466 fila)',
        'taxa_resposta': '~5.2% (22/424)',
        'observacao': 'Tick limpo após o arquivamento Oba do tick #136 (11:33). 31º dia sem resposta humana REAL (Tauste 30/09). Nenhuma resposta nova na caixa — 0 pendentes para atender. Fila com 7 pendentes MX-válidos (Confianca, SM Boa, Frisa, Frigorifico Verdi/do Sul/3R, Maxxi Ovos) aguardando o ciclo do Prospector. SMTP/IMAP OK.'
    },
    'leads_quentes': [
        '🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 31+ dias sem ação humana.',
        '🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 16+ dias sem retorno.',
        '🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês enviada; aguardando.',
        '🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).',
        '🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste (Salto/região).',
        '🟡 SONDA (ligar 11-2145-6200) / TAUSTE (ligar 15-3324-4680) / ICT FARMACÊUTICA (SAC 1173).',
        '🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada 28/10; vigiar resposta (padrão SAC→comercial).',
        '⚫ GRUPO OBA HORTIFRUTI — ENCERRADO 30/10 (caso recusado pelo sistema SAC/Salesforce).'
    ]
}

key = 'ciclo_2026_10_30_atendente_tick_1232'

# Reinsere o ciclo mais recente no topo (ordem cronológica decrescente, padrão do arquivo)
new_data = OrderedDict()
new_data[key] = entry
for k, v in data.items():
    if k != 'atualizado_em':
        new_data[k] = v
new_data['atualizado_em'] = '2026-10-30 12:32 (Atendente IA - cron #137)'

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print('✅ ecossistema.json atualizado com ciclo #137')