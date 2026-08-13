# Master Óleo — Site + Bot de Email com Atendente IA

Sistema completo para a Master Óleo (coleta de óleo usado, Salto/SP):
**site institucional + página de captura para indústrias alimentícias +
bot de email que conversa com os clientes sozinho.**

## URLs no ar

| O quê | Link |
|---|---|
| Site | https://masteroleo.eco.br |
| Indústrias (captura) | https://masteroleo.eco.br/industrias |
| Guia PDF | https://masteroleo.eco.br/guia-descarte-oleo.pdf |
| GitHub | https://github.com/juliocesarsilvadesouza998-collab/master-oleo-site |
| Painel Netlify | https://app.netlify.com/projects/master-oleo |

## Estrutura

```
master-oleo-site/
├── deploy-vercel/          → pasta publicada no Netlify (nome histórico)
│   ├── index.html          → site institucional
│   ├── industrias.html     → página de captura p/ indústrias
│   └── guia-descarte-oleo.pdf
├── bot/
│   ├── config.example.json → modelo (sem segredos)
│   ├── config.json         → credenciais locais (NÃO sobe no git)
│   ├── persona.md          → regras do atendente IA
│   └── bot_oleo.py         → sequência + respostas
├── netlify.toml            → publish = deploy-vercel + redirects
└── README.md
```

## O que já está pronto

1. **Site institucional** + **página de indústrias** + **guia PDF**
2. **GitHub** com o código
3. **Netlify** com deploy automático a cada `git push` na `main`
4. **Bot de email** + cron do atendente IA (falta só ativar Gmail)

## Como atualizar o site (deploy automático)

Qualquer alteração na pasta `deploy-vercel/` (ou no `netlify.toml`):

```bash
cd C:\Users\julio\master-oleo-site
git add -A
git commit -m "sua mensagem"
git push origin main
```

O webhook do GitHub avisa o Netlify e o site atualiza sozinho em 1–2 minutos.

## Ativação pendente (só o que falta)

### 1) Email do bot (Gmail senha de app)
1. Conta Google da empresa → https://myaccount.google.com/security
2. Ative 2FA → **Senhas de app** → crie uma para "Mail"
3. Edite `bot/config.json`:
   - `email.usuario`
   - `email.senha_app`
4. Teste:
   ```bash
   cd C:\Users\julio\master-oleo-site\bot
   python bot_oleo.py test-email
   ```

### 2) Formulário de leads (Formspree)
1. https://formspree.io → New Form → "Leads Master Óleo"
2. Troque `SEU_FORM_ID` em:
   - `deploy-vercel/index.html`
   - `deploy-vercel/industrias.html`
3. `git commit` + `git push` (o Netlify publica sozinho)

## Comandos do bot

```bash
cd C:\Users\julio\master-oleo-site\bot
python bot_oleo.py test-email
python bot_oleo.py add-lead --nome "X" --empresa "Y" --email z@z.com --tipo industria --volume 500
python bot_oleo.py send-sequence
python bot_oleo.py check-replies
python bot_oleo.py leads
```

## Observações

- Credenciais reais ficam só em `bot/config.json` (gitignore).
- No Netlify Free, projetos novos podem nascer **private** (login). Este projeto já foi aberto para público (`sso_login=false`).
- O bot acelera atendimento; orçamento final e coleta real fecham no WhatsApp (11) 96785-9631.
