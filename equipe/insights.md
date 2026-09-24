# Insights Diários — Analista de Qualidade

## 2026-09-24 (quinta-feira) — 18:23 (Cron #27 — Melhorador Contínuo)

### Resumo do ciclo

| Métrica | Valor | Δ |
|---------|-------|---|
| **Total de leads (watchdog)** | 199 | — |
| **Ativos** | 150 | — |
| **Bounce (cache)** | 56 | — |
| **Empresas em prospecao.py** | 73 | **+15** ✅ |
| **Pendentes (fila)** | 15 | — |
| **Fila extra** | 184 | — |

### Melhorias implementadas neste ciclo

1. **🎯 Fila fortalecida (+15 empresas)**: adicionadas 15 novas empresas de alto potencial à `prospecao.py` (EMPREAS):
   - **Salto/SP**: Cap-Lab (encapsulados) — na cidade-sede!
   - **Indaiatuba**: Cellera Farma, Farmoterapica, Hero Suplementos (farmacêuticas/encapsulados → óleo vegetal limpeza máquinas)
   - **Sorocaba**: Sorocaps (farmacêutica encapsulados)
   - **Jundiaí**: Hile, WBM (suplementos/encapsulados)
   - **Piracicaba**: Supermercados São Vicente (rede — alta conversão)
   - **Capela do Alto**: Ekobe (nutracêuticos — nicho prioritário)
   - **Campinas/Sorocaba**: Zuhan Refeições, Lollos Refeições (coletivas)
   - **Louveira**: Rede Frango Assado (fritura alto volume)
   - **Campo Limpo Paulista**: Mareia/Conrail (maioneses — vencidos >40% gordura!)
   - **Total**: 73 empresas na lista de prospecção ativa.

2. **📧 Template genérico de apresentação reforçado** (`prospecao.py` linha 305):
   - US$ 8 bi → **US$ 11 bi** (mercado global UCO)
   - Adicionado: **R$ 14,4 mil/ano** (600 L/mês × R$ 2,00/L)
   - Adicionado: Prova social **Madero 55 mil L/mês**
   - Adicionado: **Exportação EUA 1,4 mi t** (2023)
   - Adicionado: **PS com link para calculadora** no rodapé

3. **🌐 Site — Página standalone de calculadora** (`deploy-vercel/calculadora.html`):
   - Calculadora interativa de valor do óleo usado
   - Tabela de referência: 600L/mês → R$ 14,4k/ano até 55kL/mês → R$ 1,2M/ano
   - Indicador de água preservada (1L óleo = 25.000L água contaminada)
   - Formulário de lead com volume + valor estimado (Formspree)
   - Fallback para WhatsApp se formulário falhar
   - Schema WebApplication + SEO metadata
   - Linkável em campanhas de email e redes sociais

4. **🌐 Home page** (`deploy-vercel/index.html`):
   - Nova seção "Quanto vale o seu óleo usado?" após o hero
   - 4 números-chave: US$ 11 bi | 55 mil L/mês | R$ 14,4 mil/ano | Jan/2028
   - CTA duplo: "Abrir calculadora →" e "Simular na página"

### Diagnóstico do sistema

| Métrica | Valor | Meta |
|---------|-------|------|
| Watchdog | ✅ Saudável (exit 0) | — |
| SMTP/IMAP | ✅ OK | — |
| Emails enviados | 156 | — |
| Taxa resposta | 9.6% | >3% ✅ |
| Bounce rate | 22% (34/156) | <15% ❌ |
| Pendentes fila | 15 | >30 ❌ |
| Empresas em lista | 73 (+15) | — |
| Fila extra | 184 | — |

### Observações

- **Watchdog verde direto (exit 0)** — SMTP/IMAP operacionais, sem follow-ups atrasados, sem bounces novos.
- **15 leads pendentes na fila** — abaixo da meta de 30+. Mas com 73 empresas em prospecao.py (+15 hoje), a reposição do cron noturno deve elevar esse número.
- **Bounce rate 22%** — acima da meta de 15%. Continua sendo o calcanhar de Aquiles do sistema. A causa raiz são domínios self-hosted sem MX confiável.
- **Site ganhou calculadora standalone** — linkável em emails e campanhas. Pode gerar leads inbound se divulgada.
- **Nova oportunidade: Cap-Lab em Salto/SP** — laboratório de encapsulados na mesma cidade, usa óleo vegetal para limpeza de máquinas como a Catalent. Contato local é muito mais conversível.

### Pendências para o Estrategista

- 🔴 **Toque humano**: Dalben, Savegnago (WhatsApp 11 96785-9631), Muffato (tel 43 3371-1700)
- 🔴 **Queijos Itupeva (Rafael)** — agendar coleta-teste (lead mais próximo de fechar)
- 🟡 **Covabra** — respondeu 22/09 — priorizar follow-up humano
- 🟡 **Coocerqui** — Carlos Machado respondeu. Verificar lead.
- 🟡 **Selmi** — acompanhar ticket #89532
- 🟡 **Pague Menos** — acompanhar Josiane Marinho
- 🔧 **Bounce rate 22%** — acima da meta. Sugerir revisão de domínios self-hosted.
- 🔧 **Fila em 15** — abaixo da meta 30+. Novas empresas adicionadas para reposição.

---

## 2026-09-24 (quinta-feira) — 18:14 (Cron #26 — Atendente IA)

### Resumo do ciclo

| Métrica | Valor |
|---------|-------|
| **Total de leads (watchdog)** | 199 |
| **Ativos** | 150 |
| **Bounce (cache)** | 56 |
| **Pendentes (fila prospecção)** | 15 |
| **Fila extra** | 184 |
| **Follow-ups processados** | 2 (FP1) |
| **Respostas genuínas** | 0 (3 auto-replies Zendesk Pague Menos) |

### Atividades deste ciclo (18:14)

| Ação | Resultado | Detalhe |
|------|-----------|---------|
| ✅ sync_formspree.py | 0 notificações novas | 56 bounces em cache |
| ✅ corrigir_emails.py | 0 bounces processados | Todos já tentados |
| ⚠️ watchdog.py | exit 1 — 2 atrasados | Resolvido com prospecao_followup.py |
| ✅ prospecao_followup.py | 2 FP1 enviados | Kelco Industrial + Supermercados Sao Judas Tadeu |
| ✅ send_sequence | Sequência processada | Sem novos envios neste ciclo |
| ✅ check-replies | 3 auto-replies | Pague Menos Zendesk surveys — limpo |

### Observações

- **⚠️ Watchdog acusou exit 1** — 2 follow-ups atrasados (FP1 para Kelco e Supermercados Sao Judas Tadeu). Resolvido rodando `prospecao_followup.py`. Sistema retornou ao normal.
- **📬 3 respostas do Pague Menos** — todas pesquisas automáticas de satisfação do Zendesk ("Compartilhar seu feedback conosco"). Nenhuma resposta humana genuína de lead.
- **15 pendentes na fila** — abaixo da meta de 30+. Fila extra com 184 empresas prontas para reposição. Grandes nomes pendentes: Camil Alimentos, Cacau Show, Kopenhagen, Bunge, Embaré, Biolab, BRF Sorocaba, Tauste.
- **🥶 Dia sem respostas genuínas** — último lead humano que respondeu foi 22/09 (Savegnago, Covabra, Coocerqui). Conversão segue dependente de toque humano do Estrategista.