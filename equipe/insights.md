# Insights Diários — Analista de Qualidade

## 2026-09-21 (segunda-feira) — 19:31 (Cron #8 — noturno)

### Resumo do ciclo (cron noturno)

**Watchdog:** ✅ OK (exit 0) — tudo saudável, SMTP/IMAP normais, sem follow-ups atrasados.

**Dashboard:** 169 leads totais | 124 ativos | 55 bounces | 12 respondidos | 10 pendentes — estável, sem alterações.

**Sequência:** prospecao_followup → 0. send_sequence → OK. check-replies → 0 pendentes.

### O que foi feito neste ciclo

| Ação | Detalhe |
|------|---------|
| ✅ PASSO 0 | sync_formspree.py (0 notificações novas, 55 bounces em cache) + corrigir_emails.py (0 novos bounces) — cron #8 |
| ✅ PASSO 1 | watchdog.py → exit 0, saudável. Nada a corrigir. — cron #8 |
| ✅ PASSO 2 | prospecao_followup.py (0 follow-ups). send_sequence OK. check-replies → 0 respostas. — cron #8 |
| ✅ Relatório | ecossistema.json → cron #8. insights.md → cron #8. — cron #8 |

### Observações

- **🥶 Ciclo noturno tranquilo** — mesmo padrão do cron #7 vespertino. Sem respostas novas, sem follow-ups atrasados, sem notificações Formspree, sem pedidos de relatório ESG.
- **10 pendentes na fila** — abaixo do ideal (>30). Necessário repor fila em breve.
- **Taxa de bounce: 32,5%** (55/169) — acima do ideal (<15%). Os 55 bounces históricos continuam como passivo; sem novos para processar.
- **Nenhum lead pediu relatório ESG** neste ciclo.
- **Nenhum lead pediu remoção** da lista.

### Leads QUENTES 🔥 (sem alterações desde cron #7)

1. **🔥 PASTIFÍCIO SELMI (Sumaré/SP)** — Ticket #89532 no Zendesk. Proposta na fila de análise do SAC. Potencial para óleo vencido + resíduos >40% gordura.

2. **🔥 PAGUE MENOS (Campinas)** — Proposta enviada para Josiane Marinho. Aguardar retorno.

3. **🔥 DALBEN SUPERMERCADOS** — Gerente Luis (luish@supermercadosdalben.com.br). Proposta enviada. Aguardar retorno.

4. **🔥 QUEIJOS ITUPEVA (Rafael)** — Negociação ativa para coleta-teste de vencidos >40% gordura. Lead mais quente para conversão rápida.

5. **🔥 CABANHA CAMPESTRE 53 (Daniele Santos)** — ~600kg/mês. Aguardando detalhamento do tipo de material.

6. **🔥 BRASFRIGO (Salto/SP)** — Empresa na mesma cidade-sede (Salto). Contato via sac@brasfrigo.com.br. Pendente toque humano.

7. **🔥 SAVEGNAGO (~100 lojas)** — Aguardando retorno após apresentação comercial. Pendente toque via WhatsApp (11) 96785-9631.

8. **🔥 MUFFATO / MAX ATACADISTA** — SAC orientou ligar (43) 3371-1700. Pendente ação humana.

## 2026-09-22 (terça-feira) — Bot de SEO

### Ranking Bing (cron #9)

- **22 keywords monitoradas** — todas indexadas ✅
- **Ranking real:** todas fora do top 20 ⏳
- **Diagnóstico:** Site indexado, SEO geral OK. Sem posições ainda — normal para site novo, precisa de semanas de maturação + backlinks.
- **Ação:** Nenhuma mudança aplicada (conforme regra: "SEO OK, sem posições → reportar e parar").

## 2026-09-22 (terça-feira) — Melhorador Contínuo (17:48)

### Diagnóstico
- **10 leads pendentes** — abaixo da meta 30+. Pipeline secando.
- **Bounce 26%** (33/126) — acima do ideal <15%.
- **Respostas 10,3%** (13/126) — boa taxa, mas sem novidade desde 19/09.
- **Site:** masteroleo.eco.br = 200 OK (GitHub Pages), Netlify 403.

### Melhorias implementadas

| Ação | Arquivo | Detalhe |
|------|---------|---------|
| ✅ +15 empresas MX-verificadas | bot/prospecao.py | Unigra, AAK, Perfetti, Bakels, Kemin, Theoto, Marquespan, Flamboia, Agrana, Moinho Potenza, Bem Casado, Penina, Cowpig, CBR, Only Fruit — todas com MX Outlook/Locaweb/Mimecast |
| ✅ FP3 reformulado | bot/prospecao_followup.py | Tom mais suave, opção de saída explícita, US$11 bi + escassez global + 2028 em 2 parágrafos |
| ✅ Pipeline +33% | bot/prospecao.py | EMPRESAS: 45 → 60 empresas |

### Aprendizados
1. **Bounce alto é o maior problema estrutural**. Novos emails com MX de provedores grandes (Outlook, Locaweb) devem reduzir isso.
2. **FP3 estava repetitivo** — só repetia preço + 2028 sem diferencial do FP2. Novo template é mais honesto ("prometo que é a última"), dá saída clara.
3. **Repor fila é a alavanca mais imediata**: 10 pendentes → ~1 resposta esperada; 30 pendentes → ~3 respostas. +15 empresas = salto estimado de 60% na fila.
4. **Indústrias de óleos e gorduras (Unigra, AAK) são o melhor fit** — geram óleo vencido E óleo de limpeza de máquinas.

### Pendências para o Estrategista
- 🔴 Toque humano: Dalben, Savegnago (WhatsApp), Muffato (ligar)
- 🟡 Fechar Brasfrigo (Salto/SP), acompanhar Selmi, Pague Menos
- 🔧 Netlify 403 — site principal offline (GitHub Pages funciona)
- 📋 Pipeline: rodar `python prospecao.py --dry-run` nas 15 novas empresas