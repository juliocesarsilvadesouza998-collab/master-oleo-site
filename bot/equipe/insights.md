# Insights — Master Óleo · 07/09/2026 (tick 16:01)

## Resumo do tick (16:01)
- **Pipeline**: 140 leads (104 ativos, 38 bounces) · 11 respondidos · 14 em sequência · 90 novos — **inalterado desde o tick 15:31**.
- **Caixa**: `check-replies` = 0 pendentes (`replies_pending.json` = `[]`); `scan_inbox` (contingência) = 0 mensagens não lidas/recentes na INBOX (janela 7 dias); 33 msgids enviados indexados. **Caixa limpa confirmada em dobro.**
- **Watchdog**: saudável (exit 0) — 140 leads / 104 ativos / 38 bounces, sem follow-ups atrasados, bounces sem correção ou leads parados.
- **Follow-ups**: 0 atrasados. **Sequência**: processada, nada a enviar. **Sync Formspree**: 0 novas notificações. **Correção de emails**: 0 novas (38 bounces do cache já todos tentados).
- **Fila de prospecção** (`enviar_lote.py --status`): 115 empresas / 104 já contatados / 27 bounce / **0 pendentes**.
- **Nenhum email enviado neste tick** — dia de aguardar retornos dos canais comerciais abertos (Savegnago e Grupo IMC).

## 🏆 Leads quentes (destaque!)
1. **Savegnago Supermercados (~100 lojas)** — canal comercial oficial ABERTO: apresentação enviada 10:32 para `comercial@savegnago.com.br`. **Prazo: toque no WhatsApp (11) 96785-9631 em 10/09 se não houver retorno.**
2. **Frango Assado / Grupo IMC** — canal comercial ABERTO: apresentação enviada ~12:11 a `felix.costa@grupoimc.com.br` (SAC indicou o contato). Grupo IMC = food service gigante (Frango Assado, Viena, Pizza Hut BR) — contrato de rede se fechar. **Prazo: toque no WhatsApp em 10/09.**
3. **Andorinha Hiper Center (id 147)** — loja na própria **Salto**; se responder: pedir volume mensal + tipo e priorizar coleta-teste na unidade de Salto.
4. **Paulistão Atacadista (id 149)** — bandeira do Grupo Savegnago; **se comercial@savegnago responder, pausar envio ao Paulistão** (evitar insistência duplicada no mesmo grupo).
5. **Rede Bom Lugar / Tenda Atacado / Roldão Atacadista** — apresentações enviadas 11:31, aguardando retorno. **Rede Boa / GoodBom / Sumerbol / Bagley(Arcor)** — propostas em análise (aguardando follow-up).

## Padrão que se confirma
- SAC corporativo responde com **ack automático e fecha ticket**; canal **comercial/indicado** é onde nasce negociação — Savegnago (Central de Relacionamento indicou comercial@) e Grupo IMC (SAC indicou Felix Costa).
- Respostas de rede grande seguem o roteiro: **"envie a apresentação para X"** → enviar apresentação + perguntar **volume mensal (litros/kg)** + oferecer **coleta-teste** + WhatsApp.
- Tick 100% rotina, sem eventos novos desde 15:31 — o filtro de DSN/bounce no check_replies (implementado no tick 15:01) segue funcionando: 0 falsos positivos.

## Próximos passos recomendados
1. **10/09**: toque leve no WhatsApp (11) 96785-9631 para Savegnago e Grupo IMC se não houver retorno (cronograma de fechamento da persona).
2. Rodar `prospecao_followup.py` nos próximos ticks para leads de resposta média (Rede Boa, GoodBom, Sumerbol).
3. Se responderem: pedir volume + tipo de material, oferecer coleta-teste e relatório ESG (PDF) para fechar indústrias/redes.
4. Fila de prospecção **0 pendentes** — gargalo do Prospector segue (manter 5–8 novos/dia com MX validado).
