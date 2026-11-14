#!/usr/bin/env python3
"""Atualiza ecossistema.json e insights.md com este ciclo do atendente."""
import json, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now().astimezone()
dia_pt = {
    'Monday': 'segunda-feira', 'Tuesday': 'terça-feira', 'Wednesday': 'quarta-feira',
    'Thursday': 'quinta-feira', 'Friday': 'sexta-feira', 'Saturday': 'sábado', 'Sunday': 'domingo'
}
dia = dia_pt.get(now.strftime('%A'), now.strftime('%A'))
tick_num = 232

ts = now.strftime("%Y-%m-%d %H:%M") + f" (Atendente IA - cron tick #{tick_num} - {dia})"

novo_ciclo = {
    "timestamp": ts,
    "acoes": [
        "sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas",
        "corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)",
        "prospecao_followup.py — 0 follow-ups processados (fila zerada)",
        "bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)",
        "bot_oleo.py check-replies — 0 respostas pendentes (replies_pending.json vazio)",
        "proposta_contrato.py — não executado (sem lead com volume novo informado)",
        "relatorio_esg.py — não executado (sem solicitação ESG/certificado)"
    ],
    "diagnostico": {
        "total_leads_csv": "~469",
        "status_csv": "novo ~283 | bounce ~94 (129 cache) | respondido 24 | encerrado 15 | descartado 53",
        "bounce_cache_json": 129,
        "dias_sem_resposta_humana_fluxo_oleo": "52 (última: Tauste 30/09); 32 desde Pague Menos (14/10)",
        "respostas_reais": 0,
        "respostas_humanas_fluxo_oleo": "Nenhuma — replies_pending.json vazio, INBOX limpa",
        "propostas_contrato_geradas": 0,
        "relatorios_esg_gerados": 0,
        "observacao": "52º dia sem respostas humanas no fluxo de COMPRA de óleo. Sistema saudável — SMTP/IMAP OK. ~469 leads, 129 bounces cache. Fila de prospecção zerada — sem fonte MX-válida para repor. Pipeline bloqueado em ação humana — WhatsApp/telefone e cadastro Covabra Ivrim são barreiras."
    },
    "leads_quentes": [
        "🍀 SANOFI MEDLEY (SAC 03065348) — respondido 30/10; follow-up humano pendente (52d)",
        "🍀 PASTIFICIO SELMI (compras@selmi.com.br) — proposta 800 L/mês enviada 03/11; aguardando retorno",
        "🔴🔴🔴 SAVEGNAGO (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 52+ dias sem ação humana.",
        "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — Ticket 407470 (Josiane Marinho). 32 dias sem retorno.",
        "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — Proposta 2.500 L/mês enviada. Aguardando retorno.",
        "🔴🔴🔴 COVABRA — AÇÃO HUMANA: cadastro fornecedor isac.ivrim.com.br pendente. 56+ dias!",
        "🔴🔴 BRASFRIGO (Salto/SP) — Coleta-teste a agendar. Local.",
        "🔴🔴 QUEIJOS ITUPEVA (Rafael) — Coleta-teste a agendar.",
        "🟡 SONDA (R$6,12bi) — (11) 2145-6200.",
        "🟡 TAUSTE — (15) 3324-4680. Respondeu 30/09 (52 dias).",
        "🟡 NAGUMO — Caso 00143542, proposta 5.000 L/mês anexada"
    ]
}

# ecossistema.json in bot/equipe/
ecopath1 = os.path.join(BASE, "equipe", "ecossistema.json")
if os.path.exists(ecopath1):
    with open(ecopath1, "r", encoding="utf-8-sig") as f:
        eco = json.load(f)
    eco["atualizado_em"] = ts
    key = f"ciclo_{now.strftime('%Y_%m_%d_%H%M')}_cron_atendente_{tick_num}"
    eco[key] = novo_ciclo
    with open(ecopath1, "w", encoding="utf-8", newline="\n") as f:
        json.dump(eco, f, ensure_ascii=False, indent=1)
    print("bot/equipe/ecossistema.json atualizado.")
else:
    print("bot/equipe/ecossistema.json not found!")

# ecossistema.json em equipe/ (raiz)
ecopath2 = os.path.normpath(os.path.join(BASE, "..", "equipe", "ecossistema.json"))
if os.path.exists(ecopath2) and os.path.abspath(ecopath2) != os.path.abspath(ecopath1):
    with open(ecopath2, "r", encoding="utf-8-sig") as f:
        eco2 = json.load(f)
    eco2["atualizado_em"] = ts
    eco2[key] = novo_ciclo
    with open(ecopath2, "w", encoding="utf-8", newline="\n") as f:
        json.dump(eco2, f, ensure_ascii=False, indent=1)
    print("equipe/ecossistema.json (raiz) atualizado.")
else:
    print("equipe/ecossistema.json (raiz) é o mesmo arquivo ou não existe.")

# insights.md
insight = f"""

## {now.strftime('%Y-%m-%d %H:%M')} (Atendente IA - cron tick #{tick_num} - {dia})

### Diagnóstico do ciclo
- ✅ sync_formspree.py — 129 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails.py — 0 bounces processados (todos os 129 já tentados; nenhum bounce novo)
- ✅ prospecao_followup.py — 0 follow-ups processados (fila zerada)
- ✅ bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)
- ✅ bot_oleo.py check-replies — 0 respostas pendentes (replies_pending.json vazio)
- ⏭️ proposta_contrato.py — não executado (sem lead com volume novo informado)
- ⏭️ relatorio_esg.py — não executado (sem solicitação ESG/certificado)
- 🔴 **52º dia sem respostas humanas no fluxo de COMPRA de óleo**
- 🔴 Fila de prospecção zerada — sem fonte MX-válida para repor

### 🔥 Leads QUENTES (fechamento depende de ação humana)
1. 🍀 **Sanofi Medley** — SAC 03065348 (30/10). Follow-up humano pendente.
2. 🍀 **Pastificio Selmi** — Proposta 800 L/mês enviada 03/11. Aguardando compras.
3. 🔴🔴🔴 **SAVEGNAGO** (R$7,98bi) — WhatsApp (11) 96785-9631. 52+ dias!
4. 🔴🔴🔴 **PAGUE MENOS** (R$4,33bi) — Ticket 407470 (Josiane). 32 dias.
5. 🔴🔴🔴 **REDE CONFIANÇA** (Sorocaba) — Proposta 2.500 L/mês.
6. 🔴🔴🔴 **COVABRA** — **AÇÃO HUMANA: cadastro Ivrim** (isac.ivrim.com.br). 56+ dias.
7. 🔴🔴 **BRASFRIGO** (Salto/SP) — Coleta-teste a agendar.
8. 🔴🔴 **QUEIJOS ITUPEVA** (Rafael) — Coleta-teste a agendar.
9. 🟡 **SONDA** (R$6,12bi) — (11) 2145-6200.
10. 🟡 **TAUSTE** — (15) 3324-4680. Respondeu 30/09.
11. 🟡 **NAGUMO** — Caso 00143542, proposta 5.000 L/mês.

### Observações
- **52 dias sem resposta humana nova** (última: Tauste 30/09). Após 469 leads, cold email atingiu o teto.
- **Pipeline de fechamento 100% parado** em ação humana — WhatsApp, telefone, cadastro Ivrim.
- Nenhum bounce novo, nenhuma resposta pendente, nenhuma notificação Formspree.
- SMTP/IMAP OK. Fila de prospecção zerada — sem fonte gratuita para repor.

"""

for inspath_candidate in [
    os.path.join(BASE, "equipe", "insights.md"),
    os.path.normpath(os.path.join(BASE, "..", "equipe", "insights.md"))
]:
    inspath = os.path.normpath(inspath_candidate)
    if os.path.exists(inspath):
        with open(inspath, "a", encoding="utf-8", newline="\n") as f:
            f.write(insight)
        print(f"insights.md atualizado: {inspath}")

print("Concluído.")