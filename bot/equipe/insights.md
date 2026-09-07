# Insights — Master Óleo · 07/09/2026 (tick 14:01)

## Resumo do tick (14:01)
- **Pipeline**: 135 leads (100 ativos, 37 bounces) · 11 respondidos · 14 em sequência · 86 novos — **inalterado desde o tick 13:31**.
- **Caixa**: 0 respostas pendentes (`replies_pending.json` vazio). `check-replies` sem novidades; **contingência `scan_inbox.py` confirmou: 0 mensagens não lidas/recentes na INBOX (7 dias)** — nenhuma resposta perdida (aviso benigno de SELECT na pasta Sent, já documentado).
- **Watchdog**: saudável (exit 0). Follow-ups: 0 atrasados. Sequência: processada, nada a enviar. Sync Formspree: 0 novas notificações. Correção de emails: 0 novas.
- **Fila de prospecção** (`enviar_lote.py --status`): 110 empresas / 99 já contatados / 26 bounce / **0 pendentes**.
- **Nenhum email enviado neste tick** — dia de aguardar retornos dos canais comerciais abertos (Savegnago e Grupo IMC).

## 🏆 Leads quentes (destaque!)
1. **Savegnago Supermercados (~100 lojas)** — canal comercial oficial ABERTO: apresentação enviada 10:35 para `comercial@savegnago.com.br`. **Prazo: toque no WhatsApp (11) 96785-9631 em 10/09 se não houver retorno.**
2. **Frango Assado / Grupo IMC** — canal comercial ABERTO: apresentação enviada ~12:05 a `felix.costa@grupoimc.com.br` (SAC indicou o contato). Grupo IMC = food service gigante (Frango Assado, Viena, Pizza Hut BR) — contrato de rede se fechar. **Prazo: toque no WhatsApp em 10/09.**
3. **Rede Boa / GoodBom / Sumerbol / Bagley(Arcor)** — propostas em análise nos departamentos de compras (aguardando follow-up).

## Padrão que se confirma
- SAC corporativo responde com **ack automático e fecha ticket** (Selmi/Zendesk); canal **comercial/indicado** é onde nasce negociação — Savegnago (Central de Relacionamento indicou comercial@) e Grupo IMC (SAC indicou Felix Costa).
- Respostas de rede grande seguem o roteiro: **"envie a apresentação para X"** → enviar apresentação + perguntar **volume mensal (litros/kg)** + oferecer **coleta-teste** + WhatsApp.
- Vigilância da caixa em dobro (filtro automático + scan_inbox manual) segue confirmando caixa limpa.

## Próximos passos recomendados
1. **10/09**: toque leve no WhatsApp (11) 96785-9631 para Savegnago e Grupo IMC se não houver retorno (cronograma de fechamento da persona).
2. Rodar `prospecao_followup.py` nos próximos ticks para leads de resposta média (Rede Boa, GoodBom, Sumerbol).
3. Se responderem: pedir volume + tipo de material, oferecer coleta-teste e relatório ESG (PDF) para fechar indústrias/redes.
