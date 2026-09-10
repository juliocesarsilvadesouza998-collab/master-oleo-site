# Insights — Master Óleo · 10/09/2026 (tick 15:31)

## 🚨 ALERTA CRÍTICO MANTIDO — senha de app do Gmail REVOGADA (29º tick consecutivo)

- **Estado**: credencial de `masteroleo.eco@gmail.com` (bot/config.json) **continua rejeitada** — `AUTHENTICATIONFAILED` IMAP / `535 BadCredentials` SMTP, reconfirmado neste tick (15:31 de 10/09, testado com e sem espaços). Revogada entre 11:01 e 11:33 de 09/09.

- **Impacto**: `sync_formspree.py`, `check-replies` e **qualquer envio** **FALHARAM** pelo 29º tick. **Caixa NÃO verificada desde 11:01 de 09/09 (~28h30)** — respostas de Savegnago, Selmi, Grupo IMC, Tauste, Enxuto, Chimar podem estar órfãs na INBOX.

- **AÇÃO (humana)**: nova senha de app em https://myaccount.google.com/apppasswords → `bot/config.json` → `email.senha_app` → rodar `python sync_formspree.py && python bot_oleo.py check-replies && python prospecao_followup.py`. Reconfirmado neste tick: **não existe credencial alternativa** em projeto/git/env.

## ⚠️ 11 follow-ups FP1 ATRASADOS — todos tentados e bloqueados (535)

- `prospecao_followup.py` **tentou os 11 e falhou no SMTP (535)** — nenhum enviado, nenhum marcado (`fp1_em` vazio confirmado no CSV). **Retry automático assim que a credencial voltar** — sem ação manual além da senha.
- Lista completa (há 3 dias): **Conrail** (sac@mareia), **Nutylac**, **Gomah**, **Argenzio** (vetor laticínios), **Supermercados São Roque**, **Rede Confiança**, **Tenda Atacado** (ids 121-124/130/131/133) + **Andorinha Hiper Center** (id 147 — loja em SALTO), **Supermercados Dalben** (148), **Paulistão Atacadista** (149 — bandeira do **Grupo Savegnago**!), **Amigão Supermercados** (151).
- **7 dos 11 são supermercados/atacarejo** — o nicho que mais converte.
- ⏳ **Próximos vencimentos**: amanhã 11/09 vencem FP1 de **Sorocaba Frios, Mega Ingredientes e Grupo Lanchero** (ap 08/09 10:20); depois Enxuto/Tauste/Chimar (08/09 14:33). Se a senha não voltar, o **FP2 dos 11 vence ~13/09 (dia 6)** — o atraso dobra.

## Resumo do tick (15:31)

- **Pipeline (snapshot 15:31)**: 170 leads · **12 respondidos** · 27 sequência · **104 novos** · 25 bounce (CSV) / 41 cache · 2 encerrados · **ativos: 131** — **inalterado** (contagem direta no leads.csv).

- **Ação do tick**: rotina — sync ❌ (credencial, 29º), corrigir_emails ✅ offline (0 pendentes), watchdog ⚠️ exit 1 (credencial + **11 atrasados**), followups ❌ 11×535 (nenhum marcado), send_sequence ❌ (535 no login, sem corromper estado), check-replies ❌ (caixa cega), enviar_lote --status ✅ (**3 pendentes retidos**: Mambo, BRF Itu, Piraquê).

- **Novos leads**: 0. **Bounces novos**: 0. **Correção**: 0 pendentes.

- **Caixa**: **NÃO VERIFICADA** — `replies_pending.json` vazio (última checagem real: 11:01 de 09/09).

- **Fila**: 134 empresas / 120 contatados / 28 bounce / **3 pendentes** (Mambo, BRF, Piraquê — retidos). **Relatório ESG**: nenhum pedido detectável (caixa inacessível). **Emails no tick**: 0. **Dashboard**: 145 apresentações / 122 entregues / 23 bounces (16%) / 11 respostas / taxa 7,6% / 111 aguardando / 24 inbound.

## 🏆 Leads quentes (destaque!)

1. **Savegnago (~100 lojas) — #1:** comercial@savegnago.com.br (07/09). **PRAZO DO TOQUE WHATSAPP VENCEU HOJE (10/09)** — sem retorno desde 07/09; WhatsApp (11) 96785-9631. Obs.: o **Paulistão Atacadista (id 149)** é bandeira do mesmo grupo — se o comercial@ responder, pausar insistência no Paulistão.
2. **Grupo IMC / Rede Frango Assado — #2:** felix.costa@grupoimc.com.br (07/09). **TOQUE WHATSAPP TAMBÉM VENCIDO HOJE (10/09)** — sem retorno desde 07/09.
3. **Pastificio Selmi S/A (id 60) — #3:** canal comercial ABERTO (compras@selmi.com.br, 08/09 10:08). **Prazo: 11/09 (AMANHÃ) → WhatsApp.**
4. **Andorinha Hiper Center (id 147) — ALTA:** sugestoes@andorinhahiper.com.br — loja na própria **Salto** + Itu; FP1 atrasado (07/09); maior potencial geográfico do momento.
5. **Tauste (156)** — compras CD Valinhos (08/09 14:33); se responder = #1. **Enxuto (155) + Chimar (157)** — aguardando.
6. **Grupo Lanchero** (vencidos >40% + descaracterização), **nicho encapsulados/farmacêuticas** (Arese, Infinity Pharma, Veridi…), **Rede Boa / GoodBom / Sumerbol / Bagley** — aguardando retorno.

## Padrão que se confirma

- **SAC corporativo indica o canal comercial → é onde nasce a negociação** (Savegnago → comercial@, Grupo IMC → Felix Costa, Selmi → compras@).
- **Redes de supermercado seguem como alvo de maior potencial** — dos 11 FP1 atrasados, **7 são supermercados/atacarejo** (São Roque, Rede Confiança, Tenda, Andorinha, Dalben, Paulistão, Amigão). Padaria + rotisserie + açougue geram óleo toda semana em cada loja.
- **Vetor laticínios/queijarias** — manteiga/creme/vencidos >40% gordura; Conrail, Nutylac, Gomah e Argenzio (4 dos 11) são desse vetor.
- **Vulnerabilidade exposta (29 ticks)**: todo o pipeline depende de UMA senha de app — quando cai, sync + check-replies + envio caem juntos e os follow-ups acumulam atraso (11 FP1 com 3 dias; FP2 próximo). O watchdog com teste SMTP/IMAP alarma desde o 1º tick da queda — detecção funcionando, mas a dependência de ação humana segue sendo o gargalo.

## Próximos passos recomendados

1. **URGENTE**: regenerar senha de app e atualizar `bot/config.json` → rodar sync + check-replies + `prospecao_followup.py` (**11 FP1 atrasados** serão enviados na sequência; caixa sem verificação desde 11:01 de 09/09 — respostas podem estar paradas; fila libera os 3 novos: Mambo, BRF, Piraquê).
2. **HOJE 10/09 (já vencido)**: toque no WhatsApp de **Savegnago** e **Grupo IMC** (sem retorno desde 07/09) — ação humana independente da credencial. **11/09**: Selmi + vencem FP1 de Sorocaba Frios/Mega Ingredientes/Lanchero.
