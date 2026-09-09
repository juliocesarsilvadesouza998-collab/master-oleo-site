# Insights — Master Óleo · 09/09/2026 (tick 16:31)

## 🚨 ALERTA CRÍTICO MANTIDO — senha de app do Gmail REVOGADA (11º tick consecutivo)
- **Estado**: credencial de `masteroleo.eco@gmail.com` (bot/config.json) **continua rejeitada** — `AUTHENTICATIONFAILED` IMAP / `535 BadCredentials` SMTP, reconfirmado neste tick (16:31, testado com e sem espaços). Revogada entre 11:01 e 11:33 de 09/09.
- **Impacto**: `sync_formspree.py` e `check-replies` **FALHARAM** pelo 11º tick. **Caixa NÃO verificada desde 11:01** (>5h30) — risco de leads sem atendimento (Selmi, Savegnago, Grupo IMC, Tauste, Enxuto, Chimar em maturação).
- **AÇÃO (humana)**: nova senha de app em https://myaccount.google.com/apppasswords → `bot/config.json` → `email.senha_app` → rodar `python sync_formspree.py && python bot_oleo.py check-replies`.
- **Offline verde**: fila 0 pendentes (131/120/28), watchdog `--skip-email` exit 0, 0 follow-ups atrasados, 0 bounces novos, correção de bounces nada pendente.

## Resumo do tick (16:31)
- **Pipeline (snapshot 16:31)**: 170 leads · **12 respondidos** · 27 sequência · **104 novos** · 25 bounce (CSV) / 41 cache · 2 encerrados · **ativos: 131** — inalterado (contagem direta; caixa sem verificação desde 11:01).
- **Ação do tick**: rotina offline — nada a enviar (fluxo de email bloqueado pela credencial).
- **Novos leads**: 0. **Bounces novos**: 0. **Correção**: 0 pendentes.
- **Caixa**: **NÃO VERIFICADA** — `replies_pending.json` vazio (última checagem real: 11:01).
- **Watchdog**: ⚠️ exit 1 (somente credencial — SMTP 535 + IMAP AUTHENTICATIONFAILED; `--skip-email` exit 0). **Fila**: 131/120/28/0 pendentes. **Relatório ESG**: nenhum pedido. **Emails no tick**: 0. **Dashboard**: 145 apresentações / 122 entregues / 23 bounces (16%) / 11 respostas / taxa 7,6%.

## 🏆 Leads quentes (destaque!)
1. **Pastificio Selmi S/A (id 60) — #1:** canal comercial ABERTO (compras@selmi.com.br, 08/09 10:08). **Prazo: 11/09 → WhatsApp (11) 96785-9631.**
2. **Savegnago (~100 lojas) — #2:** comercial@savegnago.com.br (07/09). **Prazo: 10/09 (AMANHÃ) → toque WhatsApp.**
3. **Frango Assado / Grupo IMC — #3:** felix.costa@grupoimc.com.br (07/09). **Prazo: 10/09 (AMANHÃ) → toque WhatsApp.**
4. **Tauste (156)** — compras CD Valinhos (08/09 14:33); se responder = #1. **Enxuto (155) + Chimar (157)** — aguardando.
5. **Grupo Lanchero** (vencidos >40% + descaracterização), **nicho encapsulados/farmacêuticas** (Arese, Infinity Pharma, Veridi…), **Andorinha Salto (147)** — aguardando retorno.

## Padrão que se confirma
- **SAC corporativo indica o canal comercial → é onde nasce a negociação** (Savegnago → comercial@, Grupo IMC → Felix Costa, Selmi → compras@).
- **Redes de supermercado seguem como alvo de maior potencial** (padaria + rotisserie + açougue geram óleo toda semana).
- **Vetor laticínios/queijarias** (+10 leads 09/09 09:15) — manteiga/creme/vencidos >40% gordura; monitorar replies.
- **Vulnerabilidade exposta**: todo o pipeline de email depende de UMA senha de app — quando cai, sync + check-replies + envio caem juntos. Watchdog com teste SMTP/IMAP (tick 14:10) já alarma no 1º tick da queda — funcionou (11 ticks consecutivos de alerta sem falha de detecção).

## Próximos passos recomendados
1. **URGENTE**: regenerar senha de app e atualizar `bot/config.json` → rodar sync + check-replies (há >5h30 de caixa não verificada desde 11:01).
2. **AMANHÃ 10/09**: toque no WhatsApp de **Savegnago** e **Grupo IMC** (sem retorno desde 07/09) — ação humana independente da credencial. **11/09**: Selmi.
