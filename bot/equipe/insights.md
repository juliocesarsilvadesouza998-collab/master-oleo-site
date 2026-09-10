# Insights — Master Óleo · 10/09/2026 (tick 11:31)

## 🚨 ALERTA CRÍTICO MANTIDO — senha de app do Gmail REVOGADA (22º tick consecutivo)

- **Estado**: credencial de `masteroleo.eco@gmail.com` (bot/config.json) **continua rejeitada** — `AUTHENTICATIONFAILED` IMAP / `535 BadCredentials` SMTP, reconfirmado neste tick (11:31 de 10/09, testado com e sem espaços). Revogada entre 11:01 e 11:33 de 09/09.

- **Impacto**: `sync_formspree.py`, `check-replies` e **qualquer envio** **FALHARAM** pelo 22º tick. **Caixa NÃO verificada desde 11:01 de 09/09 (~24h30)** — respostas de Savegnago, Selmi, Grupo IMC, Tauste, Enxuto, Chimar podem estar órfãs na INBOX.

- **AÇÃO (humana)**: nova senha de app em https://myaccount.google.com/apppasswords → `bot/config.json` → `email.senha_app` → rodar `python sync_formspree.py && python bot_oleo.py check-replies`. Reconfirmado neste tick: **não existe credencial alternativa** em projeto/git/env.

## ⚠️ MANTIDO — 6 follow-ups FP1 ATRASADOS (bloqueados pela credencial, 3 dias) + 1 recém-vencido

- **Conrail Ind. e Com. de Prod. Alimentícios** (sac@mareia.com.br, id 121), **Nutylac Ind. de Alimentos** (contato@nutylac.com.br, 122), **Gomah Com. e Ind. de Sementes** (comercial@gomah.com.br, 123), **Argenzio Ind. de Laticínios** (sac@argenzio.com.br, 124), **Supermercados São Roque** (sac@smsr.com.br, 130), **Rede Confiança Supermercados** (sac@confianca.com.br, 131) — prospeccao-lote (apresentação 07/09 10:02–11:05). FP1 venceu (dia 3).

- `prospecao_followup.py` **tentou os 6 novamente e falhou no SMTP (535)** — nenhum enviado, nenhum marcado (`fp1_em` vazio). **Retry automático assim que a credencial voltar** — sem ação manual necessária além da senha.

- 🆕 **Tenda Atacado** (dpo@tendaatacado.com.br, id 133) cruzou o limiar de FP1 às **11:32** — 2 minutos após esta rodada do followup (apresentação 07/09 11:32). Vira o **7º atrasado** na próxima rodada.

- ⏳ **Atenção**: se a senha não for regenerada, o **FP2 desses leads vence em ~3 dias** (13/09, dia 6) — o atraso vai dobrar.

## Resumo do tick (11:31)

- **Pipeline (snapshot 11:31)**: 170 leads · **12 respondidos** · 27 sequência · **104 novos** · 25 bounce (CSV) / 41 cache · 2 encerrados · **ativos: 131** — **inalterado** (contagem direta no leads.csv).

- **Ação do tick**: rotina — sync ❌ (credencial, 22º), corrigir_emails ✅ offline (0 pendentes), watchdog ⚠️ exit 1 (credencial + 6 atrasados), followups ❌ 6×535, send_sequence ❌ (535, nada enviado), check-replies ❌ (caixa cega), enviar_lote --status ✅ (0 pendentes).

- **Novos leads**: 0. **Bounces novos**: 0. **Correção**: 0 pendentes.

- **Caixa**: **NÃO VERIFICADA** — `replies_pending.json` vazio (última checagem real: 11:01 de 09/09).

- **Fila**: 131/120/28/0 pendentes. **Relatório ESG**: nenhum pedido. **Emails no tick**: 0. **Dashboard**: 145 apresentações / 122 entregues / 23 bounces (16%) / 11 respostas / taxa 7,6%.

## 🏆 Leads quentes (destaque!)

1. **Savegnago (~100 lojas) — #1:** comercial@savegnago.com.br (07/09). **PRAZO VENCEU HOJE (10/09) → toque WhatsApp (11) 96785-9631 URGENTE** — sem retorno desde 07/09.
2. **Grupo IMC / Rede Frango Assado — #2:** felix.costa@grupoimc.com.br (07/09). **PRAZO VENCEU HOJE (10/09) → toque WhatsApp** — sem retorno desde 07/09.
3. **Pastificio Selmi S/A (id 60) — #3:** canal comercial ABERTO (compras@selmi.com.br, 08/09 10:08). **Prazo: 11/09 (AMANHÃ) → WhatsApp.**
4. **Tauste (156)** — compras CD Valinhos (08/09 14:33); se responder = #1. **Enxuto (155) + Chimar (157)** — aguardando.
5. **Grupo Lanchero** (vencidos >40% + descaracterização), **nicho encapsulados/farmacêuticas** (Arese, Infinity Pharma, Veridi…), **Andorinha Salto (147)** — aguardando retorno.

## Padrão que se confirma

- **SAC corporativo indica o canal comercial → é onde nasce a negociação** (Savegnago → comercial@, Grupo IMC → Felix Costa, Selmi → compras@).
- **Redes de supermercado seguem como alvo de maior potencial** (padaria + rotisserie + açougue geram óleo toda semana) — os 6 FP1 atrasados incluem 2 redes (São Roque, Rede Confiança).
- **Vetor laticínios/queijarias** (+10 leads 09/09 09:15) — manteiga/creme/vencidos >40% gordura; Conrail, Nutylac, Gomah e Argenzio (4 dos 6 FP1 atrasados) são desse vetor.
- **Vulnerabilidade exposta (22 ticks)**: todo o pipeline depende de UMA senha de app — quando cai, sync + check-replies + envio caem juntos e os follow-ups acumulam atraso (6 FP1 com 3 dias + 1 vencendo; FP2 próximo). O watchdog com teste SMTP/IMAP alarma desde o 1º tick da queda — detecção funcionando, mas a dependência de ação humana segue sendo o gargalo.

## Próximos passos recomendados

1. **URGENTE**: regenerar senha de app e atualizar `bot/config.json` → rodar sync + check-replies + `prospecao_followup.py` (6-7 FP1 atrasados serão enviados na sequência; caixa sem verificação desde 11:01 de 09/09 — respostas podem estar paradas).
2. **HOJE 10/09**: toque no WhatsApp de **Savegnago** e **Grupo IMC** (sem retorno desde 07/09) — ação humana independente da credencial. **11/09**: Selmi.
