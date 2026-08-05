# Master Óleo — Site + Bot de Email com Atendente IA

Sistema completo para a Master Óleo (coleta de óleo usado, Salto/SP):
**site institucional + página de captura para indústrias alimentícias +
bot de email que conversa com os clientes sozinho.**

```
master-oleo-site/
├── deploy-vercel/          → PASTA PARA PUBLICAR NO VERCEL
│   ├── index.html          → site institucional
│   ├── industrias.html     → página de captura p/ indústrias (lead magnet)
│   └── guia-descarte-oleo.pdf → isca de lead (guia gratuito)
├── bot/
│   ├── config.json         → credenciais de email + dados da empresa
│   ├── persona.md          → personalidade/regras do atendente IA
│   ├── bot_oleo.py         → script do bot (sequência + respostas)
│   ├── leads.csv           → banco de leads (criado automaticamente)
│   └── replies_pending.json → respostas aguardando o atendente IA
├── guia-descarte-oleo.md   → fonte do PDF
└── markdown_to_pdf.py      → gerador de PDF (já corrigido p/ título personalizado)
```

---

## O QUE JÁ ESTÁ PRONTO E FUNCIONANDO ✅

1. **Site institucional** (index.html) — hero, serviços, quem atendemos,
   como funciona, FAQ, formulário e WhatsApp flutuante. Tema verde + âmbar.
2. **Página de indústrias** (industrias.html) — focada em empresas
   alimentícias, com formulário que captura nome/empresa/email/volume em
   troca do guia PDF.
3. **Guia em PDF** (4 páginas) — isca de lead com conteúdo real e útil.
4. **Bot de email** (bot_oleo.py) — sequência automática: boas-vindas com
   link do guia (dia 0), follow-ups (dias 2, 5, 9) e encerramento.
5. **Atendente IA** (cron job "Atendente Master Óleo") — roda seg–sáb das
   8h às 19h a cada 30 min: envia a sequência e RESPONDE os leads com
   conversa livre (o LLM escreve cada resposta seguindo a persona.md).
6. **Lead de teste** já cadastrado (Ana Souza) para você ver o fluxo.

---

## ATIVAÇÃO — 3 PASSOS (só você pode fazer, ~20 min)

### Passo 1: Publicar o site no Vercel (gratuito, 5 min)
1. Acesse **https://vercel.com/new** e entre com sua conta Google.
2. Na opção **"Deploy a Project"** clique em **"Deploy manually"** (ou
   "Upload") e **arraste a pasta `deploy-vercel/`** para a área indicada.
   (É o mesmo processo que você usou para o site do ebook.)
3. O Vercel gera um endereço tipo `https://master-oleo.vercel.app`.
   **Anote o endereço** — você vai colar no config.json (Passo 2).
4. Confirme que funcionou abrindo o endereço + `/industrias.html` +
   `/guia-descarte-oleo.pdf`.

> Se preferir, o Vercel Drop (vercel.com/new) tem um botão de upload da
> pasta inteira. NÃO precisa de conta paga.

### Passo 2: Ativar o email do bot (gratuito, 10 min)
O bot usa uma conta Gmail com **senha de app** (não precisa do Google
Cloud, não expõe sua senha real).

1. Abra **https://myaccount.google.com/security** na conta que será a do
   bot (sugestão: crie `masteroleo.sp@gmail.com` ou use uma conta
   existente só para a empresa — não use sua conta pessoal).
2. Ative **"Verificação em duas etapas"** (2FA) se ainda não estiver ativa.
3. Em **Segurança → "Senhas de app"**, crie uma senha para "Mail".
   Copie a senha de 16 caracteres gerada.
4. Edite **`bot/config.json`** e preencha:
   - `email.usuario` → o email da conta (ex.: `masteroleo.sp@gmail.com`)
   - `email.senha_app` → a senha de app gerada
   - `empresa.link_guia` e `empresa.site` → o endereço Vercel do Passo 1
5. Teste rodando (no terminal, dentro de `master-oleo-site/bot`):
   ```
   python bot_oleo.py test-email
   ```
   Deve imprimir `SMTP OK` e `IMAP OK`.

### Passo 3: Ligar o formulário do site à captura de leads (gratuito, 5 min)
O formulário do site precisa de um endpoint para receber os leads. Use o
**Formspree** (grátis até 50 leads/mês):

1. Acesse **https://formspree.io** e crie conta (Google login).
2. **New Form** → nome: "Leads Master Óleo" → copie o ID do form
   (algo como `mzxpkwqa`).
3. Nos arquivos `deploy-vercel/index.html` e
   `deploy-vercel/industrias.html`, troque
   `https://formspree.io/f/SEU_FORM_ID` pelo seu
   `https://formspree.io/f/SEU_ID`.
4. **Republica a pasta `deploy-vercel/` no Vercel** (mesmo processo do
   Passo 1 — arraste de novo).
5. No Formspree, em Settings → Notifications, adicione o email do bot para
   receber aviso de cada lead.

> Enquanto o Formspree não for configurado, o formulário do site redireciona
> para o WhatsApp com os dados preenchidos — nada se perde.

---

## COMO O FLUXO FUNCIONA (de ponta a ponta)

```
Indústria acessa industrias.html
   → preenche formulário (nome, empresa, email, volume)
   → Formspree notifica o email do bot
   → [VOCÊ] adiciona o lead no bot (1 comando):
        python bot_oleo.py add-lead --nome "Ana" --empresa "Alimentos X" \
            --email ana@x.com --tipo industria --volume 500 --fonte site
   → Atendente IA (cron, a cada 30 min):
        • envia boas-vindas com link do guia (dia 0)
        • envia follow-ups (dias 2, 5, 9)
        • quando o lead RESPONDE, o bot responde sozinho,
          conversando livremente (preço, região, agendamento...)
   → quando o lead quer fechar, o bot direciona pro WhatsApp
```

**Como adicionar leads em lote (prospecção ativa):** você pode prospectar
indústrias alimentícias da região (Google Maps, LinkedIn, CNPJ) e adicionar
todas com o comando acima — o bot passa a nutrir cada uma automaticamente.
Sugestão de volume inicial: 20–50 leads de restaurantes/indústrias de
Salto, Itu, Indaiatuba, Sorocaba e região.

---

## COMANDOS DO BOT

```bash
cd C:\Users\julio\master-oleo-site\bot

python bot_oleo.py test-email                    # testa credenciais
python bot_oleo.py add-lead --nome "X" --empresa "Y" --email z@z.com [--tipo industria] [--volume 500] [--fonte site]
python bot_oleo.py send-sequence                 # envia emails devidos agora
python bot_oleo.py check-replies                 # lista respostas pendentes
python bot_oleo.py reply --to e@e.com --subject "Re: ..." --body "..." --in-reply-to "ID"
python bot_oleo.py leads                         # lista todos os leads
```

---

## AJUSTES COMUNS

- **Mudar texto dos emails:** edite `bot/bot_oleo.py` (funções `tpl_*`).
- **Mudar a voz do atendente:** edite `bot/persona.md`.
- **Mudar prazos da sequência:** edite `bot/config.json` → `sequencia`.
- **Horário do bot:** o cron roda seg–sáb 8h–19h. Para mudar, fale com o
  agente Hermes.
- **Email de contato do rodapé:** `contato@masteroleo.com.br` é
  placeholder — troque pelo email real (ou remova).

---

## HONESTIDADE (leia)

- O bot acelera o atendimento, mas **cliente que pede orçamento formal e
  agendamento real precisa de você**: o bot entrega no WhatsApp. Responda
  rápido nesses casos.
- Não prometa certificações que a empresa não tem (CETESB, IBAMA etc.) —
  o bot já foi programado para NÃO inventar isso.
- A isca de lead é real e útil; isso constrói confiança, não é "isca
  enganosa".
- Resultados dependem de volume de tráfego/prospecção. Site sozinho não
  vende; site + prospecção ativa + follow-up consistente, sim.
