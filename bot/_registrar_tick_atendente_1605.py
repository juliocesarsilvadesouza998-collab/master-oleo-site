#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 30/10 16:05 — registra tick #140 no ecossistema.json (prepend) e insights.md."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

tick = {
    "ciclo_2026_10_30_atendente_tick_1605": {
        "timestamp": "2026-10-30 16:05 (Atendente IA - cron #140 - sexta-feira)",
        "acoes": [
            "✅ sync_formspree.py — 119 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 bounces novos processados (todos os 119 já tentados; histórico inalterado)",
            "✅ prospecao_followup.py — 0 follow-ups atrasados",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json vazio, varredura IMAP ao vivo UNSEEN sem hits)",
            "✅ watchdog.py — exit 0: 433 leads, 307 ativos, 119 bounces, SMTP/IMAP OK",
            "✅ enviar_lote.py --status — fila 468 / 407 contatados / 93 bounce / 0 pendentes (fila 100% processada)",
            "✅ scan_inbox.py --dias 2 — 0 mensagens não lidas/recentes (433 leads, 280 msgids)",
            "⏭️ proposta_contrato.py — não executado (nenhum lead respondeu com volume novo)",
            "⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG/certificado)"
        ],
        "diagnostico": {
            "total_leads": 433,
            "status_leads": {
                "novo": 287,
                "bounce": 84,
                "respondido": 21,
                "encerrado": 13,
                "outros_prospeccao": 28
            },
            "fila_total": 468,
            "fila_contatados": 407,
            "fila_bounce": 93,
            "fila_pendentes": 0,
            "followups_enviados_hoje": 0,
            "respostas_processadas": 0,
            "propostas_contrato_geradas": 0,
            "relatorios_esg_gerados": 0,
            "bounce_cache": 119,
            "bounce_rate": "~20% (93/468 fila)",
            "taxa_resposta": "~4.8% (21/433)",
            "observacao": "Tick de manutenção limpo — mesmo estado estável dos ticks anteriores: caixa zerada, 0 bounces novos, 0 follow-ups atrasados, 0 respostas para atender. 32º dia sem resposta humana REAL (Tauste 30/09). Fila de prospecção zerou os 7 pendentes MX-válidos (agora 0) — o ciclo do Prospector contatou tudo; +9 leads no CSV (424→433) e +2 empresas na fila (466→468). Nenhuma resposta de lead com volume → sem proposta de contrato; nenhuma solicitação ESG → sem relatório. SMTP/IMAP OK. Leads quentes inalterados — fechamento segue bloqueado em ação humana (WhatsApp/telefone)."
        },
        "leads_quentes": [
            "🍀 SANOFI MEDLEY (sac.brasil@sanofi.com) — SAC encaminhou para Compras 29/10 (protocolo 03065348); respondido 30/10 10:55. Follow-up humano em 03/11.",
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 32+ dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 16+ dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês enviada; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste (Salto/região).",
            "🟡 SONDA (ligar 11-2145-6200) / TAUSTE (ligar 15-3324-4680) / NAGUMO (caso 00143542).",
            "🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada 28/10; vigiar resposta.",
            "⚫ GRUPO OBA HORTIFRUTI — ENCERRADO 30/10 (caso recusado pelo SAC/Salesforce)."
        ]
    }
}

# ecossistema.json — prepend (tick novo primeiro)
with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"ecossistema.json atualizado: {len(merged)} chaves top-level")

# insights.md — prepend bloco curto
entrada = """## 2026-10-30 16:05 (Atendente IA - cron #140)

### Números do tick
- 433 leads (287 novo, 84 bounce, 21 respondido, 13 encerrado) · fila 468 (407 contatados, 93 bounce, **0 pendentes** — fila 100% processada).
- 0 notificações Formspree, 0 bounces novos, 0 follow-ups atrasados, 0 respostas pendentes (`replies_pending.json` = `[]`, varredura IMAP ao vivo confirmou caixa limpa).
- Watchdog exit 0 — SMTP/IMAP OK. +9 leads no CSV (424→433) e +2 empresas na fila desde o último tick registrado (#133 12:04).

### O que foi feito
- Sync + auto-correção: nada a corrigir (todos os 119 bounces do cache já tentados, histórico inalterado).
- Sequência/follow-up: nada a enviar; os 7 pendentes MX-válidos foram contatados pelo ciclo do Prospector (fila em 0).
- Respostas: **nenhuma** — nada para atender, portanto sem proposta de contrato e sem relatório ESG gerados.

### Status pipeline
- **32º dia sem resposta humana REAL** (Tauste 30/09) — fechamento continua bloqueado em ação humana nos leads grandes (Savegnago, Pague Menos, Rede Confiança, Covabra) e locais (Brasfrigo, Queijos Itupeva). Protocolo de reengajamento da persona.md é a única alavanca ativa.
- Sanofi Medley segue como lead quente novo (encaminhado a Compras; follow-up humano recomendado 03/11).

---

"""

with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")