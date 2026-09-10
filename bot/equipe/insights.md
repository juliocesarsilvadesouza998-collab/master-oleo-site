# Insights — Master Óleo · 10/09/2026 (tick 10:38)

## 🚨 ALERTA CRÍTICO MANTIDO — senha de app do Gmail REVOGADA (20º tick consecutivo)
- **Estado**: credencial de `masteroleo.eco@gmail.com` (bot/config.json) **continua rejeitada** — `AUTHENTICATIONFAILED` IMAP / `535 BadCredentials` SMTP, reconfirmado neste tick (10:38 de 10/09, testado com e sem espaços). Revogada entre 11:01 e 11:33 de 09/09.
- **Impacto**: `sync_formspree.py`, `check-replies` e **qualquer envio** **FALHARAM** pelo 20º tick. **Caixa NÃO verificada desde 11:01 de 09/09 (>23h30)** — respostas de Savegnago, Selmi, Grupo IMC, Tauste, Enxuto, Chimar podem estar órfãs na INBOX.
- **AÇÃO (humana)**: nova senha de app em https://myaccount.google.com/apppasswords → `bot/config.json` → `email.senha_app` → rodar `python sync_formspree.py && python bot_oleo.py check-replies`. Verificado em ticks anteriores: **não existe credencial alternativa** em projeto/git/env.

## ⚠️ NOVO neste tick — 4 follow-ups FP1 ATRASADOS (bloqueados pela credencial)
- **Conrail Ind. e Com. de Prod. Alimentícios** (sac@mareia.com.br), **Nutylac Ind. de Alimentos** (contato@nutylac.com.br), **Gomah Com. e Ind. de Sementes** (comercial@gomah.com.br), **Argenzio Ind. de Laticínios** (sac@argenzio.com.br) — IDs 121–124, prospeccao-lote (apresentação 07/09 10:02–10:30). FP1 venceu (dia 3).
- `prospecao_followup.py` **tentou os 4 e falhou no SMTP (535)** — nenhum enviado, nenhum marcado (`fp1_em` vazio). **Retry automático assim que a credencial voltar** — sem ação manual necessária além da senha.
- Primeiro sinal de atraso do pipeline desde a queda da credencial (ticks anteriores: 0 atrasados).

## Resumo do tick (10:38)
- **Pipeline (snapshot 10:38)**: 170 leads · **12 respondidos** · 27 sequência · **104 novos** · 25 bounce (CSV) / 41 cache · 2 encerrados · **ativos: 131** — inalterado (contagem direta no leads.csv).
- **Ação do tick**: rotina — sync ❌ (credencial), corrigir_emails ✅ offline (0 pendentes), watchdog ⚠️ exit 1 (credencial + 4 atrasados), followups ❌ 4×535, send_sequence ❌ (535, nada enviado), check-replies ❌ (caixa cega).
- **Novos leads**: 0. **Bounces novos**: 0. **Correção**: 0 pendentes.
- **Caixa**: **NÃO VERIFICADA** — `replies_pending.json` vazio (última checagem real: 11:01 de 09/09).
- **Fila**: 131/120/28/0 pendentes. **Relatório ESG**: nenhum pedido. **Emails no tick**: 0. **Dashboard**: 145 apresentações / 122 entregues / 23 bounces (16%) / 11 respostas / taxa 7,6%.

## 🏆 Leads quentes (destaque!)
1. **Savegnago (~100 lojas) — #1:** comercial@savegnago.com.br (07/09). **PRAZO É HOJE (10/09) → toque WhatsApp (11) 96785-9631** — sem retorno desde 07/09.
2. **Grupo IMC / Rede Frango Assado — #2:** felix.costa@grupoimc.com.br (07/09). **PRAZO É HOJE (10/09) → toque WhatsApp** — sem retorno desde 07/09.
3. **Pastificio Selmi S/A (id 60) — #3:** canal comercial ABERTO (compras@selmi.com.br, 08/09 10:08). **Prazo: 11/09 (AMANHÃ) → WhatsApp.**
4. **Tauste (156)** — compras CD Valinhos (08/09 14:33); se responder = #1. **Enxuto (155) + Chimar (157)** — aguardando.
5. **Grupo Lanchero** (vencidos >40% + descaracterização), **nicho encapsulados/farmacêuticas** (Arese, Infinity Pharma, Veridi…), **Andorinha Salto (147)** — aguardando retorno.

## Padrão que se confirma
- **SAC corporativo indica o canal comercial → é onde nasce a negociação** (Savegnago → comercial@, Grupo IMC → Felix Costa, Selmi → compras@).
- **Redes de supermercado seguem como alvo de maior potencial** (padaria + rotisserie + açougue geram óleo toda semana).
- **Vetor laticínios/queijarias** (+10 leads 09/09 09:15) — manteiga/creme/vencidos >40% gordura; os 4 FP1 atrasados de hoje são justamente desse vetor (indústrias de laticínios/sementes).
- **Vulnerabilidade exposta**: todo o pipeline de email depende de UMA senha de app — quando cai, sync + check-replies + envio caem juntos e os follow-ups começam a acumular atraso (primeiro caso hoje: 4 FP1). Watchdog com teste SMTP/IMAP alarma no 1º tick da queda — funcionou (20 ticks consecutivos de alerta sem falha de detecção, mas a dependência de ação humana segue sendo o gargalo).

## Próximos passos recomendados
1. **URGENTE**: regenerar senha de app e atualizar `bot/config.json` → rodar sync + check-replies + `prospecao_followup.py` (4 FP1 atrasados serão enviados na sequência; caixa sem verificação desde 11:01 de 09/09 — respostas podem estar paradas).
2. **HOJE 10/09**: toque no WhatsApp de **Savegnago** e **Grupo IMC** (sem retorno desde 07/09) — ação humana independente da credencial. **11/09**: Selmi.
