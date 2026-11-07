#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza ecossistema.json e insights.md com este ciclo (07/11/2026)."""
import json, datetime, os

BASE = os.path.dirname(__file__)

now = datetime.datetime.now().astimezone()
ts = now.strftime("%Y-%m-%d %H:%M") + " (Atendente IA - cron tick - sábado)"
weekday = now.strftime("%A")

acoes = [
    "✅ sync_formspree.py — 122 bounces cache, 0 notificações Formspree novas",
    "✅ corrigir_emails.py — 0 bounces processados (todos os 122 já tentados; nenhum bounce novo)",
    "✅ prospecao_followup.py — 0 follow-ups atrasados (fila zerada)",
    "✅ bot_oleo.py send_sequence — sequência processada (0 envios pendentes)",
    "✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio)",
    "✅ scan_inbox.py — INBOX: 0 não lidas (455 leads, caixa limpa)",
    "✅ watchdog — exit 1 (455 leads, 323 ativos, 122 bounces, SMTP/IMAP OK; 1 bounce sem correção)",
    "proposta_contrato/relatorio_ESG — não acionados (nenhum lead informou volume; nenhum pedido de relatório)",
    "FILA DE PROSPECÇÃO: zerada — 0 MX-válidos pendentes. 394 em fila_extra aguardando validação.",
]

diagnostico = {
    "total_leads_watchdog": 455,
    "ativos_watchdog": 323,
    "bounce_cache_json": 122,
    "watchdog": "exit 1 — 455 leads, 323 ativos, 122 bounces, SMTP/IMAP OK",
    "fila_extra": "394 empresas (0 pendentes MX-válidos — precisa reposição via lista CNPJ)",
    "dias_sem_resposta_humana_nova": "38 (última: Tauste 30/09; Sanofi Medley 30/10 = encaminhamento a Compras, não resposta de aceitação)",
    "respostas_reais": 0,
    "respostas_humanas": "Nenhuma. 38º dia desde a última resposta humana real (Tauste 30/09). Du Porto respondeu 04/11 informando que não gera óleo de fritura — ofertado vencidos >40%.",
    "respostas_auto": 0,
    "propostas_contrato_geradas": 0,
    "relatorios_esg_gerados": 0,
    "observacao": "38o dia sem respostas humanas novas. Sistema saudavel (SMTP/IMAP OK). Fila de prospeccao zerada. Pipeline 100% bloqueado em acao humana — todos os 10+ leads quentes aguardam WhatsApp/telefone.",
}

novo_ciclo = {
    "timestamp": ts,
    "acoes": acoes,
    "diagnostico": diagnostico,
    "leads_quentes": [
        "SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 38 dias sem ação humana.",
        "PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). Sem retorno desde 14/10.",
        "REDE CONFIANCA (Sorocaba) — proposta 2.500 L/mês na mesa, sem resposta.",
        "COVABRA — AÇÃO HUMANA: preencher cadastro fornecedor (isac.ivrim.com.br). 46+ dias sem ação.",
        "BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local, respondeu.",
        "QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.",
        "SONDA (R$6,12bi) — Ligar (11) 2145-6200.",
        "TAUSTE — Ligar (15) 3324-4680. Respondeu 30/09 — 38 dias.",
        "NAGUMO — Caso 00143542, proposta anexada 14/10.",
        "SANOFI MEDLEY — SAC encaminhou a Compras 29/10 (protocolo 03065348); follow-up humano venceu 03/11 — PENDENTE.",
        "UNIAO SUPERMERCADOS (14 lojas, Itu) — Apresentação enviada 28/10; sem retorno.",
        "TOURINHO ALIMENTOS — Enviado 05/11, aguardar retorno.",
        "SCALA LATICINIOS — Enviado 05/11, aguardar retorno.",
        "DU PORTO — Respondeu 04/11, não gera óleo de fritura. Ofertado vencidos >40% gordura com descaracterização.",
    ]
}

# Atualiza ecossistema.json
ecopath = os.path.join(BASE, "equipe", "ecossistema.json")
with open(ecopath, "r", encoding="utf-8") as f:
    eco = json.load(f)

eco["atualizado_em"] = ts
key = f"ciclo_2026_11_07_atendente_cron_sabado"
eco[key] = novo_ciclo

with open(ecopath, "w", encoding="utf-8", newline="\n") as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)
print("✅ ecossistema.json atualizado.")

# Atualiza insights.md
insight = f"""
## 2026-11-07 (sábado) — {now.strftime('%H:%M')} (Atendente IA - cron tick sábado)

### Diagnóstico do ciclo
- ✅ sync_formspree: 122 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails: 0 bounces processados (todos 122 já tentados)
- ✅ prospecao_followup: 0 follow-ups atrasados (fila zerada)
- ✅ send_sequence: sequência processada (0 envios pendentes)
- ✅ check-replies: 0 respostas (replies_pending.json vazio)
- ✅ scan_inbox: 0 não lidas — caixa limpa
- ✅ watchdog: exit 1 — **455 leads, 323 ativos, 122 bounces, SMTP/IMAP OK**
- 🔴 **38 dias sem resposta humana nova** no fluxo de COMPRA de óleo (última: Tauste 30/09)
- 🔴 **Fila de prospecção ZERADA** — 0 pendentes MX-válidos; 394 na fila_extra (9 não integradas ao leads.csv)
- 🔴 **Pipeline de fechamento 100% bloqueado** — todos os leads quentes aguardam ação humana via WhatsApp/telefone

### Ações deste ciclo
| Ação | Resultado |
|------|-----------|
| sync_formspree.py | 122 bounces cache, 0 notificações novas |
| corrigir_emails.py | 0 processados (todos 122 já tentados) |
| prospecao_followup.py | **0 FP** (fila de follow-ups zerada) |
| send_sequence | sequência processada (0 envios) |
| check-replies | 0 respostas (replies_pending.json vazio) |
| scan_inbox.py | INBOX: 0 não lidas |
| proposta_contrato/relatorio_ESG | Não acionados (0 leads com volume) |

### Leads QUENTES (fluxo de compra de óleo — fechamento depende de ação humana)
0. 🟢 **Du Porto** (sac@duporto.com.br) — respondeu 04/11, não gera óleo de fritura; ofertado vencidos >40% gordura com descaracterização.
1. 🔥🔥🔥 **Savegnago** (R$7,98bi — #1 interior SP) — **38+ dias sem ação humana.** WhatsApp (11) 96785-9631.
2. 🔥🔥🔥 **Pague Menos** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 24 dias sem retorno.
3. 🔥🔥🔥 **Rede Confiança** (Sorocaba) — Proposta 2.500 L/mês. Aguardando retorno.
4. 🔥🔥🔥 **Covabra** — **AÇÃO HUMANA: preencher cadastro de fornecedor** (isac.ivrim.com.br). 46+ dias sem ação.
5. 🔥🔥 **Brasfrigo (Salto/SP)** — Agendar coleta-teste. Local, respondeu.
6. 🔥🔥 **Queijos Itupeva (Rafael)** — Agendar coleta-teste.
7. 🟡 **Sonda** (R$6,12bi) — Ligar (11) 2145-6200.
8. 🟡 **Tauste** — Ligar (15) 3324-4680. Respondeu 30/09 (38 dias).
9. 🟡 **Nagumo** — Caso 00143542, proposta anexada 14/10.
10. 🟢 **Sanofi Medley** (sac.brasil@sanofi.com) — encaminhado a Compras 29/10 (protocolo 03065348). Follow-up humano venceu 03/11 — ainda pendente.
11. 🟢 **União Supermercados** (14 lojas, Itu) — Apresentação enviada 28/10; sem retorno.
12. 🟢 **Tourinho Alimentos** — Enviado 05/11, aguardar retorno.
13. 🟢 **Scala Laticinios** — Enviado 05/11, aguardar retorno.

### Observações
- **38 dias sem resposta humana nova** no fluxo de compra. Última resposta real: Tauste (30/09).
- **Única resposta recente**: Du Porto (04/11) informou que não gera óleo de fritura — ofertamos compra de vencidos >40% gordura com descaracterização.
- **Sanofi Medley** (protocolo 03065348, encaminhado a Compras 29/10): follow-up humano venceu 03/11 — **ainda pendente**, sem retorno do comprador.
- **Fila de prospecção zerada** — 394 empresas em fila_extra.json (não integradas ao leads.csv).
- **Pipeline de fechamento 100% parado** — as 10+ maiores oportunidades aguardam ação humana.
- Nenhum lead informou volume para gerar proposta de contrato ou relatório ESG.
"""

inspath = os.path.join(BASE, "equipe", "insights.md")
with open(inspath, "a", encoding="utf-8", newline="\n") as f:
    f.write(insight)
print("✅ insights.md atualizado.")
print("Tick #162 concluído.")