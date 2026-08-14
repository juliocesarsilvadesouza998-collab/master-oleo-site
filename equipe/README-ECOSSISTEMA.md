# 🌿 Ecossistema Master Óleo — IA Auto-corretiva

Este é o **sistema de IAs que trabalham juntas** para prospectar, enviar e
melhorar continuamente a operação da Master Óleo (compra de óleo de cozinha
usado e gordura vegetal usada — Salto/SP e região).

## 🧠 Membros da equipe

| Papel | Job | Quando | Responsabilidade |
|---|---|---|---|
| **Atendente** | `497505018e92` | seg–sáb 8h–19h (30/30min) | Envia sequência, responde leads, conversa livre |
| **Prospector** | `prospector-masteroleo` | seg–sáb 09:00 | Busca novas empresas grandes na web, valida email (MX), adiciona à fila, envia lote |
| **Analista de Qualidade** | `analista-masteroleo` | seg–sáb 19:30 | Revisa os envios do dia: bounces, respostas, erros; corrige leads.csv e bounces.json |
| **Estrategista** | `estrategista-masteroleo` | domingo 08:00 | Lê tudo, pesquisa mercado, define metas da semana, sugere melhorias e corrige templates/persona |

## 🔄 Como elas se ajudam (correção mútua)

1. **Prospector** descobre empresas → adiciona ao `prospecao.py`/fila → **Atendente** usa a fila para enviar.
2. **Atendente** envia emails → **Analista** verifica bounces e respostas → marca leads como `bounce`/`respondido`.
3. **Analista** encontra padrão de erro → registra em `equipe/insights.md` → **Estrategista** corrige o template/persona.
4. **Estrategista** define metas semanais → **Prospector** foca nas cidades/segmentos definidos.
5. Qualquer erro detectado por um membro é **registrado no arquivo de memória do ecossistema** (`equipe/ecossistema.json`) para os outros membros aprenderem.

## 📁 Arquivos compartilhados

- `bot/leads.csv` — todos os leads (fonte: formspree | prospeccao | prospeccao-lote)
- `bot/bounces.json` — cache de emails inválidos (nunca reenviar)
- `bot/enviar_lote.py` — envia lote respeitando limite diário (`--max`)
- `equipe/ecossistema.json` — memória compartilhada: metas, aprendizados, histórico
- `equipe/insights.md` — aprendizados de qualidade (bounces, respostas, melhorias)
- `equipe/relatorios/` — relatórios diários de cada membro

## 🎯 Metas atuais

- Enviar **50 emails de prospecção** a partir de 2026-08-14
- Foco: empresas grandes (porte Arcor) em Campinas, Indaiatuba, Itu, Sorocaba,
  Jundiaí, Louveira, Valinhos, Piracicaba e Salto/SP
- Regra de reputação: **máx 15 emails/dia** (não queimar o Gmail)
- Prospecção semanal contínua para manter a fila ≥ 30 pendentes

## 💼 Fluxo de fechamento (outbound — NÓS contatamos)

1. **Apresentação** (dia 0): email profissional deixa claro que a Master Óleo
   está contatando a empresa para COMPRAR o óleo/gordura usados — nunca
   "obrigado pelo seu interesse" (isso é para quem nos procurou).
2. **Follow-up 1** (dia 3): reforça a proposta de compra, pede litros/kg por
   mês + tipo de material.
3. **Follow-up 2** (dia 6): destaca que para >500L/mês a logística é 100% por
   nossa conta, pede conversa rápida no WhatsApp.
4. **Follow-up 3** (dia 10): último contato, porta aberta, encerra o ciclo.
5. **Resposta do lead** → Atendente IA assume a conversa (negociação de valor
   conforme quantidade/qualidade) e fecha pelo WhatsApp.

Scripts: `bot/enviar_lote.py` (apresentação) + `bot/prospecao_followup.py`
(follow-ups FP1/FP2/FP3) + `bot/corrigir_emails.py` (auto-correção de
bounces: busca email correto na web, atualiza lead e reenvia). O Atendente
roda todos em cada tick.

## 🔧 Auto-correção de emails com bounce

Quando um email de prospecção dá bounce (`bot/corrigir_emails.py`):
1. Identifica o lead com bounce
2. Busca o email CORRETO da empresa (mapa manual validado + busca na web com filtro de artefatos)
3. Valida MX do novo domínio
4. Atualiza o lead no leads.csv (status volta a "novo")
5. Reenvia a apresentação para o email correto
6. Registra tudo em `bot/correcoes_emails.json` (histórico de correções)

## ⚙️ Regras de ouro (todos os membros)

1. NUNCA reenviar para email com bounce (consultar `bounces.json`)
2. NUNCA enviar mais de 15 emails de prospecção/dia (respeitar `--max`)
3. NUNCA inventar valores, preços ou promessas — a Master Óleo **compra** óleo e gordura vegetal usados, valor negociado por quantidade
4. Sempre verificar MX do domínio antes de adicionar email novo
5. Registrar erros e aprendizados em `equipe/ecossistema.json` e `equipe/insights.md`
6. Responder relatórios em pt-BR, objetivos, com números reais

## 📈 Métricas para acompanhar (Analista)

- Emails enviados no dia / total da semana
- Taxa de bounce (alvo < 15%)
- Respostas recebidas (alvo: > 3% dos enviados)
- Leads do Formspree convertidos
- Conversas respondidas pelo Atendente
