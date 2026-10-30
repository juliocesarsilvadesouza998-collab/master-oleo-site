#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 30/10 13:33 — registra tick #139 no ecossistema.json (prepend) e insights.md."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

tick = {
    "ciclo_2026_10_30_atendente_tick_1333": {
        "timestamp": "2026-10-30 13:33 (Atendente IA - cron #139 - sexta-feira)",
        "acoes": [
            "✅ sync_formspree.py — 118 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 bounces novos processados (todos os 118 já tentados; histórico inalterado)",
            "✅ prospecao_followup.py — 0 follow-ups atrasados",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json vazio)",
            "✅ watchdog.py — exit 0: 424 leads, 299 ativos, 118 bounces, SMTP/IMAP OK",
            "✅ enviar_lote.py --status — fila 466 / 398 contatados / 92 bounce / 7 pendentes MX-válidos (Frisa, Verdi, do Sul, 3R, Maxxi Ovos, Confianca, SM Boa)",
            "✅ scan_inbox.py --dias 2 — 0 mensagens não lidas/recentes (424 leads, 271 msgids)",
            "⏭️ proposta_contrato.py — não executado (nenhum lead respondeu com volume novo)",
            "⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG/certificado)"
        ],
        "diagnostico": {
            "total_leads": 424,
            "status_leads": {
                "novo": 299,
                "bounce": 89,
                "respondido": 22,
                "encerrado": 14
            },
            "fila_total": 466,
            "fila_contatados": 398,
            "fila_bounce": 92,
            "fila_pendentes": 7,
            "followups_enviados_hoje": 0,
            "respostas_processadas": 0,
            "propostas_contrato_geradas": 0,
            "relatorios_esg_gerados": 0,
            "bounce_cache": 118,
            "bounce_rate": "~21% (92/466 fila)",
            "taxa_resposta": "~5.2% (22/424)",
            "observacao": "Tick de manutenção limpo — mesmas condições do #138 (13:02): caixa zerada, 0 bounces novos, 0 follow-ups atrasados, 0 respostas para atender. 32º dia sem resposta humana REAL (Tauste 30/09). Fila mantém 7 pendentes MX-válidos aguardando o ciclo do Prospector. SMTP/IMAP OK. Nenhuma resposta de lead com volume → sem proposta de contrato; nenhuma solicitação ESG → sem relatório."
        },
        "leads_quentes": [
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 32+ dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 16+ dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês enviada; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste (Salto/região).",
            "🟡 SONDA (ligar 11-2145-6200) / TAUSTE (ligar 15-3324-4680) / ICT FARMACÊUTICA (SAC 1173).",
            "🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada 28/10; vigiar resposta (padrão SAC→comercial).",
            "⚫ GRUPO OBA HORTIFRUTI — ENCERRADO 30/10 (caso recusado pelo sistema SAC/Salesforce)."
        ]
    }
}

# ecossistema.json — prepend
with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)  # tick novo primeiro (dict preserva ordem de inserção)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"ecossistema.json atualizado: {len(merged)} ciclos registrados")

# insights.md — prepend bloco curto
entrada = """## 2026-10-30 13:33 (Atendente IA - cron #139)

### Números do tick
- 424 leads (299 novo, 89 bounce, 22 respondido, 14 encerrado) · fila 466 (398 contatados, 92 bounce, **7 pendentes** MX-válidos).
- 0 notificações Formspree, 0 bounces novos, 0 follow-ups atrasados, 0 respostas pendentes (`replies_pending.json` = `[]`).
- Watchdog exit 0 — SMTP/IMAP OK. Caixa IMAP limpa (0 mensagens recentes).

### O que foi feito
- Sync + auto-correção: nada a corrigir (todos os 118 bounces do cache já tentados, histórico inalterado desde 09:32).
- Sequência/follow-up: nada a enviar (fila de envio processada pelo ciclo do Prospector).
- Respostas: **nenhuma** — nada para atender, portanto sem proposta de contrato e sem relatório ESG gerados.

### Status pipeline
- **32º dia sem resposta humana REAL** (Tauste 30/09) — o fechamento continua bloqueado em ação humana nos 4 leads grandes (Savegnago, Pague Menos, Rede Confiança, Covabra) e nos locais (Brasfrigo, Queijos Itupeva). Protocolo de reengajamento da persona.md é a única alavanca ativa.
- 7 pendentes MX-válidos aguardando o próximo ciclo do Prospector (09:15).

---

"""

with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")