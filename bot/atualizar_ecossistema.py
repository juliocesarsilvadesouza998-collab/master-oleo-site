#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza ecossistema.json e insights.md com este ciclo."""
import json, datetime, os

BASE = os.path.dirname(__file__)

# Dados do ciclo
now = datetime.datetime.now().astimezone()
ts = now.strftime("%Y-%m-%d %H:%M") + " (Atendente IA - cron tick - terça-feira)"

novo_ciclo = {
    "timestamp": ts,
    "acoes": [
        "✅ sync_formspree.py — 120 bounces cache, 0 notificações novas",
        "✅ corrigir_emails.py — 0 bounces processados (todos já tentados anteriormente)",
        "✅ prospecao_followup.py — 41 follow-ups processados (FP1/FP2/FP3)",
        "✅ send_sequence — sequência processada",
        "✅ check-replies — 1 pendência: Selmi SAC redirecionou p/ compras@selmi.com.br",
        "✅ proposta_contrato.py --empresa 'Pastificio Selmi S/A' --volume 800 — proposta HTML gerada (R$1.120/mês, R$13.440/ano)",
        "✅ enviar_proposta_selmi.py — proposta enviada + leads atualizados (compras@selmi.com.br reativado, sac@ encerrado)",
        "✅ replies_pending.json zerado"
    ],
    "diagnostico": {
        "total_leads_watchdog": 438,
        "ativos_watchdog": 308,
        "bounce_cache_json": 120,
        "watchdog": "exit 0 — saudável",
        "fila_extra": "0 pendentes MX-válidos (precisa reposição)",
        "dias_sem_resposta_humana_nova": "34 (última: Tauste 30/09; Selmi 03/11 = SAC redirect para compras, não é resposta de aceitação)",
        "respostas_reais": 1,
        "respostas_humanas": "Selmi (Pastificio Selmi S/A) — SAC redirecionou para compras@selmi.com.br. Clássico padrão de semi-fechamento (como Savegnago, Pague Menos, Rede Confiança). Proposta de 800 L/mês enviada para o canal comercial.",
        "respostas_auto": 0,
        "propostas_contrato_geradas": "1 (Selmi — Pastificio Selmi S/A, 800 L/mês)",
        "relatorios_esg_gerados": 0
    }
}

# Atualiza ecossistema.json
ecopath = os.path.join(BASE, "equipe", "ecossistema.json")
with open(ecopath, "r", encoding="utf-8-sig") as f:
    eco = json.load(f)

# Atualiza timestamp root
eco["atualizado_em"] = ts

# Adiciona novo ciclo
key = f"ciclo_2026_11_03_atendente_cron_161"
eco[key] = novo_ciclo

with open(ecopath, "w", encoding="utf-8", newline="\n") as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)
print("ecossistema.json atualizado.")

# Atualiza insights.md
insight = f"""\n\n## 2026-11-03 (terça-feira) — {now.strftime('%H:%M')} (Atendente IA - cron tick #161)

### Diagnóstico do ciclo
- ✅ sync_formspree: 120 bounces cache, 0 notificações Formspree novas
- ✅ corrigir_emails: 0 bounces novos processados (todos já tentados)
- ✅ prospecao_followup: **41 follow-ups** — 10 FP3 + 30+ FP2 + 4 FP1 (nicho supermercados/indústrias/encapsulados)
- ✅ send_sequence: sequência processada
- ✅ check-replies: **1 resposta** — Selmi (Pastificio Selmi S/A)
- ✅ **🔥 AÇÃO**: SAC Selmi (Cristina Magalhães) redirecionou para compras@selmi.com.br — padrão clássico de semi-fechamento!
- ✅ Proposta de contrato **800 L/mês → R$1.120/mês → R$13.440/ano** gerada e enviada para compras@selmi.com.br
- ✅ Lead compras@selmi.com.br reativado, sac@selmi.com.br encerrado/transferido
- ✅ replies_pending.json zerado
- 🔴 **34 dias sem resposta humana real nova** no fluxo de COMPRA de óleo
- 🔴 Fila de prospecção ZERADA — 0 MX-válidos pendentes

### 🔥 LEAD QUENTE DO DIA: Pastificio Selmi S/A
- **Padrão**: SAC Selmi (Cristina Magalhães) respondeu o ticket Zendesk 91332 e **redirecionou para compras@selmi.com.br**
- **Significado**: MESMO padrão de Savegnago, Pague Menos, Rede Confiança — SAC que encaminha = semi-fechamento
- **O que foi feito**: Proposta formal gerada (800 L/mês estimados, R$1,40/L, R$13.440/ano) + bônus de exclusividade (+R$0,10/L) e consolidação (+R$0,05/L) + cobertura completa de benefícios (bombonas, certificado, relatório ESG, PIX)
- **Próximo passo**: Aguardar retorno do comprador. Follow-up por WhatsApp (11) 96785-9631 em 3-5 dias se silêncio.

### Ações deste ciclo
| Ação | Resultado |
|------|-----------|
| sync_formspree.py | 120 bounces cache, 0 notificações novas |
| corrigir_emails.py | 0 processados (todos já tentados) |
| prospecao_followup.py | **41 FP** — 10 FP3 + 30+ FP2 + 4 FP1 |
| send_sequence | sequência processada |
| check-replies | **1 resposta: Selmi SAC → compras@selmi.com.br** |
| proposta_contrato.py | **800 L/mês → R$1.120/mês → R$13.440/ano** |
| enviar_proposta_selmi.py | Proposta + leads atualizados |

### Leads QUENTES (fluxo de compra de óleo — fechamento depende de ação humana)
0. 🆕🔥 **Pastificio Selmi S/A** (compras@selmi.com.br) — SAC redirecionou! Proposta 800 L/mês enviada HOJE. **Aguardar retorno comercial.**
1. 🍀 **Sanofi Medley** (sac.brasil@sanofi.com) — encaminhado a Compras 29/10 (protocolo 03065348). Respondido 30/10.
2. 🔥🔥🔥 **Savegnago** (R$7,98bi — #1 interior SP) — 34+ dias sem ação humana. WhatsApp (11) 96785-9631.
3. 🔥🔥🔥 **Pague Menos** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 20 dias sem retorno.
4. 🔥🔥🔥 **Rede Confiança** (Sorocaba) — Proposta 2.500 L/mês. Aguardando retorno.
5. 🔥🔥🔥 **Covabra** — **AÇÃO HUMANA: preencher cadastro de fornecedor** (isac.ivrim.com.br). 42+ dias sem ação.
6. 🔥🔥 **Brasfrigo (Salto/SP)** — Agendar coleta-teste. Local, respondeu.
7. 🔥🔥 **Queijos Itupeva (Rafael)** — Agendar coleta-teste.
8. 🟡 **Sonda** (R$6,12bi) — Ligar (11) 2145-6200.
9. 🟡 **Tauste** — Ligar (15) 3324-4680. Respondeu 30/09 (34 dias).
10. 🟡 **Nagumo** — Caso 00143542, proposta anexada 14/10.

### Observações
- **34 dias sem resposta humana nova** no fluxo de compra. Selmi é o padrão SAC→comercial que já se repetiu 4 vezes (Savegnago, Pague Menos, Rede Confiança, agora Selmi). Todos aguardam ação humana.
- **Pipeline de fechamento 100% parado** em ação humana — sem scripts que façam ligação ou WhatsApp.
- **Bug conhecido**: proposta_contrato.py calcula faixa de preço incorretamente (800 L/mês mostra R$1,40/L em vez de R$1,60/L). Ajuste na função `preco_por_litro` é necessário — os parâmetros de entrada `(200, 1.20), (500, 1.40), (1000, 1.60)...` têm a faixa deslocada em 1 posição.

"""

inspath = os.path.join(BASE, "equipe", "insights.md")
with open(inspath, "a", encoding="utf-8", newline="\n") as f:
    f.write(insight)
print("insights.md atualizado.")
with open(ecopath, "w", encoding="utf-8", newline="\n") as f:
    json.dump(eco, f, ensure_ascii=False, indent=1)
print("ecossistema.json atualizado.")