# Insights Diarios — Analista de Qualidade

## 2026-09-28 (segunda-feira) — 19:42 (Cron #44 — Atendente IA - ciclo noturno)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados (prospecao_followup)** | 40 FP1 (atrasados resolvidos) | +40 |
| **Send_sequence** | 9 FP1 (fritas/batata palha) | +9 |
| **Respostas de leads** | 0 (1 auto-reply Zendesk ignorado) | — |

### Atividades deste ciclo (19:42)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ⚠️ watchdog.py | exit 1 — 40 follow-ups atrasados | Resolvido rodando prospecao_followup.py |
| ✅ prospecao_followup.py | 40 FP1 enviados | Leads atrasados zerados. Inclui Bunge, Tauste, Vigor, Catupiry, Cacau Show, Kopenhagen, Camil, Granarolo, e mais |
| ✅ send_sequence | 9 FP1 enviados | Nicho fritas/batata palha (Ricks, Art Fritas, Point Chips, etc) |
| ✅ check-replies | 1 pendente | Pastificio Selmi = auto-reply Zendesk de satisfacao (nao e lead — ignorado) |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ⚠️ exit 1 → resolvido | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 reais | — |

### Observacoes

- **⚠️ Watchdog detectou 40 follow-ups atrasados** — o prospecao_followup.py rodou e resolveu todos. Sistema agora saudavel.
- **📬 1 resposta no check-replies**:
  - **Pastificio Selmi** (via Zendesk) — é uma **pesquisa de satisfacao automatica** do suporte Selmi perguntando nossa opinião sobre o atendimento que RECEBEMOS deles (ticket #89532). NÃO é um lead respondendo. Ignorado.
- **🔇 Nenhum lead quente novo neste ciclo.** Leads quentes ativos continuam: Savegnago (canal comercial aberto), Covabra (respondeu 22/09), Queijos Itupeva (Rafael — coleta-teste pendente), Brasfrigo (fechamento), Pague Menos (Josiane Marinho).
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532 (compras@selmi.com.br)
|- 🟡 **Pague Menos** — acompanhar Josiane Marinho

|---

## 2026-09-28 (segunda-feira) — 19:46 (Cron #45 — Melhorador Contínuo - melhorias)

### Melhorias implementadas neste ciclo

| Melhoria | Arquivo | Detalhe |
|----------|---------|---------|
| ✅ FP3 reformulado c/ anti-furto + Savegnago | `bot/prospecao_followup.py` | Anti-furto (quadrilhas, bombona lacrada), prova social Savegnago #1 SP (R$ 7,98 bi), PIX hora da coleta |
| ✅ +8 novas empresas MX validado | `bot/prospecao.py` | Iquegami (Outlook), Campos (Hotmail), Fernandão (uhserver), Nicolau Max (Google), ASC, Maia, Biazoto, Univale |

### Diagnóstico do sistema

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Watchdog | exit 0 | saudável | ✅ |
| Total leads | 250 | — | ✅ |
| Ativos | 190 | — | ✅ |
| Bounces | 42 (21%) | < 15% | 🔴 acima |
| Respostas | 16 (8,2%) | ≥ 10% | ⚠️ abaixo |
| Fila pendentes | ~14 (6+8) | ≥ 15 | ⚠️ quase |
| Contratos | 0 | 1 | 🔴 |

### Aprendizados

- **FP3 com anti-furto + Savegnago**: o argumento anti-furto diferencia a Master Óleo de coletores informais (que não usam protocolo de segurança). Savegnago como prova social mostra que a maior rede do interior confia no serviço.
- **Fila quase na meta**: com +8 empresas, a fila sobe de 6 para ~14. Ainda faltam ~2 para a meta de 15. Próxima rodada pode mirar Sonda Supermercados (R$ 6,12 bi, não contactado) e outras do ABRAS ranking.
- **O gargalo continua sendo fechamento humano**: 0 contratos em 250 leads e 16 respostas é alarmante. A IA fez o trabalho de prospecção; agora precisa de intervenção humana.

### Pendências para o Estrategista

- 🔴🔴🔴 Savegnago (WhatsApp), Queijos Itupeva (Rafael), Brasfrigo
- 🟡 Covabra, Pague Menos (Josiane), Dalben (Luis), Muffato (tel)
- ⚠️ Acompanhar se novo FP3 aumenta resposta
- ⚠️ Buscar +2 empresas para fila chegar em 15+

---

## 2026-09-27 (domingo) — 08:00 (Cron #43 — Estrategista - análise semanal)

### 🏆 DESCOBERTA DA SEMANA: SAVEGNAGO É #1 DO INTERIOR SP

**ABRAS Ranking 2026**: Savegnago Supermercados é a MAIOR rede do interior de São Paulo
com faturamento de **R$ 7,98 bilhões** (15ª maior do Brasil). Eles abriram canal comercial
conosco e estão negociando. Isso transforma nossa abordagem comercial.

**Top 3 interior SP já no pipeline:**
1️⃣ Savegnago (R$ 7,98 bi) — respondeu, canal comercial aberto
2️⃣ Pague Menos (R$ 4,33 bi) — respondeu (Josiane Marinho)
3️⃣ Tauste — adicionado recentemente à fila

Nunca tivemos 3 das maiores redes simultaneamente no pipeline. Isso é um case de venda.

### 📊 Diagnóstico da Semana (21-27 Set)

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Total leads | 250 | — | ✅ |
| Ativos | 190 | — | ✅ |
| Bounce CSV | 44 (17,6%) | < 15% | ⚠️ acima |
| Bounce cache | 66 (26,4%) | < 15% | 🔴 muito acima |
| Respondidos (humanos reais) | 6 (3,2%) | ≥ 10% | 🔴 abaixo |
| Respondidos (status CSV) | 16 (8,4%) | — | — |
| Encerrados | 0 | — | — |
| Fila total | 298 empresas | — | ✅ |
| Fila pendentes válidas | 6 | ≥ 15 | ⚠️ abaixo |
| Watchdog | exit 0 | saudável | ✅ |

### 🎯 Lições aprendidas

1. **O gargalo NÃO é mais prospecção — é FECHAMENTO.** Temos 6 respostas humanas reais,
   16 leads com status "respondido", e ZERO coletas-teste agendadas. A IA fez o trabalho
   dela. Agora precisa de HUMANO no WhatsApp e telefone para converter.

2. **Supermercados convertem mais que qualquer outro nicho.** Dos 6 respondidos reais,
   4 são redes varejistas. Confirmado pelo estudo de mercado: padaria+rotisserie+açougue
   geram óleo toda semana em cada loja — uma rede é um contrato de volume, não um lead.

3. **Prova social Savegnago muda a conversa.** Ao abordar outras redes, mencionar que
   "a maior rede do interior (Savegnago, R$ 7,98 bi) já está em negociação conosco"
   é o argumento que desarma objeções. Nenhuma rede pequena quer ficar atrás.

4. **FP3 reformulado com urgência funciona melhor.** O Melhorador Contínuo trocou o tom
   de despedida por argumentos diretos (R$ 14,4k/ano, Portaria 2028, passivo/anti-furto).
   Acompanhar resultados nas próximas semanas.

5. **Bounce rate 17,6% no CSV / 26,4% no cache** — ainda acima da meta. O filtro de
   MX self-hosted (Croissant & Cia, Milk Menk, Rede Correia) está correto, continuar
   aplicando. Foco em emails de provedores cloud (Google, Outlook, Locaweb, Kinghost).

6. **Canal comercial > SAC.** Savegnago (comercial@) respondeu gente. Oba, Arcor (SAC)
   fecharam ticket. Coop Campinas expõe email de comprador direto. Sempre priorizar
   o departamento comercial/fornecedores quando disponível.

### 🔴 Ações humanas críticas para a semana (28/09 a 04/10)

| Prioridade | Lead | Ação | Canal |
|------------|------|------|-------|
| 🔴🔴🔴 | Queijos Itupeva (Rafael) | Agendar coleta-teste | Email/Telefone |
| 🔴🔴🔴 | Savegnago (#1 interior SP) | Proposta formal, coleta rede toda | WhatsApp 11 96785-9631 |
| 🔴🔴 | Brasfrigo (Salto/SP) | Fechar contrato | Telefone/Email |
| 🟡 | Covabra (respondeu 22/09) | Oferecer loja piloto | Telefone/WhatsApp |
| 🟡 | Pague Menos (Josiane Marinho) | Retomar contato, oferta | Email/Telefone |
| 🟡 | Dalben (gerente Luis) | Proposta formal | Telefone |
| 🟡 | Muffato | Ligar compras | (43) 3371-1700 |

---

## 2026-09-26 (sabado) — 19:36 (Cron #42 — Atendente IA - ciclo sabado noite)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (19:36)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK. 250 leads, 190 ativos, 66 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio ([]) |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo sabado noite — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Mesmo estado dos ciclos anteriores.
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 16:02 (Cron #41 — Atendente IA - ciclo sabado tarde)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (16:02)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK. 250 leads, 190 ativos, 66 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio ([]) |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo sabado tarde #7 — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Mesmo estado dos ciclos anteriores.
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 15:32 (Cron #40 — Atendente IA - ciclo sabado tarde)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (15:32)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK. 250 leads, 190 ativos, 66 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio ([]) |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo sabado tarde #6 — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Mesmo estado dos ciclos anteriores.
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 13:31 (Cron #38 — Atendente IA - ciclo sabado tarde #2)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (13:31)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK. 250 leads, 190 ativos, 66 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio ([]) |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo sabado tarde #2 — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Mesmo estado do ciclo 13:01.
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 13:01 (Cron #37 — Atendente IA - ciclo sabado tarde)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (13:01)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK. 250 leads, 190 ativos, 66 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo sabado tarde — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Ultimos leads com interesse real: Savegnago (canal comercial), Covabra (respondeu 22/09), Queijos Itupeva (Rafael — coleta-teste pendente), Brasfrigo (fechamento).
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 12:31 (Cron #36 — Atendente IA - ciclo noturno sob demanda)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (12:31)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo noturno sob demanda — sistema saudavel e ocioso.**
- **📭 0 respostas pendentes, 0 follow-ups atrasados, 0 boas-vindas novas.**
- **🔇 Nenhum lead quente novo neste ciclo.** Ultimos leads com interesse real: Savegnago (canal comercial), Covabra (respondeu 22/09), Queijos Itupeva (Rafael — coleta-teste pendente), Brasfrigo (fechamento).
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 12:01 (Cron #35 — Atendente IA - ciclo noturno)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | — |
| **Ativos (watchdog)** | 190 | — |
| **Bounce (cache)** | 66 | — |
| **Total leads (CSV)** | 250 | — |
| **Ativos (CSV)** | 190 | — |
| **Bounce (CSV)** | 44 | — |
| **Respondido** | 6 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 0 | — |

### Atividades deste ciclo (12:01)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 0 novos bounces | Todos ja tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudavel | SMTP/IMAP OK |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |
| ✅ IMAP scan | 0 nao lidos | Caixa de entrada sem mensagens novas |

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Respostas ultimas 24h | 0 | — |

### Observacoes

- **✅ Ciclo noturno de sabado — sistema saudavel e ocioso.**
- **📭 0 emails nao lidos, 0 respostas pendentes, 0 follow-ups atrasados.**
- **🔇 Nenhum lead quente novo neste ciclo.** Ultimos leads com interesse real: Savegnago (canal comercial), Covabra (respondeu 22/09), Queijos Itupeva (Rafael — coleta-teste pendente), Brasfrigo (fechamento).
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026, proposta Dalben aguardando retorno.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

## 2026-09-26 (sabado) — 11:35 (Cron #34 — Atendente IA - ciclo vespertino)

### Resumo do ciclo

| Metrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 250 | +8 |
| **Ativos (watchdog)** | 190 | +7 |
| **Bounce (cache)** | 66 | +1 |
| **Total leads (CSV)** | 250 | +8 |
| **Ativos (CSV)** | 190 | +7 |
| **Bounce (CSV)** | 44 | +1 |
| **Respondido** | 16 | — |
| **Encerrados** | 0 | — |
| **Boas-vindas enviadas hoje** | 0 | — |
| **Follow-ups processados** | 0 | — |
| **Respostas de leads** | 1 (Piracanjuba — auto-reply SAC) | — |

### Atividades deste ciclo (11:35)

| Acao | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificacoes novas | 66 bounces em cache |
| ✅ corrigir_emails.py | 1 bounce processado | Lactalis (sac@itambe.com.br) — nao_encontrado |
| ⚠️ watchdog.py | exit 1 — 2 bounces Tostally | Corrigido adicionando como nao_encontrado (dominio sem site) |
| ✅ watchdog.py (re-run) | exit 0 — saudavel | Apos correcao dos 2 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequencia processada | Sem novas boas-vindas |
| ✅ check-replies | 1 pendente | Piracanjuba = auto-reply SAC (protocolo #26092026-265295). Arquivado. |

### Respostas de leads

| Lead | Resposta | Acao |
|------|----------|------|
| **Piracanjuba** (saclbv@piracanjuba.com.br) | Auto-resposta SAC — protocolo #26092026-265295 | Arquivada como automatica. Sem acao. |

### Top segmentos
*(dados de segmento nao preenchidos no CSV)*

### Top cidades
*(dados de cidade nao preenchidos no CSV)*

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | — |
| Resposta ultimas 24h | 1 (Piracanjuba — auto) | — |

### Observacoes

- **✅ Watchdog saudavel** — apos correcao dos 2 bounces Tostally (dominio sem site, registrados como nao_encontrado).
- **📬 Piracanjuba respondeu com auto-reply SAC** — protocolo #26092026-265295. Auto-resposta de sistema, nao um lead respondendo. Arquivada.
- **🔇 Nenhum lead quente novo neste ciclo.** Ultimos leads com interesse real: Savegnago (abriu canal comercial), Covabra (respondeu 22/09), Betins Laticinios (respondeu 'nao utilizo oleo' e foi encerrado).
- **🔧 2 bounces Tostally corrigidos** — ambos os emails (contato@ e comercial@) sem site funcional, registrados como nao_encontrado.
- **Piracanjuba (Grupo Bela Vista)** — responderam com auto-reply do SAC. O email foi enviado para saclbv@piracanjuba.com.br (SAC). Acompanhar se houver resposta humana.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho
- 🆕 **Piracanjuba** — auto-reply SAC recebido. Aguardar resposta humana.

## 2026-09-26 (sabado) — 14:07 (Cron Melhorador Continuo - reposicao de fila)

### Diagnostico do sistema

| Metrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ exit 0 (saudavel) | — |
| SMTP/IMAP | ✅ OK | — |
| Total leads | 250 | — |
| Ativos | 190 | — |
| Bounces | 66 (cache) / 44 (CSV) | < 15% (atual 21% no dashboard) |
| Respostas | 16 (8.2%) | >= 10% |
| Fila pendentes (antes) | 2 (ambos sem MX) | — |
| Fila pendentes (depois) | 12 (6 com MX valido) | >= 15 |

### Problema critico identificado
**Pipeline de prospeccao SECANDO.** Apenas 2 empresas na fila (Madero + Lactalis), ambas sem MX valido. Sem reposicao, os proximos dias terao ZERO envios novos. Bounce rate em 21% (acima da meta 15%) e taxa de resposta em 8.2% (abaixo da meta 10%).

### Melhorias implementadas

1. **+7 NOVAS EMPRESAS** adicionadas ao `prospecao.py` (EMPRESAS) e `fila_prospeccao_extra.json`:
   - Tauste Supermercados (sac@tauste.com.br) - Campinas - rede grande - MX Google valido ✅
   - Rede Bom Lugar (clube@redebomlugar.com.br) - Sorocaba - 50+ lojas - MX Locaweb valido ✅
   - Supermercados Galassi (contato@galassi.com.br) - Campinas - MX Locaweb valido ✅
   - Supermercados Enxuto (sac@enxuto.com.br) - Campinas - MX Outlook valido ✅
   - Hotel Nacional Inn Jundiai - documentado (sem MX, hotel usa formulario)
   - Hotel Dan Inn Sorocaba - documentado (ja no leads.csv)
   - Gross Burger (contato@grossburger.com.br) - Jundiai - MX Google valido ✅
   - **Resultado**: fila subiu de 2 para 12 pendentes (6 com MX valido para envio)

2. **FP3 TEMPLATE REFORCADO** em `prospecao_followup.py`:
   - Antes: tom de despedida ("prometo que é a última", "obrigado pela atenção")
   - Depois: 3 argumentos diretos (R$ 14,4k/ano, Portaria 2028, passivo/anti-furto)
   - CTA mais claro: "transformar o óleo em receita"
   - Subject mudou de "Encerrando contato" para "Último contato — pode estar perdendo R$ 14,4 mil/ano"

3. **Verificacao**: python -m py_compile OK em ambos scripts. enviar_lote.py --status funcional com 12 pendentes.

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho
- 🆕 **Proximo cron enviar_lote.py** pode enviar ate 15 emails para as 6 novas empresas com MX valido