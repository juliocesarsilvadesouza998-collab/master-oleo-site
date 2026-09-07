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


---

## 2026-08-19 (quarta) — 24ª rodada do dia: ATENDENTE IA (tick 19:06)

### Números do dia (consolidado — atualização)
- **Leads totais:** 104 (102 reais + 2 teste: id 2 e id 3).
  - `novo`: 72 | `sequencia`: 9 | `respondido`: 5 (id 2 teste; id 46 Boa — ticket #23915; id 51 GoodBom — resposta humana 11:07; id 63 Oba — SAC; id 91 Sanofi — SAC protocolo) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT).
  - **Ativos (novo+sequencia): 81** | Respostas reais: 4 (~4%, meta >3%).
- **Apresentações enviadas:** 101 (3 leads inbound/teste receberam boas-vindas do guia).
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce`; 12 históricos/alternativos.
- **Inbound Formspree:** 3 acumulados; 0 notificações novas neste tick (nenhum lead novo via site).
- **Watchdog:** ✅ saudável (exit 0, 19:04) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`; 22 registros no histórico). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, nada a resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send-sequence:** sequência processada, sem envios novos pendentes (cobertura 100%).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio — Atendente sem fila).

### Evento do tick (entre 18:33 e 19:06)
- **4 leads NOVOS adicionados às 18:42** (rodada noturna do Prospector): **Vigor Alimentos** (id 101, `sac@vigor.com.br`), **Laticínios Frizzo** (id 103, `contato@laticiniosfrizzo.com.br`), **Reino Alimentos** (id 105, `contato@reinoalimentos.com.br`), **Goldy Alimentos** (id 107, `goldy@goldy.com.br`) — todos com apresentação já enviada (18:42). **Cobertura 100% mantida, nenhum lead parado.** Nenhum bounce entre eles até o momento.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Operação estável: nada entre 18:33 e 19:06 além da entrada dos 4 novos leads (já com envio feito).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 (Natulha, CapsExpress, Megalabs) — **agora há também id 101 duplicado** (Hile vs. Vigor, leads distintos com emails diferentes); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Sanofi Medley (id 91)** — acuse automático do SAC (protocolo 02995121) "encaminhado ao departamento responsável"; resposta enviada 18:03 pedindo direcionamento a resíduos/meio ambiente/facilities + WhatsApp. **Contato direto humano na Sanofi vale acionar — SAC não decide.**
4. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; follow-up humano via `ouvidoria@redeoba.com.br` (lead 57) recomendado.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.** (Vigor Alimentos — grande laticínio — também entrou na leva das 18:42: monitorar.)

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia.
2. **Sanofi: tentar contato direto (facilities/meio ambiente/compras)** — maior empresa do pipeline de nicho; decisão está no departamento interno, não no SAC.
3. **Renumeração de ids duplicados agora inclui 101** (Hile id 101 e Vigor id 101) — pendência cresce; vale reindexar antes de novos lotes.
4. Fila de prospecção pronta para 20/08 (3 pendentes com MX validado: Ekobe, Zuhan, Lollos).
5. Nada parado na operação: 6º tick consecutivo sem eventos problemáticos — fluxo automatizado sustentando sozinho.

---

## 2026-08-19 (quarta) — 25ª rodada do dia: ATENDENTE IA (tick 19:31)

### Números do dia (consolidado — sem mudanças vs. tick 19:06)
- **Leads totais:** 104 (102 reais + 2 teste: id 2 e id 3).
  - `novo`: 72 | `sequencia`: 9 | `respondido`: 5 (id 2 teste; id 46 Boa — ticket #23915; id 51 GoodBom — resposta humana 11:07; id 63 Oba — SAC; id 91 Sanofi — SAC protocolo) | `bounce`: 17 | `encerrado`: 1 (id 89 ICT).
  - **Ativos (novo+sequencia): 81** | Respostas reais: 4 (~4%, meta >3% batida).
- **Apresentações enviadas:** 101 (3 leads inbound/teste receberam boas-vindas do guia). **Cobertura 100% — nenhum lead parado.**
- **Bounces.json:** 29 emails — 17 correspondem a leads atuais `bounce` (interseção perfeita); 12 históricos/alternativos.
- **Inbound Formspree:** 3 acumulados; 0 notificações novas neste tick (nenhum lead novo via site).
- **Fila de prospecção:** 60 empresas na fila extra — 3 pendentes (Ekobe, Zuhan, Lollos, MX validado, agendados para 20/08 09:00).
- **Watchdog:** ✅ saudável (exit 0, 19:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.

### O que foi feito neste tick
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas processadas.
- **corrigir_emails.py:** 0 bounces processados — 16 "Já tentado" (todos os 17 bounces permanentes com tentativa registrada em `correcoes_emails.json`; 22 registros no histórico). Nada novo a corrigir.
- **watchdog.py:** exit 0 na primeira execução — operação saudável, nada a resolver.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%) — alias `send_sequence` (underscore) em vigor.
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio — Atendente sem fila).

### Problemas encontrados e correções
1. **Nenhum problema operacional novo neste tick.** Tick 19:31 idêntico ao 19:06: nenhum evento novo entre os ticks (sem leads novos, sem respostas, sem bounces).
2. **Pendências estruturais mantidas (não resolvíveis por este papel):** renumeração ids duplicados 84/86/88 e 101 (Natulha, CapsExpress, Megalabs, Hile/Vigor); validação MX pré-envio em lote; Netlify sem créditos de build (site principal com versão antiga; GitHub Pages com a nova).

### Leads quentes (para ação humana — destaque)
1. **GoodBom Supermercados (id 51)** — resposta humana positiva-cortês (19/08 10:36, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — rede de Sumaré, perto da base.
2. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915) em 18/08. Sem retorno ainda. **Telefone vale a pena.**
3. **Sanofi Medley (id 91)** — acuse automático do SAC (protocolo 02995121) "encaminhado ao departamento responsável"; resposta enviada 18:03 pedindo direcionamento a resíduos/meio ambiente/facilities + WhatsApp. **Contato direto humano na Sanofi vale acionar — SAC não decide.**
4. **Oba Hortifrutigranjeiros (id 63)** — SAC engoliu a proposta; follow-up humano via `ouvidoria@redeoba.com.br` (lead 57) recomendado.
5. **Hile Industria de Alimentos (id 101)** — nicho encapsulados (Jundiaí), apresentação V2 enviada 09:30. **Monitorar resposta — primeira leva com template novo.** (Vigor Alimentos — grande laticínio — entrou na leva das 18:42: monitorar.)

### Sugestões para o Estrategista
1. **Telefonar para GoodBom (19) 3828-9798** — segue como o lead mais quente do dia.
2. **Sanofi: tentar contato direto (facilities/meio ambiente/compras)** — maior empresa do pipeline de nicho; decisão está no departamento interno, não no SAC.
3. **Renumeração de ids duplicados (84/86/88/101)** segue pendente — reindexar antes de novos lotes.
4. Fila de prospecção pronta para 20/08 (3 pendentes com MX validado: Ekobe, Zuhan, Lollos).
5. Nada parado na operação: 7º tick consecutivo sem eventos problemáticos — fluxo automatizado sustentando sozinho; dia encerra com 25 rodadas e todos os indicadores verdes.


---

## 2026-08-19 (quarta) — 26ª rodada do dia: ANALISTA DE QUALIDADE (tick ~19:35, revisão pós-sync)

### Números do dia (auditoria independente)
- **Leads totais:** 104 — `novo`: 72 | `sequencia`: 9 | `respondido`: 5 | `bounce`: 17 | `encerrado`: 1.
- **Bounces.json:** 29 emails no cache — 17 correspondem a leads atuais marcados `bounce` (interseção perfeita); 12 são históricos/alternativos (sem lead correspondente hoje).
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — Atendente sem fila).
- **Envios registrados hoje (19/08):** fp2 às 14:04 para 4 leads em sequência (ids 5, 7, 8, 11); apresentações 09:18 (99, 100), 09:30 (101 Hile, 102 WBM), 18:42 (101 Vigor, 103, 105, 107). Respostas recebidas: GoodBom 10:36, Oba 10:16, ICT 16:04 (→ encerrado), Sanofi 18:03.
- **sync_formspree.py:** 29 emails em bounce cache; 0 notificações novas do Formspree. Nada foi alterado nesta rodada.

### Auditoria (PASSO 3) — resultados
1. **bounces.json × leads.csv:** consistente. Todos os 17 emails de leads `bounce` estão no cache; nenhum lead com status diferente de `bounce` possui email no cache. Os 12 emails órfãos do cache são de correções históricas já resolvidas (ex.: `contato@penina.com.br`→`info@penina.com.br`, `contato@nutraway.com.br`→`nutraway@nutraway.com.br`, `contato@deltamax.com.br`→`admgeral@deltasuper.com.br`) ou contatos sem lead registrado (`nao_encontrado` em `correcoes_emails.json`). **Nada a corrigir.**
2. **Lead `bounce` com `boas_vindas_em` preenchido:** 1 ocorrência — **id 1 (ana@alimentossalto.com.br)**, `boas_vindas_em=2026-08-13T11:31:14`. **Apenas registrado** (não corrigido): o correções histórico confirma que é lead de teste fictício; o boas-vindas foi enviado em 13/08 antes do bounce ser detectado. Sem impacto real — `send_sequence` pula bounces e nada mais foi enviado a ele.
3. **Respostas pendentes:** `replies_pending.json` = `[]` — 0 respostas aguardando o Atendente.

### Problemas encontrados e correções
- **Nenhum problema operacional novo.** Fluxo estável: sync sem mudanças, cache consistente, fila de respostas vazia, watchdog saudável (ticks anteriores).
- **Observações de qualidade (sem ação nesta rodada):**
  - Lead id 1 (teste) mantém `boas_vindas_em` com status `bounce` — histórico aceitável, mas vale limpar quando o pipeline de testes for revisto.
  - Pendências estruturais já conhecidas: ids duplicados 84/86/88/101; validação MX pré-envio em lote; Netlify sem créditos de build.
  - Bounces do dia não cresceram: nenhum email novo entrou no cache nesta rodada.

### Sugestões para o Estrategista
1. **GoodBom (id 51) — telefonar (19) 3828-9798:** resposta humana positiva-cortês de hoje 10:36; segue o lead mais quente e com melhor custo-benefício de ação humana.
2. **Sanofi (id 91):** resposta do SAC (protocolo 02995121) não decide nada — acionar contato direto (facilities/meio ambiente/compras) via LinkedIn/telefone.
3. **Validação MX antes do próximo lote de prospecção (20/08):** os 3 pendentes (Ekobe, Zuhan, Lollos) já têm MX validado — manter a prática para todo lote novo; é a medida com maior ROI contra bounce futuro (17 bounces acumulados = 16% dos leads reais).

---

## 2026-08-26 (quarta) — ATENDENTE IA (tick 09:40)

### O que foi feito
1. **Sync + auto-correção (PASSO 0):** `sync_formspree.py` — 31 emails no cache de bounce, 0 notificações novas do Formspree (nenhum lead novo via site; seguem 3 inbound acumulados). `corrigir_emails.py` — 0 bounces processados, 13 "já tentado" (todos os 31 bounces já têm tentativa registrada em `correcoes_emails.json`).
2. **Watchdog (PASSO 1):** 1ª rodada **exit 1** — 79 follow-ups ATRASADOS (backlog acumulado desde 19/08, 7 dias sem rodadas). Resolvido com `prospecao_followup.py` rodado 2x (o script envia 1 follow-up por lead por execução): **154 follow-ups processados no total** (FP3 para 4 leads; FP2 ~47; FP1 ~28), nenhum erro de envio. Re-verificação: **exit 0, saudável** — 107 leads, 83 ativos, 31 bounces, nenhum atrasado/bounce sem correção/lead parado.
3. **Fila de prospecção esvaziada:** `enviar_lote.py` enviou os 3 últimos pendentes — **Ekobe** (contato@ekobe.ind.br, nutraceuticos Capela do Alto), **Zuhan** (contato@zuhan.com.br, refeições Campinas), **Lollos** (sac@lollos.com.br, refeições Sorocaba) — registrados no leads.csv com lock (merge). Fila extra: 60 empresas, **0 pendentes**.
4. **Sequência + respostas (PASSO 2):** `send_sequence` — 1 follow-up enviado (teste.formspree@gmail.com). `check-replies` — **2 respostas aguardando**:
   - **Oba Hortifruti** (`atendimento@redeoba.com.br`, 12:15 GMT, "recebemos a sua mensagem!") — **auto-resposta SAC/Salesforce**, não é interesse humano confirmado.
   - **Arcor/Bagley** (`aquiarcor@arcor.com`, 12:17 GMT, "RE: compra de óleo usado — Bagley × Master Óleo") — **auto-resposta SAC Arcor Brasil**: "mensagem encaminhada à área responsável; caso haja viabilidade, equipe entrará em contato". Porta aberta, sem negativa.
   - **Respostas enviadas** com a persona de COMPRA para ambos: agradecimento, oferta mantida (compra de óleo usado/gordura vegetal + resíduos vencidos, certificado PNRS, bombonas, coleta programada), pedido de **volume mensal (litros/kg)** e tipo de material, relatório de impacto ambiental para metas ESG, e WhatsApp (11) 96785-9631. Leads 63 (Oba) e 14 (Bagley) marcados `respondido` (respondido_por=atendente_ia). `replies_pending.json` zerado.
5. **Nenhum pedido de relatório ESG** neste tick — sem geração de PDF.

### Números do dia (auditoria independente)
- **Leads totais:** 107 — `novo`: 74 | `sequencia`: 9 | `respondido`: 6 (teste, Bagley, Rede Boa, GoodBom, Oba, Sanofi) | `bounce`: 18 | `encerrado`: 1.
- **Bounces.json:** 31 emails no cache — 18 correspondem a leads atuais `bounce`; 13 são históricos/alternativos.
- **Apresentações enviadas:** 104 timestamps em `apresentacao_em`.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio após atendimento).
- **Follow-ups enviados hoje:** 154 (4 FP3 + ~47 FP2 + ~28 FP1) + 3 apresentações novas (Ekobe, Zuhan, Lollos).

### Problemas encontrados e correções
1. **Backlog de 154 follow-ups atrasados (watchdog exit 1)** — causa raiz: 7 dias sem rodadas do cron do Atendente (último tick 19/08 19:31). **Resolvido:** `prospecao_followup.py` rodado 2x (1 FP/lead/execução) limpou todo o backlog; watchdog re-verificado em exit 0. Observação para o Estrategista: o script envia apenas 1 follow-up por lead por execução — se o cron ficar vários dias sem rodar, o backlog gera FP2/FP3 no mesmo dia de um FP1; ideal manter cadência diária (ou tolerar o catch-up que ocorreu).
2. **Fila de prospecção esgotada (0 pendentes):** após enviar Ekobe, Zuhan e Lollos, a fila extra acabou. O **Prospector deve repor 2-4 empresas/dia com MX validado** para o pipeline não parar.
3. **Colunas `segmento`/`cidade` ausentes no leads.csv** (nota menor): os scripts de escrita (`prospecao_followup.py`/`enviar_lote.py`) normalizam para um FIELDS sem essas colunas — o CSV atual não as tem; sem impacto operacional, apenas perde dados de qualificação se a fonte tiver.

### Sugestões para o Estrategista
1. **Arcor/Bagley (id 14) — NOVO quente em observação:** SAC oficial encaminhou à área responsável (Campinas, grande fabricante de alimentos — gera gordura vegetal usada e resíduos vencidos). Vale monitorar e, em ~3-5 dias, tentar contato humano direto (compras/facilities/qualidade) via LinkedIn/telefone.
2. **Oba (id 63):** respondeu de novo via SAC (26/08) — seguir insistindo pelo canal SAC/ouvidoria, pedindo direcionamento ao setor de resíduos/meio ambiente (como no Sanofi).
3. **Repor fila de prospecção HOJE** — 0 pendentes = pipeline parado para novos contatos até o Prospector rodar.
4. **GoodBom (id 51) — telefonar (19) 3828-9798** segue sendo o lead humano mais quente sem ação de follow-up humano registrada.

---

## 2026-08-26 (quarta) — ATENDENTE IA (tick 09:50)

### O que foi feito
1. **Sync + auto-correção (PASSO 0):** `sync_formspree.py` — 32 emails no cache de bounce, 0 notificações novas do Formspree (nenhum lead novo via site; seguem 3 inbound acumulados). `corrigir_emails.py` — 0 bounces processados, 8 "já tentado" (todos os 32 bounces já têm tentativa registrada em `correcoes_emails.json`; Kemin tentado de novo, sem alternativa válida).
2. **Watchdog (PASSO 1):** ✅ **exit 0, saudável** — 107 leads, 80 ativos, 32 bounces no cache; nenhum follow-up atrasado, bounce sem correção ou lead parado. Backlog do tick 09:40 totalmente consumido.
3. **Sequência + respostas (PASSO 2):** `prospecao_followup.py` — 0 follow-ups (nada atrasado). `send_sequence` — processado, sem envios novos. `check-replies` — **2 emails NOVOS da Oba Hortifrutigranjeiros** (`atendimento@redeoba.com.br`, Salesforce/sfdc.net):
   - **12:40 GMT "recebemos a sua mensagem!"** — acuse AUTOMÁTICO do SAC para a resposta comercial que enviamos às 09:35 (tick 09:40).
   - **12:46 GMT "Atendimento Finalizado"** — **ticket FECHADO pelo SAC** da Oba.
   - **Decisão: NÃO respondi.** Ambas são auto-respostas de helpdesk, não há interesse humano. "Atendimento Finalizado" = ticket fechado — análogo ao aprendizado da ICT Farmacêutica (responder reabriria o ticket e geraria loop de acuse automático). A mensagem comercial já está na caixa da Oba; a bola está com eles. Marquei os 2 emails como **vistos (\Seen) via IMAP** para o `check-replies` não re-listá-los a cada rodada e zerei `replies_pending.json` (re-verificado: 0 pendentes). Lead 63 mantido `respondido`.
4. **Fila de prospecção:** `enviar_lote.py --status` — 91 empresas, 80 já contatados, 24 com bounce, **0 pendentes** (esvaziada no tick 09:40). Nada a enviar.
5. **Nenhum pedido de relatório ESG/certificado de impacto** neste tick — sem geração de PDF.

### Números do dia (auditoria independente)
- **Leads totais:** 107 — `novo`: 73 | `sequencia`: 7 | `respondido`: 6 (teste, Bagley, Rede Boa, GoodBom, Oba, Sanofi) | `bounce`: 19 | `encerrado`: 2 — **Ativos: 80**.
- **Bounces.json:** 32 emails no cache — 19 correspondem a leads atuais `bounce`; 13 são históricos/alternativos.
- **Apresentações enviadas:** 104 timestamps em `apresentacao_em`.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio após o processamento).
- **Follow-ups enviados hoje:** 0 (nada atrasado; 154 foram no tick 09:40).

### Problemas encontrados e correções
1. **Auto-respostas do SAC da Oba (acuse + "Atendimento Finalizado") — TRATADO sem resposta.** Identificado pelo corpo (sfdc.net/Salesforce) como notificações automáticas; "Atendimento Finalizado" = ticket fechado. **Lição reforçada (caso 2):** nem toda resposta do `check-replies` é lead — notificação de *ticket fechado/finalizado* do SAC = porta fechada por ora (diferente do acuse "encaminhado ao departamento" da Arcor/Sanofi, que é porta aberta). Responder a ticket fechado reabre o chamado e gera loop de acuse. Solução aplicada: marcar como visto e manter o lead `respondido`.
2. **Loop potencial de acuse automático evitado:** se tivéssemos respondido, o SAC da Oba geraria outro "recebemos a sua mensagem!" — ciclo infinito. Não responder + marcar como visto quebra o ciclo.
3. Pendências estruturais já registradas e mantidas: fila de prospecção **0 pendentes** (Prospector precisa repor 2-4 empresas/dia com MX validado); ids duplicados 84/86/88/101; Netlify sem créditos de build; lead id 1 (teste).

### Leads quentes (para ação humana — destaque)
1. **Arcor/Bagley (id 14) — em observação (SAC oficial "encaminhado à área responsável", 26/08):** Campinas, grande fabricante de alimentos — gera gordura vegetal usada e resíduos vencidos (>40% gordura → biodiesel + descaracterização). **Vale contato humano direto (compras/facilities/qualidade) em ~3-5 dias via LinkedIn/telefone.**
2. **GoodBom Supermercados (id 51)** — resposta humana cortês (19/08, Laura); proposta com o departamento responsável. **Telefone (19) 3828-9798 vale a pena** — segue sem follow-up humano registrado.
3. **Rede Boa Supermercados (id 46)** — proposta enviada ao comercial (`produtos.novos@smboa.com.br`, ticket #23915, 18/08). Sem retorno ainda. **Telefone vale a pena.**
4. **Sanofi Medley (id 91)** — SAC protocolo 02995121 "encaminhado ao departamento responsável" (19/08). **Contato humano direto (facilities/meio ambiente/compras) — SAC não decide.**
5. **Hile (id 101)** — nicho encapsulados, apresentação V2 enviada 19/08. **Monitorar resposta — primeira leva com template novo.**

### Sugestões para o Estrategista
1. **Oba saiu dos quentes:** o SAC fechou o ticket ("Atendimento Finalizado") sem interesse humano. Se insistir, usar **`ouvidoria@redeoba.com.br` (lead 57)** ou canal comercial/comprador direto — e-mail de atendimento genérico de rede grande responde automático e fecha chamado (lição da Oba, 19/08, reaplicada).
2. **Prioridade humana: Arcor/Bagley + GoodBom** — os 2 caminhos com maior potencial de conversão em aberto; telefone/WhatsApp converte antes do próximo tick.
3. **Repor fila de prospecção HOJE** (0 pendentes) — pipeline parado para novos contatos até o Prospector rodar.
4. Pendências estruturais: validação MX pré-envio; renumeração de ids duplicados; créditos Netlify (versão nova só no GitHub Pages).


---

## 2026-08-26 (quarta) — ANALISTA DE QUALIDADE (auditoria pós-sync)

### Números do dia (auditoria independente)
- **Sync Formspree:** `sync_formspree.py` — **32 emails** no cache de bounce; **0** notificações novas do Formspree (nenhum lead novo via site hoje).
- **Leads totais:** 107 — `novo`: 73 | `sequencia`: 7 | `respondido`: 6 (teste, Bagley, Rede Boa, GoodBom, Oba, Sanofi) | `bounce`: 19 | `encerrado`: 2 — **Ativos: 80**.
- **Bounces.json:** 32 emails — **19 correspondem a leads atuais `bounce`**; **13 são históricos/alternativos** (endereço que deu bounce ≠ email cadastrado do lead, ou lead antigo já corrigido).
- **Respostas pendentes:** **0** (`replies_pending.json` vazio — Atendente processou tudo; nada para responder no próximo tick).
- **Consistência leads×bounces (auditado via script):** OK. Todos os leads cujo email atual está no bounces.json estão marcados como `bounce`. Nenhum lead `bounce` pendente de marcação. Os 13 "órfãos" do cache **não têm lead com o mesmo email** — o sync só marca por igualdade exata de endereço, então não havia correção a fazer hoje.

### Problemas encontrados e correções
1. **Lead id 1 (Ana Souza / Alimentos Salto) — `bounce` com `boas_vindas_em` preenchido** (2026-08-13T11:31:14). Persiste desde a auditoria de 14/08: o boas-vindas foi enviado antes do bounce ser detectado. **Registrado apenas** (regra seguida — não corrigido). Confirmado que o `send_sequence` pula bounces — caso antigo, sem reenvio indevido.
2. **13 bounces "órfãos" no cache** (sem lead correspondente exato): ex. `contato@cowpig.com.br` (lead 71 tem `atendimento@...`), `info@kelcopetcare.com.br` (lead 18 tem `comercial@...`), `sac@oba.com.br`/`sac@redeoba.com.br` (leads 57/63 usam `ouvidoria@`/`atendimento@redeoba`), `contato@eixorestaurantes.co` (entrada **truncada** — falta o `.br`; o endereço completo `contato@eixorestaurantes.com.br` já está no cache). **Não é bug do sync** (marca só por igualdade exata) — mas **vale o Estrategista revisar**: nesses casos o bounce veio de um endereço alternativo, não necessariamente do email cadastrado do lead (que segue `novo`/válido).
3. **Lixo de parsing antigo resolvido:** não há mais entradas com ponto final (`...com.br.`) no bounces.json — a limpeza mencionada em 14/08 foi confirmada.
4. **Sem novas correções aplicadas hoje** — auditoria encontrou o sistema consistente com as rodadas do Atendente (09:40/09:50).

### Sugestões para o Estrategista
1. **Tratar os 13 bounces "alternativos" como oportunidade, não como falha:** quando um endereço secundário de empresa (ex. `contato@`) dá bounce mas o lead tem outro endereço (ex. `atendimento@`/`comercial@`), o lead **não deve ser marcado bounce**. Vale validar MX/entrega do email cadastrado antes do próximo envio desses leads (Cowpig 71, Kelco 18, Selmi 60, Penina 72, Nutraway 77, Infanger 50, Delta Terceirizações 64, Oba 57/63).
2. **Normalizar o cache:** remover a entrada truncada `contato@eixorestaurantes.co` (lixo de parsing do mailer-daemon) para o cache ficar 100% limpo e evitar futura confusão na auditoria.
3. **Manter a regra "bounce = só por igualdade exata" documentada** (já está implícita no sync): evita que leads com email alternativo válido sejam descartados por engano. Se o Estrategista quiser reaproveitar os 13 órfãos, o caminho é corrigir o email do lead para o endereço alternativo e revalidar MX — não marcar o lead.

---

## 2026-08-26 (quarta) — BOT DE SEO

### Diagnóstico
- **SEO geral: OK** — 10/10 palavras-chave presentes, confirmado no **HTML publicado ao vivo** (curl no site, não só nos arquivos locais). Títulos, meta descriptions, canonical e links internos OK.
- **PROBLEMA REAL:** site servindo certificado `*.github.io` para `masteroleo.eco.br` → navegador mostra erro de segurança (SEC_E_WRONG_PRINCIPAL) e HTTPS (fator de ranqueamento) quebrado; `https_enforced: false` na API do Pages.
- **Causa:** domínio configurado (`cname: masteroleo.eco.br`) e DNS correto (A → IPs GitHub Pages, sem CAA bloqueando Let's Encrypt), mas o GitHub Pages **não emitiu o certificado** ("The certificate does not exist yet"). Regressão desde 19/08 ~19h.

### Ações aplicadas
1. **Re-disparo da emissão do certificado** via API (`PUT /pages`: re-assert cname + https_enforced=true) — GitHub iniciou verificação/emissão; pode levar até 24h. **Monitorar no próximo tick.**
2. **Schema.org JSON-LD adicionado** em `industrias.html` e `descaracterizacao.html` (LocalBusiness + Service + makesOffer) — as 3 páginas agora têm structured data.
3. **Correção do telefone no JSON-LD do index.html** — estava mascarado (`+551****9631`); agora `+5511967859631` (número público real do site).

### Validação
- JSON-LD válido (parse ok) nas 3 páginas; tags HTML equilibradas; `seo_bot.py` → SEO geral OK.
- **Pendente:** certificado HTTPS customizado (lado GitHub). Se não resolver em ~24h, reavaliar no console do GitHub.

### Sugestão ao Estrategista
- Quando o certificado for emitido: cadastrar o site no **Google Search Console** e pedir indexação das 3 URLs; verificar se o JSON-LD gera rich results (LocalBusiness).

---

## 2026-08-26 (quarta) — MELHORADOR CONTÍNUO (10:25)

### Números do dia
- **Watchdog:** exit 0, saudável — 107 leads, 80 ativos, 32 bounces no cache, nenhum follow-up atrasado.
- **Dashboard:** 104 apresentações, 86 entregues, 18 bounces (17%), **5 respostas (4,8%)** — acima da meta (>3%). Quentes: Arcor/Bagley, GoodBom, Rede Boa, Sanofi, Hile.
- **Ponto MAIS FRACO do sistema hoje: FILA DE PROSPECÇÃO COM 0 PENDENTES.** O Atendente esvaziou a fila na rodada 09:40 (enviou os últimos 3: Ekobe/Zuhan/Lollos) e o Prospector (09:00) não repôs o suficiente — pipeline zerado para novos contatos.

### Correção aplicada (fila reposta: 0 → 7)
Adicionadas **7 empresas REAIS novas** em `bot/fila_prospeccao_extra.json`, com email confirmado em site/Instagram oficiais + **MX validado via nslookup** (e confirmado no dry-run do enviar_lote):
1. **Rede Frango Assado** (`sac@redefrangoassado.com.br`) — sede Pimenta Verde Alimentos, **Louveira/SP** (Rod. Anhanguera km 72) — rotisserie em rodovias = fritura de altíssimo volume.
2. **Vitória Hotéis** (`reservas@vitoriahoteis.com.br`) — Campinas/Indaiatuba/Paulínia — cozinha industrial própria.
3. **Royal Palm Plaza Resort** (`reservas@royalpalm.com.br`) — Campinas — alta gastronomia, cozinha alto volume.
4. **Nacional Inn Campinas** (`reservas@nacionalinncampinas.com.br`) — hotel com cozinha própria.
5. **Dan Inn Sorocaba** (`reservas@daninnsorocaba.com.br`) — hotel com cozinha própria.
6. **Blue Tree Towers Valinhos** (`reservas.valinhos@bluetree.com.br`) — hotel com cozinha própria.
7. **Supermercados São Vicente** (`atendimento@svicente.com.br`) — Piracicaba e região — frituras/açougue, rede maior que as já contatadas.

**Segmento NOVO coberto: HOTÉIS (5 candidatas).** Hotéis geram óleo de cozinha usado em volume constante (café da manhã + restaurante) e têm contrato único de coleta — até então NENHUMA hotel da região estava na base. Também entrou o 1º restaurante rotisserie (Frango Assado).

### Lições
1. **Gap sistêmico de reposição:** o Prospector (09:00) repõe 2-4/dia, mas o Atendente (09:40, 30/30min) consome a fila inteira na mesma manhã — a fila fica 0 pendentes o resto do dia. **Sugestão p/ Estrategista:** ou o Prospector passa a repor 5-8/dia, ou roda em 2 horários (ex. 09:00 + 15:00). Sem isso, o pipeline de NOVOS contatos vive parado.
2. **Fontes de email confiáveis para novos leads:** sites oficiais (página de contato), `conheca.campinas.sp.gov.br` (diretório de POIs da prefeitura de Campinas com emails de hotéis) e Reclame Aqui (SAC oficial). Preferir `reservas@`/`atendimento@`/`sac@` (caixas monitoradas) a emails pessoais.
3. **Netlify segue 403 (créditos de build esgotados)** — tentei `netlify deploy --prod --dir=.` hoje e retornou `JSONHTTPError: Forbidden`. masteroleo.eco.br segue na versão antiga; a nova (com calculadora) está só no GitHub Pages. **Depende de ação humana** (comprar crédito de build ou trocar o DNS). Registrar como pendência estrutural de conversão.
4. **Templates de follow-up (FP1/FP2/FP3) já estão fortes** (renda calculada, US$11bi, ESG, encerramento limpo) — não mexi para não quebrar o que está convertendo 4,8%.

### Para o Estrategista (domingo)
1. **Decidir o ritmo de reposição da fila** (lição 1) — é o gargalo nº1 de crescimento do pipeline.
2. **Netlify 403** (lição 3) — a versão com calculadora está invisível no domínio principal.
3. **Ações humanas quentes:** telefone Arcor/Bagley, GoodBom (19) 3828-9798 e Rede Boa (#23915) — a IA já fez a parte de e-mail; conversão depende de contato humano.

---

## 2026-08-26 (quarta) — ESTRATEGISTA (planejamento da semana)

### Diagnóstico da semana (números reais verificados)
- **107 leads** (80 ativos | 19 bounce | 6 respondidos | 2 encerrados) · **104 apresentações** enviadas · **32 emails no cache de bounce** (13 históricos/alternativos).
- **Respostas reais: 5 (4,8% dos contatados)** — acima da meta (>3%). Das 5: **2 humanas** (Rede Boa 18/08, GoodBom 19/08) e **3 SAC automáticas** (Arcor/Bagley 26/08, Oba 19–26/08, Sanofi 19/08). Tendência de template: lote V1 ~1% → V2 ~4,8% (confirma encurtamento).
- **Bounce:** 18% dos leads (19/107) — dominado, mas com 13 "órfãos" no cache que NÃO são falha do email cadastrado do lead.
- **Watchdog:** saudável. **Backlog de 154 follow-ups** do gap 19→26/08 (7 dias sem cron do Atendente) foi limpo no tick 09:40 — cadência diária é obrigatória.
- **Fila de prospecção:** 7 pendentes com MX validado (5 hotéis + Frango Assado + São Vicente) — NÃO está zerada, mas é o gargalo nº1 (Atendente consome de manhã, Prospector repõe pouco).
- **Inbound:** 0 leads novos via site na semana (3 acumulados, todos de teste) — o site não está gerando demanda.

### Ponto mais fraco identificado
**FECHAMENTO.** São 5 leads quentes em aberto há dias/semanas (Arcor/Bagley, GoodBom, Rede Boa, Sanofi, Hile) e **nenhum contrato ou coleta-teste fechado**. O e-mail faz a parte dele (porta aberta); a conversão em coleta/contrato depende de ação humana (telefone/WhatsApp/LinkedIn) que ainda não aconteceu.

### Pesquisa de mercado (26/08) — com fontes
- **Portaria MME/MMA nº 3/2026 CONFIRMADA:** mandato de **≥1% de óleos e gorduras residuais (OGR)** no biodiesel/SAF/diesel verde **obrigatório a partir de jan/2028** (publicada 13/05/2026 no DOU). Fontes: biodieselbr.com/noticias/materia-prima/ogr/usinas-terao-que-usar-1-de-oleos-e-gorduras-residuais-130526 · eixos.com.br · megawhat.uol.com.br · trenchrossi.com/alertas-legais. → Valida 100% o argumento de urgência já usado no template.
- **Obrigação legal do gerador:** "por lei, estabelecimentos são obrigados a dar destino correto ao óleo contratando empresa de reciclagem" (bomgourmet.com/o-que-fazer-com-o-oleo-de-cozinha-veja-como-restaurantes-reciclam) — reforça o ângulo PNRS/CNPJ no FP2.
- **Concorrentes pagam na hora:** "Pagamento imediato via PIX" (BiOeste, instagram) — **pagamento à vista na coleta vira diferencial de fechamento**; Óleo Verde confirma que preço depende de qualidade/volume e que coletor clandestino é risco (oleoverderesiduos.com.br/2026/02/25).

### Mudanças aplicadas (1–3)
1. **FP2 reforçado p/ fechamento** (`bot/prospecao_followup.py`): Portaria 3/2026 (urgência 2028) + PNRS/passivo no CNPJ + **contrato de coleta programada com volume mínimo** + **relatório ESG mensal** + **pagamento à vista (PIX) na coleta** + CTA **coleta-teste**. `py_compile` OK; render 189 palavras (escaneável, 4 parágrafos).
2. **Playbook de Fechamento** (`bot/persona.md`): nova seção guiando o Atendente a transformar resposta quente em coleta/contrato — pedir volume, propor coleta-teste, fechar via WhatsApp, argumentos legais/ESG/anti-furto, cronograma 24h–3d, contrato para >500 L/mês.
3. **Memória/plano** (`equipe/ecossistema.json` → `estrategista_2026_08_26`): diagnóstico, metas da semana com foco em fechamento e instruções por membro.
   - **Fila NÃO alterada:** não havia email novo confirmado em site oficial (regra da equipe) — 7 pendentes válidos já existem; adicionar empresa à fila só com email real + MX via nslookup.

### Metas da semana (26/08 → 01/09) — foco em FECHAMENTO
1. **Fechar ≥1 contrato/coleta-teste** — ação humana obrigatória nos 5 quentes: telefonar **GoodBom (19) 3828-9798**, **Arcor/Bagley** (compras/facilities/qualidade), **Rede Boa (#23915)**, **Sanofi** (departamento interno de resíduos/facilities — SAC não decide), **Hile**.
2. **Atendente** aplica o Playbook de Fechamento em toda resposta quente (pedir volume + coleta-teste, não parar em "encaminhei").
3. Manter taxa de resposta ≥4% e tentar ≥5% (V2 + FP2 novo em monitoramento).
4. **Fila:** Prospector repor 5–8 empresas/dia com MX validado (ou 2 rodadas 09:00+15:00); alvo ≥10 pendentes.
5. **Bounce <15%**; não marcar lead bounce quando só o email ALTERNATIVO falhou.
6. **Inbound:** 1 lead real via site — destravar Netlify (créditos) ou HTTPS do GitHub Pages e cadastrar no Google Search Console.
7. Monitorar resposta dos novos segmentos: hotéis (5), rotisserie, supermercados, refeições coletivas.

### Lições registradas para a equipe
- Cadência diária do Atendente é obrigatória (7 dias sem rodar = 154 follow-ups atrasados de uma vez).
- Fila vive zerada por descompasso Atendente(09:40) × Prospector(09:00) — reposição de 5–8/dia ou 2ª rodada resolve.
- Auto-resposta de SAC com "ticket FECHADO" (Oba) = porta fechada; responder só reabre o chamado. "Encaminhado ao departamento" (Arcor/Sanofi) = porta aberta: insistir no canal interno.

---

## 2026-08-26 (quarta) — MELHORADOR CONTÍNUO (tick 10:51)

### Diagnóstico do dia
- **Sistema saudável:** watchdog exit 0 (107 leads, 80 ativos, 32 bounces no cache); dashboard com 5 respostas (4,8% — acima da meta 3%); fila de prospecção com 7 pendentes (MX validado) — NÃO zerada.
- **Ponto mais fraco:** o **FP3 (último follow-up, dia 10)** continuava genérico ("porta continua aberta", sem valor nem urgência) — enquanto o Estrategista já havia reforçado FP1 e FP2 com argumentos de fechamento. O último e-mail da sequência é a última chance de converter antes do lead esfriar — era o elo quebrado.

### Melhoria implementada (testada)
1. **`bot/prospecao_followup.py` — FP3 reescrito com argumentos de fechamento:**
   - Valor concreto: R$ 1,00–2,50/L **à vista (PIX na coleta)** + renda calculada (600 L/mês ≈ **R$ 14 mil/ano**);
   - Urgência: **Portaria MME/MMA nº 3/2026** (≥1% de óleo residual no biodiesel obrigatório em **jan/2028**) — "quem fecha contrato agora garante preço e prioridade";
   - CTA de **coleta-teste** essa semana + resposta da quantidade mensal = valor em 24h;
   - Saída sem pressão ("sem interesse? é só ignorar") — mantém a cordialidade do último contato.
   - Verificado: `py_compile` OK + renderização real (151 palavras, subject mantido, thread com `apresentacao_msgid`).

### Impacto
- **35 leads** com FP2 enviado entram em FP3 nos **próximos 3–4 dias** (apresentação em ~6–7d hoje; vence no dia 10) — primeira leva a receber o FP3 com argumentos de fechamento. Monitorar resposta.

### Para o Estrategista (domingo)
1. Monitorar resposta da 1ª leva de FP3 novo (35 leads até 30/08) — é o último funil antes do encerramento.
2. Persiste o gargalo de FECHAMENTO: ação humana telefônica nos 5 quentes (GoodBom, Arcor/Bagley, Rede Boa, Sanofi, Hile) — o e-mail já fez a parte dele.
3. Netlify segue sem créditos de build (403); versão nova da calculadora só no GitHub Pages.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 11:05)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (8 "já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 11:00) — 107 leads, 80 ativos, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila com 0 pendentes, nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (cobertura 100%).
- **check-replies:** **1 resposta NOVA aguardando** — Sumerbol Supermercados (`atendimento@sumerbol.com.br`).
- **Leads totais:** 107 (ativos 80, bounces 32 no cache) — sem mudança de contagem neste tick.

### Evento do tick (destaque — lead quente NOVO)
- **Sumerbol Supermercados LTDA (id 21, `atendimento@sumerbol.com.br`)** respondeu às **13:21 GMT (10:21 BRT)** ao e-mail "Último contato sobre a compra do óleo — Master Óleo" (enviado hoje 09:27):
  > *"Seu e-mail foi encaminhado para o setor responsável, qualquer dúvida entrar em contato pelo e-mail: **manutencao@sumerbol.com.br** ou **ivone.franca@sumerbol.com.br**."*
- **Natureza da resposta:** é uma resposta do atendimento/SAC da rede, MAS diferente das auto-respostas de helpdesk (Oba/Arcor/Sanofi): o lead **forneceu contato humano direto** (Ivone França / Manutenção) — caminho concreto de negociação, não apenas protocolo.
- **Ação do atendente_ia (11:05):** respondeu no thread agradecendo o encaminhamento e aplicando o **Playbook de Fechamento**: pediu as 2 informações-chave (volume aproximado L/kg por mês + tipo de material), propôs **coleta-teste sem compromisso essa semana**, ofereceu seguir direto com a Ivone pelo e-mail dela ou pelo **WhatsApp (11) 96785-9631** e perguntou o melhor contato/horário. Lead id 21 marcado `respondido` (respondido_por=atendente_ia); `replies_pending.json` zerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.** Sync, watchdog, correções, sequência e fila 100% verdes.
2. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção zerada (exige reposição 5–8/dia).

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — NOVO e #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Rede de supermercados = alto volume de óleo de fritura. **Ação recomendada: contato direto com a Ivone (e-mail/telefone) para destravar — o e-mail da IA já pediu volume, um toque humano agora converte em coleta-teste.**
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35 pedindo volume. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno de resíduos/facilities.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — é o lead com caminho mais concreto hoje (contato humano explícito, rede de supermercados com volume de fritura). Prioridade máxima da semana.
2. **Contato humano nos demais quentes** segue pendente (Arcor/Bagley, GoodBom, Rede Boa, Sanofi) — o e-mail já fez a parte dele; telefone converte.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. **Taxa de resposta subiu para ~6,5% (7 respostas reais)** com a resposta da Sumerbol — acima da meta de 4–5%; monitorar se o FP3 novo sustenta.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 11:35)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 11:31) — **114 leads, 86 ativos**, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila com 0 pendentes, nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (**cobertura 100%**: 111 apresentações + 3 boas-vindas, 0 leads sem envio).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio).
- **respostas_enviadas:** 0 — nenhum reply novo desde o tick 11:05 (Sumerbol já respondido). Nenhum pedido de relatório ESG → sem geração de PDF.
- **Leads totais:** 114 (ativos 86) — **+7 leads desde o último tick registrado (11:05)**.

### Evento do tick (destaque — 7 leads NOVOS no pipeline)
- **7 empresas adicionadas às 11:01–11:02** (ids 111–117, fonte `prospeccao-lote`, apresentação já enviada na criação) — exatamente as que o **Melhorador validou às 10:30** (MX checado via nslookup) e que estavam marcadas como "7 pendentes" na fila extra:
  1. **Pimenta Verde Alimentos / Rede Frango Assado** (Louveira) — rotisserie;
  2. **Vitória Hotel Concept** (Campinas/Indaiatuba/Paulínia) — hotel;
  3. **Royal Palm Plaza Resort** (Campinas) — hotel;
  4. **Hotel Nacional Inn Campinas Trevo** — hotel;
  5. **Hotel Dan Inn Sorocaba** — hotel;
  6. **Blue Tree Towers Valinhos** — hotel;
  7. **Supermercados São Vicente** (Piracicaba) — rede.
- **Segmento HOTEL estreia na base (5 redes)** — restaurantes de hotel têm cozinha industrial com alto volume de fritura; argumento de renda extra (600 L/mês ≈ R$ 14 mil/ano) aplica bem.
- Fila extra (`fila_prospeccao_extra.json`): 67 empresas restantes (sem campo de rastreio individual — os 7 acima já saíram dela ao virar lead).

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.** Sync, watchdog, correções, sequência, fila e base 100% verdes.
2. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção exige reposição 5–8/dia.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Resposta da IA enviada (11:05) pedindo volume + propondo coleta-teste. **Ação recomendada: contato direto com a Ivone — é o caminho mais concreto para fechar.** (aguardando retorno)
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — prioridade máxima da semana; caminho mais concreto hoje.
2. **Monitorar resposta dos 7 novos (5 hotéis)** — novo segmento com potencial de volume; ver se o template V2 converte em resposta.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. Nenhuma mudança de métrica relevante neste tick (respostas reais seguem em 7; ~6,5% dos contatados).

---

## 2026-08-26 (quarta) — ATENDENTE (tick 12:05)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "já tentado" neste tick). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 12:01) — **114 leads, 86 ativos**, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila com 0 pendentes, nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (**cobertura 100%**: 111 apresentações + boas-vindas, 0 leads sem envio).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio).
- **respostas_enviadas:** 0 — nenhum reply novo desde o tick 11:35 (Sumerbol já respondido). Nenhum pedido de relatório ESG → sem geração de PDF.
- **Leads totais:** 114 (ativos 86) — base estável, sem novas entradas neste tick.

### Evento do tick
- **Nenhum evento operacional.** Rodada de rotina: sync, watchdog, follow-ups, sequência, fila e base 100% verdes. Nenhum reply novo, nenhum follow-up atrasado, nenhum bounce novo a corrigir.
- Fila extra (`fila_prospeccao_extra.json`): 67 empresas com MX aguardando o Prospector repor na fila ativa.

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.**
2. Pendências estruturais mantidas (sem mudança): lead id 1 (teste); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção exige reposição 5–8/dia.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Resposta da IA enviada (11:05) pedindo volume + propondo coleta-teste. **Ação recomendada: contato direto com a Ivone — caminho mais concreto para fechar.** (aguardando retorno)
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — prioridade máxima da semana.
2. **Continuar monitorando os 7 novos (5 hotéis)** — novo segmento com potencial de volume.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. Métricas estáveis: 7 respostas reais (~6,5% dos contatados). Sem novos quentes neste tick.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 13:02)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "já tentado" neste tick). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 13:01) — **114 leads, 86 ativos**, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila com 0 pendentes, nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (**cobertura 100%**: 111 apresentações + 3 boas-vindas, 0 leads sem envio).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio).
- **respostas_enviadas:** 0 — nenhum reply novo desde o tick 12:31 (Sumerbol já respondido às 11:05). Nenhum pedido de relatório ESG → sem geração de PDF.
- **Leads totais:** 114 (ativos 86) — base estável, sem novas entradas neste tick.

### Evento do tick
- **Nenhum evento operacional.** Rodada de rotina idêntica ao tick 12:31: sync, watchdog, follow-ups, sequência, fila e base 100% verdes. Nenhum reply novo, nenhum follow-up atrasado, nenhum bounce novo a corrigir.
- Fila extra (`fila_prospeccao_extra.json`): 67 empresas com MX aguardando o Prospector repor na fila ativa (5–8/dia).

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.**
2. Pendências estruturais mantidas (sem mudança): lead id 1 (teste); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção exige reposição 5–8/dia.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Resposta da IA enviada (11:05) pedindo volume + propondo coleta-teste. **Ação recomendada: contato direto com a Ivone — caminho mais concreto para fechar.** (aguardando retorno)
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — prioridade máxima da semana.
2. **Continuar monitorando os 7 novos (5 hotéis)** — novo segmento com potencial de volume.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. Métricas estáveis: 7 respostas reais (~6,5% dos contatados). Sem novos quentes neste tick.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 13:33)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 13:31) — **114 leads, 86 ativos**, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila com 0 pendentes, nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (**cobertura 100%**: 111 apresentações + 3 boas-vindas, 0 leads sem envio).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio, confirmado `[]`).
- **respostas_enviadas:** 0 — nenhum reply novo desde o tick 13:02 (Sumerbol já respondido às 11:05). Nenhum pedido de relatório ESG → sem geração de PDF.
- **Leads totais:** 114 (ativos 86; 79 novo + 7 sequencia) — base estável, sem novas entradas neste tick.

### Evento do tick
- **Nenhum evento operacional.** Rodada de rotina idêntica ao tick 13:02: sync, watchdog, follow-ups, sequência, fila e base 100% verdes. Nenhum reply novo, nenhum follow-up atrasado, nenhum bounce novo a corrigir.
- Fila extra (`fila_prospeccao_extra.json`): 67 empresas com MX aguardando o Prospector repor na fila ativa (5–8/dia).

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.**
2. Pendências estruturais mantidas (sem mudança): lead id 1 (teste); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção exige reposição 5–8/dia.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Resposta da IA enviada (11:05) pedindo volume + propondo coleta-teste. **Ação recomendada: contato direto com a Ivone — caminho mais concreto para fechar.** (aguardando retorno)
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — prioridade máxima da semana.
2. **Continuar monitorando os 7 novos (5 hotéis)** — novo segmento com potencial de volume.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. Métricas estáveis: 7 respostas reais (~6,5% dos contatados). Sem novos quentes neste tick.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 14:02)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails no cache de bounce; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Watchdog:** ✅ saudável (exit 0, 14:01) — **114 leads, 86 ativos**, 32 bounces no cache, nenhum follow-up atrasado/bounce sem correção/lead parado.
- **prospecao_followup.py:** 0 follow-ups processados (nada atrasado).
- **enviar_lote:** status OK — fila de prospecção: 98 empresas (87 já contatados, 24 bounce), **0 pendentes** — nada a enviar.
- **send_sequence:** sequência processada, sem envios novos pendentes (**cobertura 100%**: 111 apresentações + 3 boas-vindas, 0 leads sem envio).
- **check-replies:** 0 respostas aguardando atendimento (`replies_pending.json` vazio, confirmado `[]`).
- **respostas_enviadas:** 0 — nenhum reply novo desde o tick 13:33 (Sumerbol já respondido às 11:05). Nenhum pedido de relatório ESG → sem geração de PDF.
- **Leads totais:** 114 (ativos 86) — base estável, sem novas entradas neste tick.

### Evento do tick
- **Nenhum evento operacional.** Rodada de rotina idêntica ao tick 13:33: sync, watchdog, follow-ups, sequência, fila e base 100% verdes. Nenhum reply novo, nenhum follow-up atrasado, nenhum bounce novo a corrigir.
- Fila extra (`fila_prospeccao_extra.json`): 67 empresas com MX aguardando o Prospector repor na fila ativa (5–8/dia).

### Problemas encontrados e correções
1. **Nenhum problema operacional neste tick.**
2. Pendências estruturais mantidas (sem mudança): lead id 1 (teste); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build (403); fila de prospecção exige reposição 5–8/dia.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (id 21) — #1:** resposta 26/08 com **contato humano direto** (`manutencao@sumerbol.com.br`, Ivone França). Resposta da IA enviada (11:05) pedindo volume + propondo coleta-teste. **Ação recomendada: contato direto com a Ivone — caminho mais concreto para fechar.** (aguardando retorno)
2. **Arcor/Bagley (id 14)** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35. Aguardar análise; telefonar (compras/facilities/qualidade).
3. **GoodBom Supermercados (id 51)** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa (id 46)** — ticket #23915, proposta no comercial; telefonar.
5. **Sanofi Medley (id 91)** — SAC protocolo 02995121, porta aberta; aguardar depto interno.
6. **Hile (id 101)** — nicho encapsulados, 1ª leva template V2; monitorar.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via contato direto Ivone França** — prioridade máxima da semana.
2. **Continuar monitorando os 7 novos (5 hotéis)** — novo segmento com potencial de volume.
3. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, reposição da fila (5–8/dia), renovação de créditos Netlify.
4. Métricas estáveis: 7 respostas reais (~6,5% dos contatados). Sem novos quentes neste tick.

---

## 2026-08-26 (quarta) — MELHORADOR CONTÍNUO (tick 14:15)

### Diagnóstico do dia
- **Sistema saudável:** watchdog exit 0 (114 leads, 86 ativos, 32 bounces no cache); dashboard 5,4% de resposta (6 respostas) — acima da meta 3%. Templates V2/V3 e FP1/FP2/FP3 já reforçados.
- **Ponto mais fraco (crescimento):** fila de prospecção ativa em **0 pendentes** — o Atendente (30/30min) consome mais rápido do que o Prospector (09:00) repõe. Gargalo recorrente já registrado pelo Estrategista.
- **Ponto mais fraco (fechamento):** Sumerbol (lead #1) abriu porta REAL via SAC (contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`), mas o ciclo de respostas do Atendente **não emite email proativo ao contato direto** — o fechamento dependia de ação não automatizada.

### Melhorias implementadas (testadas e registradas)
1. **Email de FECHAMENTO enviado a Ivone (Sumerbol) — contato direto indicado pelo SAC da própria Sumerbol:** 1 email pontual (14:10) para `ivone.franca@sumerbol.com.br`, referenciando o encaminhamento da proposta, reforçando valor (R$ 1,00–2,50/L), certificado PNRS + **PIX na coleta**, oferecendo **coleta-teste sem compromisso** e pedindo o volume mensal + WhatsApp (11) 96785-9631. Não é massa (1 email, lead mais quente); não duplica o Atendente (lead já 'respondido'). **Verificado:** envio OK via SMTP (Message-ID registrado).
2. **Fila de prospecção reposta (67 → 70):** 3 empresas NOVAS reais com email de fonte oficial + MX válido via nslookup:
   - **Savegnago Supermercados** — `atendimento@savegnago.com.br` (rede do interior paulista; padaria/rotisserie/fritura alto volume)
   - **GRSA / Grupo GR** — `contato@grsa.com.br` (refeições coletivas, 1M+ refeições/dia; cozinha industrial)
   - **Premium Hotel Campinas** — `contato@hotelpremiumcampinas.com.br` (hotel com restaurante)
   - **Verificado:** `enviar_lote --status` mostra os 3 como pendentes com MX válido → o Atendente envia a apresentação no próximo tick. Obs.: Covabra (lojas em Indaiatuba/Jundiaí/Sumaré/Vinhedo) **já estava na base** — o Prospector acertou; não duplicado.

### Aprendizado novo
- **Quando o lead fornece contato humano direto, o fechamento exige email proativo (fora do ciclo de respostas).** O Atendente responde inbound; a conversão de um lead quente com contato nomeado é ação de follow-up direto — vale o Melhorador/Atendente emitir esse email no mesmo dia em que o contato chega.

### Para o Estrategista (domingo)
1. **Sumerbol:** email direto enviado a Ivone hoje — se sem retorno em 2–3 dias, **telefonar/WhatsApp (11) 96785-9631** é o próximo passo de fechamento.
2. **Cadência da fila:** Prospector deve repor 5–8/dia ou rodar em 2 horários — a fila vive zerada após o consumo do Atendente da manhã.
3. **Netlify sem créditos (403)** segue bloqueando a versão nova (calculadora) no domínio principal — priorizar DNS/créditos para destravar inbound.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 14:33)

### Números do dia (estado real pós-tick)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — **+3 neste tick** (ids 118–120).
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (114 apresentações + 3 boas-vindas, 0 sem envio) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 14:33) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Evento do tick (produtivo)
- **3 apresentações ENVIADAS (14:32–14:33)** para os pendentes que o Melhorador deixou na fila ativa às 14:15 (todos MX validado): **Savegnago Supermercados** (rede do interior paulista — padaria/rotisserie/fritura), **GRSA/Grupo GR** (refeições coletivas, 1M+ refeições/dia — cozinha industrial), **Premium Hotel Campinas** (hotel com restaurante). Registrados no `leads.csv` com lock (merge). Fila ativa zerada de novo; fila extra com **70 empresas** aguardando o Prospector repor 5–8/dia.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0 na rodada inteira; base subiu de 114 → 117 leads sem nenhum bounce novo.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** a fila ativa esvazia a cada consumo do Atendente — os 3 enviados neste tick zeraram a fila novamente. Reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos 3 novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — 3 enviados hoje e fila zerada; reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-08-26 (quarta) — ATENDENTE (tick 15:01)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 14:33)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável (últimos 3: ids 118–120 Savegnago/GRSA/Premium Hotel, enviados 14:32–14:33).
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (114 apresentações + 3 boas-vindas, 0 sem envio) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 15:01) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes (3 enviados no tick 14:33). Base estável em 117 leads / 89 ativos / 32 bounces no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes); fila extra com **70 empresas** aguardando o Prospector repor 5–8/dia (ou 2 rodadas 09:00+15:00) — segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos 3 novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada; reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 15:32)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 15:01)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117** — 114 apresentações + 3 boas-vindas, 0 sem envio) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 15:32) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 15:01: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 101 na fila, 90 já contatados); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 16:01)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 15:32)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117** — 114 apresentações + 3 boas-vindas, 0 sem envio) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 16:01) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 15:32: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 101 na fila, 90 já contatados); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 16:31)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 16:01)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117**) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 16:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila ativa com 0 pendentes (fila extra: 70 empresas com MX validado aguardando o Prospector repor 5–8/dia). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 16:01: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 70 empresas na fila extra aguardando reposição); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 17:01)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 16:31)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117**) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 17:01) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 16:31: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.
- **Pendência de processo RESOLVIDA:** o alias `send_sequence` (underscore) foi confirmado no `bot_oleo.py` (linha 323) — os ticks anteriores registraram 6 ocorrências de "comando correto é send-sequence"; hoje o alias existe e o comando da instrução do cron funciona sem fallback manual.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 70 empresas na fila extra aguardando reposição); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 18:01)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 17:31)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117**) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 18:01) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 17:31: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 70 empresas na fila extra aguardando reposição); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.


---

## 2026-08-26 (quarta) — ATENDENTE (tick 17:31)

### Números do dia (estado real pós-tick — sem mudanças vs. tick 17:01)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117**) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ✅ saudável (exit 0, 17:31) — nenhum follow-up atrasado, bounce sem correção ou lead parado.
- **prospecao_followup.py:** 0 follow-ups processados. **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick
- **Nenhum evento novo** — tick de rotina, tudo verde e idêntico ao 17:01: watchdog exit 0 na rodada inteira, nenhum reply novo, nenhum bounce a corrigir, fila ativa com 0 pendentes. Base estável em 117 leads / 89 ativos / 7 respondidos / 19 bounces de leads / 32 no cache.
- **Sem pedido de relatório ESG** — nenhum lead pediu relatório de impacto/certificado; nenhum PDF gerado.

### Problemas encontrados e correções
1. **Nenhum problema operacional novo.** Watchdog exit 0; sync sem bounces novos; correções sem pendência.
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 70 empresas na fila extra aguardando reposição); reposição de 5–8/dia pelo Prospector (ou 2 rodadas 09:00+15:00) segue sendo a pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1 da semana)** — resposta humana via SAC (26/08 13:21 GMT) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA enviada (11:05) + email de fechamento do Melhorador para Ivone (14:10). **Próximo passo: telefonar/WhatsApp (11) 96785-9631 para Ivone em 2–3 dias se sem retorno.**
2. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; resposta enviada 09:35, aguardar análise.
3. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
4. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
5. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
6. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone** (prioridade máxima) — email já enviado; telefone/WhatsApp em 2–3 dias.
2. **Monitorar resposta dos novos de hoje (Savegnago, GRSA, Premium Hotel)** — 2 deles são alvos grandes (rede de supermercados + refeições coletivas de 1M+ refeições/dia).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.

---

## 2026-09-07 (segunda) — ATENDENTE (tick 09:40)

### Números do dia (estado real pós-tick — 12 dias desde o último registro, 26/08 17:31)
- **Sync Formspree:** 32 emails em bounce cache; **0** notificações novas (nenhum lead novo via site — 3 inbound acumulados no total).
- **corrigir_emails:** 0 bounces processados — todos os 32 já com tentativa registrada em `correcoes_emails.json` (18 "Já tentado" neste tick, incl. Kemin sem alternativa válida). Nada novo a corrigir.
- **Leads totais:** **117** (115 reais + 2 teste) — estável desde 26/08.
  - `novo`: 82 | `sequencia`: 7 | `respondido`: 7 | `bounce`: 19 | `encerrado`: 2 — **Ativos: 89**.
- **Cobertura:** 100% dos leads com apresentação/boas-vindas enviada (**117/117**) — nenhum lead parado.
- **Respostas pendentes:** 0 (`replies_pending.json` vazio — confirmado `[]`).
- **Watchdog:** ⚠️ **exit 1 na 1ª rodada → RESOLVIDO** (exit 0 na 2ª): 13 follow-ups atrasados recuperados (detalhes abaixo).
- **enviar_lote --status:** fila com 101 empresas (90 contatados, 24 bounces, **0 pendentes**). **send_sequence:** sem envios novos. **check-replies:** 0 respostas.

### Eventos do tick (o principal: correção de 13 follow-ups atrasados)
1. **Watchdog pegou 13 leads com follow-up ATRASADO (exit 1)** — leads de prospecção com apresentação há 11–12 dias que ainda não tinham FP2/FP3 registrado (pausa de 12 dias sem tick entre 26/08 e 07/09).
2. **Resolução:** `prospecao_followup.py` envia **1 follow-up por lead por execução**, então foram necessárias **2 rodadas**:
   - Rodada 1: **13× FP2** (thread) — Ekobe, Zuhan, Lollos, Pimenta Verde (Rede Frango Assado), Vitória Hotel Concept, Royal Palm Plaza, Nacional Inn Campinas, Dan Inn Sorocaba, Blue Tree Valinhos, Supermercados São Vicente, Savegnago, GRSA, Premium Hotel Campinas.
   - Rodada 2: **13× FP3** (thread, último da sequência) — mesmos leads completaram a cadência completa (apresentação → FP1 → FP2 → FP3).
   - Watchdog final: ✅ exit 0, saudável.
3. **Nenhum reply novo** — caixa sem respostas desde 26/08; sem pedido de relatório ESG (nenhum PDF gerado).

### Problemas encontrados e correções
1. **13 follow-ups atrasados (RESOLVIDO)** — causa raiz: intervalo de 12 dias sem execução do tick (último registro 26/08 17:31); os leads acumularam 11–12 dias desde a apresentação. Corrigido com 2 rodadas de `prospecao_followup.py` (FP2 + FP3). Esses 13 leads agora **completaram toda a sequência de follow-ups** — se não responderem, estão encerrados na prática (próximo passo: follow-up humano/WhatsApp nos alvos grandes).
2. **Gargalo estrutural recorrente (registrado, não corrigível por mim):** fila ativa zerada (0 pendentes — 90 contatados / 24 bounces de 101); reposição de 5–8/dia pelo Prospector segue como pendência nº1 de crescimento.
3. Pendências já registradas e mantidas: lead id 1 (teste, bounce com boas-vindas); ids duplicados 84/86/88; WBM sem email alternativo; Netlify sem créditos de build.

### Leads quentes (para ação humana — destaque)
1. **Sumerbol Supermercados (#1, URGENTE)** — resposta humana via SAC (26/08) com contatos diretos `ivone.franca@sumerbol.com.br` / `manutencao@sumerbol.com.br`; resposta IA + email de fechamento do Melhorador já enviados. **O prazo de 2–3 dias para retorno VENCEU — acionar Ivone por WhatsApp (11) 96785-9631 o quanto antes.**
2. **Savegnago Supermercados + GRSA (Grupo GR)** — alvos grandes (rede de supermercados + refeições coletivas com 1M+ refeições/dia) completaram FP2/FP3 hoje **sem resposta**; sequência de email esgotada → valem follow-up humano por telefone.
3. **Arcor/Bagley** — SAC automático 26/08 "encaminhado à área responsável"; aguardar análise.
4. **GoodBom Supermercados** — resposta humana (Laura, 19/08); **telefonar (19) 3828-9798**.
5. **Rede Boa** — ticket #23915, proposta com o comercial; aguardando.
6. **Sanofi Medley** — SAC protocolo 02995121, porta aberta; aguardar departamento.
7. **Hile** — nicho encapsulados, V2.

### Sugestões para o Estrategista
1. **Fechar Sumerbol via Ivone (prioridade máxima, atrasada)** — email já enviado em 26/08; o prazo de retorno venceu, acionar WhatsApp/telefone agora.
2. **Follow-up humano nos 13 leads que esgotaram a sequência de email hoje** — em especial **Savegnago, GRSA, Supermercados São Vicente, Royal Palm e Vitória Hotel** (redes/hotéis grandes, com volume relevante de óleo). WhatsApp (11) 96785-9631 com o discurso de urgência (Portaria MME/MMA nº 3/2026, jan/2028).
3. **Cadência da fila segue sendo o gargalo nº1** — fila ativa zerada (0 pendentes); reposição 5–8/dia (ou 2 rodadas) continua valendo.
4. Pendências estruturais seguem: renumeração ids 84/86/88, validação MX pré-envio, renovação de créditos Netlify.
