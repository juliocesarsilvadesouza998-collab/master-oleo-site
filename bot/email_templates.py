#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — TEMPLATES HTML PROFISSIONAIS
===========================================
Templates de e-mail com identidade visual Master Óleo (verde/âmbar),
responsivos, com header, footer, botões CTA e tipografia moderna.

Uso:
  from email_templates import tpl_base, tpl_apresentacao_oleo, tpl_desmoldante
  html = tpl_apresentacao_oleo(nome_lead, empresa_lead, cidade)
"""

# Paleta Master Óleo
VERDE = "#14532d"
VERDE_CLARO = "#1a6b3c"
VERDE_FUNDO = "#e7f6ec"
AMBER = "#f59e0b"
AMBER_ESCURO = "#d97706"
CINZA = "#5b6b60"
CINZA_CLARO = "#f7f5ef"
BRANCO = "#ffffff"
TEXTO = "#1c2a21"
BORDA = "#e4e9e2"


def wrap_professional(html_content, titulo="Master Óleo"):
    """Embrulha qualquer HTML no template profissional com header/footer."""
    return _base(f'<div style="line-height:1.65;color:{TEXTO};font-size:15px">\n    {html_content}\n    </div>', titulo)


def _base(content, titulo="Master Óleo"):
    """Wrapper HTML responsivo com header, conteúdo e footer."""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  @media only screen and (max-width:620px){{.container{{width:100%!important;padding:0 15px!important}}
  .content{{padding:20px 15px!important}} .header{{padding:20px 15px!important;text-align:center!important}}
  .footer{{padding:15px!important;font-size:12px!important}}}}
</style>
</head>
<body style="margin:0;padding:0;background-color:{CINZA_CLARO};font-family:'Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:{CINZA_CLARO};padding:20px 0">
<tr><td align="center">
<table class="container" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background-color:{BRANCO};border-radius:12px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.06)">

  <!-- HEADER -->
  <tr><td class="header" style="background:linear-gradient(135deg,{VERDE},{VERDE_CLARO});padding:28px 32px;text-align:left">
    <table width="100%"><tr>
      <td style="vertical-align:middle">
        <span style="font-size:22px;font-weight:800;color:{BRANCO};letter-spacing:-.5px">Master <span style="color:{AMBER}">Óleo</span></span>
        <div style="font-size:11px;color:#a9cdb7;margin-top:2px;letter-spacing:.3px">Coleta e destinação de resíduos oleosos</div>
      </td>
      <td style="vertical-align:middle;text-align:right">
        <span style="font-size:12px;color:#a9cdb7">Salto/SP</span>
      </td>
    </tr></table>
  </td></tr>

  <!-- CONTEÚDO -->
  <tr><td class="content" style="padding:32px;line-height:1.65;color:{TEXTO};font-size:15px">
    {content}
  </td></tr>

  <!-- DIVISOR -->
  <tr><td style="padding:0 32px"><hr style="border:none;border-top:1px solid {BORDA};margin:0"></td></tr>

  <!-- FOOTER -->
  <tr><td class="footer" style="padding:20px 32px;font-size:12px;color:{CINZA};line-height:1.6">
    <table width="100%">
      <tr>
        <td style="vertical-align:top">
          <b style="color:{TEXTO}">Master Óleo</b><br>
          Salto/SP · (11) 96785-9631<br>
          <a href="https://masteroleo.eco.br" style="color:{VERDE_CLARO};text-decoration:none">masteroleo.eco.br</a>
        </td>
        <td style="vertical-align:top;text-align:right;font-size:11px">
          Se não quiser receber nossos contatos,<br>
          responda este e-mail com "descadastrar".
        </td>
      </tr>
    </table>
    <div style="margin-top:12px;padding-top:12px;border-top:1px solid {BORDA};font-size:11px;color:#a9cdb7;text-align:center">
      © 2026 Master Óleo · Comércio e Logística de Óleos e Gorduras · Todos os direitos reservados
    </div>
  </td></tr>

</table>
</td></tr></table>
</body></html>"""


def _btn(texto, link, cor_fundo=AMBER, cor_texto="#3b2600"):
    """Botão CTA estilizado."""
    return f"""
<table cellpadding="0" cellspacing="0" style="margin:20px 0"><tr><td style="border-radius:8px;background:{cor_fundo};padding:13px 28px;text-align:center">
  <a href="{link}" target="_blank" style="display:inline-block;font-size:15px;font-weight:700;color:{cor_texto};text-decoration:none">{texto}</a>
</td></tr></table>"""


def _destaque(texto):
    """Card de destaque com fundo claro."""
    return f"""<table width="100%" cellpadding="0" cellspacing="0" style="background:{VERDE_FUNDO};border-radius:8px;margin:16px 0">
<tr><td style="padding:16px 20px;font-size:14px;color:{VERDE};line-height:1.5">{texto}</td></tr></table>"""


# ==================== TEMPLATES ====================

def tpl_apresentacao_oleo(nome_lead="", empresa="", cidade="região", segmento="alimentação"):
    """Template de apresentação para compra de óleo — B2B profissional."""
    return _base(f"""
    <p style="margin:0 0 8px;font-size:14px;color:{CINZA}">Assunto: Destinação de óleo usado com certificado</p>

    <p style="margin:0 0 16px">Prezados,</p>

    <p style="margin:0 0 16px">
      A <b style="color:{VERDE}">Master Óleo</b>, de Salto/SP, atua na <b>compra e destinação de óleos vegetais usados,
      vencidos e gorduras</b> para produção de biodiesel — com <b>coleta programada, bombonas fornecidas
      e certificado de destinação</b> a cada retirada.
    </p>

    <p style="margin:0 0 16px">
      O mercado global de óleo usado (UCO) vale <b style="color:{VERDE}">US$ 8 bilhões</b> e a
      <b style="color:{VERDE}">Portaria MME/MMA nº 3/2026</b> torna obrigatório o uso de ≥1% de óleo residual
      no biodiesel a partir de <b>janeiro de 2028</b> — quem fecha contrato agora garante preço e prioridade.
    </p>

    {_destaque(
      "✅ <b>Compramos</b> óleo de fritura, óleo vegetal vencido, margarina e gordura >40%<br>"
      "✅ <b>Certificado de destinação</b> (PNRS + MTR) em toda coleta<br>"
      "✅ <b>Bombonas fornecidas</b> com troca cheia/vazia<br>"
      "✅ <b>Pagamento à vista</b> (PIX) na coleta"
    )}

    <p style="margin:0 0 16px">
      <b>{empresa or "Sua empresa"}</b> gera esse tipo de material? Podemos fazer uma avaliação
      sem compromisso — <b>envie o volume aproximado</b> que retornamos com a proposta.
    </p>

    {_btn("Quero saber quanto recebo →", f"https://wa.me/5511967859631?text=Ol%C3%A1!%20Quero%20avaliar%20meu%20%C3%B3leo%20usado.%20Gero%20aproximadamente%20X%20litros%20por%20m%C3%AAs.")}

    <p style="margin:0;font-size:13px;color:{CINZA}">
      Atenciosamente,<br>
      <b style="color:{TEXTO}">Julio</b><br>
      Master Óleo · Salto/SP · (11) 96785-9631
    </p>
    """)


def tpl_desmoldante(nome_lead="", empresa=""):
    """Template de apresentação para desmoldante vegetal concentrado."""
    return _base(f"""
    <p style="margin:0 0 8px;font-size:14px;color:{CINZA}">Assunto: Desmoldante vegetal concentrado — amostra grátis</p>

    <p style="margin:0 0 16px">Prezados,</p>

    <p style="margin:0 0 16px">
      Desenvolvemos um <b style="color:{VERDE}">desmoldante concentrado à base de óleo vegetal</b>
      para concreto pré-moldado, artefatos de cimento e formas metálicas — com excelente
      custo-benefício e baixo impacto ambiental.
    </p>

    {_destaque(
      "🔬 <b>Base vegetal renovável</b> — alternativa mais limpa que diesel<br>"
      "📐 <b>Alto rendimento</b> — diluição 1:5 a 1:10 em água (50-100 m²/L)<br>"
      "🧼 <b>Peça limpa</b> — sem manchas, sem porosidade, sem resíduo<br>"
      "🛡️ <b>Protege a forma metálica</b> contra oxidação e desgaste<br>"
      "🖌️ <b>Aplica com trincha, pano, pistola ou automático</b>"
    )}

    <p style="margin:0 0 16px">
      <b>Apresentação:</b> Galão de 50 L (mín. 4 unidades) · <b>R$ 650,00/galão</b><br>
      Com diluição 1:7, rende 400 L de produto pronto — <b>custo de ~R$ 1,63/L</b>.<br>
      Enviamos <b style="color:{VERDE}">amostra grátis</b> para todo o Brasil, sem compromisso.
    </p>

    {_btn("Solicitar amostra grátis →", f"https://wa.me/5511967859631?text=Ol%C3%A1!%20Quero%20solicitar%20uma%20amostra%20do%20desmoldante%20vegetal%20para%20concreto%20pr%C3%A9-moldado.")}

    <p style="margin:0;font-size:13px;color:{CINZA}">
      Atenciosamente,<br>
      <b style="color:{TEXTO}">Julio</b><br>
      Master Óleo · Salto/SP · (11) 96785-9631<br>
      <a href="https://masteroleo.eco.br/desmoldante.html" style="color:{VERDE_CLARO};text-decoration:none">masteroleo.eco.br/desmoldante</a>
    </p>
    """, titulo="Master Óleo — Desmoldante")


def tpl_followup(nome_lead="", empresa="", dias=3):
    """Template de follow-up (FP1/FP2/FP3) com tom progressivo."""
    urgencias = {3: "Gostaria de saber se teve oportunidade de avaliar.",
                 6: "É a última vez que entro em contato por e-mail. Se houver interesse, me chame no WhatsApp.",
                 10: "Vou arquivar este contato. Se precisar no futuro, estou à disposição."}
    msg = urgencias.get(dias, urgencias[3])
    return _base(f"""
    <p style="margin:0 0 16px">Prezados,</p>

    <p style="margin:0 0 16px">
      Recentemente enviamos uma proposta de <b style="color:{VERDE}">destinação de óleo usado</b>
      para a <b>{empresa}</b>.
    </p>

    <p style="margin:0 0 16px">{msg}</p>

    {_btn("Falar no WhatsApp →", "https://wa.me/5511967859631")}

    <p style="margin:0;font-size:13px;color:{CINZA}">
      Atenciosamente,<br>
      <b style="color:{TEXTO}">Julio</b><br>
      Master Óleo · (11) 96785-9631
    </p>
    """)


def tpl_proposta_oleo(empresa="", volume="", preco_l=2.00):
    """Template de proposta comercial para venda de óleo."""
    valor_total = round(float(volume or 0) * preco_l, 2) if volume else 0
    return _base(f"""
    <p style="margin:0 0 16px">Prezados,</p>

    <p style="margin:0 0 16px">
      Conforme conversamos, segue a <b style="color:{VERDE}">proposta comercial</b> para
      <b>{empresa}</b>:
    </p>

    <table width="100%" cellpadding="8" cellspacing="0" style="border:1px solid {BORDA};border-radius:8px;margin:16px 0;font-size:14px">
      <tr><td style="border-bottom:1px solid {BORDA};background:{VERDE_FUNDO};font-weight:700;color:{VERDE}" colspan="2">📋 Proposta de Coleta</td></tr>
      <tr><td style="border-bottom:1px solid {BORDA};color:{CINZA}">Volume estimado</td><td style="font-weight:700">{volume or "—"}</td></tr>
      <tr><td style="border-bottom:1px solid {BORDA};color:{CINZA}">Valor por litro</td><td style="font-weight:700">R$ {preco_l:.2f}</td></tr>
      <tr><td style="border-bottom:1px solid {BORDA};color:{CINZA}">Valor total estimado</td><td style="font-weight:700;color:{VERDE}">R$ {valor_total:.2f}</td></tr>
      <tr><td style="border-bottom:1px solid {BORDA};color:{CINZA}">Pagamento</td><td>À vista (PIX) na coleta</td></tr>
      <tr><td style="color:{CINZA}">Frequência</td><td>Semanal / Quinzenal / Mensal</td></tr>
    </table>

    <p style="margin:0 0 16px">
      <b>Inclui:</b> bombonas fornecidas · coleta programada · certificado de destinação ·
      relatório ESG mensal (opcional) · bônus de exclusividade para contrato de 12 meses.
    </p>

    {_btn("Confirmar primeira coleta →", "https://wa.me/5511967859631")}

    <p style="margin:0;font-size:13px;color:{CINZA}">
      Atenciosamente,<br>
      <b style="color:{TEXTO}">Julio</b><br>
      Master Óleo · (11) 96785-9631
    </p>
    """)


def tpl_obrigado(nome_lead=""):
    """Template de agradecimento após contato."""
    return _base(f"""
    <p style="margin:0 0 16px">Olá{nome_lead and ' ' + nome_lead + ',' or ','}</p>

    <p style="margin:0 0 16px">
      Obrigado pelo contato! Recebemos sua mensagem e vamos analisar seu material.
    </p>

    <p style="margin:0 0 16px">
      Enquanto isso, se tiver qualquer dúvida, pode me chamar diretamente no WhatsApp.
    </p>

    {_btn("Falar conosco →", "https://wa.me/5511967859631")}

    <p style="margin:0;font-size:13px;color:{CINZA}">
      Abraço,<br>
      <b style="color:{TEXTO}">Julio</b><br>
      Master Óleo · (11) 96785-9631
    </p>
    """)


# Dicionário para acesso programático
TEMPLATES = {
    "apresentacao_oleo": tpl_apresentacao_oleo,
    "desmoldante": tpl_desmoldante,
    "followup_3": lambda n, e: tpl_followup(n, e, 3),
    "followup_6": lambda n, e: tpl_followup(n, e, 6),
    "followup_10": lambda n, e: tpl_followup(n, e, 10),
    "proposta_oleo": tpl_proposta_oleo,
    "obrigado": tpl_obrigado,
}


if __name__ == "__main__":
    # Teste: gera HTML de exemplo
    print(tpl_apresentacao_oleo("João", "Supermercados ABC", "Campinas", "supermercado"))