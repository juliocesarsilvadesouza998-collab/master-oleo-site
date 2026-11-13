#!/usr/bin/env python3
"""Envia proposta de contrato como anexo para o lead"""
import json, smtplib, ssl, sys, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr, make_msgid

os.chdir(os.path.dirname(__file__) or '.')

with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)
e = cfg['email']

to = sys.argv[1]
proposta_path = sys.argv[2]
empresa = sys.argv[3] if len(sys.argv) > 3 else to

# Read the proposal HTML
with open(proposta_path, 'r', encoding='utf-8') as f:
    proposal_html = f.read()

# Build email
msg = MIMEMultipart('mixed')
msg['From'] = formataddr((str(Header(cfg['empresa']['nome'], 'utf-8')), e['usuario']))
msg['To'] = to
msg['Subject'] = Header(f'Proposta de Coleta Master Óleo × {empresa}', 'utf-8')
msg['Message-ID'] = make_msgid()

# Body text
body = MIMEMultipart('alternative')
body_txt = f"""Olá, equipe {empresa}!

Conforme nosso contato anterior, segue em anexo a proposta formal de coleta de óleo usado para a Savegnago.

Resumo da proposta:
• Volume estimado: 5.000 L/mês
• Valor de referência: R$ 2,00/L
• Receita estimada: R$ 10.000/mês | R$ 120.000/ano
• Bônus de exclusividade: +R$ 0,10/L
• Bônus de consolidação (todas as lojas): +R$ 0,05/L
• Pagamento: à vista (PIX) na coleta
• Certificado de destinação + relatório ESG mensal

Próximos passos:
1. Confirmar o volume real de todas as lojas
2. Agendar uma coleta-teste piloto em 1 loja
3. Estruturar contrato para a rede completa

Para alinhar os detalhes, pode me chamar no WhatsApp (11) 96785-9631 ou responder este email.

Atenciosamente,
Master Óleo
www.masteroleo.eco.br
"""

body_html_text = f"""<html><body style="font-family:Segoe UI,Arial,sans-serif;color:#1c2a21">
<p>Olá, equipe {empresa}!</p>
<p>Conforme nosso contato anterior, segue em anexo a <b>proposta formal de coleta de óleo usado</b>.</p>
<table style="border:1px solid #14532d;border-radius:8px;padding:12px;margin:12px 0">
<tr><td><b>Volume estimado:</b></td><td>5.000 L/mês</td></tr>
<tr><td><b>Valor de referência:</b></td><td>R$ 2,00/L</td></tr>
<tr><td><b>Receita estimada:</b></td><td><b>R$ 10.000/mês</b> | <b>R$ 120.000/ano</b></td></tr>
<tr><td><b>Bônus de exclusividade:</b></td><td>+R$ 0,10/L</td></tr>
<tr><td><b>Bônus de consolidação:</b></td><td>+R$ 0,05/L (todas as lojas)</td></tr>
<tr><td><b>Pagamento:</b></td><td>à vista (PIX) na coleta</td></tr>
<tr><td><b>Certificado:</b></td><td>Destinação + relatório ESG mensal</td></tr>
</table>
<p><b>Próximos passos:</b></p>
<ol>
<li>Confirmar o volume real de todas as lojas</li>
<li>Agendar uma coleta-teste piloto em 1 loja</li>
<li>Estruturar contrato para a rede completa</li>
</ol>
<p>Para alinhar os detalhes, pode me chamar no <b>WhatsApp (11) 96785-9631</b> ou responder este email.</p>
<p>Atenciosamente,<br><b>Master Óleo</b><br><a href="https://masteroleo.eco.br">www.masteroleo.eco.br</a></p>
</body></html>"""

body.attach(MIMEText(body_txt, 'plain', 'utf-8'))
body.attach(MIMEText(body_html_text, 'html', 'utf-8'))
msg.attach(body)

# Attach the proposal
with open(proposta_path, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(proposta_path))
    msg.attach(part)

# Send
ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(e['smtp_host'], e['smtp_port'], context=ctx, timeout=30) as s:
    s.login(e['usuario'], e['senha_app'])
    s.sendmail(e['usuario'], [to], msg.as_string())

print(f"OK: Proposta enviada para {to}")