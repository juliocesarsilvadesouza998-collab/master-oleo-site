import json

with open('../equipe/ecossistema.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

key = 'ciclo_2026_11_18_1415_cron_atendente'
data[key] = {
    'timestamp': '2026-11-18 14:15 (Atendente IA — cron tick — quarta-feira)',
    'acoes': [
        'sync_formspree.py — 133 bounces cache, 0 notificações Formspree novas',
        'corrigir_emails.py — 0 bounces processados (todos os 133 já tentados; nenhum bounce novo)',
        'prospecao_followup.py — 0 follow-ups processados (fila zerada)',
        'bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)',
        'bot_oleo.py check-replies — 0 respostas pendentes (replies_pending.json vazio)',
        'proposta_contrato.py — não executado (sem lead com volume novo informado)',
        'relatorio_esg.py — não executado (sem solicitação ESG/certificado)'
    ],
    'diagnostico': {
        'total_leads_csv': 473,
        'status_csv': 'novo 286 | bounce 95 (133 cache) | respondido 24 | encerrado 15 | descartado 53',
        'bounce_cache_json': 133,
        'dias_sem_resposta_humana_fluxo_oleo': '65 (Tauste 30/09); 35 desde Pague Menos (14/10)',
        'respostas_reais': 0,
        'respostas_humanas_fluxo_oleo': 'Nenhuma — replies_pending.json vazio, INBOX limpa',
        'propostas_contrato_geradas': 0,
        'relatorios_esg_gerados': 0,
        'observacao': '65º dia sem respostas humanas no fluxo de COMPRA de óleo. Sistema saudável — SMTP/IMAP OK. 473 leads, 133 bounces cache. Fila de prospecção zerada — 65 dias sem cold email. Nada mudou desde o tick anterior — replies_pending vazio, INBOX limpa, 0 respostas. Pipeline bloqueado em ação humana (WhatsApp/telefone).'
    },
    'leads_quentes': [
        '🍀 PASTIFICIO SELMI (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno',
        '🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 65+ dias sem ação humana.',
        '🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 35 dias sem retorno.',
        '🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada. Aguardando retorno.',
        '🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br pendente. 65+ dias!',
        '🔴🔴 BRASFRIGO (Salto/SP) — Coleta-teste a agendar. Local.',
        '🔴🔴 QUEIJOS ITUPEVA (Rafael) — Coleta-teste a agendar.',
        '🟡 SONDA (R$6,12bi) — (11) 2145-6200.',
        '🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09 (65 dias).',
        '🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês'
    ]
}

data['ultima_execucao'] = '2026-11-18T14:15:00-03:00'
data['atualizado_em'] = '2026-11-18 ~14:15 (Atendente IA — cron tick — quarta-feira)'

with open('../equipe/ecossistema.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print('ecossistema.json atualizado')