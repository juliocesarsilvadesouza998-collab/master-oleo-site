#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atendente IA 28/10 19:09 (tick #16): registra ciclo + correção do parser de bounces."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
EQUIPE = os.path.join(BASE, "..", "equipe")
ECOSSISTEMA = os.path.join(EQUIPE, "ecossistema.json")
INSIGHTS = os.path.join(EQUIPE, "insights.md")

tick = {
    "ciclo_2026_10_28_atendente_tick_1909": {
        "timestamp": "2026-10-28 19:09 (Atendente IA - cron quarta-feira - tick diurno #16)",
        "acoes": [
            "✅ sync_formspree.py — 112 bounces cache, 0 notificações Formspree novas",
            "✅ corrigir_emails.py — 0 processados (todos os bounces anteriores já tentados)",
            "✅ prospecao_followup.py — 0 follow-ups (nada atrasado)",
            "✅ send_sequence — sequência processada (nada a enviar)",
            "✅ check-replies — 0 respostas pendentes (replies_pending.json vazio)",
            "✅ scan_inbox.py --tudo --dias 3 — 28 mensagens: bounces + auto-acks ICT (protocolos 1173/1174) + Artema já atendida + 4 spam. Nenhum lead não atendido.",
            "✅ watchdog.py — exit 0: 392 leads, 276 ativos, 112 bounces, SMTP/IMAP OK",
            "✅ enviar_lote.py --status — fila 430 / 370 contatados / 89 bounce / 0 pendentes",
            "🔧 CORREÇÃO APLICADA em sync_formspree.py (2 bugs no detector de bounces): (1) fetch passou de BODY.PEEK[TEXT] para RFC822 decodificando TODAS as partes — bounces no formato multipart/report do Gmail (ex. Ponto Certo) ficavam invisíveis; (2) o filtro descartava QUALQUER endereço @gmail.com, escondendo leads legítimos hospedados no Gmail.",
            "🔧 EFEITO DA CORREÇÃO: cache 112 → 115 bounces; lead 'Mercado Ponto Certo' (Tietê/SP, bounce real 28/10 15:40 — 550 5.1.1 conta inexistente) foi registrado e marcado status=bounce (antes estava 'novo' com e-mail inválido).",
            "⏭️ corrigir_emails.py (2ª passada) — Ponto Certo: nenhum e-mail alternativo encontrado via busca web → permanece bounce, sem reenvio (política do projeto aplicada).",
            "✅ Organ Alimentos (Organutech) — mudança de endereço para contato@organupar.com.br já corrigida em 27/10; confirmado em correcoes_emails.json, nada a refazer.",
            "⏭️ proposta_contrato.py — não executado (nenhum lead com volume novo)",
            "⏭️ relatorio_esg.py — não executado (nenhuma solicitação ESG)"
        ],
        "diagnostico": {
            "fila_total": 430,
            "fila_contatados": 370,
            "fila_bounce": 89,
            "fila_pendentes": 0,
            "leads_csv": 392,
            "leads_bounce_status": 87,
            "bounce_cache_json": 115,
            "respostas_total": 22,
            "respondidos_hoje": [
                "ICT Farmacêutica 09:33 (auto-ack SAC, protocolos 1173/1174 — aguarda setor de compras)",
                "Artema Pre Moldados 14:43 (desmoldante, respondido_atendente — pediu amostra grátis)"
            ],
            "caixa_nao_lidas": 0,
            "dias_sem_resposta_humana": "30 (última: Pague Menos 14/10; última real: Tauste 30/09)",
            "observacao": "Tick #16 — 16º ciclo consecutivo sem novas respostas humanas. Diferencial do tick: o detector de bounces estava CEGO para o formato multipart/report do Gmail e para leads no Gmail, deixando um lead com e-mail inválido marcado como 'novo' (risco de reenvio eterno e de inflar falsa esperança). Corrigido e validado: cache 112→115, lead reclassificado. Pipeline de prospecção segue parado (0 pendentes); reabastecimento depende de listas CNPJ (Leadjet).",
            "melhoria_aplicada": "sync_formspree.py — parser de bounces robusto (RFC822 multi-parte) + filtro de exclusão corrigido (só o e-mail do bot é ignorado)"
        },
        "leads_quentes": [
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. 30+ dias sem ação humana.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 15 dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês enviada; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste (Salto/região).",
            "🟡 SONDA (ligar 11-2145-6200) / TAUSTE (ligar 15-3324-4680) / ICT FARMACÊUTICA (SAC 1173).",
            "🟢 UNIÃO SUPERMERCADOS (14 lojas, Itu) — apresentação enviada 28/10 15:3x; vigiar resposta."
        ]
    }
}

with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

entrada = """## 2026-10-28 19:09 (Atendente IA - cron quarta-feira - tick diurno #16)

### Diagnóstico do ciclo
- ✅ **Watchdog** — exit 0: 392 leads, 276 ativos, SMTP/IMAP OK
- ✅ **Fila** — 430 / 370 contatados / 89 bounce / **0 pendentes** (inalterado)
- ✅ **Caixa** — varredura (tudo, 3 dias): 28 mensagens = bounces Gmail + auto-acks ICT (protocolos 1173/1174) + resposta Artema já atendida + 4 spam. **Nenhum lead não atendido**
- ✅ **Sequência/replies** — 0 follow-ups, 0 respostas pendentes (16º tick consecutivo sem novos contatos)
- ⏭️ **proposta_contrato / relatorio_esg** — não executados (sem volume novo, sem pedido ESG)

### 🔧 Problema real encontrado e resolvido neste tick
**O detector de bounces estava cego para dois casos** (`sync_formspree.py`):
1. **Formato `multipart/report` do Gmail** — o script usava `BODY.PEEK[TEXT]`, que não expõe a parte com o endereço. Bounces novos ficavam invisíveis ao pipeline (cache travado em 112 mesmo com DSN na caixa).
2. **Filtro `"gmail.com" not in el`** — descartava QUALQUER lead hospedado no Gmail, tratando-o como ruído.

**Consequência real:** o lead **Mercado Ponto Certo (Tietê/SP)** recebeu o e-mail em 28/10 15:41, o Gmail devolveu **550 5.1.1 (conta não existe)** às 15:40, e o lead **continuava com status `novo`** — ficaria na fila como se fosse válido (risco de reenvio eterno e de mascarar o bounce rate real).

**Correção aplicada e validada:** fetch via `RFC822` decodificando todas as partes + exclusão apenas do próprio e-mail do bot. Resultado: **cache 112 → 115 bounces**, Ponto Certo registrado e marcado `status=bounce`. Na 2ª passada do `corrigir_emails.py`, nenhum e-mail alternativo foi encontrado → permanece bounce, **sem reenvio** (política do projeto). Organ Alimentos (→ contato@organupar.com.br) confirmado como já corrigido em 27/10.

### Leads QUENTES
| Prioridade | Lead | Status/próximo passo |
|:----------:|------|----------------------|
| 🔴🔴🔴 | SAVEGNAGO (R$7,98bi) | WhatsApp (11) 96785-9631 — 30+ dias sem ação humana |
| 🔴🔴🔴 | PAGUE MENOS (R$4,33bi) | Ticket 407470 (Josiane Marinho) — 15 dias |
| 🔴🔴🔴 | REDE CONFIANÇA (Sorocaba) | Proposta 2.500 L/mês enviada |
| 🔴🔴🔴 | COVABRA | Cadastro fornecedor portal Ivrim (ação humana) |
| 🔴🔴 | BRASFRIGO / QUEIJOS ITUPEVA | Coleta-teste a agendar (região de Salto) |
| 🆕🔴 | ARTEMA PRÉ-MOLDADOS (Paranaguá/PR — desmoldante) | Pediu amostra grátis; respondido 14:43 — enviar amostra + follow-up de venda |
| 🟡 | SONDA (11-2145-6200) / TAUSTE (15-3324-4680) / ICT FARMACÊUTICA (SAC 1173) | Ligar / aguardar compras |
| 🟢 | UNIÃO SUPERMERCADOS (14 lojas, Itu) | Apresentação enviada 28/10 — vigiar resposta |

### Observações
- **16º tick consecutivo sem resposta humana nova.** O gargalo segue sendo ação humana (WhatsApp/telefone) nos leads quentes + reposição da fila (listas CNPJ/Leadjet).
- **Qualidade do dado melhorou neste tick:** o bounce rate e o status dos leads agora refletem a caixa real — um lead inválido que estava oculto foi reclassificado.
- Bounce rate atual: **~29%** (112→115 de 392) — segue acima da meta de 15%, reforçando a necessidade de listas CNPJ validadas.

---
"""

with open(INSIGHTS, encoding="utf-8") as f:
    current = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + current)

print("ecossistema.json + insights.md atualizados (tick #16 registrado)")
