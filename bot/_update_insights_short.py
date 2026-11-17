#!/usr/bin/env python3
import os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, 'equipe', 'insights.md')

new_entry = '''
## 2026-11-17 11:34 (Atendente IA - cron - terça-feira)

### Diagnóstico do ciclo
- ✅ sync_formspree.py — 133 bounces cache, 0 notificações Formspree novas (ok)
- ✅ corrigir_emails.py — 0 bounces processados (todos os 130 já tentados; nenhum bounce novo)
- ✅ prospecao_followup.py — 2 FP3 enviados (Copacol - Cooperativa Agroindustrial Consolata, EcoTaua/Taua Food)
- ✅ bot_oleo.py send_sequence — sequência processada, 0 envios novos (fila drenada)
- ✅ bot_oleo.py check-replies — 0 respostas (replies_pending.json vazio, confirmado)
- ⏭️ proposta_contrato/relatorio_ESG — não acionados (0 leads com volume informado ou solicitação de relatório)
- 🔴 **62º dia sem respostas humanas no fluxo de COMPRA de óleo** (última: Tauste 30/09)
- 🔴 Fila de prospecção zerada — sem fonte de busca gratuita para repor leads

### Leads QUENTES (fechamento depende de ação humana)
1. 🍀 **PASTIFICIO SELMI** — proposta 800 L/mês (03/11), aguardando retorno compras.
2. 🔴🔴🔴 **SAVEGNAGO** (R$7,98bi, #1 interior SP) — WhatsApp (11) 96785-9631. 62+ dias sem ação.
3. 🔴🔴🔴 **PAGUE MENOS** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 34 dias sem retorno.
4. 🔴🔴🔴 **REDE CONFIANÇA** (Sorocaba) — Proposta 2.500 L/mês enviada.
5. 🔴🔴🔴 **COVABRA** — **AÇÃO HUMANA: cadastro fornecedor** isac.ivrim.com.br. 66+ dias.
6. 🔴🔴 **BRASFRIGO** (Salto/SP) — Coleta-teste a agendar. Local.
7. 🔴🔴 **QUEIJOS ITUPEVA** (Rafael) — Coleta-teste a agendar.
8. 🟡 **SONDA** (R$6,12bi) — (11) 2145-6200.
9. 🟡 **TAUSTE** — (15) 3324-4680. Respondeu 30/09 (62 dias).
10. 🟡 **SANOFI MEDLEY** — Protocolo 03065348 (29/10).
11. 🟡 **NAGUMO** — Caso 00143542, proposta 5.000 L/mês.

### Observações
- **62 dias sem resposta humana nova** (última: Tauste 30/09). 473 leads trabalhados, canal email no teto.
- **2 FP3 enviados** (Copacol, EcoTaua) — follow-ups finais da sequência.
- **Nenhum bounce novo**, nenhuma resposta pendente, nenhuma notificação Formspree.
- **Pipeline de fechamento 100% parado** em ação humana — sem scripts que liguem ou enviem WhatsApp.
- Sistema saudável — SMTP/IMAP OK.
- Ação humana necessária: **enviar WhatsApp para Savegnago** e **preencher cadastro Covabra** (isac.ivrim.com.br).

---
'''

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = new_entry + content

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('insights.md atualizado OK')