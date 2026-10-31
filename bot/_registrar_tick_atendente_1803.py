#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 30/10 18:03 — registra tick #146 no ecossistema.json (prepend) e insights.md."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

tick = {
    "ciclo_2026_10_30_atendente_tick_1803": {
        "timestamp": "2026-10-30 18:03 (Atendente IA - cron #146 - sexta-feira)",
        "acoes": [
            "✅ sync_formspree.py — 119 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 bounces novos processados (todos os 119 já tentados; histórico inalterado)",
            "✅ prospecao_followup.py — 0 follow-ups atrasados",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json = [], varredura IMAP scan_inbox.py --dias 2 confirmou caixa limpa)",
            "✅ watchdog.py — exit 0: 433 leads, 307 ativos, 119 bounces, SMTP/IMAP OK",
            "✅ enviar_lote.py --status — fila 468 / 407 contatados / 93 bounce / 0 pendentes (fila 100% processada)",
            "⏭️ proposta_contrato.py — não executado (nenhum lead respondeu com volume novo; 0 leads COM VOLUME no CSV)",
            "⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG/certificado)"
        ],
        "diagnostico": {
            "total_leads": 433,
            "status_leads": {
                "novo": 307,
                "bounce": 90,
                "respondido": 22,
                "encerrado": 14
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
            "taxa_resposta": "~5.1% (22/433)",
            "observacao": "Tick #146 — mesmo estado estável dos ticks anteriores: caixa zerada, 0 bounces novos, 0 follow-ups atrasados, 0 respostas para atender. 32º dia sem resposta humana REAL (Tauste 30/09). Fila de prospecção 100% drenada (0 pendentes MX-válidos). Nenhum lead informou volume (0 registros COM VOLUME no CSV) → sem proposta de contrato; nenhuma solicitação ESG → sem relatório. SMTP/IMAP OK. Fechamento segue bloqueado em ação humana (WhatsApp/telefone) — leads quentes inalterados. Sanofi Medley segue como lead quente novo (encaminhado a Compras em 29/10, follow-up humano recomendado 03/11)."
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
entrada = """## 2026-10-30 18:03 (Atendente IA — cron #146, sexta-feira)

### Números do tick
- **433 leads** (307 novo, 90 bounce, 22 respondido, 14 encerrado) · fila **468** (407 contatados, 93 bounce, **0 pendentes** — fila 100% processada).
- 0 notificações Formspree, 0 bounces novos, 0 follow-ups atrasados, 0 respostas pendentes (`replies_pending.json` = `[]`; `scan_inbox.py --dias 2` confirmou caixa limpa).
- Watchdog exit 0 — SMTP/IMAP OK. Números estáveis vs. tick #145 (16:32).

### O que foi feito
- Sync + auto-correção: nada a corrigir — todos os 119 bounces do cache já tentados, histórico inalterado.
- Sequência/follow-up: nada a enviar (fila zerada).
- Respostas: **nenhuma** — caixa limpa, sem lead para atender; **0 leads COM VOLUME** no CSV → sem proposta de contrato; nenhuma solicitação ESG → sem relatório.
- 6ª rodada do dia de sexta-feira (#141 14:32 → #146 18:03) — todas com diagnóstico limpo idêntico.

### Status pipeline
- **32º dia sem resposta humana REAL** (Tauste 30/09) — fechamento 100% bloqueado em ação humana nos leads grandes (Savegnago, Pague Menos, Rede Confiança, Covabra) e locais (Brasfrigo, Queijos Itupeva). Protocolo de reengajamento via WhatsApp da persona.md segue sendo a única alavanca ativa.
- Sanofi Medley segue como único lead quente novo (encaminhado a Compras 29/10; follow-up humano recomendado 03/11).

---

"""

with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")