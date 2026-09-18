# Insights da Operação — Master Óleo
## Atualizado em: 18/09/2026 14:14 (Melhorador Contínuo)

### Melhorias Implementadas em 18/09

1. **Seção PROVA SOCIAL no site** (deploy-vercel/index.html) — 3 cases reais:
   - BSBIOS × Madero (55 mil L/mês, 270 restaurantes)
   - Catalent Indaiatuba/Sorocaba (cliente real encapsulados)
   - Mercado UCO US$8bi→US$15bi + exportação EUA + Portaria 3/2026
   
2. **FP1 fortalecido com escassez global** (prospecao_followup.py) — antes FP1 só tinha preço e renda calculada; agora inclui exportação EUA + jan/2028 como gatilho de urgência, alinhando FP1 com a força do FP2.

3. **Aprendizado novo — sites de supermercados regionais não expõem email público** (Revolução, Yeda, São Roque, União): só formulário ou WhatsApp. Fila precisa de fontes alternativas (páginas de fornecedores, diretórios setoriais ABIA/SINDALIMENTOS, LinkedIn).

### Resumo do Tick Atual (14:01)

| Indicador | Valor | Meta | Status |
|-----------|-------|------|--------|
| Leads totais | 239 | — | ✅ |
| Ativos | 164 | — | ✅ |
| Apresentações enviadas | 206 | — | ✅ |
| Entregues (est.) | 177 | — | ✅ |
| Bounce rate | 14% | <15% | ✅ |
| Respostas | 18 | — | ✅ |
| Taxa de resposta | ~8% | >3% | ✅ BATIDA (2º mês) |
| Watchdog verde consecutivo | 36 | — | ✅ |
| Fila pendentes | 0 | ≥10 | ❌ ZERADA |

### Ações Realizadas neste Tick

1. **Sync + Auto-correção:** sync_formspree.py e corrigir_emails.py OK (49 bounces no cache, nenhum novo)
2. **Watchdog:** 36º tick verde consecutivo (SMTP OK, IMAP OK, sem follow-ups atrasados)
3. **Sequência:** 0 follow-ups processados, 0 envios novos pelo send_sequence, 0 respostas pendentes
4. **Desemperramento da fila:** UNISO (ouvidoria@uniso.br) e Sapore (suprimentos@sapore.com.br) — estavam PENDENTES há vários ticks sem serem enviados automaticamente. Enviados manualmente via `enviar_lote.py --max 10`
5. **Check-replies:** replies_pending.json vazio — nenhuma resposta para atender

### Leads QUENTES (prioridade máxima)

| Lead | Contato | Situação | Ação Necessária |
|------|---------|----------|-----------------|
| **Dalben Supermercados** | Luis (luish@supermercadosdalben.com.br) | Respondeu 18/09 10:23 | Aguardando retorno dele — lead quente nº1 |
| **Savegnago Supermercados** | comercial@savegnago.com.br | Apresentação enviada 07/09 | Toque WhatsApp (11) 96785-9631 URGENTE (prazo 10/09 vencido) |
| **Grupo IMC / Frango Assado** | Geral | Apresentação enviada | Toque WhatsApp (11) 96785-9631 (prazo 10/09 vencido) |
| **Selmi** | compras@selmi.com.br | Apresentação enviada 11/09 | Toque leve WhatsApp (prazo vencido) |
| **Queijos Itupeva** | Rafael | Negociação ativa | Agendar coleta-teste (R$0,50-1,50/kg, descaracterização cortesia) |
| **Sumerbol (Ivone Franca)** | ivone.franca@sumerbol.com.br | Email de fechamento enviado | Toque WhatsApp/telefone |
| **GoodBom (Laura)** | (19) 3828-9798 | Proposta encaminhada | Telefonar |
| **Rede Boa** | produtos.novos@smboa.com.br | Ticket #23915 | Toque leve |
| **Arcor/Bagley** | SAC | Protocolo encaminhado | Aguardando retorno |
| **Sanofi Medley** | SAC | Protocolo 02995121 | Aguardando direcionamento interno |

### Gargalos Atuais

1. **Fila de prospecção ZERADA (0 pendentes)** — gargalo nº1 recorrente. Prospector precisa repor com urgência (5-8/dia, 2 horários)
2. **Fechamento zero em 2 meses** — 18 respostas reais, nenhum contrato ou coleta-teste. Ação humana (WhatsApp/telefone) é o elo que falta
3. **Netlify 403** — site masteroleo.eco.br sem créditos de build (versão antiga no ar)
4. **Inbound zerado** — site não gera leads; só GitHub Pages com versão nova ativo

### Novos Enviados (18/09)

- **UNISO - Universidade de Sorocaba** (ouvidoria@uniso.br) — restaurante universitário próprio (~400+ refeições/dia), nicho NOVO (universidades)
- **Sapore S.A.** (suprimentos@sapore.com.br) — rede nacional de refeições coletivas (1,3M refeições/dia), canal de compras (quem decide)

### Pendências WhatsApp/Telefone (ação humana necessária)

- Savegnago — (16) 3946-2088 / WhatsApp (11) 96785-9631
- Grupo IMC / Frango Assado — WhatsApp (11) 96785-9631
- Selmi — WhatsApp/compras@selmi.com.br
- Queijos Itupeva — WhatsApp (11) 940333759 (fechar coleta-teste)
- Sumerbol (Ivone) — WhatsApp/telefone
- GoodBom (Laura) — (19) 3828-9798