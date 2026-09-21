# Insights Diários — Analista de Qualidade

## 2026-09-21 (segunda-feira) — 14:20 (Melhorador Contínuo)

### Resumo do dia

**Watchdog:** ⚠️ exit 1 — 2 follow-ups atrasados (UNISO, Sapore) → RESOLVIDOS via prospecao_followup.py

**Dashboard:** 169 leads totais | 122 enviados | 34 bounces | 10 respondidos | 13 novos pendentes

**Fila de prospecção:** 13 pendentes (recuperada de 1! ✅)

### Diagnóstico e melhorias implementadas

| Problema | Ação tomada |
|----------|-------------|
| 🟥 FILA CRÍTICA (1 pendente) | +15 empresas adicionadas ao `bot/prospecao.py` (linha 71): Delta SM, Boa SM, Irmãos Barrera, SM Real, Beira Rio, Infanger, GoodBom, Covabra, Atacado Diniz, Oba Hortifruti, Mania de Churrasco, SupraFoods, Pague Menos, São Judas Tadeu, Natari — todas com MX válido |
| 🟥 leads.csv truncado | Bug: `apresentacao_msgid` faltava no FIELDS do prospecao.py → crash no merge_write_leads. **Corrigido** (FIELDS atualizado). leads.csv **reconstruído** com 169 leads do prospecao.py + fila_extra região |
| 🟡 follow-ups atrasados | UNISO (ouvidoria) e Sapore (suprimentos) — FP1 processado com sucesso |

### 7 novos emails enviados

1. ✅ Kelco Industrial (Indaiatuba) — info@kelcopetcare.com.br
2. ✅ Rosaves Aves (Sorocaba) — contato@rosaves.com.br
3. ✅ Delta Supermercados (Piracicaba) — admgeneral@deltasuper.com.br
4. ✅ Supermercados Real (Tatuí) — contato@supermercadosreal.com.br
5. ✅ Beira Rio Supermercados (Piracicaba) — contato@beirariosm.com.br
6. ✅ Supermercado Infanger (Vinhedo) — contato@infanger.com.br
7. ✅ Supermercados Pague Menos (Campinas) — falecom@supermercadospaguemenos.com.br
8. ✅ Supermercados São Judas Tadeu (Bauru) — faleconosco@supersaojudas.com.br

### Lições aprendidas (CRÍTICO)

1. **BUG GRAVE**: `merge_write_leads` crasha se `FIELDS` não tiver `apresentacao_msgid` — o arquivo é truncado sem dados. Isso é um **bug de design**: escrever em modo "w" antes de validar os dados destrói o arquivo em caso de erro.
2. **prospecao.py** só processa empresas hardcoded na lista EMPRESAS. A `fila_prospeccao_extra.json` (180 empresas) fica inativa. Recomendo refatorar para consumir da fila_extra quando a lista principal acabar.
3. **Sem backup** do leads.csv — uma perda de dados dessas é irrecuperável. Sugiro backup automático.

### Leads QUENTES 🎯

1. **🔥 DALBEN SUPERMERCADOS:** Gerente Luis (luish@supermercadosdalben.com.br) — proposta enviada.
2. **🔥 MUFFATO / MAX ATACADISTA:** SAC orientou ligar (43) 3371-1700.
3. **🔥 SAVEGNAGO (~100 lojas):** Aguardando retorno. Tocar WhatsApp (11) 96785-9631 URGENTE.
4. **🔥 QUEIJOS ITUPEVA (Rafael):** Negociação ativa coleta-teste.
5. **🔥 CABANHA CAMPESTRE 53 (Daniele Santos):** Interesse confirmado! ~600kg/mês.
6. **🔥 BRASFRIGO (Salto/SP):** Empresa na mesma cidade — sac@brasfrigo.com.br.

### Pendências para o Estrategista

- Toque humano: Dalben (ligar), Savegnago (WhatsApp), Muffato (telefone)
- Fechar Brasfrigo (Salto/SP) — empresa na mesma cidade
- Netlify: créditos de build esgotados (403) — site principal fora do ar
- Estudar refatoração do prospecao.py para consumir `fila_prospeccao_extra.json`
- Implementar backup automático do leads.csv