# Insights — Master Óleo · 26/09/2026 (16:31)

---

# Insights — Master Óleo · 26/09/2026 (19:36) — CRON ANALISTA DE QUALIDADE

## Resumo do Tick (Análise de Qualidade)

### ✅ O que foi feito

**Passo 1 — Sync Formspree:**
- `sync_formspree.py`: OK — 66 bounces em cache, 0 notificações novas processadas.
- Nenhum bounce novo detectado neste ciclo.

**Passo 2 — Auditoria de Leads:**
- `bot_oleo.py leads`: OK — 250 leads no total.
- **Consistência bounces.json ↔ leads.csv**: ✅ Todos os 44 leads marcados como "bounce" no CSV têm entrada correspondente em bounces.json.
- **Nenhum bounce com boas_vindas_em preenchido**: ✅ (não há inconsistência)
- **22 emails órfãos em bounces.json** (sem lead correspondente no CSV) — são resquícios de tentativas anteriores de correção de email, leads removidos ou emails alternativos. Não causam erro mas podem ser limpos.

**Passo 3 — Respostas Pendentes:**
- `replies_pending.json`: `[]` — 0 respostas aguardando atendimento.

### 📊 Pipeline

| Indicador | Valor |
|---|---|
| Leads totais | **250** |
| Leads **novo** | **181** |
| Leads **sequencia** | **9** |
| Leads **respondido** | **16** |
| Leads **bounce** | **44** |
| Leads **encerrado** | **0** |
| Bounces em cache (bounces.json) | **66** |
| Respostas pendentes | **0** |
| Emails órfãos no bounces.json | **22** (sem lead) |

### ❌ Problemas Encontrados e Correções

1. **22 emails órfãos em bounces.json** — não são leads ativos, mas acumulam no cache. Exemplos: `ana@alimentossalto.com.br`, `contato@arcor.com`, `3d@roldao.com.br`, `ecommerce704@redetop.com.br` etc. **Sugestão:** limpar bounces.json removendo entradas sem lead correspondente, para manter o cache enxuto.
2. **Nenhum novo bounce ou lead desde o último tick (16:31)** — sistema estável, sem variação.
3. **Nenhuma resposta pendente** — caixa de entrada sem novos replies para atender.

### 🎯 Observações

- 181 leads em "novo" representa 72,4% do pipeline — a maioria ainda não recebeu sequência ou está aguardando envio.
- 9 leads em "sequencia" — em progresso, monitorar avanço.
- 16 respondidos — todos com auto-reply ou resposta genérica (confirmado no tick anterior).
- Betins Laticínios (ID 111) segue como lead respondido mais recente.

### 📝 Recomendações para o Estrategista

1. **Atacar os 181 leads "novo"** — 72% do pipeline está parado em "novo". Revisar se a fila de prospecção extra (`fila_prospeccao_extra.json`) está sendo alimentada e se os envios estão dentro do ritmo esperado.
2. **Limpar bounces.json** — remover os 22 emails órfãos que não correspondem a leads ativos, evitando poluição visual no cache.
3. **Priorizar follow-up humano nos 16 respondidos** — verificar se alguma resposta tinha conteúdo comercial real (ex: Supermercados Dalben, Covabra, Brasfrigo, Max Atacadista) e agendar contato telefônico se aplicável.

### ✅ O que foi feito

**Passo 0 — Sync + Auto-correção:**
- `sync_formspree.py`: OK — 0 notificações novas do Formspree (66 bounces em cache).
- `corrigir_emails.py`: OK — 0 processados (todos os bounces já têm tentativa de correção registrada anteriormente).

**Passo 1 — Watchdog:**
- ✅ **EXIT 0 — sistema saudável.** SMTP OK · IMAP OK. Nenhum follow-up atrasado, nenhum lead parado.

**Passo 2 — Sequência e Respostas:**
- `prospecao_followup.py`: 0 follow-ups atrasados para processar.
- `send_sequence`: OK — sequência processada.
- `check-replies`: **0 respostas** aguardando atendimento (replies_pending.json = []).
- Nenhuma resposta humana para atender neste ciclo.

### 📊 Pipeline atual
| Indicador | Valor | Δ desde 14h31 26/09 |
|---|---|---|
| Leads totais | **250** | → |
| Leads ativos | **190** | → |
| Bounces (cache) | **66** | → |
| Respondidos | **16** | → |
| Encerrados | 0 | → |
| Follow-ups atrasados | **0** | ✅ |
| Respostas pendentes | 0 | → |

**Nota:** Pipeline estável desde o tick anterior (14:31). Nenhuma variação nos números — o sistema operou normalmente sem novos leads ou bounces.

### ❌ Problemas resolvidos
Nenhum problema encontrado neste ciclo.

### ℹ️ Observações
- Mesmo cenário do tick 14:31: 0 respostas pendentes, 0 follow-ups atrasados.
- Nenhum lead novo do Formspree desde o último tick.
- Betins Laticínios segue como o lead mais recente a ter resposta registrada (auto-reply provável, sem conteúdo comercial).

### 🎯 Leads QUENTES (respostas humanas com interesse)
**NENHUM** neste tick. Nenhuma resposta com conteúdo real na caixa de entrada para atender.

### 📝 Recomendações
1. **Atacar fila extra (~202 empresas)** — próximo passo natural para expandir pipeline.
2. **Acompanhar Betins Laticínios** — monitorar se foi resposta real ou apenas auto-reply; vale follow-up via WhatsApp se confirmar interesse.
3. **Pipeline estável** — sistema operando sem intervenção; manter cron ativo e revisar leads respondidos sem conteúdo real.