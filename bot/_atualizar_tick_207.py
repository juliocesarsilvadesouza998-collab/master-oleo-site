#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 12/11/2026 — registra tick #207 no ecossistema.json e insights.md."""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

now = datetime.datetime.now().astimezone()
ts = now.strftime("%Y-%m-%d %H:%M") + f" (Atendente IA - cron tick #207 - quinta-feira)"

novo_ciclo = {
    "ciclo_2026_11_12_cron_207_atendente": {
        "timestamp": ts,
        "acoes": [
            "sync_formspree.py — 128 bounces cache, 0 notificações Formspree novas (OK)",
            "corrigir_emails.py — 0 bounces processados (todos os 128 já tentados; nenhum bounce novo)",
            "prospecao_followup.py — 0 follow-ups atrasados (fila zerada)",
            "bot_oleo.py send_sequence — sequência processada, 0 envios novos",
            "bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)",
            "_miniscan_inbox.py — INBOX: 0 não lidas",
            "watchdog.py — exit 1: 462 leads, 330 ativos, 93 bounce CSV, 128 cache. SMTP OK · IMAP OK · 1 bounce sem correção (conhecido)",
            "proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação de relatório)"
        ],
        "diagnostico": {
            "total_leads_csv": 462,
            "status_csv": "novo 330 | bounce 93 | respondido 24 | encerrado 15",
            "bounce_cache_json": 128,
            "dias_sem_resposta_humana_fluxo_oleo": "45 (última: Tauste 30/09); 29 dias desde Pague Menos (14/10)",
            "respostas_reais": 0,
            "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX limpa",
            "respostas_auto": 0,
            "propostas_contrato_geradas": 0,
            "relatorios_esg_gerados": 0,
            "observacao": "45º dia sem respostas humanas no fluxo de COMPRA de óleo (última: Tauste 30/09). Sistema saudável — SMTP/IMAP OK. 462 leads (330 ativos), 128 bounces cache. Fila de prospecção zerada — sem fonte de busca gratuita para repor. Nenhuma resposta para processar, nenhum lead informou volume para gerar proposta de contrato ou relatório ESG. Pipeline de fechamento segue bloqueado em ação humana (WhatsApp/telefone) — protocolo de reengajamento da persona aguardando execução manual."
        },
        "leads_quentes": [
            "🍀 SANOFI MEDLEY (SAC 03065348) — respondido 30/10; follow-up humano pendente (45d)",
            "🍀 PASTIFICIO SELMI (ticket 91322) — proposta enviada 03/11; aguardando retorno compras",
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 45+ dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 29 dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada. Aguardando retorno.",
            "🔴🔴🔴 COVABRA — **AÇÃO HUMANA: preencher cadastro fornecedor** (isac.ivrim.com.br). 53+ dias sem ação.",
            "🔴🔴 BRASFRIGO (Salto/SP) — Agendar coleta-teste. Local, respondeu.",
            "🔴🔴 QUEIJOS ITUPEVA (Rafael) — Agendar coleta-teste.",
            "🟡 SONDA (R$6,12bi) — (11) 2145-6200.",
            "🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09.",
            "🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês anexada (14/10)."
        ]
    }
}

# ecossistema.json — prepend
with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(novo_ciclo)
merged.update(eco)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"ecossistema.json atualizado: {len(merged)} ciclos")

# insights.md — prepend bloco
entrada = f"""## 2026-11-12 ~{now.strftime('%H:%M')} (Atendente IA — cron tick #207 - quinta-feira)

### Ações executadas
| Ação | Resultado |
|------|-----------|
| ✅ sync_formspree.py | 128 bounces cache, 0 notificações Formspree novas |
| ✅ corrigir_emails.py | 0 bounces novos (todos os 128 já tentados) |
| ✅ prospecao_followup.py | 0 follow-ups atrasados (fila zerada) |
| ✅ bot_oleo.py send_sequence | Sequência processada, 0 envios |
| ✅ bot_oleo.py check-replies | 0 respostas pendentes (replies_pending.json vazio) |
| ✅ _miniscan_inbox.py | INBOX: 0 não lidas |
| ✅ watchdog.py | exit 1: 462 leads, 330 ativos, 93 bounce CSV, 128 cache. SMTP OK · IMAP OK |
| ⏭️ proposta_contrato.py | Não executado (sem lead com volume novo) |
| ⏭️ relatorio_esg.py | Não executado (sem solicitação ESG/certificado) |

### Diagnóstico
| Indicador | Valor |
|-----------|-------|
| Total leads | 462 |
| `novo` | 330 |
| `respondido` | 24 |
| `bounce` | 93 (128 cache) |
| `encerrado` | 15 |
| Follow-ups atrasados | 0 ✅ |
| Respostas pendentes | 0 ✅ |
| Fila prospecção | 0 MX-válidos ❌ (fila drenada — 45º dia sem cold email) |
| Dias sem resposta humana | **45** (Tauste 30/09); 29 desde Pague Menos (14/10) |
| Caixa IMAP | 0 não lidas ✅ |
| SMTP/IMAP | OK ✅ |

### 🔥 Leads QUENTES (fluxo de compra de óleo — fechamento depende de ação humana)
0. 🍀 **Sanofi Medley** (SAC 03065348) — respondido 30/10; follow-up humano pendente (45d)
1. 🍀 **Pastificio Selmi** (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno comercial
2. 🔴🔴🔴 **Savegnago** (R$7,98bi — #1 interior SP) — 45+ dias sem ação humana. WhatsApp (11) 96785-9631
3. 🔴🔴🔴 **Pague Menos** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 29 dias sem retorno
4. 🔴🔴🔴 **Rede Confiança** (Sorocaba) — Proposta 2.500 L/mês. Aguardando retorno
5. 🔴🔴🔴 **Covabra** — **AÇÃO HUMANA: preencher cadastro de fornecedor** (isac.ivrim.com.br). 53+ dias sem ação
6. 🔴🔴 **Brasfrigo** (Salto/SP) — Agendar coleta-teste. Local, respondeu
7. 🔴🔴 **Queijos Itupeva** (Rafael) — Agendar coleta-teste
8. 🟡 **Sonda** (R$6,12bi) — Ligar (11) 2145-6200
9. 🟡 **Tauste** — Ligar (15) 3324-4680. Respondeu 30/09 (45 dias)
10. 🟡 **Nagumo** — Caso 00143542, proposta anexada 14/10

### Observações
- **45º dia sem resposta humana nova** no fluxo de compra de óleo. Todas as últimas respostas (Tauste, Savegnago, Pague Menos, Rede Confiança, Covabra, Selmi) aguardam ação humana — WhatsApp ou ligação.
- **Pipeline de fechamento 100% bloqueado** em ação humana — nenhum script faz ligação ou envia WhatsApp. O protocolo de reengajamento semanal da persona (Savegnago → Pague Menos → Rede Confiança → Brasfrigo) ainda não foi executado.
- **Fila de prospecção zerada** sem fonte gratuita para repor. Próximo passo: listas CNPJ pagas (Leadjet CNAE 1052-0, 1041-4, 1043-1).
- SMTP/IMAP funcionando normalmente. Sistema saudável, apenas aguardando ação humana para destravar.

---

"""
with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")