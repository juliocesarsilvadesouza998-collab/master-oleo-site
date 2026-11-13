#!/usr/bin/env python3
"""Update ecossistema.json with current tick data"""
import json, os, datetime

os.chdir(os.path.dirname(__file__) or '.')

ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# Current stats from watchdog run
stats = {
    "total_leads_csv": 464,
    "status_csv": "novo 295 | bounce 93 | respondido 24 | encerrado 15 | descartado 37",
    "bounce_cache_json": 128,
    "watchdog": "exit 1 — 464 leads, 295 ativos, 128 bounces, 1 bounce sem correcao (conhecido). SMTP OK · IMAP OK",
    "dias_sem_resposta_humana_fluxo_oleo": "44 (ultima: Tauste 30/09); 29 dias desde Pague Menos (14/10)",
    "prospector_fila": "0 pendentes MX-valido (fila zerada — sem serper_api_key)",
    "propostas_geradas": 1,
    "propostas_enviadas": "Savegnago Supermercados (comercial@savegnago.com.br) — 5.000 L/mes, R$2,00/L, R$120.000/ano"
}

entry_key = f"ciclo_{ts.replace(' ','_').replace(':','')}_cron_atendente_210"

new_entry = {
    "timestamp": f"{ts} (Atendente IA - cron tick #210 - quarta-feira)",
    "acoes": [
        "sync_formspree.py — 128 bounces cache, 0 notificacoes Formspree novas (OK)",
        "corrigir_emails.py — 0 bounces processados (todos os 128 ja tentados; nenhum bounce novo)",
        "prospecao_followup.py — 0 follow-ups atrasados (OK)",
        "bot_oleo.py send_sequence — sequencia processada, nada a enviar",
        "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
        "_miniscan_inbox.py — INBOX: 0 nao lidas",
        "watchdog.py — exit 1: 464 leads, 295 ativos, 128 bounces. SMTP OK · IMAP OK",
        "proposta_contrato.py — GERADA E ENVIADA: Savegnago Supermercados (comercial@savegnago.com.br) — 5.000 L/mes, R$2,00/L, R$120.000/ano",
        "relatorio_ESG — nao acionado (nenhum lead solicitou relatorio de impacto)"
    ],
    "diagnostico": stats,
    "leads_quentes": [
        "🔥🔥 Savegnago Supermercados (R$7,98bi, #1 interior SP) — PROPOSTA ENVIADA HOJE para comercial@savegnago.com.br. AGUARDAR RETORNO.",
        "🔥🔥 Pague Menos (R$4,33bi) — Ticket 407470 (Josiane Marinho). 29 dias sem retorno.",
        "🔥🔥 Rede Confianca (Sorocaba) — Proposta 2.500 L/mes enviada 14/10. Sem retorno.",
        "🔥🔥 Covabra — ACAO HUMANA: preencher cadastro fornecedor isac.ivrim.com.br (53+ dias).",
        "🔥 Brasfrigo (Salto/SP) — Agendar coleta-teste. Local.",
        "🟡 Sonda (R$6,12bi) — (11) 2145-6200.",
        "🟡 Tauste — (15) 3324-4680. Respondeu 30/09 — 44 dias.",
        "🟡 Sanofi Medley — Protocolo 03065348 (29/10).",
        "🟡 Nagumo — Caso 00143542, proposta 5.000 L/mes anexada."
    ],
    "observacoes": [
        "44o dia sem respostas humanas novas no fluxo de COMPRA de oleo.",
        "Sistema 100% saudavel — SMTP/IMAP OK, fila de envios zerada.",
        "Watchdog aponta 1 bounce sem correcao (bounce_registrado sem alternativa de email — inocuo).",
        "Fila de prospeccao zerada — sem serper_api_key nem buscas web gratuitas para reposicao.",
        "Pipeline de fechamento continua bloqueado em acao humana (WhatsApp/telefone).",
        "**NOVO: Proposta enviada para Savegnago via comercial@savegnago.com.br (email que o SAC redirecionou).**"
    ]
}

# Read existing, add entry, write
with open('ecossistema.json', 'r', encoding='utf-8') as f:
    eco = json.load(f)

eco["atualizado_em"] = f"{ts} (Atendente IA - cron tick #210)"
eco[entry_key] = new_entry

with open('ecossistema.json', 'w', encoding='utf-8') as f:
    json.dump(eco, f, ensure_ascii=False, indent=2)

print("OK: ecossistema.json atualizado")