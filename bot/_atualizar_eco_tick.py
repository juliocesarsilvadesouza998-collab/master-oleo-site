#!/usr/bin/env python3
"""Atualiza ecossistema.json com dados do tick Atendente 30/10 10:15."""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ECO_PATH = os.path.join(BASE, 'ecossistema.json')

with open(ECO_PATH, 'r', encoding='utf-8') as f:
    eco = json.load(f)

old_key = 'ciclo_2026_10_30_cron_atendente_matinal'
new_key = 'ciclo_2026_10_30_cron_atendente_10h15'

if old_key in eco:
    del eco[old_key]

eco[new_key] = {
    'timestamp': '2026-10-30 10:15 (Atendente IA - cron tick #132 - sexta-feira)',
    'acoes': [
        'sync_formspree.py — 116 bounces cache, 0 notificações Formspree novas',
        'corrigir_emails.py — 0 bounces novos processados (todos os 116 já tentados)',
        'prospecao_followup.py — 0 follow-ups atrasados',
        'send_sequence — sequência processada (sem leads pendentes de envio)',
        'check-replies — 0 respostas (replies_pending.json vazio)',
        '_analise_diaria.py — 392 leads (275 novo, 87 bounce, 21 respondido, 9 encerrado). Fila 430/370 contatados/90 bounce/0 pendentes. SMTP/IMAP OK',
        'proposta_contrato/relatorio_ESG — não acionados (0 leads com volume novo ou solicitação)'
    ],
    'diagnostico': {
        'total_leads_watchdog': 392,
        'ativos_watchdog': 275,
        'bounce_cache_json': 116,
        'watchdog': 'exit 0 — saudável, SMTP/IMAP OK',
        'fila_total': 392,
        'fila_contatados': '275 novo, 87 bounce, 21 respondido, 9 encerrado',
        'fila_pendentes_validas': '0 — fila de prospecção 100% drenada (430 empresas, 370 contatados, 90 bounce)',
        'dias_sem_resposta_humana_fluxo_oleo': '30 (última: Tauste 30/09); 16 dias desde Pague Menos (14/10)',
        'respostas_reais': 0,
        'respostas_humanas_fluxo_oleo': 'Nenhuma — replies_pending.json vazio, caixa IMAP limpa',
        'respostas_auto': 0,
        'propostas_contrato_geradas': 0,
        'relatorios_esg_gerados': 0,
        'observacao': '30º dia sem respostas humanas no fluxo de COMPRA de óleo (última: Tauste 30/09). Sistema saudável — watchdog exit 0, SMTP/IMAP OK. Nenhum follow-up atrasado. Fila de prospecção 100% drenada (0 pendentes MX-válidos). Pipeline de fechamento bloqueado em ação humana — os mesmos 8+ leads quentes aguardam WhatsApp/telefone. Nenhum lead informou volume novo para gerar proposta de contrato ou relatório ESG.',
        'leads_quentes': [
            '🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. PRIORIDADE ABSOLUTA. 30+ dias sem ação humana.',
            '🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Acompanhar ticket 407470 (Josiane Marinho). 16 dias sem retorno.',
            '🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada. Aguardando retorno.',
            '🔴🔴🔴 COVABRA — **AÇÃO HUMANA: preencher cadastro de fornecedor** (isac.ivrim.com.br). 17+ dias sem ação.',
            '🔴🔴 BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local, respondeu.',
            '🔴🔴 QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.',
            '🟡 SONDA (R$6,12bi) — Ligar (11) 2145-6200.',
            '🟡 TAUSTE — Ligar (15) 3324-4680. Respondeu 30/09.',
            '🟡 NAGUMO — Caso 00143542, proposta anexada 14/10. Follow-up humano em aberto.',
            '🟡 LOPES SUPERMERCADOS — Aguardar retorno após envio.',
            '🟡 SACCO (Campinas) — Aguardar retorno após envio.',
            '🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — Apresentação enviada 28/10; vigiar resposta.'
        ]
    }
}

eco['atualizado_em'] = '2026-10-30 10:15 (Atendente IA - cron tick 30/10)'

with open(ECO_PATH, 'w', encoding='utf-8') as f:
    json.dump(eco, f, indent=2, ensure_ascii=False)

print('ecossistema.json atualizado com sucesso')