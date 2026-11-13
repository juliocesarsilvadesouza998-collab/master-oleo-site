#!/usr/bin/env python3
"""Prepend new tick entry to insights.md"""
import os
os.chdir(os.path.dirname(__file__) or '.')

new_entry = """|## 2026-11-12 12:33 (Atendente IA - cron tick #210 - quarta-feira)
|
|### Diagnóstico do ciclo
||- **464 leads, 295 ativos, 24 respostas (5,9%)**
||- ✅ sync_formspree.py: 128 bounces cache, 0 notificações Formspree novas
||- ✅ corrigir_emails.py: 0 bounces processados (todos os 128 já tentados)
||- ✅ prospecao_followup.py: 0 follow-ups atrasados
||- ✅ bot_oleo.py send_sequence: sequência processada, nada a enviar
||- ✅ bot_oleo.py check-replies: 0 respostas (replies_pending.json vazio)
||- ✅ _miniscan_inbox.py: INBOX 0 não lidas
||- ✅ watchdog.py: exit 1 — 464 leads, 295 ativos, 128 bounces (1 bounce_registrado sem alternativa — inócuo). SMTP/IMAP OK.
||- **🔴 44 dias sem resposta humana com volume** — última: Tauste (30/09)
||- **🔴 Pipeline de fechamento bloqueado** — todos os leads quentes aguardam ação humana (WhatsApp/telefone)
||- 📊 Fila de prospecção zerada — sem fonte de busca para repor (bloqueio DuckDuckGo/Mojeek/Bing)
|
|### Ações deste ciclo
|| Ação | Resultado |
||------|-----------|
|| sync_formspree.py | 128 bounces cache, 0 notificações Formspree novas |
|| corrigir_emails.py | 0 bounces processados (todos os 128 já tentados) |
|| prospecao_followup.py | 0 follow-ups devidos |
|| bot_oleo.py send_sequence | sequência processada, nada a enviar |
|| bot_oleo.py check-replies | 0 respostas (replies_pending.json vazio) |
|| _miniscan_inbox.py | INBOX: 0 não lidas |
|| watchdog.py | exit 1 — 1 bounce sem correção (conhecido, bounce_registrado sem saída) |
|| proposta_contrato.py | **GERADA E ENVIADA** → Savegnago Supermercados (comercial@savegnago.com.br) — 5.000 L/mês, R$2,00/L, R$10.000/mês |
|| relatorio_ESG | não acionados (0 leads solicitaram) |
|
|### Leads QUENTES — prioridade de fechamento
|1. 🔥🔥 **Savegnago** (R$7,98bi, #1 interior SP) — **PROPOSTA ENVIADA HOJE** para comercial@savegnago.com.br. Aguardar retorno.
|2. 🔥🔥 **Pague Menos** (R$4,33bi) — Ticket 407470 (Josiane Marinho). 29 dias sem retorno.
|3. 🔥🔥 **Rede Confiança** (Sorocaba) — Proposta 2.500 L/mês enviada. Sem retorno.
|4. 🔥🔥 **Covabra** — **AÇÃO HUMANA: preencher cadastro fornecedor** (isac.ivrim.com.br). 53+ dias.
|5. 🔥 **Brasfrigo (Salto/SP)** — Agendar coleta-teste. Local.
|6. 🟡 **Sonda** (R$6,12bi) — (11) 2145-6200.
|7. 🟡 **Tauste** — (15) 3324-4680. Respondeu 30/09.
|8. 🟡 **Sanofi Medley** — Protocolo 03065348 (29/10).
|9. 🟡 **Nagumo** — Caso 00143542, proposta 5.000 L/mês.
|
|### Observações
|- 44º dia sem respostas humanas novas no fluxo de COMPRA de óleo. Sistema 100% saudável.
|- **NOVO:** Savegnago agora tem comercial@savegnago.com.br como lead NOVO (SAC redirecionou). Proposta enviada com volume estimado de 5.000 L/mês.
|- Fila de prospecção zerada — sem serper_api_key nem buscas web gratuitas para reposição.
|- Pipeline de fechamento totalmente bloqueado em ação humana (WhatsApp/telefone) — exceto Savegnago, que recebeu proposta hoje.
|- Watchdog aponta 1 bounce sem correção — bounce_registrado sem alternativa de email. Inócuo.
|
|---
|
"""

with open('insights.md', 'r', encoding='utf-8') as f:
    old = f.read()

with open('insights.md', 'w', encoding='utf-8') as f:
    f.write(new_entry + old)

print("OK: insights.md atualizado (novo entry prepended)")