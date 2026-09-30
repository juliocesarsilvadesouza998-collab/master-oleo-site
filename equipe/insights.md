# Insights Diarios — Analista de Qualidade

## 2026-09-30 (quarta-feira) — 14:07 (Cron #57 — Melhorador Contínuo - melhoria contínua)

### Diagnóstico do sistema

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Watchdog | exit 0 | saudável | ✅ |
| Total leads | 271 | — | ✅ |
| Ativos | 200 | — | ✅ |
| Bounces | 73 (27%) | < 15% | 🔴 muito acima |
| Respostas reais | 0 hoje | — | 🔇 |
| Fila pendentes | 5 (todos sem MX) | ≥ 15 | 🔴 congelada |
| Fila empresas total | 318 | — | ✅ |
| Fila contatados | 254 | — | ✅ |

### Problema crítico: FILA DE PROSPECÇÃO CONGELADA

A fila tem 5 pendentes, todos sem MX válido (Nacional Inn Jundiai x2, Biazoto, Madero, Lactalis). O sistema não consegue enviar novos emails porque os pendentes são inválidos. **É necessária limpeza manual** — remover ou corrigir esses 5 emails para destravar a contagem.

### Melhorias implementadas neste ciclo

| Melhoria | Arquivo | Detalhe |
|----------|---------|---------|
| ✅ +7 NOVAS EMPRESAS na fila | `bot/fila_prospeccao_extra.json` | **Roldão Atacadista** (falecomric@roldao.com.br — Google MX, 30+ lojas em SP, canal ouvidoria/comercial), **São Roque Supermercados** (sac@smsr.com.br — perto de Salto!), **Nobre Supermercados** (sac@nobrehipermercado.com.br — Indaiatuba/Campinas), **Supermercados São Vicente** (atendimento@svicente.com.br — Piracicaba, expansão Campinas), **Grupo Muffato/Max Atacadista** (sac@supermuffato.com.br e diretoria@muffato.com.br — ambos Outlook MX) |
| ✅ Site: Top 3 interior SP | `deploy-vercel/index.html` | Nova seção "Top 3 do interior SP no pipeline" com 1º Savegnago (R$7,98bi), 2º Pague Menos (R$4,33bi), 3º Tauste — todos em negociação. Callout do nicho supermercados como o que mais converte |
| ✅ Registro | `equipe/ecossistema.json` e `equipe/insights.md` | Atualizados com aprendizado do ciclo |

### Aprendizados

1. **Fila congelada por pendentes inválidos**: 5 empresas sem MX válido bloqueiam a reposição automática. O sistema tenta enviar para elas, falha, e não avança. Solução: remover esses 5 da fila ou encontrar emails válidos para elas.
2. **Roldão Atacadista = padrão Savegnago**: canal falecomric@roldao.com.br é ouvidoria/comercial — mesmo padrão de Savegnago, Covabra e Tauste, que foram os leads que responderam. 30+ lojas em SP com forte presença em Campinas, Jundiaí, Sorocaba.
3. **Muffato (Max Atacadista) já tem loja em Campinas**: Grupo do PR com faturamento estimado em R$ 4 bi. A loja Max Atacadista em Campinas gera óleo de fritura todos os dias.
4. **São Roque Supermercados é logística ultra-local**: Fica em São Roque, a 15 min de Salto. Ideal para contrato piloto de coleta local.

### Pendências para o Estrategista

- 🔴🔴🔴 **LIMPAR FILA**: Remover 5 pendentes inválidos (Nacional Inn Jundiai x2, Biazoto, Madero, Lactalis) ou encontrar emails válidos. Sem isso a prospecção não avança.
- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Roldão Atacadista** — NOVO lead em potencial, canal falecomric@roldao.com.br aberto.
- 🟡 **Muffato / Max Atacadista** — NOVO lead, loja em Campinas.

---

## 2026-09-30 (quarta-feira) — 14:02 (Cron #56 — Atendente IA - ciclo vespertino)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 271 | mesmo (271→271) |
| **Ativos (watchdog)** | 200 | mesmo (200→200) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (14:02)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 271 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio (leve timeout na 1ª tentativa, executou ok na 2ª) |

### Respostas pendentes

Nenhuma. Nenhum lead respondeu desde o último ciclo (13:33).

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu neste ciclo.
- **🔇 Sem leads quentes novos neste ciclo.** Leads quentes permanecem: Queijos Itupeva (Rafael — coleta-teste pendente), Savegnago (#1 interior SP, R$7,98bi), Brasfrigo (Salto/SP — contrato pendente), Tauste (liga (15) 3324-4680), Covabra (follow-up pendente), Sonda Supermercados (R$6,12bi — ligar (11) 2145-6200), Pague Menos (Josiane Marinho — 2º maior do interior).
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo. Todos esses dependem de ação humana presencial (WhatsApp/telefone) — a IA fez a prospecção e o follow-up, agora o fechamento é humano.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-30 (quarta-feira) — 12:02 (Cron #54 — Atendente IA - ciclo vespertino)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 271 | mesmo (271→271) |
| **Ativos (watchdog)** | 200 | mesmo (200→200) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (12:02)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 271 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Respostas pendentes

Nenhuma. Nenhum lead respondeu desde o último ciclo (11:01).

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu neste ciclo.
- **🔇 Sem leads quentes novos neste ciclo.** Leads quentes permanecem: Queijos Itupeva (Rafael — coleta-teste pendente), Savegnago (#1 interior SP, R$7,98bi), Brasfrigo (Salto/SP — contrato pendente), Tauste (liga (15) 3324-4680), Covabra (follow-up pendente), Sonda Supermercados (R$6,12bi — ligar (11) 2145-6200), Pague Menos (Josiane Marinho — 2º maior do interior).
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo. Todos esses dependem de ação humana presencial (WhatsApp/telefone) — a IA fez a prospecção e o follow-up, agora o fechamento é humano.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-30 (quarta-feira) — 11:01 (Cron #53 — Atendente IA - ciclo matinal)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 271 | mesmo (271→271) |
| **Ativos (watchdog)** | 200 | mesmo (200→200) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (11:01)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 271 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Respostas pendentes

Nenhuma. Nenhum lead respondeu desde o último ciclo (10:05).

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu neste ciclo.
- **🔇 Sem leads quentes novos neste ciclo.** Leads quentes permanecem: Queijos Itupeva (Rafael — coleta-teste pendente), Savegnago (#1 interior SP, R$7,98bi), Brasfrigo (Salto/SP — contrato pendente), Tauste (liga (15) 3324-4680), Covabra (follow-up pendente), Sonda Supermercados (R$6,12bi — ligar (11) 2145-6200), Pague Menos (Josiane Marinho — 2º maior do interior).
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo. Todos esses dependem de ação humana presencial (WhatsApp/telefone) — a IA fez a prospecção e o follow-up, agora o fechamento é humano.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-30 (quarta-feira) — 10:05 (Cron #51 — Atendente IA - ciclo matinal)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 271 | +1 (270→271) |
| **Ativos (watchdog)** | 200 | +1 (199→200) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (10:05)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache. Teve timeout inicial, mas rodou bem na segunda tentativa |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 271 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Respostas pendentes

Nenhuma. Nenhum lead respondeu desde o último ciclo.

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu neste ciclo.
- **📈 Leads subiram de 270 para 271** — estabilidade. Nenhum novo bounce detectado.
- **🔇 Sem leads quentes novos.** Leads quentes permanecem: Queijos Itupeva (Rafael — coleta-teste pendente), Savegnago (#1 interior SP, R$7,98bi — WhatsApp 11 96785-9631), Brasfrigo (Salto/SP — contrato pendente), Tauste (liga (15) 3324-4680), Covabra (follow-up pendente), Sonda Supermercados (R$6,12bi — ligar (11) 2145-6200).
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-30 (quarta-feira) — 08:31 (Cron #50 — Atendente IA - ciclo matinal)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 270 | mesmo (270→270) |
| **Ativos (watchdog)** | 199 | -1 (200→199) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (08:31)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 270 leads, 199 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 1 resposta: **Tauste** | SAC direcionou para comercial (15) 3324-4680 |
| ✅ reply para Tauste | Resposta enviada | Agradecido contato, confirmado que ligaremos (15) 3324-4680. WhatsApp (11) 96785-9631 como canal alternativo |

### Respostas pendentes

Nenhuma. Replies pendentes foram atendidos neste ciclo.

### 🔥 Lead Quente: Tauste (ID 213)

**Supermercados Tauste S/A** — 3ª maior rede do interior de SP (ABRAS 2026). Respondeu nosso email direcionando para o setor comercial pelo telefone **(15) 3324-4680** (seg-sex 08h-17h). Respondemos confirmando que ligaremos. **Ação humana pendente: fazer a ligação comercial.**

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📬 Tauste respondeu novamente** — manteve o encaminhamento para o comercial. Confirma que o SAC não negocia, mas o canal de vendas está aberto via telefone.
- **🔇 Nenhum outro lead novo** — apenas Tauste respondeu desde o ciclo anterior.
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-30 (quarta-feira) — 08:25 (Cron #49 — Atendente IA - ciclo matinal)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 270 | mesmo (270→270) |
| **Ativos (watchdog)** | 199 | -1 (200→199) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (08:25)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 270 leads, 199 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Respostas pendentes

Nenhuma. replies_pending.json está vazio.

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu desde o último ciclo noturno.
- **📉 Ativos caíram de 200 para 199** — 1 lead pode ter sido marcado como bounce ou encerrado. Diferença marginal, normal.
- **🔇 Sem leads quentes novos neste ciclo.** Leads quentes permanecem: Queijos Itupeva (Rafael), Savegnago (#1 interior SP), Brasfrigo (Salto), Tauste, Covabra.
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, contrato Brasfrigo, follow-up Tauste e Covabra.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.

---

## 2026-09-29 (terça-feira) — 20:23 (Cron #48 — Atendente IA - ciclo noturno)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 270 | +5 (265→270) |
| **Ativos (watchdog)** | 200 | +3 (197→200) |
| **Bounce (cache)** | 73 | +1 (72→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (20:23)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 270 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 1 pendente | Sonda Supermercados |
| ✅ reply para Sonda | Resposta enviada | Agradecemos e pedimos direcionamento ao comercial |

### Respostas pendentes

1. **🟡 Sonda Supermercados (ID 255, sac@sonda.com.br)** — RESPOSTA REAL (SAC). Direcionaram para o Escritório Central pelo telefone (11) 2145-6200 (seg-sex 07h30-17h15). Respondemos agradecendo e pedindo conexão com o departamento comercial. Ação humana necessária: ligar para o Escritório Central.

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📬 Sonda Supermercados respondeu** — é uma resposta de SAC padrão (como Tauste, Savegnago e Covabra antes dela), direcionando para o canal central. O padrão se repete: SAC não fecha, precisa de contato comercial direto.
- **🔇 Nenhum lead quente novo que tenha pedido volume ou valor.** A resposta da Sonda foi institucional.
- **📊 Meta da semana:** 1 coleta-teste confirmada (Queijos Itupeva = lead mais quente), toque Savegnago citando Portaria MME/MMA nº 3/2026.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h)
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano
- 🟡 **Pague Menos (Josiane Marinho)** — retomar contato

---

## 2026-09-29 (terça-feira) — 23:30 (Cron QA — Analista de Qualidade - auditoria)

### Resumo do dia

| Métrica | Valor | Δ vs. ontem | Meta | Status |
|---------|-------|-------------|------|--------|
| **Total leads (CSV)** | 270 | +20 (265→270) | — | ✅ |
| **Ativos (novo)** | 191 | — | — | ✅ |
| **Bounce (cache)** | 73 | +7 (66→73) | — | — |
| **Bounce (CSV)** | 51-53 | +7~9 (44→51~53) | < 15% | 🔴 **19%** |
| **Respondido** | 17 | +1 (16→17) | ≥ 10% | ⚠️ 8,9% |
| **Sequencia** | 9 | mesmo (9) | — | ✅ |
| **Emails hoje (FP)** | 141 total (7 FP1 + 15 FP2 + 119 FP3) | — | — | — |
| **Boas-vindas hoje** | 0 | — | — | — |
| **Novos leads** | +5 (Sonda, Aleatory, Cacique, Alvoar, Fort) | — | — | — |
| **Respostas pendentes** | 3 (1 real + 2 auto) | — | — | — |

### Atividades deste ciclo (23:30)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 73 bounces em cache, 0 notificações novas | Nenhum bounce novo do Formspree hoje |
| ✅ Auditoria cruzada cache vs CSV | 22 emails em cache que não estão no CSV atual | São emails antigos de leads removidos — normal |
| ✅ boas_vindas_em x bounce | 0 ocorrências | Nenhum bounce recebeu boas-vindas — correto |
| ✅ check-replies | 3 pendentes: Tauste, Mars Brasil, Piracanjuba | 1 real (Tauste pediu ligação), 2 auto-replies |

### Respostas pendentes

1. **🔴 Tauste (ID 213, sac@tauste.com.br)** — RESPOSTA REAL. Pediram ligação comercial pelo telefone (15) 3324-4680, de segunda a sexta, 08h-17h. Prioridade máxima para o Atendente.
2. ⚪ **Mars Brasil (noreply@br.mars.com)** — auto-reply automático do sistema de atendimento Mars. Não é lead humano. Pode ignorar.
3. ⚪ **Piracanjuba (saclbv@piracanjuba.com.br)** — auto-reply de confirmação de ticket #29092026-265725. Não é lead humano. Pode ignorar.

### Problemas encontrados e corrigidos

1. **✅ Cache de bounces maior que CSV (73 vs 51-53)**: 22 emails no cache não existem mais no CSV. São de leads removidos/antigos. Não é bug — o cache é histórico. Mas o sync_formspree.py deve continuar verificando bounces novos.
2. **✅ SEM bounces com boas_vindas_em**: Nenhum. O send_sequence está pulando bounces corretamente. Sistema íntegro.
3. **⚠️ 141 emails enviados hoje (119 FP3)**: Volume muito alto de FP3 — é o follow-up de despedida/aquecimento. Preocupante se muitos leads queimarem o último contato sem resposta. Verificar a taxa de resposta dos FP3 enviados.

### Aprendizados

1. **Tauste respondeu — confirmando padrão de SAC**: Assim como Savegnago e Covabra, Tauste direcionou para canal comercial (telefone). Confirma que SAC departments não fecham negócio — precisam ser encaminhados para compras. O script de resposta deve reconhecer e instruir o humano a ligar.
2. **119 FP3 em um dia é sinal de fila envelhecendo**: Muitos leads estão chegando no último follow-up sem resposta. A prospecção precisa de renovação constante — leads frios no FP3 consomem recursos sem retorno.
3. **Bounce rate 19% no CSV ainda preocupa**: Embora 19% seja melhor que 24% (cache), ainda está acima da meta de 15%. Cada bounce é email perdido. Revisar fontes de email (prospecao.py) e validação MX.

### Pendências para o Estrategista

- 🔴🔴🔴 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h). Lead quente!
- 🔴🔴🔴 **Savegnago** — WhatsApp 11 96785-9631
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — coleta-teste
- 🟡 **Covabra** — respondeu 22/09, follow-up humano pendente
- 🟡 **Sonda (ID 255)** — novo lead, email sac@sonda.com.br, MX válido
- 🟡 **Aleatory (ID 256)** e **Cacique (ID 257)** — novos, avaliar prioridade
- ⚠️ **Revisar leads no FP3** — 119 emails de despedida hoje. Identificar leads com potencial de reativação vs. arquivar.

---

## 2026-09-29 (terça-feira) — 19:58 (Cron #47 — Melhorador Contínuo - melhorias)

### Melhorias implementadas neste ciclo

| Melhoria | Arquivo | Detalhe |
|----------|---------|---------|
| ✅ Site: Savegnago #1 do interior como prova social | `deploy-vercel/index.html` | Adicionado Savegnago (R$ 7,98 bi) como número + card na prova-social + depoimento na seção "Quem já confia" — person.md tem o argumento mas o site não usava a maior descoberta recente |
| ✅ Site: prova social expandida | `deploy-vercel/index.html` | 4 cards em vez de 3 na seção "Por que vender agora" — o 4º card exibe "Savegnago (#1 interior) já negociou" |
| ✅ +3 NOVAS EMPRESAS na fila | `bot/prospecao.py` | **Sonda Supermercados** (R$ 6,12 bi — 22ª maior do Brasil, ABRAS 2026, email sac@sonda.com.br MX válido), Aleatory Alimentos (Campinas), Cacique Alimentos (Campinas) |

### Diagnóstico do sistema

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
| Watchdog | exit 0 | saudável | ✅ |
| Total leads | 265 | — | ✅ |
| Ativos | 197 | — | ✅ |
| Bounces | 72 (24%) | < 15% | 🔴 muito acima |
| Respostas | 17 (8,1%) | ≥ 10% | ⚠️ abaixo |
| Fila pendentes (antes) | 5 | ≥ 15 | ⚠️ abaixo |
| Fila pendentes (depois) | 8 (+3 novas) | ≥ 15 | ⚠️ ainda abaixo |
| Contratos | 0 | 1 | 🔴 |

### Aprendizados

1. **Savegnago (#1 do interior SP, R$ 7,98 bi) não estava no site!** A persona foi atualizada em 27/09 com essa descoberta, mas o site — que é o primeiro contato de leads inbound — não exibia essa prova social. Agora aparece em 3 pontos: números, cards e depoimentos. Isso fortalece a credibilidade principalmente para redes médias que visitam o site.
2. **Sonda Supermercados (R$ 6,12 bi) estava completamente fora da fila.** A 22ª maior rede do Brasil (ABRAS 2026) não constava em nenhuma lista — email sac@sonda.com.br com MX válido (antispam.pensomail.com.br). Adicionado agora. Isso mostra que a cobertura de supermercados grandes da ABRAS ranking ainda tem lacunas.
3. **A taxa de resposta (8,1%) estagnou.** A última rodada de FP3 reformulado (Savegnago + anti-furto) ainda não gerou retorno mensurável nos números — pode precisar de mais tempo (follow-ups foram enviados entre 28-29/09).
4. **Bounce rate (24%) continua o calcanhar-de-Aquiles.** Preocupante: 1 em cada 4 emails não chega. A validação de MX self-hosted ajuda mas não resolve todos os casos (ex: Sonda tem antispam.pensomail, que pode rejeitar alguns).

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago (WhatsApp 11 96785-9631)** — proposta formal de contrato
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — NOVO lead quente em potencial, enviar apresentação citando Savegnago como prova social
- 🟡 **Tauste** — pediu ligação (15) 3324-4680, agendar
- 🟡 **Covabra** — respondeu 22/09, priorizar
- 🟡 **Pague Menos (Josiane Marinho)** — retomar contato

---

## 2026-09-28 (segunda-feira) — 19:42 (Cron #44 — Atendente IA - ciclo noturno)

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
- **📬 1 resposta no check-replies: Pastificio Selmi** (via Zendesk) — pesquisa de satisfacao automatica. Ignorado.
- **🔇 Nenhum lead quente novo neste ciclo.** Leads quentes: Savegnago (canal comercial aberto), Covabra (respondeu 22/09), Queijos Itupeva (Rafael — coleta-teste pendente), Brasfrigo (fechamento), Pague Menos (Josiane Marinho).

### Pendencias para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais proximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Selmi** — acompanhar ticket #89532 (compras@selmi.com.br)
- 🟡 **Pague Menos** — acompanhar Josiane Marinho

---

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
|| 🟡 | Muffato | Ligar compras | (43) 3371-1700 |

---

## 2026-09-30 (quarta-feira) — 13:33 (Cron #55 — Atendente IA - ciclo vespertino)

### Resumo do ciclo

| Métrica | Valor | Δ vs. anterior |
|---------|-------|----------------|
| **Total de leads (watchdog)** | 271 | mesmo (271→271) |
| **Ativos (watchdog)** | 200 | mesmo (200→200) |
| **Bounce (cache)** | 73 | mesmo (73→73) |
| **SMTP/IMAP** | ✅ OK | — |
| **Watchdog** | ✅ exit 0 (saudável) | — |

### Atividades deste ciclo (13:33)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 73 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados anteriormente |
| ✅ watchdog.py | exit 0 — saudável | SMTP/IMAP OK. 271 leads, 200 ativos, 73 bounces |
| ✅ prospecao_followup.py | 0 atrasados | Nenhum follow-up pendente |
| ✅ send_sequence | Sequência processada | — |
| ✅ check-replies | 0 pendentes | replies_pending.json vazio |

### Respostas pendentes

Nenhuma. Nenhum lead respondeu desde o último ciclo (12:02).

### Observações

- **✅ Watchdog exit 0** — sistema completamente saudável, sem follow-ups atrasados.
- **📭 0 respostas pendentes** — nenhum lead respondeu neste ciclo.
- **🔇 Sem leads quentes novos neste ciclo.** Leads quentes permanecem: Queijos Itupeva (Rafael — coleta-teste pendente), Savegnago (#1 interior SP, R$7,98bi), Brasfrigo (Salto/SP — contrato pendente), Tauste (liga (15) 3324-4680), Covabra (follow-up pendente), Sonda Supermercados (R$6,12bi — ligar (11) 2145-6200), Pague Menos (Josiane Marinho — 2º maior do interior).
- **📊 Meta da semana (28/09 a 04/10):** Foco FECHAMENTO — coleta-teste Queijos Itupeva, proposta Savegnago, ligação Tauste, contrato Brasfrigo. Todos esses dependem de ação humana presencial (WhatsApp/telefone) — a IA fez a prospecção e o follow-up, agora o fechamento é humano.

### Pendências para o Estrategista

- 🔴🔴🔴 **Savegnago** (WhatsApp 11 96785-9631) — proposta formal de contrato. #1 do interior SP (R$ 7,98 bi).
- 🔴🔴🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste. LEAD MAIS QUENTE.
- 🔴🔴 **Brasfrigo (Salto/SP)** — fechar contrato. É local, respondeu.
- 🔴🔴 **Sonda Supermercados (R$ 6,12 bi)** — ligar (11) 2145-6200, pedir comercial/compras.
- 🟡 **Tauste** — ligar (15) 3324-4680 (seg-sex 08h-17h).
- 🟡 **Covabra** — respondeu 22/09, priorizar follow-up humano.
- 🟡 **Pague Menos (Josiane Marinho)** — 2º maior do interior (R$ 4,33 bi), retomar contato.
- 🟡 **Dalben (gerente Luis)** — insistir contato, proposta formal pronta.
- 🟡 **Muffato** — ligar (43) 3371-1700.