#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 28/10 15:30 (tick #9): registra ciclo no ecossistema.json (prepend) e insights.md."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

tick = {
    "ciclo_2026_10_28_atendente_tick_1530": {
        "timestamp": "2026-10-28 15:30 (Atendente IA - cron quarta-feira - tick diurno #9)",
        "acoes": [
            "✅ sync_formspree.py — 112 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 processados (todos os 112 bounces já tentados anteriormente)",
            "✅ prospecao_followup.py — 0 follow-ups processados (nada pendente)",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json vazio)",
            "✅ scan_inbox.py --dias 7 — 0 não lidas/recentes na caixa (392 leads, 321 msgids)",
            "🔥 enviar_lote.py --max 15 — DESTRAVOU a fila: 11 emails de apresentação enviados (fila reabastecida 14:06 pelo Melhorador estava parada; Prospector só roda 09:15). Municípios novos: Tietê (Tiba, Potiguara, Ponto Certo, TBS), Itu (Mercado Atual, União Supermercados), Sorocaba (Boi na Brasa), Cerquilho (Stabilê, M&M, Tiãozinho), Unialimentar (email corrigido gmail)",
            "🐛 FIX: enviar_lote.py quebrou ao gravar — lead desmoldante com id NÃO numérico 'ARTEMA20261028' (linha 382, inserido pelo fluxo desmoldante 14:42) estourava int() no merge_write_leads e IMPEDIA qualquer lote futuro de persistir. Patch: base_id = max apenas de ids numéricos.",
            "🔧 RECUPERAÇÃO: _reparo_lote.py — leu a pasta Sent do Gmail, confirmou os 11 envios reais (32 mensagens enviadas hoje) e registrou os 11 leads no leads.csv com apresentacao_em + apresentacao_msgid autênticos (evita reenvio duplicado e mantém correlação de thread para check-replies)",
            "🎯 Resultado: fila 430 / 370 contatados / 89 bounce / 0 PENDENTES — pipeline 100% drenado pela primeira vez",
        ],
        "diagnostico": {
            "fila_total": 430,
            "fila_contatados": 370,
            "fila_bounce": 89,
            "fila_pendentes": 0,
            "fila_pendentes_antes": 11,
            "enviados_hoje_atendente": 11,
            "respostas_total": 22,
            "respondidos_hoje": ["ICT Farmacêutica 09:33 (respondido_atendente)", "Artema Pre Moldados 14:43 (desmoldante, respondido_atendente)"],
            "caixa_nao_lidas": 0,
            "observacao": "Sem respostas novas para atender neste tick. Pipeline de prospecção ZERADO pela primeira vez (0 pendentes). Gargalo segue sendo AÇÃO HUMANA nos leads quentes (Savegnago 29d, Pague Menos 14d, Covabra Ivrim, Rede Confiança, Sonda/Tauste ligações). Bug do id não numérico teria travado TODOS os envios futuros — corrigido e testado."
        },
        "leads_quentes": [
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 30 dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 15 dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana, lead mais maduro).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste.",
            "🟡 SONDA — ligar (11) 2145-6200. 🟡 TAUSTE — ligar (15) 3324-4680. 🟡 ICT FARMACÊUTICA respondeu 28/10 09:33 — acompanhar.",
            "🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada HOJE 15:3x; rede local grande, observar resposta (padrão SAC→comercial)."
        ]
    }
}

with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"ecossistema.json atualizado: {len(merged)} ciclos registrados")

entrada = """## 2026-10-28 15:30 (Atendente IA - cron quarta-feira - tick diurno #9)

### Diagnóstico do ciclo
- ✅ **Watchdog** — 392 leads, caixa sem não-lidas (scan 7d), SMTP/IMAP OK
- ✅ **sync_formspree.py**: 112 bounces cache, 0 notificações Formspree novas
- ✅ **corrigir_emails.py**: 0 processados — todos os 112 bounces já tentados anteriormente
- ✅ **prospecao_followup.py**: 0 follow-ups — nada atrasado
- ✅ **send_sequence**: sequência processada (nada a enviar)
- ✅ **check-replies**: 0 respostas pendentes — replies_pending.json vazio
- ✅ **scan_inbox.py --dias 7**: 0 não lidas — caixa zerada (392 leads, 321 msgids)
- ⏭️ **proposta_contrato.py**: não executado — nenhum lead novo com volume informado
- ⏭️ **relatorio_esg.py**: não executado — nenhuma solicitação ESG

### 🔥 Ação principal: pipeline de prospecção 100% DESTRAVADO
- A fila estava com **11 pendentes enviáveis** desde o reabastecimento do Melhorador (14:06), mas o Prospector só roda 09:15 — os leads ficariam ~19h parados.
- **enviar_lote.py --max 15 → 11 emails enviados** para: Unialimentar (gmail corrigido), Stabilê, M&M, Tiãozinho (Cerquilho), Tiba, Potiguara, Ponto Certo, TBS (Tietê), Mercado Atual + União Supermercados (Itu, 14 lojas), Churrascaria Boi na Brasa (Sorocaba).
- **Resultado: fila 430 / 370 contatados / 89 bounce / 0 pendentes** — primeira vez que o pipeline drena por completo.

### 🐛 Bug corrigido (crítico)
- **`merge_write_leads` quebrava com id não numérico**: o fluxo desmoldante inseriu a linha `ARTEMA20261028` (Artema Pre Moldados, 14:42) no leads.csv; `int('ARTEMA20261028')` estourava ValueError na gravação de QUALQUER lote futuro. O lote enviou os 11 emails mas não persistiu nada.
- **Fix**: `base_id = max((int(l.get("id")) for l in atuais if str(l.get("id") or "").strip().isdigit()), default=0)` — ignora ids não numéricos.
- **Recuperação sem duplicar**: `_reparo_lote.py` leu a pasta Sent (32 envios de hoje), confirmou os 11 Message-IDs reais e registrou os leads com `apresentacao_em` + `apresentacao_msgid` autênticos — próximo lote não reenvia e a correlação de thread do check-replies funciona.
- **Lição**: ids de lead não são garantidamente numéricos (fluxo desmoldante usa `DESMOLDANTE+data`). Qualquer script que faça `int()` em id precisa filtrar. O fix ficou no próprio `enviar_lote.py` (fonte compartilhada).

### Respondidos hoje (já atendidos — nada pendente)
- **ICT Farmacêutica** (Votorantim, nicho encapsulados) — respondeu 09:33, marcado respondido pelo atendente no tick da manhã.
- **Artema Pre Moldados** (Paranaguá/PR, fluxo desmoldante) — respondeu 14:42, respondido 14:43.

### Leads QUENTES (inalterado — aguardam ação humana)
| Prioridade | Lead | Próximo passo |
|:----------:|------|----------------|
| 🔴🔴🔴 | **SAVEGNAGO** (R$7,98bi, #1 interior SP) | WhatsApp (11) 96785-9631. 30 dias sem ação. |
| 🔴🔴🔴 | **PAGUE MENOS** (R$4,33bi) | Acompanhar ticket 407470 (Josiane Marinho). 15 dias. |
| 🔴🔴🔴 | **REDE CONFIANÇA** (Sorocaba) | Proposta 2.500 L/mês enviada; aguardando. |
| 🔴🔴🔴 | **COVABRA** | Cadastro fornecedor no portal Ivrim (isac.ivrim.com.br) — ação humana. |
| 🔴🔴 | **BRASFRIGO / QUEIJOS ITUPEVA** | Agendar coleta-teste (região de Salto). |
| 🟡 | **SONDA / TAUSTE** | Ligar (11) 2145-6200 / (15) 3324-4680. |
| 🟢 | **UNIÃO SUPERMERCADOS** (Itu, 14 lojas) | Apresentação enviada hoje — vigiar resposta (padrão SAC→comercial). |

### Decisões deste ciclo
- **Enviar lote fora do horário do Prospector**: justificado — fila reabastecida 14:06, leads MX-validados pelo Melhorador, limite diário ainda folgado (11 de 15). Enviar = destravar; esperar = 19h parado.
- **Corrigir bug no código compartilhado** (`enviar_lote.py`): impacto positivo em todos os agentes que usam merge_write_leads (Prospector, Estrategista, Atendente).

---

"""

with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")