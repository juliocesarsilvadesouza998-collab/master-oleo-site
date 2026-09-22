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

### Pendências para o Estrategista

- **🔴 Alta prioridade:** Toque humano Dalben (ligar Luis), Savegnago (WhatsApp), Muffato (ligar 43 3371-1700)
- **🟡 Média prioridade:** Fechar Brasfrigo (Salto/SP), acompanhar Selmi ticket #89532, acompanhar Pague Menos
- **🔧 Infra:** Netlify créditos esgotados (403) — site principal offline; versão nova no GitHub Pages
- **📋 Manutenção:** Repor fila de prospecção com +15-20 empresas (pendentes = 10, abaixo do ideal 30+)
- **📊 Qualidade:** Revisar lista de 55 bounces para eventual limpeza/migração de dados