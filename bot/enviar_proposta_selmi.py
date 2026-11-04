#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Envia proposta para Selmi (compras@selmi.com.br) após redirect do SAC."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from bot_oleo import load_config, cfg_email, smtp_send, read_leads, write_leads, now_iso, find_lead

# Lê a proposta HTML
with open(os.path.join(os.path.dirname(__file__), "proposta-contrato-pastificio-selmi-s-a-2026-11-03.html"), "r", encoding="utf-8") as f:
    proposta_html = f.read()

# Corpo do email
cover = """
<div style="font-family:Arial,sans-serif;max-width:700px;margin:auto;color:#1c2a21">
<p>Olá, equipe Selmi!</p>

<p>A <b>Cristina Magalhães</b>, do SAC Selmi, nos redirecionou para este contato comercial — agradecemos a indicação.</p>

<p>Somos a <b>Master Óleo</b>, de Salto/SP, e <b>compramos óleo de cozinha usado, gordura vegetal e resíduos vencidos com >40% de gordura</b> para transformação em biodiesel. Já atendemos indústrias como a <b>Catalent</b> (Indaiatuba/Sorocaba) e estamos em negociação com as 3 maiores redes do interior SP (Savegnago #1, Pague Menos #2, Tauste #3 — ABRAS 2026).</p>

<p>Segue abaixo nossa <b>proposta de coleta</b> estimada para o Pastifício Selmi:</p>

""" + proposta_html + """

<div style="font-family:Arial,sans-serif;max-width:700px;margin:auto;color:#1c2a21;margin-top:20px">
<p><b>Por que fechar contrato agora?</b></p>
<ul>
<li><b>Urgência regulatória:</b> a Portaria MME/MMA nº 3/2026 obriga ≥1% de óleo residual no biodiesel a partir de jan/2028 — quem fecha contrato agora garante preço e prioridade.</li>
<li><b>Mercado aquecido:</b> B16 em vigor (março/2026), Petrobras investindo R$ 23 mi na coleta de óleo residual em SP.</li>
<li><b>Escudo legal:</b> certificado de destinação + MTR em cada coleta (PNRS — Lei 12.305/2010).</li>
<li><b>Pagamento à vista (PIX)</b> em até 48h.</li>
</ul>

<p>Podemos agendar uma <b>coleta-teste</b> na próxima semana, sem compromisso. É só responder este e-mail ou chamar no WhatsApp (11) 96785-9631.</p>

<p>Atenciosamente,<br>
<b>Júlio — Master Óleo</b><br>
WhatsApp (11) 96785-9631 · masteroleo.eco.br</p>
</div>
"""

def main():
    cfg = load_config()
    e = cfg_email(cfg)
    
    # Envia para compras@selmi.com.br
    to = "compras@selmi.com.br"
    subject = "Proposta de Coleta de Óleo Usado — Master Óleo × Pastifício Selmi"
    
    mid = smtp_send(cfg, e, to, subject, cover)
    print(f"Proposta enviada para {to} (Message-ID: {mid})")
    
    # Atualiza leads
    leads = read_leads()
    
    # 1) Atualiza lead 59 (compras@selmi.com.br) — re-ativar como respondido
    lead59 = find_lead(leads, "compras@selmi.com.br")
    if lead59:
        lead59["status"] = "respondido"
        lead59["respondido_em"] = now_iso()
        lead59["respondido_por"] = "atendente_ia"
        lead59["ultima_resposta"] = "SAC Selmi redirecionou para compras — proposta enviada"
        print(f"Lead 59 ({lead59['email']}) atualizado.")
    
    # 2) Marca lead 9672890911 (sac@selmi.com.br) como encerrado (SAC já respondeu)
    for l in leads:
        if l.get("id", "") == "9672890911":
            l["status"] = "respondido"
            l["ultima_resposta"] = "SAC redirecionou para compras@selmi.com.br — lead transferido"
            print(f"Lead 9672890911 (sac@selmi.com.br) encerrado/transferido.")
            break
    
    write_leads(leads)
    print("Leads atualizados com sucesso.")

if __name__ == "__main__":
    main()