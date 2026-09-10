# Insights — Master Óleo · 10/09/2026 (tick 10:00)

## 🚨 ALERTA CRÍTICO MANTIDO — senha de app do Gmail REVOGADA (19º tick consecutivo)
- **Estado**: credencial de `masteroleo.eco@gmail.com` (bot/config.json) **continua rejeitada** — `AUTHENTICATIONFAILED` IMAP / `535 BadCredentials` SMTP, reconfirmado neste tick (09:54 de 10/09, testado com e sem espaços). Revogada entre 11:01 e 11:33 de 09/09.
- **Verificação extra deste tick**: busquei credencial alternativa no projeto, histórico git (só placeholder) e variáveis de ambiente — **não existe backup**. A única saída é ação humana.
- **Impacto**: `sync_formspree.py` e `check-replies` **FALHARAM** pelo 19º tick. **Caixa NÃO verificada desde 11:01 de 09/09 (>23h)** — risco de leads sem atendimento (Selmi, Savegnago, Grupo IMC, Tauste, Enxuto, Chimar em maturação).
- **AÇÃO (humana)**: nova senha de app em https://myaccount.google.com/apppasswords → `bot/config.json` → `email.senha_app` → rodar `python sync_formspree.py && python bot_oleo.py check-replies`.
- **Offline verde**: fila 0 pendentes (131/120/28), 0 follow-ups atrasados, 0 bounces novos, correção de bounces nada pendente.

## Resumo do tick (10:00)
- **Pipeline (snapshot 10:00)**: 170 leads · **12 respondidos** · 27 sequência · **104 novos** · 25 bounce (CSV) / 41 cache · 2 encerrados · **ativos: 131** — inalterado (contagem direta; caixa sem verificação desde 11:01 de 09/09).
- **Ação do tick**: rotina offline — follow-ups 0 devidos, sequência nada a enviar (confirmei no código: `smtp_send` propaga erro, sem risco de envio falso/marcação indevida).
- **Novos leads**: 0. **Bounces novos**: 0. **Correção**: 0 pendentes.
- **Caixa**: **NÃO VERIFICADA** — `replies_pending.json` vazio (última checagem real: 11:01 de 09/09).
- **Watchdog**: ⚠️ exit 1 (somente credencial — SMTP 535 + IMAP AUTHENTICATIONFAILED). **Fila**: 131/120/28/0 pendentes. **Relatório ESG**: nenhum pedido. **Emails no tick**: 0. **Dashboard**: 145 apresentações / 122 entregues / 23 bounces (16%) / 11 respostas / taxa 7,6%.

## 🏆 Leads quentes (destaque!)
1. **Savegnago (~100 lojas) — #1:** comercial@savegnago.com.br (07/09). **PRAZO É HOJE (10/09) → toque WhatsApp (11) 96785-9631** — sem retorno desde 07/09.
2. **Grupo IMC / Rede Frango Assado — #2:** felix.costa@grupoimc.com.br (07/09). **PRAZO É HOJE (10/09) → toque WhatsApp** — sem retorno desde 07/09.
3. **Pastificio Selmi S/A (id 60) — #3:** canal comercial ABERTO (compras@selmi.com.br, 08/09 10:08). **Prazo: 11/09 (AMANHÃ) → WhatsApp.**
4. **Tauste (156)** — compras CD Valinhos (08/09 14:33); se responder = #1. **Enxuto (155) + Chimar (157)** — aguardando.
5. **Grupo Lanchero** (vencidos >40% + descaracterização), **nicho encapsulados/farmacêuticas** (Arese, Infinity Pharma, Veridi…), **Andorinha Salto (147)** — aguardando retorno.

## Padrão que se confirma
- **SAC corporativo indica o canal comercial → é onde nasce a negociação** (Savegnago → comercial@, Grupo IMC → Felix Costa, Selmi → compras@).
- **Redes de supermercado seguem como alvo de maior potencial** (padaria + rotisserie + açougue geram óleo toda semana).
- **Vetor laticínios/queijarias** (+10 leads 09/09 09:15) — manteiga/creme/vencidos >40% gordura; monitorar replies.
- **Vulnerabilidade exposta**: todo o pipeline de email depende de UMA senha de app — quando cai, sync + check-replies + envio caem juntos. Watchdog com teste SMTP/IMAP alarma no 1º tick da queda — funcionou (19 ticks consecutivos de alerta sem falha de detecção, mas a dependência de ação humana segue sendo o gargalo).

## Próximos passos recomendados
1. **URGENTE**: regenerar senha de app e atualizar `bot/config.json` → rodar sync + check-replies (há >23h de caixa não verificada desde 11:01 de 09/09 — a cada tick sem credencial, respostas de Savegnago/Tauste/Enxuto/Chimar podem estar paradas na caixa).
2. **HOJE 10/09**: toque no WhatsApp de **Savegnago** e **Grupo IMC** (sem retorno desde 07/09) — ação humana independente da credencial. **11/09**: Selmi.
