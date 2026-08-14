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
