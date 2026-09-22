# Insights Master Óleo — 21/09/2026 (15:32)

> **Nota:** Este arquivo agora contém registro cumulativo de múltiplos ticks do dia.
> A auditoria mais recente está no final.

## Pipeline
- **169 leads** no total (125 novo / 12 respondido / 33 bounce no CSV; 55 no cache de bounces)
- **125 ativos** — pipeline estável
- Dashboard: **126 apresentações enviadas, 93 entregues (26% bounce), 12 respostas, taxa de resposta 9,5%** (↑ de 8,7% com Selmi)

## Atividade do tick (15:32 — 10º do dia)
- ✅ Sync Formspree: 0 notificações novas
- ✅ Corrigir emails: 0 processados (todos os 55 bounces já com tentativa registrada)
- ✅ Watchdog: **exit 0 direto** — tudo saudável (SMTP OK · IMAP OK; nenhum follow-up atrasado, bounce ou lead parado)
- ✅ Prospecção follow-up: 0 atrasados
- ✅ Send sequence: OK, 0 emails
- ✅ Check replies: **1 resposta — PASTIFICIO SELMI via Zendesk** (Cristina Magalhães) — redirecionou para o **canal comercial direto: compras@selmi.com.br** 🎯
- ✅ 1 resposta enviada (proposta comercial para compras@selmi.com.br)

## 🔥 LEADS QUENTES (respondidos com interesse)

### 🏆 PASTIFICIO SELMI S/A (Sumaré/SP) — NOVO QUENTE 🔥
- **Ticket Zendesk 89518**: Cristina Magalhães (SAC Selmi) respondeu orientando contato via **compras@selmi.com.br** — canal de COMPRAS oficial!
- **Ação imediata**: email enviado para compras@selmi.com.br com proposta completa:
  - Pagamento por óleo vegetal usado + gordura/resíduos da produção
  - Certificado de destinação (MTR) em toda coleta
  - Descaracterização de resíduos vencidos
  - Coleta programada + bombonas fornecidas
  - Relatório ESG mensal
  - WhatsApp (11) 96785-9631
- Lead atualizado: email → compras@selmi.com.br, status → respondido
- **Próximo passo**: aguardar resposta do compras@selmi.com.br; se houver abertura, perguntar volume mensal + tipo de material e levar para WhatsApp
- Selmi é uma das maiores massas do Brasil — potencial de contrato industrial de alto volume

### 🏆 SUPERMERCADOS PAGUE MENOS SA (Campinas/SP) — QUENTE (aguardando retorno)
- Proposta completa já enviada para **josiane.marinho@supermercadospaguemenos.com.br** — canal comercial oficial
- Aguardando retorno da Josiane (volume mensal + nº de lojas); se silêncio em ~3 dias, toque leve no WhatsApp.

## Sem interesse / automáticas
- Nenhuma neste tick.

## Pendências da fila extra
- Fila de prospecção: **41 pendentes** (226 empresas totais: 167 contatados / 39 bounce / 41 pendentes)
- SuperViva Supermercados Salto <faleconosco@superviva.com.br> ainda pendente

## Gargalos humanos (aguardando ação externa/time)
- ~~**Selmi** — RESOLVIDO: SAC redirecionou para compras@selmi.com.br — email enviado!~~ ✅
- **Savegnago** (comercial@) — prazo 10/09, vencido há 12 dias
- **Grupo IMC** (felix.costa@grupoimc.com.br) — prazo 10/09, vencido há 12 dias
- **Queijos Itupeva** (Rafael) — aguardando relação de volumes + coleta-teste
- **Dalben** (gerente Luis) — aguardando volume mensal desde 18/09

## Observação
Tick produtivo: a resposta da Selmi pelo Zendesk redirecionando para compras@selmi.com.br é EXATAMENTE o tipo de abertura que buscamos — SAC que reconhece o valor e passa para o canal certo. Selmi é uma gigante (Pastifício Selmi S/A, Sumaré/SP, uma das maiores fabricantes de massas do Brasil) — contrato industrial de alto volume em potencial. Pague Menos segue quente aguardando retorno da Josiane. Próximos passos: (1) tocar a fila de 41 pendentes em lotes; (2) cobrar gargalos vencidos (Savegnago, Grupo IMC — 12 dias).

---

## 🧪 Auditoria de Qualidade — 21/09/2026 (19:38)

### 1. Sincronização (sync_formspree.py)
- ✅ 55 emails já em bounce cache (nenhum bounce novo detectado hoje)
- ✅ 0 notificações do Formspree processadas
- ✅ Nenhum bounce com `boas_vindas_em` preenchido (consistente)

### 2. Pipeline atual
| Status        | Contagem |
|---------------|----------|
| **novo**      | 124      |
| **sequencia** | 0        |
| **respondido**| 13       |
| **bounce**    | 33       |
| **encerrado** | 0        |
| **Total**     | 169      |

- **Leads ativos (novo + respondido):** 136
- **Bounce rate:** 33/169 = **19,5%**

### 3. Discrepância encontrada: bounces.json × leads.csv

O `bounces.json` tem **55 emails**, mas apenas **33 leads** estão marcados como bounce no CSV. A diferença de **22 emails** é explicada:

- São emails de **campanhas anteriores** que já foram corrigidos (ex.: `contato@selmi.com.br` → `compras@selmi.com.br`; `contato@scallet.com.br` → `pedidos@scallet.com.br`)
- Nenhum lead **ativo** (novo/respondido) tem email presente na cache de bounces — **não há reenvio para emails inválidos** ✅
- O `sync_formspree.py` só marca como bounce no CSV quando recebe notificação do Formspree; os bounces detectados via mailer-daemon vão apenas para a cache

**Recomendação:** seria bom o sync também atualizar o CSV quando detecta bounce via mailer-daemon, para manter consistência total.

### 4. Respostas pendentes
- `replies_pending.json`: **vazio** (0 respostas pendentes) ✅
- Última resposta processada: **Pastifício Selmi** (compras@selmi.com.br) — já encaminhada

### 5. Problemas identificados

| Problema | Severidade | Status |
|----------|------------|--------|
| 22 emails orphans na cache de bounces sem lead marcado no CSV | 🟡 Média | Registrado — não causa reenvio, mas polui métricas |
| Nenhum problema crítico hoje | ✅ | — |

### 6. Sugestões para o Estrategista

1. **🔧 Melhoria técnica (dev):** Fazer o `sync_formspree.py` também atualizar o `leads.csv` quando detectar bounce via mailer-daemon (não apenas via Formspree). Isso mantém o CSV como fonte da verdade e evita as 22 entradas órfãs.

2. **📊 Gargalos humanos**: Savegnago e Grupo IMC estão **12 dias vencidos** (prazo 10/09). Se ainda não houver resposta, vale um contato telefônico direto — esses são leads de alto volume que não podem esfriar.

3. **🎯 Priorizar Dalben e Queijos Itupeva**: Ambos responderam e estão aguardando retorno do time comercial (volumes mensais). São leads quentes que podem fechar ainda esta semana com um follow-up rápido.

---

## 🔄 Tick 22/09/2026 (17:44)

### Atividade do tick
- ✅ **Sync Formspree**: 0 notificações novas (55 bounces em cache)
- ✅ **Corrigir emails**: 0 processados (todos os 55 com tentativa)
- ⚠️ **Watchdog**: EXIT 1 → **122 follow-ups ATRASADOS** detectados → RESOLVIDO via `prospecao_followup.py` (122 FP1 enviados em lote)
- ✅ **Prospecção follow-up**: 122 processados (nenhum atrasado restante)
- ✅ **Send sequence**: OK, sequência processada
- ✅ **Check replies**: **2 respostas encontradas**:
  1. **COVABRA SUPERMERCADOS** (via Zendesk) — Ana Paula respondeu com **portal de fornecedores oficial** solicitando cadastro 🏆
  2. **VITAFOR** (via Freshdesk) — auto-resposta de ticket (não comercial)

### Ações tomadas
- ✅ **Covabra** — Resposta enviada para support@covabra.zendesk.com:
  - Agradecimento pelo portal de fornecedores
  - Cadastro realizado no portal
  - Pergunta sobre **volume mensal (litros/kg)** e **tipo de material**
  - Sugestão de WhatsApp (11) 96785-9631 para agilizar
- ✅ **Vitafor** — Apenas auto-resposta Freshdesk (ticket 515718). Nenhuma resposta necessária. Aguardar contato humano.
- ✅ **replies_pending.json** — Limpo (0 pendentes)

### 🔥 LEADS QUENTES desta rodada

#### 🏆 COVABRA SUPERMERCADOS — NOVO QUENTE 🔥🔥
- **O quê**: Rede de supermercados com diversas lojas na região (Campinas, Valinhos, região)
- **Resposta**: Ana Paula (via Zendesk) respondeu com **link do portal oficial de fornecedores** — canal comercial direto e formal!
- **Ação**: Registro feito no portal + email de resposta enviado perguntando **volume mensal** e oferecendo **WhatsApp** para negociação rápida
- **Potencial**: Rede de supermercados = contrato de volume (óleo de fritura de padarias/rotisserias/açougues + possíveis vencidos)
- **Próximo passo**: Aguardar resposta com volume — se confirmar, levar para WhatsApp e fechar coleta-teste

### Pipeline atual
| Status        | Contagem |
|---------------|----------|
| **novo**      | 123      |
| **sequencia** | 0        |
| **respondido**| 13       |
| **bounce**    | 33       |
| **encerrado** | 0        |
| **Total**     | 169      |

- **Leads ativos (novo + respondido):** 136
- **Bounce rate:** 33/169 = **19,5%** (estável)
- **Bounce cache:** 55 emails (cache de bounces de todas as campanhas)

### Gargalos humanos (aguardando ação externa)
- **Savegnago** (comercial@) — prazo 10/09, vencido há 13 dias
- **Grupo IMC** (felix.costa@grupoimc.com.br) — prazo 10/09, vencido há 13 dias
- **Queijos Itupeva** (Rafael) — aguardando relação de volumes + coleta-teste
- **Dalben** (gerente Luis) — aguardando volume mensal desde 18/09

### Observação
Tick produtivo: 122 follow-ups atrasados foram zerados (todos os FP1 enviados). Covabra Supermercados respondeu com portal oficial de fornecedores — é o **2º lead de rede de supermercados consecutivo** a abrir canal comercial (depois do Selmi ontem). Redes de supermercados continuam sendo o nicho que mais converte. Covabra tem lojas em Campinas, Valinhos e região — potencial de contrato de múltiplas lojas.