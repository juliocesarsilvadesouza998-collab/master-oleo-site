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
