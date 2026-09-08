# Insights — Master Óleo · 08/09/2026 (tick 10:08)

## Resumo do tick (10:08)
- **Pipeline**: 140 leads (104 ativos, 38 bounces) · **12 respondidos (+1)** · 14 em sequência · 89 novos · 23 bounce · 2 encerrados.
- **Caixa**: `check-replies` encontrou **1 resposta NOVA** — Pastificio Selmi via Zendesk (ticket #88925, Cristina Magalhães/SAC): indicou **compras@selmi.com.br** como canal para tratar a compra do óleo. **Atendida no mesmo tick.**
- **Watchdog**: saudável (exit 0) — sem follow-ups atrasados, bounces sem correção ou leads parados.
- **Follow-ups**: 0 atrasados. **Sequência**: processada, nada a enviar. **Sync Formspree**: 0 novas notificações. **Correção de emails**: 0 novas (38 bounces do cache já todos tentados).
- **Fila de prospecção** (`enviar_lote.py --status`): 115 empresas / 104 já contatados / 27 bounce / **0 pendentes**.
- **Emails enviados neste tick: 2** — (1) cortesia na thread Zendesk agradecendo à Cristina (ticket encerrado de nossa parte); (2) **proposta completa para compras@selmi.com.br** com a indicação do SAC como referência (faixa R$ 1,00–2,50/L, PIX na coleta, certificado de destinação, CTA volume + tipo + WhatsApp). Lead 60 marcado `respondido` (10:08:38).
- **Relatório ESG**: nenhum pedido neste tick — sem geração de PDF.

## 🏆 Leads quentes (destaque!)
1. **Pastificio Selmi S/A (id 60) — NOVO #1:** canal comercial ABERTO — o SAC (Cristina, Zendesk #88925) indicou **compras@selmi.com.br** e a proposta completa foi enviada 08/09 10:08. Indústria de massas de grande porte = óleo de fritura + possível resíduo >40% gordura. **Prazo: sem retorno até 11/09 → toque leve no WhatsApp (11) 96785-9631.**
2. **Savegnago Supermercados (~100 lojas)** — canal comercial oficial ABERTO (comercial@savegnago.com.br, apresentação 07/09). **Prazo: toque no WhatsApp em 10/09 se não houver retorno.**
3. **Frango Assado / Grupo IMC** — canal comercial ABERTO (felix.costa@grupoimc.com.br, apresentação 07/09 ~12:05). **Prazo: toque no WhatsApp em 10/09.**
4. **Andorinha Hiper Center (id 147)** — loja na própria **Salto**; se responder: pedir volume mensal + tipo e priorizar coleta-teste na unidade de Salto.
5. **Paulistão Atacadista (id 149)** — bandeira do Grupo Savegnago; se comercial@savegnago responder, pausar envio ao Paulistão (evitar insistência duplicada no mesmo grupo).
6. **Rede Bom Lugar / Tenda Atacado / Roldão Atacadista / Dalben / Amigão** — apresentações 07/09, aguardando retorno. **Rede Boa / GoodBom / Sumerbol / Bagley(Arcor)** — propostas em análise.

## Padrão que se confirma (3ª vez na semana)
- **SAC corporativo fecha ticket e INDICA o canal comercial → é lá que nasce a negociação.** Savegnago (Central de Relacionamento → comercial@), Grupo IMC (SAC → Felix Costa) e agora **Selmi (SAC → compras@)**. O roteiro é consistente: agradecer no SAC + enviar proposta completa no canal indicado.
- Respostas de grande gerador seguem o roteiro: **"envie a apresentação/proposta para X"** → enviar proposta + perguntar **volume mensal (litros/kg)** + oferecer **coleta-teste** + WhatsApp.
- Fixes de 07/09 seguem funcionando: filtro de DSN/bounce (0 falsos positivos) e correlação de plataforma + `reply --lead-id` (marcou o lead 60 corretamente na resposta Zendesk).

## Próximos passos recomendados
1. **10/09**: toque leve no WhatsApp (11) 96785-9631 para Savegnago e Grupo IMC se não houver retorno (cronograma de fechamento da persona).
2. **11/09**: toque para Selmi se compras@selmi.com.br não responder.
3. Se responderem: pedir volume + tipo de material, oferecer coleta-teste e relatório ESG (PDF) para fechar indústrias/redes.
4. Fila de prospecção **0 pendentes** — gargalo do Prospector segue (manter 5–8 novos/dia com MX validado).
