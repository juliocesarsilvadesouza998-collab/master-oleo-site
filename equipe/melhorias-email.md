# 📧 Melhorias no sistema de email — Prospecção B2B Master Óleo

> Análise de 2026-08-18 com base em bot/prospecao.py, bot/prospecao_followup.py,
> bot/bot_oleo.py, bot/persona.md e equipe/estudo-mercado-oleo.md.
> Referências de boas práticas: cold email B2B (benchmarks Lemkin/Topo/Gong),
> estratégias JBS/Óleo Verde/Ambiental Santos (estudo de mercado).

---

## 1. Fraquezas identificadas (5)

1. **Email longo demais, com 5 bullets e 2 CTAs.** A apresentação atual tem ~200 palavras, lista 5 benefícios (pagamento, certificado, coleta, bombonas, relatório ESG) e ainda pede 2 informações (volume E tipo de material) + oferece WhatsApp + "proposta em 24h". Regra de ouro do cold email B2B: <125 palavras, 1 mensagem, 1 CTA. Excesso de features dilui a mensagem central: **nós PAGAMOS pelo seu resíduo**.

2. **Abertura institucional genérica.** "Olá, {nome}. Sou da Master Óleo, de Salto/SP, e estou entrando em contato porque..." é abertura clássica de e-mail em massa. As 2 primeiras linhas são as únicas que determinam se o e-mail é lido — devem falar do PROSPECTO (o resíduo da empresa dele), não da empresa que envia.

3. **CTA de fricção alta e disperso.** "Me responda com a quantidade aproximada (litros ou kg por mês) E o tipo de material" = pedido duplo. Cada informação extra pedida reduz resposta. O CTA ideal é UMA pergunta simples e específica (só o volume), que é exatamente a informação que destrava a negociação (persona.md: "Para saber o valor, precisamos da quantidade aproximada").

4. **FP1 com erro factual e follow-ups fora do thread.** (a) O FP1 é enviado no dia 3, mas o texto diz "Semana passada apresentei..." — factualmente errado e quebra credibilidade. (b) Os follow-ups FP1/FP2/FP3 são enviados SEM `In-Reply-To`/`References` e com assunto novo, ou seja, chegam como e-mails frios separados — perdem o contexto da conversa, parecem mais spam e reduzem resposta. Devem continuar o thread original com assunto "Re: ...".

5. **Zero prova social da própria Master Óleo.** O e-mail cita dado de mercado global (US$ 11 bi — bom), mas nada que valide a própria empresa: "X litros coletados", "X empresas atendidas na região", "coletamos para usinas de biodiesel". Benchmarks B2B: menção de clientes/volume próprio aumenta taxa de resposta. A JBS cresceu +154% em 2024 coletando óleo — esse tipo de validação do SETOR ajuda, mas quem compra de você precisa de prova SUA.

> **Bônus técnico:** em `prospecao.py` (linha 163) e `prospecao_followup.py` (linha 65),
> a versão plain-text é gerada com `re.sub(r"<[^>]+>", "", html)` — sem conversão de
> `</p>`/`<br>` em quebras de linha. Clientes de texto puro e filtros de spam leem um
> bloco de texto corrido. Usar a mesma lógica de `_plain_from_html` do `bot_oleo.py`.

---

## 2. Template de apresentação B2B (otimizado)

**Assunto (principal):**
```
O óleo de fritura da {empresa} vale dinheiro
```

**Assuntos alternativos para teste A/B:**
```
B: Receita extra com o óleo usado da {empresa}
C: Compramos o óleo de cozinha usado da {empresa}
```

**Corpo (cópia pronta):**

```
Olá, {nome}.

Toda fritura gera um resíduo — e o da {empresa} hoje sai de graça. No mercado, isso mudou: o óleo de cozinha usado virou commodity energética, um setor global de US$ 11 bilhões que cresce ~7% ao ano (biodiesel e combustível de aviação).

A Master Óleo, de Salto/SP, compra esse material. Na prática, para vocês:

1. Pagamento pelo óleo e pela gordura vegetal usados — referência de R$ 1,00 a R$ 2,50/litro, conforme qualidade e volume;
2. Certificado de destinação em toda coleta — comprovação da PNRS (Lei 12.305/2010);
3. Coleta programada e bombonas fornecidas — custo logístico zero para a sua equipe.

Para eu te enviar uma estimativa de valor em até 24h: qual o volume aproximado que vocês geram por mês (litros ou kg)?

Se preferir, me chama no WhatsApp (11) 96785-9631.

Abraço,
{nome}
Master Óleo · Compra de óleo e gordura vegetal usados · Salto/SP
```

**HTML drop-in para `tpl_apresentacao` (prospecao.py):**

```python
return {
    "subject": f"O óleo de fritura da {lead.get('empresa','')} vale dinheiro",
    "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Toda fritura gera um resíduo — e o da {lead.get('empresa','')} hoje sai de graça. No mercado, isso mudou: o óleo de cozinha usado virou <b>commodity energética</b>, um setor global de <b>US$ 11 bilhões</b> que cresce ~7% ao ano (biodiesel e combustível de aviação).</p>
<p>A <b>{g['nome']}</b>, de {g['cidade']}, compra esse material. Na prática, para vocês:</p>
<ul>
  <li><b>Pagamento pelo óleo e pela gordura vegetal usados</b> — referência de R$ 1,00 a R$ 2,50/litro, conforme qualidade e volume;</li>
  <li><b>Certificado de destinação em toda coleta</b> — comprovação da PNRS (Lei 12.305/2010);</li>
  <li><b>Coleta programada e bombonas fornecidas</b> — custo logístico zero para a sua equipe.</li>
</ul>
<p>Para eu te enviar uma estimativa de valor em até 24h: <b>qual o volume aproximado que vocês geram por mês (litros ou kg)?</b></p>
<p>Se preferir, me chama no WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {g['cidade']}</p>
</div>"""
}
```

---

## 3. Template de follow-up FP1 (otimizado)

**Assunto (deve repetir o da apresentação com "Re:" para continuar o thread):**
```
Re: O óleo de fritura da {empresa} vale dinheiro
```

**Corpo (cópia pronta):**

```
Olá, {nome}.

Te escrevi há poucos dias sobre a compra do óleo usado da {empresa} — como sei que a caixa de entrada enche, deixo aqui o essencial:

A Lei 12.305/2010 (PNRS) exige destinação comprovada dos resíduos. Com a Master Óleo isso deixa de ser preocupação e vira receita: pagamos de R$ 1,00 a R$ 2,50/litro, com certificado em toda coleta e bombonas fornecidas.

Para eu te passar o valor exato da sua operação: quanto vocês geram por mês (litros ou kg)? Me responde esse número que eu te mando a estimativa ainda esta semana.

Alternativa rápida: WhatsApp (11) 96785-9631.

Abraço,
{nome}
```

**HTML drop-in para `tpl_fp` (prospecao_followup.py, n == 1):**

```python
subj = f"Re: O óleo de fritura da {lead['empresa']} vale dinheiro"
html = f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead['nome']}.</p>
<p>Te escrevi há poucos dias sobre a <b>compra do óleo usado da {lead['empresa']}</b> — como sei que a caixa de entrada enche, deixo aqui o essencial:</p>
<p>A Lei 12.305/2010 (PNRS) exige <b>destinação comprovada</b> dos resíduos. Com a {g['nome']} isso deixa de ser preocupação e vira <b>receita</b>: pagamos de R$ 1,00 a R$ 2,50/litro, com certificado em toda coleta e bombonas fornecidas.</p>
<p>Para eu te passar o valor exato da sua operação: <b>quanto vocês geram por mês (litros ou kg)?</b> Me responde esse número que eu te mando a estimativa ainda esta semana.</p>
<p>Alternativa rápida: WhatsApp {g['telefone_whatsapp']}.</p>
<p>Abraço,<br><b>{g['nome']}</b></p>
</div>"""
```

---

## 4. Melhorias de processo (3)

### 1. Enviar em janela de alta resposta (terça–quinta, 8h–10h)
Benchmarks B2B: terça, quarta e quinta entre 8h e 10h concentram as maiores taxas de
abertura e resposta; segunda e sexta são os piores dias. **Ação:** agendar o cron de
`prospecao.py`/`prospecao_followup.py` para rodar apenas em dias úteis (Ter–Qui) pela
manhã, e pular envios que caírem em feriado/fim de semana (se o lead foi cadastrado na
sexta, o FP1 cai na segunda — melhor agendar para terça).

### 2. Continuar o thread nos follow-ups (In-Reply-To + References + "Re:")
Hoje FP1/FP2/FP3 chegam como e-mails novos e separados. **Ação:** salvar o
`Message-ID` da apresentação no `leads.csv` (nova coluna `apresentacao_msgid`) no
momento do envio em `prospecao.py`; no `prospecao_followup.py`, passar
`in_reply_to=apresentacao_msgid` e `references=apresentacao_msgid` (o `smtp_send` já
suporta) e usar assunto com "Re:" igual ao original. Isso mantém o contexto da
conversa no cliente, melhora entregabilidade e reduz cara de spam.

### 3. Segmentar por segmento + testar assuntos A/B
Cada segmento tem dor diferente (estudo de mercado, seção 3):
- **Indústria** (ex.: Kerry, Castelo, Shinoda): ângulo ESG + volume contratual —
  "relatório de impacto ambiental para metas ESG e licenciamentos" + contrato de
  volume constante;
- **Restaurantes/padarias** (ex.: Scallet, Casa Aliança): ângulo receita extra +
  espaço — "o tanque/reserva que ocupa espaço vira dinheiro no caixa";
- **Supermercados/atacado** (ex.: Dias, Sumerbol, Zarelli): ângulo volume + parceria
  contínua.
**Ação:** 2 versões de assunto por lote (ex.: "O óleo de fritura da {empresa} vale
dinheiro" vs "Receita extra com o óleo usado da {empresa}") e comparar abertura e
resposta por versão no `leads.csv`; manter a vencedora.

---

## Nota técnica (implementação)
- Corrigir geração do plain-text em `prospecao.py` e `prospecao_followup.py`
  (converter `</p>` e `<br>` em `\n`, como `_plain_from_html` do `bot_oleo.py`).
- Manter FP_DIAS = [3, 6, 10] (ritmo bom); FP2 pode manter o reforço de valor de
  mercado; FP3 mantém o tom de encerramento ("porta aberta").
