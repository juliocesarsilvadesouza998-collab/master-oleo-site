# Insights Diários — Ecossistema Master Óleo

Registro diário do Analista de Qualidade: números, problemas encontrados e sugestões para o Estrategista.

---

## 2026-08-14 (sexta)

### Números do dia
- **Sync Formspree:** 21 emails no cache de bounce; **0** notificações novas do Formspree processadas (nenhum lead novo via site hoje).
- **Leads totais:** 56 (2 deles são de teste: id 2 "Julio (teste)" e id 3 "Cliente Teste Formspree").
  - `novo`: 32
  - `sequencia`: 9
  - `respondido`: 2 (id 2 teste; id 46 Boa Supermercados — respondido pela IA Atendente em 10:34)
  - `bounce`: 13
  - `encerrado`: 0
- **Bounces.json:** 21 emails — 13 correspondem a leads atuais marcados como `bounce`; 8 são históricos/corrigidos (não são mais email atual de nenhum lead).
- **Respostas pendentes:** 0 (`replies_pending.json` vazio).
- **Emails enviados hoje:** sem log de volume além dos timestamps do CSV. Registrado: rodada de reenvio de apresentação às 10:36 para 5 leads com email corrigido (Kelco, Rosaves, Supermercados Real, Beira Rio, Infanger).

### Problemas encontrados e correções
1. **Lead id 1 (Ana Souza / Alimentos Salto Ltda) — `bounce` com `boas_vindas_em` preenchido** (2026-08-13T11:31:14). O email `ana@alimentossalto.com.br` está no cache de bounce, mas o boas-vindas foi enviado mesmo assim (ou o bounce foi detectado depois do envio). **Registrado apenas** (conforme regra, não corrigido). Investigar se o `send_sequence` valida o cache antes do envio do boas-vindas.
2. **Re-bounce após correção:** Rosaves (id 25 → `avesideal@rosaves.com.br`) e Beira Rio (id 49 → `faleconosco@beirariosm.com.br`) foram corrigidos e reenviados às 10:36, mas **voltaram a bounce**. A rodada de correção das 18:30 tentou achar alternativas — **12 empresas com `nao_encontrado`** em `correcoes_emails.json` (incluindo Alimentare, Scallet, Kerry, Bagley, Zarelli, Ultrapan, Marquespan, Theoto, Irmaos Barrera).
3. **Cache com lixo de parsing:** 3 entradas do bounces.json têm ponto final no final (`contato@beirariosm.com.br.`, `faleconosco@beirariosm.com.br.`, `sac@theoto.com.br.`) — provavelmente lixo do parser do mailer-daemon. Não atrapalham (nenhum lead usa), mas poluem o cache.
4. **Consistência OK:** todos os leads cujo email atual está no bounces.json estão marcados como `bounce` — sync confirmou e manteve (nada a corrigir).

### Sugestões para o Estrategista
1. **Rosaves e Beira Rio merecem canal alternativo** (telefone/LinkedIn): 2 tentativas de correção por web falharam (`nao_encontrado`). São empresas grandes da região — vale follow-up humano em vez de insistir em email.
2. **Validar MX/email na 1ª coleta** (prospeccao-lote e formulário do site) para reduzir o bounce rate — hoje ~23% dos leads (13/56) são bounce; boa parte poderia ser filtrada antes do envio.
3. **Revisar o fluxo boas-vindas × cache de bounce:** o caso do lead id 1 sugere que o envio do boas-vindas pode não checar o bounces.json (ou checa só no momento do envio e o bounce veio depois). Garantir checagem dupla (na fila e no envio) evita gastar envio em email morto.

---

## 2026-08-18 (terça)

### Números do dia
- **Sync Formspree:** 30 emails no cache de bounce; **21 leads marcados como `bounce`**; **0** notificações novas do Formspree (nenhum lead novo via site hoje).
- **Leads totais:** 77
  - `novo`: 45
  - `sequencia`: 9
  - `respondido`: 2 (id 2 teste; id 46 Boa Supermercados)
  - `bounce`: 21
  - `encerrado`: 0
- **Bounces.json:** 30 emails — 21 correspondem a leads atuais marcados como `bounce`; 9 são históricos/alternativos sem lead correspondente (incluindo 3 com ponto final no fim, lixo de parsing).
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Emails enviados hoje:** 63 no total — 45 FP1 (18:48–18:51) para leads de prospecção contatados em 13–14/08; 16 apresentações (18:59–19:08) para leads novos; 2 follow-ups do lead de teste id 3 (18:42).

### Problemas encontrados e correções
1. **Lead id 1 (ana@alimentossalto.com.br, fonte=site) — `bounce` com `boas_vindas_em` preenchido** (2026-08-13T11:31:14). **Registrado apenas** (conforme regra). Caso recorrente do registro de 14/08: o boas-vindas foi enviado antes de o bounce ser detectado pelo sync — provável email morto, sem correção real (lead fictício de teste).
2. **8 leads receberam apresentação HOJE e o bounce veio na mesma janela** (corridas do mesmo dia): ids 63 (sac@oba.com.br), 64 (contato@deltaterceirizacoes.com.br), 66 (comercial@suprafoods.com.br), 69 (contato@bompeixe.com.br), 70 (contato@deltamax.com.br), 71 (contato@cowpig.com.br), 72 (contato@penina.com.br), 77 (contato@nutraway.com.br) — envio às 19:06–19:08, correções tentadas às 19:10 com `nao_encontrado` em `correcoes_emails.json`. O `enviar_lote.py` filtra o cache de bounce no envio, mas o mailer-daemon só devolve o erro minutos depois — impossível evitar sem validação prévia. Nada a corrigir hoje; leads ficam como bounce.
3. **Cache de bounce com lixo de parsing:** segue presente (mesmo registro de 14/08): `contato@beirariosm.com.br.`, `faleconosco@beirariosm.com.br.`, `sac@theoto.com.br.` (ponto final capturado pelo regex). Não afeta leads, mas polui o cache.
4. **Consistência OK (auditoria):** todos os 21 leads `bounce` têm o email no bounces.json; nenhum lead não-bounce tem email no cache. O sync já havia corrigido — nada a ajustar no leads.csv.

### Sugestões para o Estrategista
1. **Follow-up humano nos 8 bounces de hoje:** são empresas relevantes (Oba, Bom Peixe, Delta Max, Cowpig, Penina, SupraFoods, Nutraway, Delta Terceirizações) e a correção por web deu `nao_encontrado`. Vale telefone/LinkedIn. **Atenção:** Oba e Bom Peixe têm leads duplicados com email alternativo válido — id 57 `ouvidoria@redeoba.com.br` e id 32 `sac@bompeixe.com.br` já estão na fila (FP1 enviado hoje); confirmar que o contato alternativo será usado em vez de abandonar a empresa.
2. **Validar MX antes do envio em lote** (enviar_lote.py já filtra o cache; adicionar checagem MX/DNS) — reduziria os 8 bounces de hoje, todos de domínios que devolvem erro rapidamente.
3. **Normalizar emails no parse do sync** (remover "." final e espaços antes de gravar no bounces.json) para parar de acumular lixo no cache e evitar falso-negativo em futuras checagens.

### Auditoria final do dia (sync + revisão noturna)

> Números consolidados pós-rodadas de prospecção do fim do dia — **atualizam** os do início da seção (77 → 89 leads).

#### Números finais do dia
- **Sync Formspree (rodado na auditoria):** 28 emails em bounce cache; **0** notificações novas do Formspree (nenhum lead novo via site hoje).
- **Leads totais:** 89 (87 reais + 2 de teste: id 2 e id 3).
  - `novo`: 61
  - `sequencia`: 9
  - `respondido`: 3 (id 2 teste; id 46 Boa Supermercados; **id 89 ICT Farmacêutica — novo hoje**)
  - `bounce`: 16
  - `encerrado`: 0
- **Criados hoje:** 27 leads (nicho encapsulados/farmacêuticas + Oba, Cowpig, Penina, Nutraway etc.).
- **Apresentações enviadas hoje:** 28 timestamps em `apresentacao_em` (18:59–19:29).
- **Bounces.json:** 28 emails — 16 correspondem a leads atuais `bounce`; 12 são emails antigos de leads corrigidos hoje (Penina, Nutraway, Cowpig, Kelco, Infanger, Selmi, Real, Oba, Delta Terc, Beira Rio, Rosaves, SupraFoods) — correto: ficam no cache para nunca reenviar.
- **Respostas pendentes:** **1** em `replies_pending.json` — ICT Farmacêutica (`suporte@ictfarmaceutica.com.br`) respondeu com protocolo Nº 1057 (auto-resposta de central de atendimento às 19:31). O Atendente responde no próximo tick.

#### Problemas encontrados e correções
1. **Lead id 1 (Ana Souza, `ana@alimentossalto.com.br`) — `bounce` com `boas_vindas_em` preenchido** (13/08 11:31). **Registrado apenas** (conforme regra). Recorrente dos registros de 14/08 e início de hoje; lead de teste fictício, sem correção real.
2. **Números da entrada anterior desatualizados** (77 leads / 21 bounces): após as auto-correções (7 bounces corrigidos com email real dos sites + reenvio) e a nova leva do nicho encapsulados, o estado real é 89 leads / 16 bounces. **Corrigido neste registro.**
3. **Lixo de parsing no bounces.json — RESOLVIDO:** os 3 emails com ponto final (`contato@beirariosm.com.br.` etc.) não estão mais no cache (28 entradas limpas, nenhuma com `.` final). Verificar se a normalização entrou no sync ou foi limpeza manual.
4. **Consistência OK (auditoria a):** todos os 16 leads `bounce` têm o email atual no bounces.json; nenhum lead não-bounce tem email atual no cache. Nada a corrigir no leads.csv.
5. **Duplicidade de empresa:** 4 empresas com 2 leads (Scallet, Kerry, Bagley, Delta Max) — na maioria, 1 email com bounce + 1 alternativo válido em sequência/novo (ex.: Delta Max id 70 bounce / id 45 `admgeral@deltasuper.com.br` novo). Funciona como fallback, mas polui a base — considerar mesclagem futura.

#### Sugestões para o Estrategista (fim do dia)
1. **ICT Farmacêutica respondeu (protocolo Nº 1057) — priorizar follow-up humano:** é auto-resposta de central, mas a empresa registrou a solicitação. Um contato telefônico rápido pode converter; não deixar só com o tick do Atendente.
2. **Validar MX/DNS antes do envio em lote:** os bounces de hoje (Oba, Bom Peixe, Delta Max, Cowpig, Penina, Nutraway, Delta Terc, SupraFoods) vieram minutos após o envio. Checagem MX prévia reduziria a taxa de bounce (~18% dos leads reais hoje).
3. **Mesclar leads duplicados por empresa** (Scallet, Kerry, Bagley, Delta Max) para o pipeline contar 1 lead por empresa e não reenviar para a mesma empresa por 2 caminhos.

---

## 2026-08-19 (quarta)

### Números do dia
- **Sync Formspree:** 28 emails no cache de bounce; **0** notificações novas do Formspree (nenhum lead novo via site hoje).
- **corrigir_emails:** 0 bounces processados — todos os 15 pendentes de dias anteriores já tiveram tentativa registrada em `correcoes_emails.json` (maioria `nao_encontrado` ou `corrigido_e_enviado`). Nada novo a corrigir.
- **Leads totais:** 96
  - `novo`: 69
  - `sequencia`: 9
  - `respondido`: 2 (id 2 teste; id 46 Boa Supermercados — ticket #23915)
  - `bounce`: 16
  - `encerrado`: 0
- **Bounces.json:** 28 emails — 16 correspondem a leads atuais marcados como `bounce`; 12 são históricos/alternativos de leads corrigidos (correto: ficam no cache para nunca reenviar).
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0) — nenhum follow-up atrasado, bounces corrigidos ou leads parados.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (sem envios novos pendentes nesta janela).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Lead id 1 (Ana Souza, `ana@alimentossalto.com.br`) — `bounce` com `boas_vindas_em` preenchido** (13/08 11:31). **Registrado apenas** (conforme regra); lead de teste fictício, sem correção real. Recorrente dos registros anteriores.
2. **IDs duplicados no leads.csv — DETECTADO hoje:** ids 84, 86 e 88 aparecem 2× cada (Cap-Lab/Persona One/Nutrisenior e Natulha/CapsExpress/Megalabs compartilham o mesmo id, com emails diferentes). São leads distintos válidos — o pipeline funciona (email é a chave real), mas a numeração ficou duplicada na leva de encapsulados de 18/08. **Sugestão:** renumeração (ex.: 84a/84b ou reindexar 78–98) para evitar confusão em relatórios futuros.
3. **Consistência OK (auditoria):** todos os 16 leads `bounce` têm o email atual no bounces.json; nenhum lead não-bounce tem email atual no cache. Nada a ajustar.
4. **ICT Farmacêutica (id 89):** resposta registrada ontem (protocolos 1057/1058 — central de atendimento, "em breve entraremos em contato") mantida como `novo` com nota no `ultima_resposta`. Ainda não há resposta real — **aguardar retorno + FP1 no dia 3** (sem envio hoje).

### Sugestões para o Estrategista
1. **Renumeração dos ids duplicados 84/86/88** (2ª ocorrência: Natulha, CapsExpress, Megalabs) para manter integridade do banco antes que o pipeline cresça mais.
2. **Follow-up humano em paralelo:** Rede Boa (proposta enviada 18/08) e ICT Farmacêutica (protocolo registrado) são os 2 caminhos mais quentes — um contato telefônico pode converter antes do próximo tick.
3. **Validar MX antes do envio em lote:** taxa de bounce estável em ~17% (16/96), mas a maioria dos bounces é de domínios que devolvem rápido — checagem MX prévia reduziria desperdício de envios.

---

## 2026-08-19 (quarta) — 2ª rodada: MELHORADOR CONTÍNUO

### Diagnóstico do dia
- **Ponto mais fraco: taxa de resposta de 1% (1 resposta real em 97 apresentações)** — meta é >3%. Watchdog saudável, bounces estáveis (16%), fila extra esgotada, site no ar.
- **Causa raiz identificada:** template de apresentação longo demais (~160 palavras, 3 bullets + portaria). Em cold email B2B, corpo longo derruba resposta — o lead lê o assunto e abandona.

### Melhorias implementadas (testadas e commitadas)
1. **`bot/prospecao.py` — template de apresentação V2 encurtado:** de ~160 para ~131 palavras, estrutura escaneável de 4 parágrafos (mercado → oferta → urgência lei 2028 → CTA de volume). Assunto mais direto: "Óleo usado da {empresa} vale dinheiro". Mantidos os argumentos que convertem: US$ 8 bi, R$ 1,00–2,50/L, PNRS, Portaria MME/MMA 3/2026 (jan/2028), CTA "quanto vocês geram por mês?" + WhatsApp. Verificado: `py_compile` OK + renderização real do template via script (131 palavras, subject correto).
2. **`bot/prospecao_followup.py` — FP1 reforçado com renda anual calculada:** adicionado "um estabelecimento que gera 600 L/mês recebe cerca de R$ 14 mil por ano" (argumento da persona que faltava no follow-up). Assunto alinhado ao novo template ("Re: óleo usado da..."). Verificado: `py_compile` OK + renderização do FP1.
3. **Site principal (masteroleo.eco.br) — tentativa de atualizar, BLOQUEADA:** o Netlify está servindo a versão antiga (sem calculadora/Catalent); GitHub Pages já tem a versão nova (verificado: HTTP 200 + calculadora + Catalent no ar). Tentei deploy via API com token válido (site c0800dab = master-oleo) e o Netlify respondeu **403 "Account credit usage exceeded - new deploys are blocked until credits are added"** — créditos de build esgotados. Não é bug do pipeline; é limite do plano gratuito.

### Para o Estrategista (domingo)
1. **Renovar créditos/plano Netlify** (ou subir plano pago) para publicar a versão nova no domínio principal — hoje o backup (GitHub Pages) é o único com a calculadora. Alternativa: apontar o domínio masteroleo.eco.br para o GitHub Pages.
2. **Acompanhar o efeito do template V2** nas respostas dos próximos 3-5 dias (lote de hoje é a primeira leva com o novo texto).
3. Seguem pendências já registradas: renumeração de ids duplicados 84/86/88; follow-up humano em Rede Boa + ICT Farmacêutica; validação MX prévia ao envio.

---

## 2026-08-19 (quarta) — 3ª rodada: ATENDENTE (tick 09:42)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas do Formspree (nenhum lead novo via site hoje — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces novos corrigidos. Todos os 17 bounces atuais já têm tentativa registrada em `correcoes_emails.json` (22 entradas). Hoje foi tentado **WBM** (`contato@wbm.com.br`, adicionada às 09:30) → `nao_encontrado` — empresa do nicho encapsulados sem email alternativo válido na web.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 72
  - `sequencia`: 9
  - `respondido`: 2 (id 2 teste; id 46 Boa Supermercados — ticket #23915)
  - `bounce`: 17
  - `encerrado`: 0
- **Cobertura:** 100% dos leads com apresentação ou boas-vindas enviada (`apresentacao_em`/`boas_vindas_em` preenchidos) — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita, consistência OK); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **WBM Industria de Suplementos (id 102) — bounce logo no envio (09:30) e sem correção possível:** `contato@wbm.com.br` voltou inválido minutos após o envio; busca por email alternativo na web deu `nao_encontrado` (registrado em `correcoes_emails.json` às 09:42). Lead marcado como `bounce` com nota "EMAIL INVÁLIDO — não reenviar". **Sugestão:** follow-up humano (telefone/LinkedIn) — é fabricante de suplementos de Jundiaí, nicho prioritário.
2. **Lead id 1 (Ana Souza, `ana@alimentossalto.com.br`) — `bounce` com `boas_vindas_em` preenchido** (13/08 11:31). **Registrado apenas** (conforme regra); lead de teste fictício. Recorrente dos registros anteriores.
3. **Consistência OK (auditoria):** todos os 17 leads `bounce` têm o email atual no bounces.json; nenhum lead não-bounce tem email atual no cache. Nada a ajustar no leads.csv.
4. **IDs duplicados 84/86/88** (Natulha, CapsExpress, Megalabs) — pendência já registrada, mantida.

### Leads quentes (para ação humana)
1. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
2. **ICT Farmacêutica (id 89)** — respondeu com protocolos 1057/1058 (central de atendimento) em 18/08, "em breve entraremos em contato". **Aguardar + FP1 no dia 3** (sem envio hoje); contato telefônico pode acelerar.
3. **Hile Industria de Alimentos (id 101)** — novo lead do nicho encapsulados (Jundiaí, `contato@hile.com.br`), apresentação enviada hoje 09:30. **Primeira leva com template V2 — monitorar resposta.**

### Sugestões para o Estrategista
1. **Follow-up humano em WBM** (nicho prioritário, email morto, sem alternativa na web) — telefone/LinkedIn antes de abandonar.
2. **Renumeração dos ids duplicados 84/86/88** segue pendente (2º dia consecutivo registrado).
3. **Validação MX/DNS antes do envio em lote:** bounces de hoje (WBM) voltaram em minutos; checagem MX prévia reduziria desperdício e daria chance de correção antes de marcar como bounce.
4. **Netlify sem créditos segue bloqueando deploy da versão nova** (calculadora + Catalent) — GitHub Pages é o único no ar com a versão nova.

---

## 2026-08-19 (quarta) — 4ª rodada: ATENDENTE (tick 09:45)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 09:42)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas do Formspree (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 17 bounces atuais já têm tentativa registrada em `correcoes_emails.json` (22 entradas). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 72
  - `sequencia`: 9
  - `respondido`: 2 (id 2 teste; id 46 Boa Supermercados — ticket #23915)
  - `bounce`: 17
  - `encerrado`: 0
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita, consistência OK); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 09:45) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Nenhum problema novo neste tick.** Operação estável: tick 09:45 idêntico ao 09:42 (rodada em sequência do mesmo cron).
2. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
2. **ICT Farmacêutica (id 89)** — respondeu com protocolos 1057/1058 (central de atendimento) em 18/08, "em breve entraremos em contato". Aguardar retorno + FP1 no dia 3; contato telefônico pode acelerar.
3. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta nos próximos dias — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Follow-up humano nos 3 caminhos quentes** (Rede Boa, ICT Farmacêutica, Hile) — telefone converte antes do próximo tick.
2. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-19 (quarta) — 5ª rodada: ATENDENTE (tick 10:32)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site).
- **corrigir_emails:** 0 bounces processados — todos os 16 bounces atuais já têm tentativa registrada (histórico: 22 entradas — 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 71
  - `sequencia`: 9
  - `respondido`: 3 (id 2 teste; id 46 Boa Supermercados — ticket #23915; **id 63 Oba Hortifrutigranjeiros — SAC automático**)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 80** (caiu de 81: Oba saiu de 'novo' → 'respondido')
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 10:32) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Evento entre ticks (consolidado)
- **Oba Hortifrutigranjeiros S/A (id 63, `atendimento@redeoba.com.br`) respondeu às 10:16** — mas as 3 mensagens eram **notificações automáticas do SAC/Salesforce** ("recebemos sua mensagem", "Atendimento Finalizado", pedido de CPF/nome completo — tratou proposta B2B como chamado de consumidor), **não resposta humana**. O tick das 10:16 respondeu UMA vez esclarecendo o caráter comercial e direcionando para WhatsApp (11) 96785-9631, e marcou o lead como `respondido` (correto: SAC fechou o chamado, não há o que responder de novo).
- **Problema de processo detectado e corrigido:** o tick das 10:16 gravou seu relatório em **`bot/equipe/`** (pasta errada, não rastreada) em vez de `equipe/`. Conteúdo consolidado neste arquivo e no `ecossistema.json`; a pasta `bot/equipe/` foi removida para evitar relatórios duplicados/órfãos.

### Problemas encontrados e correções
1. **`bot/equipe/` criado por engano pelo tick 10:16** — consolidado em `equipe/` e removido. (Causa provável: execução com working directory diferente; atenção dos próximos ticks ao caminho.)
2. Nenhum outro problema novo. Pendências já registradas e mantidas: lead id 1 (teste, bounce); ids duplicados 84/86/88; WBM sem email alternativo (sugestão de follow-up humano mantida); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
2. **Oba Hortifrutigranjeiros (id 63)** — rede varejista grande; o SAC engoliu a proposta comercial. Esclarecimento enviado hoje + WhatsApp. **Follow-up humano recomendado via `ouvidoria@redeoba.com.br` (lead 57) ou WhatsApp (11) 96785-9631** — cadeia de hortifruti gera volume relevante de óleo de fritura.
3. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar retorno + FP1 no dia 3; contato telefônico pode acelerar.
4. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Lições da Oba:** para redes varejistas grandes, priorizar canais comerciais/ouvidoria/comprador direto em vez de e-mail de atendimento genérico (SAC corporativo responde automático e fecha chamado). `ouvidoria@redeoba.com.br` é caminho melhor para futuras prospecções de redes.
2. Follow-up humano nos caminhos quentes (Rede Boa, Oba, ICT, Hile) — telefone/WhatsApp converte antes do próximo tick.
3. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 6ª rodada: ATENDENTE (tick 11:07)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site).
- **corrigir_emails:** 0 bounces processados — todos os 16 bounces atuais já têm tentativa registrada (histórico: 22 entradas — 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70
  - `sequencia`: 9
  - `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; **id 51 GoodBom Supermercados — 1ª resposta humana do dia**; id 63 Oba Hortifrutigranjeiros — SAC automático)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 79** (caiu de 80: GoodBom saiu de 'novo' → 'respondido')
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Watchdog:** ✅ saudável (exit 0, 11:03) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%). *(Nota: comando correto é `send-sequence` com hífen, não `send_sequence`.)*
- **check-replies:** 1 resposta nova encontrada e ATENDIDA no mesmo tick (fila zerada ao final — sem risco de resposta dupla).

### Evento do tick (destaque)
- **GoodBom Supermercados LTDA (id 51, `contato@goodbom.com.br`) respondeu às 10:36 BRT** — resposta HUMANA (Laura, Equipe GoodBom): *"Agradecemos por compartilhar a apresentação... sua proposta foi encaminhada ao departamento responsável para análise. Caso haja interesse em uma possível parceria, nossa equipe entrará em contato."* Rede de supermercados de Sumaré (Av. Rebouças, 355 – Centro; tel. (19) 3828-9798; goodbom.com.br) — região de atuação da Master Óleo. **Não é interesse confirmado, mas também não é negativa: porta aberta.**
- **Ação do atendente_ia (11:07):** respondeu agradecendo, mantendo disponibilidade para dúvidas do departamento e pedindo as 2 informações-chave (volume aproximado L/kg por mês + tipo de material), com oferta de WhatsApp (11) 96785-9631. Lead marcado como `respondido`; `replies_pending.json` zerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Sync, watchdog, correções e sequência 100% verdes.
2. **Observação de processo:** o comando de envio é `send-sequence` (hífen); `send_sequence` (underscore) retorna erro de argumento inválido — usar o nome correto nos cron jobs/instruções.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51) — NOVO caminho quente:** resposta humana positiva-cortês em 19/08; proposta está com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** para agilizar a análise — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — é a primeira resposta humana não-negativa desde Rede Boa; acompanhamento telefônico pode destravar a análise comercial em dias.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile) — telefone/WhatsApp converte antes do próximo tick.
3. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.
4. **Taxa de resposta subiu de 2% → 3%** com a resposta da GoodBom (meta >3%): ainda cedo para atribuir ao template V2 (essa resposta veio de envio de 18/08), mas o movimento é o primeiro sinal positivo — monitorar próximos 3-5 dias.



---

## 2026-08-19 (quarta) — 7ª rodada: ATENDENTE (tick 11:32)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 11:07)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 16 bounces atuais já têm tentativa registrada em `correcoes_emails.json` (22 entradas: 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70
  - `sequencia`: 9
  - `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 10:36; id 63 Oba Hortifrutigranjeiros — SAC automático)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 79**
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 11:32) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Operação estável: tick 11:32 idêntico ao 11:07 (nenhum evento novo entre os ticks).
2. **Observação de processo (reforço):** a instrução do cron diz `send_sequence` (underscore), mas o comando real é `send-sequence` (hífen) — o underscore retorna `invalid choice` e a execução falharia se o cron usasse o nome errado. Já registrado no tick 11:07; **corrigir a instrução/cron para `send-sequence`**.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Corrigir a instrução do cron:** usar `python bot_oleo.py send-sequence` (hífen), não `send_sequence`.
2. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa desde Rede Boa; acompanhamento pode destravar a análise comercial em dias.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 9ª rodada: ATENDENTE (tick 12:06)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 11:32)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 16 bounces atuais já têm tentativa registrada em `correcoes_emails.json` (22 entradas: 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70
  - `sequencia`: 9
  - `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 10:36; id 63 Oba Hortifrutigranjeiros — SAC automático)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 79**
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 12:06) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Operação estável: tick 12:06 idêntico ao 11:32 (nenhum evento novo entre os ticks).
2. **Observação de processo (reforço, 3ª ocorrência):** a instrução do cron diz `send_sequence` (underscore), mas o comando real é `send-sequence` (hífen) — o underscore retorna `invalid choice`. **Corrigir a instrução/cron para `send-sequence`** (executado corretamente neste tick).
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Corrigir a instrução do cron:** usar `python bot_oleo.py send-sequence` (hífen), não `send_sequence` (3ª ocorrência registrada — pode estar causando falha silenciosa em outros ambientes).
2. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa desde Rede Boa; acompanhamento pode destravar a análise comercial em dias.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.



---

## 2026-08-19 (quarta) — 10ª rodada: ATENDENTE (tick 12:32)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 12:06)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 16 bounces atuais já têm tentativa registrada em `correcoes_emails.json` (22 entradas: 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70
  - `sequencia`: 9
  - `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 10:36; id 63 Oba Hortifrutigranjeiros — SAC automático)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 79**
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (97 apresentação + 3 boas-vindas, 0 sem envio) — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 12:32) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Operação estável: tick 12:32 idêntico ao 12:06 (nenhum evento novo entre os ticks).
2. **Observação de processo (reforço, 4ª ocorrência):** a instrução do cron diz `send_sequence` (underscore), mas o comando real é `send-sequence` (hífen) — o underscore retorna `invalid choice` (falhou neste tick na 1ª tentativa, corrigido na hora). **Corrigir a instrução/cron para `send-sequence`** — risco de falha silenciosa em ambientes que não tenham o fallback manual.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Corrigir a instrução do cron:** usar `python bot_oleo.py send-sequence` (hífen), não `send_sequence` (4ª ocorrência registrada hoje — prioridade baixa de código, mas alta de processo).
2. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa desde Rede Boa; acompanhamento pode destravar a análise comercial em dias.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88 (2º dia), validação MX pré-envio, renovação de créditos Netlify.



---

## 2026-08-19 (quarta) — 11ª rodada: ATENDENTE (tick 13:05)

*Relatório consolidado aqui no tick 13:31 — havia sido gravado por engano em `bot/equipe/` (local errado, padrão já registrado no tick 10:32); conteúdo preservado e pasta removida.*

### Números do dia (estado real pós-tick — sem mudanças vs. tick 12:32)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 17 bounces permanentes já têm tentativa registrada em `correcoes_emails.json`. Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70 | `sequencia`: 9 | `respondido`: 4 | `bounce`: 17 | `encerrado`: 0 — **Ativos: 79**
- **Respostas pendentes:** 0 (`replies_pending.json` vazio).
- **Watchdog:** ✅ saudável (exit 0) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **send-sequence:** sem envios novos. **check-replies:** 0 respostas.
- **Leads quentes do tick:** GoodBom Supermercados (atendido 11:07) e Oba Hortifruti (atendido 10:16).

---

## 2026-08-19 (quarta) — 13ª rodada: ATENDENTE (tick 14:05)

### Números do dia (estado real pós-tick — evento: 4 FP2 atrasados detectados e enviados)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — 16 "Já tentado" (os 17 bounces permanentes já têm tentativa registrada em `correcoes_emails.json`; 22 entradas no histórico). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70 | `sequencia`: 9 | `respondido`: 4 | `bounce`: 17 | `encerrado`: 0 — **Ativos: 79**
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ⚠️ 1ª rodada **exit 1** → **4 follow-ups ATRASADOS** (FP2 vencidos — apresentação há 6 dias): Casa Alianca - Padaria Gourmet, Supermercados Dias, Sapore S.A., Massima Alimentacao. → **RESOLVIDO no mesmo tick:** `prospecao_followup.py` enviou os 4 FP2 (14:04). Re-verificação: ✅ **exit 0, saudável**.
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%). Comando real: `send-sequence` (hífen).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **4 FP2 atrasados (watchdog exit 1) — RESOLVIDO:** Casa Alianca, Supermercados Dias, Sapore S.A. e Massima Alimentacao tinham apresentação enviada em 13/08 e FP2 vencido (limite 6 dias). `prospecao_followup.py` enviou os 4 na sequência (14:04:38–14:04:54, thread com `apresentacao_msgid`). Watchdog re-verificado: exit 0. **Nada ficou parado.**
2. **Observação de processo (6ª ocorrência):** a instrução do cron diz `send_sequence` (underscore), mas o comando real é `send-sequence` (hífen) — o underscore retorna `invalid choice`. **Corrigir a instrução/cron para `send-sequence`** (executado corretamente neste tick, com fallback manual).
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Corrigir a instrução do cron:** usar `python bot_oleo.py send-sequence` (hífen), não `send_sequence` (6ª ocorrência registrada hoje).
2. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa desde Rede Boa; acompanhamento pode destravar a análise comercial em dias.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 12ª rodada: ATENDENTE (tick 13:31)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 12:32)
- **Sync Formspree:** 29 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — os 17 bounces permanentes foram pulados como "Já tentado" (histórico em `correcoes_emails.json`: 22 entradas — 19 `nao_encontrado`, 2 `corrigido_e_enviado`, 1 `ja_existia`). Nada novo a corrigir.
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70
  - `sequencia`: 9
  - `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 10:36; id 63 Oba Hortifrutigranjeiros — SAC automático)
  - `bounce`: 17
  - `encerrado`: 0
  - **Ativos (novo+sequencia): 79**
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada — nenhum lead parado.
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 são históricos/alternativos de leads corrigidos.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Watchdog:** ✅ saudável (exit 0, 13:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada (nenhum envio novo pendente — cobertura já 100%). Comando real executado: `send-sequence` (hífen).
- **check-replies:** 0 respostas aguardando atendimento.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Operação estável: tick 13:31 idêntico ao 12:32 (nenhum evento novo entre os ticks).
2. **Correção de processo (feita):** o relatório do tick 13:05 foi gravado em `bot/equipe/` (local errado) — conteúdo consolidado em `equipe/` e pasta `bot/equipe/` removida. **Manter o padrão: relatórios sempre em `equipe/` na raiz.**
3. **Observação de processo (reforço, 5ª ocorrência):** a instrução do cron diz `send_sequence` (underscore), mas o comando real é `send-sequence` (hífen) — o underscore retorna `invalid choice`. **Corrigir a instrução/cron para `send-sequence`** (executado corretamente neste tick).
4. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); WBM sem email alternativo (follow-up humano sugerido); Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Corrigir a instrução do cron:** usar `python bot_oleo.py send-sequence` (hífen), não `send_sequence` (5ª ocorrência registrada hoje).
2. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa desde Rede Boa; acompanhamento pode destravar a análise comercial em dias.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.



---

## 2026-08-19 (quarta) — 15ª rodada: MELHORADOR CONTÍNUO (tick 14:07)

### Diagnóstico do dia
- **Ponto mais fraco: FILA DE PROSPECÇÃO ESGOTADA (0 pendentes)** — o Prospector de amanhã (09:00) não teria empresas para enviar. Operação em si saudável: watchdog exit 0, 100 leads (79 ativos), 16 bounces (16%), 3 respostas (3,1%, meta >3% batida), cobertura 100%.
- **2ª fragilidade:** bug de processo `send_sequence` (underscore) vs `send-sequence` (hífen) — registrado 6× hoje nos ticks do Atendente; cada ocorrência gasta um retry manual no tick.

### Melhorias implementadas (testadas)
1. **`bot/fila_prospeccao_extra.json` — 3 empresas NOVAS adicionadas (fila: 57 → 60):**
   - **Ekobé Indústria de Nutracêuticos e Cosméticos** (`contato@ekobe.ind.br`, Capela do Alto/SP) — **NICHO PRIORITÁRIO**: fábrica de gomas/cápsulas/nutracêuticos, investiu R$ 20 mi na maior estrutura de gomas da América Latina. MX Locaweb válido.
   - **Zuhan Refeições Corporativas** (`contato@zuhan.com.br`, Campinas/SP) — cozinhas industriais/refeições coletivas (Grande ABC + Campinas): alto volume de óleo de fritura. MX Birdsnet válido.
   - **Lollos Refeições Empresariais** (`sac@lollos.com.br`, Sorocaba/SP) — cozinha central + refeições transportadas: alto volume. MX com A record válido.
   - Emails confirmados nos sites oficiais (não `contato@` adivinhado), MX validado via `nslookup`, sem duplicidade no leads.csv. Verificado: JSON válido, 60 entradas, 60 emails únicos.
2. **`bot/bot_oleo.py` — bug `send_sequence` CORRIGIDO na raiz:** adicionado alias `send_sequence` (underscore) junto ao `send-sequence` no argparse (linha 323). Agora ambos os nomes funcionam — a instrução do cron com underscore não falha mais, independente de correção do cron. Verificado: `py_compile` OK + `python bot_oleo.py send_sequence --help` exit 0 (parser aceita).

### Para o Estrategista (domingo)
1. **Pendências estruturais mantidas:** renumeração ids duplicados 84/86/88 (3º dia); validação MX pré-envio em lote; renovação de créditos Netlify (domínio principal segue com versão antiga; GitHub Pages com a nova).
2. **Follow-up humano nos caminhos quentes:** GoodBom (19) 3828-9798, Rede Boa, Oba (via ouvidoria@redeoba.com.br), ICT Farmacêutica, Hile.
3. **WBM** (nicho prioritário, email morto sem alternativa) — telefone/LinkedIn antes de abandonar.




---

## 2026-08-19 (quarta) — 16ª rodada do dia: ATENDENTE IA (tick 14:30)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 0
  - **Ativos (novo+sequencia): 79** | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 14:30) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução (diferente do tick 14:05, que pegou 4 FP2 atrasados — já resolvidos). Operação saudável.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). **Alias `send_sequence` (underscore) funcionou** — correção do Melhorador (tick 14:07) em vigor; a instrução do cron não falha mais.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio) — Atendente sem fila de respostas.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 14:30 idêntico ao 14:05: nenhum evento novo entre os ticks (sem novos leads, sem novas respostas, sem bounces novos).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa do dia; acompanhamento pode destravar a análise comercial.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 17ª rodada do dia: ATENDENTE IA (tick 15:31)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 70 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 0
  - **Ativos (novo+sequencia): 79** | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 15:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) funcionou — correção do Melhorador (tick 14:07) segue em vigor, sem falha de processo.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio) — Atendente sem fila de respostas.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 15:31 idêntico ao 14:30: nenhum evento novo entre os ticks (sem novos leads, sem novas respostas, sem bounces novos).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **ICT Farmacêutica (id 89)** — protocolos 1057/1058 (18/08), "em breve entraremos em contato". Aguardar + FP1 no dia 3; contato telefônico pode acelerar.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — primeira resposta humana não-negativa do dia; acompanhamento pode destravar a análise comercial.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, ICT, Hile).
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 18ª rodada do dia: ATENDENTE IA (tick 16:04)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 69 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 1 (**id 89 ICT Farmacêutica — NOVO hoje**)
  - **Ativos (novo+sequencia): 78** (caiu de 79: ICT saiu de 'novo' → 'encerrado') | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 16:06) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) funcionou — correção do Melhorador (tick 14:07) segue em vigor.
- **check-replies:** **2 notificações encontradas — NÃO eram leads, eram avisos automáticos de CANCELAMENTO de tickets do Movidesk da ICT Farmacêutica** (tickets 1057 e 1058, cancelados pela agente Julia Leite em 19/08 15:33 BRT). O próprio aviso diz: "SOMENTE RESPONDA ESTE E-MAIL SE VOCÊ NÃO ESTIVER DE ACORDO COM O CANCELAMENTO, POIS O TICKET SERÁ REABERTO COM A SUA RESPOSTA".

### Problemas encontrados e correções
1. **ICT Farmacêutica (id 89) CANCELOU os tickets 1057/1058 — lead fechado, não é mais quente:** a empresa registrou nossos emails (prospecção de encapsulados/farmacêuticas) como tickets na central Movidesk e a agente Julia Leite os cancelou hoje às 15:33. **Interpretação:** sinal de desinteresse pelo canal e-mail (o contato anterior "em breve entraremos em contato" não se concretizou — foi o agente quem cancelou). **Ação correta tomada:** NÃO responder (responder reabriria o ticket = invasivo e contra a regra de não insistir); lead marcado como `encerrado` com nota explicativa no `ultima_resposta` (nenhum novo e-mail será enviado; canal aberto para retomada via WhatsApp (11) 96785-9631); `replies_pending.json` zerado (notificações de sistema descartadas, sem risco de resposta dupla). **Remover ICT da lista de leads quentes.**
2. **Aprendizado de processo:** nem toda "resposta" no check-replies é um lead — sistemas de helpdesk (Movidesk/Zendesk/Salesforce) respondem automaticamente com notificações de protocolo/cancelamento. Regra nova: antes de responder, verificar se o corpo é humano/comercial ou notificação de sistema; se for notificação de cancelamento, respeitar o sinal (não reabrir ticket) e encerrar o lead.
3. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Remover ICT Farmacêutica da lista de leads quentes** — tickets cancelados pelo agente hoje (15:33); lead encerrado por sinal de desinteresse. Se quiser insistir, o único canal respeitoso é WhatsApp (11) 96785-9631, e mesmo assim com cautela (a empresa demonstrou não querer o contato).
2. **Telefonar para GoodBom (19) 3828-9798** — continua sendo o lead mais quente do dia.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-19 (quarta) — 19ª rodada do dia: ATENDENTE IA (tick 16:31)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 69 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT Farmacêutica — desde o tick 16:04)
  - **Ativos (novo+sequencia): 78** | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 16:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) segue funcionando.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio) — Atendente sem fila de respostas.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 16:31 idêntico ao 16:04: nenhum evento novo entre os ticks (sem novos leads, sem novas respostas, sem bounces novos).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia; acompanhamento pode destravar a análise comercial.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, Hile).
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.
4. Nada novo desde o tick 16:04 — se o dia de trabalho da equipe está encerrando, o resumo consolidado do dia (18 rodadas + esta) já está completo nos relatórios.

---

## 2026-08-19 (quarta) — 20ª rodada do dia: ATENDENTE IA (tick 17:02)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 69 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT Farmacêutica — desde o tick 16:04)
  - **Ativos (novo+sequencia): 78** | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 17:02) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) segue funcionando.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio) — Atendente sem fila de respostas.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 17:02 idêntico ao 16:31: nenhum evento novo entre os ticks (sem novos leads, sem novas respostas, sem bounces novos).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia; acompanhamento pode destravar a análise comercial.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, Hile).
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.
4. Nada novo desde o tick 16:31 — dia segue estável; resumo consolidado do dia (20 rodadas) completo nos relatórios.

---

## 2026-08-19 (quarta) — 21ª rodada do dia: ATENDENTE IA (tick 17:30)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 69 | `sequencia`: 9 | `respondido`: 4 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT Farmacêutica — desde o tick 16:04)
  - **Ativos (novo+sequencia): 78** | Respostas reais: 3 (~3,1%, meta >3% batida)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Fila de prospecção (enviar_lote --status):** 91 empresas — 77 contatados, 22 bounces, **3 pendentes** (Ekobe/nutracêuticos Capela do Alto, Zuhan/refeições Campinas, Lollos/Sorocaba — MX validado, agendados para o Prospector de 20/08 09:00).
- **Watchdog:** ✅ saudável (exit 0, 17:30) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) segue funcionando.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio) — Atendente sem fila de respostas.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 17:30 idêntico ao 17:02: nenhum evento novo entre os ticks (sem novos leads, sem novas respostas, sem bounces novos).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
4. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia; acompanhamento pode destravar a análise comercial.
2. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, Hile).
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.
4. Fila de prospecção com 3 pendentes abastecida (Ekobe/Zuhan/Lollos) — nada a fazer hoje; o Prospector de 20/08 09:00 consome. Dia fechou estável: 21 rodadas, zero eventos novos desde 16:04.

---

## 2026-08-19 (quarta) — 22ª rodada do dia: ATENDENTE IA (tick 18:03)

### Números do dia (consolidado)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 69 | `sequencia`: 9 | `respondido`: 5 (id 2 teste; id 46 Boa Supermercados — ticket #23915; id 51 GoodBom Supermercados — resposta humana 11:07; id 63 Oba Hortifrutigranjeiros — SAC automático; id 91 Sanofi Medley — SAC automático protocolo, 18:03) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT Farmacêutica — desde o tick 16:04)
  - **Ativos (novo+sequencia): 78** | Respostas reais: 4 (~4%, meta >3% batida — Boa + GoodBom humanas; Oba + Sanofi SAC automáticos)
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 são históricos/alternativos.
- **Inbound Formspree:** 3 (nenhum lead novo via site neste tick — 0 notificações novas).
- **Watchdog:** ✅ saudável (exit 0, 18:02) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, sem problemas para resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%). Alias `send_sequence` (underscore) segue funcionando.
- **check-replies:** 1 resposta NOVA — **Sanofi Medley** (`sac.brasil@sanofi.com`, 19/08 20:49 GMT, "Re: Protocolo: 02995121"), acuse automático do SAC (atendente Deborah): "sua solicitação foi encaminhada ao departamento responsável e, caso haja interesse, o departamento entrará em contato". **Não é interesse confirmado nem negativa.**
- **Resposta enviada (18:03):** agradecimento pelo retorno + oferta mantida (compra de óleo vegetal usado, certificado MTR em toda coleta, bombonas, coleta programada) + pedido de direcionamento ao setor de resíduos/meio ambiente/facilities da unidade + WhatsApp (11) 96785-9631 para avaliação sem compromisso + CTA ("qual o melhor caminho para seguirmos?"). Lead id 91 marcado `respondido` (`respondido_por=atendente_ia`); `replies_pending.json` zerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Único evento: resposta automática do SAC da Sanofi — tratada com resposta leve (porta aberta), sem reabrir ticket nem insistir.
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Sanofi Medley (id 91)** — **NOVO neste tick**: acuse automático do SAC com protocolo (02995121), "encaminhado ao departamento responsável". Porta aberta com farmacêutica gigante em Hortolândia (nicho encapsulados/farmacêuticas). Respondido pedindo direcionamento interno. **Se o humano tiver contato direto na Sanofi (facilities/compras), vale acionar — SAC não decide.**
4. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; esclarecimento + WhatsApp enviados. **Follow-up humano via `ouvidoria@redeoba.com.br` (lead 57)** recomendado.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia.
2. **Sanofi: tentar contato direto (facilities/meio ambiente/compras) por LinkedIn ou rede de contatos** — o SAC confirmou que encaminhou, mas a decisão está no departamento interno. É a maior empresa do pipeline de nicho.
3. Follow-up humano nos demais caminhos quentes (Rede Boa, Oba, Hile).
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.
5. Dia fechou com evento positivo no fim: 4 respostas no dia (2 humanas + 2 SAC), taxa ~4% acima da meta. Fila de prospecção abastecida para 20/08.

---

## 2026-08-19 (quarta) — 23ª rodada do dia: ATENDENTE IA (tick 18:33)

### Números do dia (consolidado — atualização)
- **Leads totais:** 100 (98 reais + 2 teste: id 2 e id 3).
  - `novo`: 68 | `sequencia`: 9 | `respondido`: 5 (id 2 teste; id 46 Boa — ticket #23915; id 51 GoodBom — resposta humana 11:07; id 63 Oba — SAC; id 91 Sanofi — SAC protocolo) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT).
  - **Ativos (novo+sequencia): 77** (Sanofi saiu de ativo para respondido desde o tick 18:03) | Respostas reais: 4 (~4%).
- **Apresentações enviadas:** 97 (os 3 leads inbound/teste — ids 1, 2, 3 — receberam boas-vindas do guia, não apresentação de prospecção).
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 históricos/alternativos.
- **Watchdog:** ✅ saudável (exit 0, 18:33) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas do Formspree (nenhum lead novo via site).
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada; 22 registros no histórico).
- **watchdog.py:** exit 0 na primeira execução — operação saudável, nada a resolver (sem follow-ups atrasados, sem bounces sem correção, sem leads parados).
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%) — alias `send_sequence` (underscore) em vigor.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio).
- **enviar_lote.py --status:** fila de prospecção = 91 empresas: 77 contatados, 22 com bounce, **3 pendentes** (Ekobe — nutracêuticos Capela do Alto; Zuhan — refeições Campinas; Lollos — Sorocaba; MX validado, agendados para 20/08 09:00 pelo Prospector).

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick** — nenhum evento novo entre 18:03 e 18:33 (sem leads novos, sem respostas, sem bounces). Nada a corrigir.
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs); validação MX pré-envio em lote; Netlify sem créditos de build (GitHub Pages com a versão nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana (19/08 10:36, Laura), proposta com o departamento responsável. **Telefone (19) 3828-9798.**
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (ticket #23915) em 18/08; sem retorno ainda.
3. **Sanofi Medley (id 91)** — acuse automático do SAC (protocolo 02995121) "encaminhado ao departamento responsável"; resposta enviada 18:03 pedindo direcionamento a resíduos/meio ambiente/facilities + WhatsApp. **Contato direto humano na Sanofi vale acionar — SAC não decide.**
4. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; follow-up humano via `ouvidoria@redeoba.com.br` (lead 57) recomendado.
5. **Hile (id 101)** — nicho encapsulados (Jundiaí), apresentação V2; monitorar resposta.

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — lead mais quente do dia, sem novidades desde 11:07.
2. **Sanofi: tentar contato direto (facilities/meio ambiente/compras)** — maior empresa do pipeline de nicho; decisão está no departamento interno, não no SAC.
3. Fila de prospecção pronta para 20/08 (3 pendentes com MX validado) — manter o Prospector com reposição diária de 2-4 empresas.
4. Nada parado na operação: 5º tick consecutivo sem eventos novos — fluxo automatizado sustentando sozinho.

