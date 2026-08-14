# 🌿 Ecossistema Master Óleo — IA Auto-corretiva

Este é o **sistema de IAs que trabalham juntas** para prospectar, enviar e
melhorar continuamente a operação da Master Óleo (compra de óleo de cozinha
usado e gordura vegetal usada — Salto/SP e região).

## 🧠 Membros da equipe

| Papel | Job | Quando | Responsabilidade |
|---|---|---|---|
| **Atendente** | `497505018e92` | seg–sáb 8h–19h (30/30min) | Envia sequência, responde leads, conversa livre |
| **Prospector** | `prospector-masteroleo` | seg–sáb 07:15 | Busca novas empresas grandes na web, valida email (MX), adiciona à fila, envia lote |
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
