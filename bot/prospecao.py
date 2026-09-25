#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Prospecção Ativa
================================
Envia emails de apresentação B2B para empresas alimentícias 
e registra os leads no leads.csv para follow-up automático.

Uso:
  python prospecao.py                    # envia para a lista (rate limit 5s)
  python prospecao.py --dry-run          # mostra o que faria sem enviar
  python prospecao.py --list             # lista empresas e emails candidatos
"""
import argparse, csv, datetime, json, os, re, ssl, smtplib, sys, time
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

BASE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE, "config.json")
LEADS_PATH = os.path.join(BASE, "leads.csv")
FIELDS = ["id","nome","empresa","email","tipo","volume","segmento","cidade","fonte","status",
          "criado_em","boas_vindas_em","follow1_em","follow2_em","follow3_em",
          "apresentacao_em","apresentacao_msgid","fp1_em","fp2_em","fp3_em",
          "ultima_resposta","respondido_em","respondido_por"]

# Empresas com MX válido + email (corrigido onde houve bounce)
# Fontes: econodata rankings 2026 (Campinas, Indaiatuba, Itu, Sorocaba) + sites oficiais
EMPRESAS = [
    # --- Salto/região (base) ---
    {"nome": "Alimentare Servicos", "empresa": "Alimentare Servicos de Alimentacao LTDA", "email": "contato@alimentare.com.br", "cidade": "Salto/SP", "segmento": "Restaurantes e refeicoes coletivas"},
    {"nome": "Casa Alianca Gourmet", "empresa": "Casa Alianca - Padaria Gourmet", "email": "contato@padariaalianca.com.br", "cidade": "Salto/SP", "segmento": "Padaria e confeitaria"},
    {"nome": "Restaurante Scallet", "empresa": "Restaurante e Pizzaria Scallet", "email": "pedidos@scallet.com.br", "cidade": "Salto/SP", "segmento": "Restaurante"},
    {"nome": "Supermercados Dias", "empresa": "Supermercados Dias", "email": "contato@jvmsupermarket.com.br", "cidade": "Salto/SP", "segmento": "Supermercado"},
    {"nome": "Massima Alimentacao", "empresa": "Massima Alimentacao", "email": "contato@massimaalimentacao.com.br", "cidade": "Regiao", "segmento": "Refeicoes coletivas"},
    # --- Campinas (grandes) ---
    {"nome": "Sapore S.A.", "empresa": "Sapore S.A.", "email": "contato@sapore.com.br", "cidade": "Campinas/SP", "segmento": "Restaurantes (rede nacional)"},
    {"nome": "Kerry do Brasil", "empresa": "Kerry do Brasil LTDA", "email": "dpo.kerry@lbca.com.br", "cidade": "Campinas/SP", "segmento": "Industria de ingredientes"},
    {"nome": "Bagley do Brasil", "empresa": "Bagley do Brasil Alimentos LTDA", "email": "aquiarcor@arcor.com", "cidade": "Campinas/SP", "segmento": "Industria de alimentos (snacks)"},
    {"nome": "Alimentare Nutricao", "empresa": "Alimentare Nutricao e Servicos LTDA", "email": "contato@redealimentare.com.br", "cidade": "Campinas/SP", "segmento": "Refeicoes coletivas (1 mi refeicoes/mes)"},
    {"nome": "Higa Atacado", "empresa": "Higa Produtos Alimenticios LTDA", "email": "contato@higa.com.br", "cidade": "Campinas/SP", "segmento": "Atacado e varejo de alimentos"},
    # --- Indaiatuba (grandes) ---
    {"nome": "Kelco Pet Care", "empresa": "Kelco Industrial Produtos Animais LTDA", "email": "info@kelcopetcare.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de alimentos pet"},
    {"nome": "Palacios Brasil", "empresa": "Palacios Brasil Comercializacao de Alimentos LTDA", "email": "palacios@palaciosbrasil.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de embutidos e frios"},
    {"nome": "Crista Margarina", "empresa": "Crista Industria e Comercio LTDA", "email": "faleconosco@cristamargarina.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria de gorduras e margarinas"},
    {"nome": "Sumerbol Supermercados", "empresa": "Sumerbol Supermercados LTDA", "email": "atendimento@sumerbol.com.br", "cidade": "Indaiatuba/SP", "segmento": "Supermercados (rede)"},
    # --- Itu (grandes) ---
    {"nome": "Monin Brasil", "empresa": "Monin Brasil Industria", "email": "faleconosco@monin.com", "cidade": "Itu/SP", "segmento": "Industria de xaropes e sabores"},
    # --- Sorocaba (grandes) ---
    {"nome": "Sorocaba Refrescos", "empresa": "Sorocaba Refrescos S.A.", "email": "last@sorocabarefrescos.com.br", "cidade": "Sorocaba/SP", "segmento": "Engarrafadora Coca-Cola"},
    {"nome": "Supermercado UNE", "empresa": "Supermercado UNE LTDA", "email": "rh@superune.com.br", "cidade": "Sorocaba/SP", "segmento": "Supermercados (rede)"},
    {"nome": "Shinoda Alimentos", "empresa": "Shinoda Alimentos LTDA", "email": "comercial.granja@shinoda.com.br", "cidade": "Sorocaba/SP", "segmento": "Industria de ovos e alimentos"},
    {"nome": "Rosaves Aves", "empresa": "Abatedouro de Aves Ideal LTDA (Rosaves)", "email": "contato@rosaves.com.br", "cidade": "Sorocaba/SP", "segmento": "Abatedouro e frigorifico de aves"},
    # --- Jundiaí (grandes) ---
    {"nome": "Fini Company Brasil", "empresa": "Sanchez Cano LTDA (Fini)", "email": "fini@rpmacomunicacao.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de balas e guloseimas"},
    {"nome": "Food Brands Kisabor", "empresa": "Food Brands Industria de Produtos Alimenticios S/A", "email": "sac@kisabor.ind.br", "cidade": "Jundiai/SP", "segmento": "Industria de condimentos e alimentos"},
    {"nome": "Castelo Alimentos", "empresa": "Castelo Alimentos S/A", "email": "sacc@casteloalimentos.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de biscoitos e massas"},
    {"nome": "CRS Brands", "empresa": "CRS Brands Industria e Comercio S/A", "email": "contato@crsbrands.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de bebidas e alimentos"},
    # --- Louveira (grandes) ---
        {"nome": "Prime Cater", "empresa": "Prime Cater Comercial de Produtos Alimenticios S/A", "email": "contato@pmct.com.br", "cidade": "Louveira/SP", "segmento": "Refeicoes coletivas e catering"},
        {"nome": "PGR Sao Paulo Refeicoes", "empresa": "P.G.R. Sao Paulo Refeicoes LTDA", "email": "marcia.mendes@somospremium.com.br", "cidade": "Louveira/SP", "segmento": "Restaurantes e refeicoes"},
        # --- Piracicaba (grandes) ---
        {"nome": "Bom Peixe", "empresa": "Bom Peixe Industria e Comercio LTDA", "email": "sac@bompeixe.com.br", "cidade": "Piracicaba/SP", "segmento": "Industria de pescados e conservas"},
        {"nome": "Laticinios Noiva da Colina", "empresa": "Laticinios Noiva da Colina LTDA", "email": "contato@vimilk.com.br", "cidade": "Piracicaba/SP", "segmento": "Industria de laticinios"},
        # --- Valinhos (grandes) ---
        {"nome": "Zarelli Supermercados", "empresa": "Zarelli Supermercados LTDA", "email": "contato@supermercadoszarelli.com.br", "cidade": "Valinhos/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Chr Hansen Brasil", "empresa": "Chr Hansen Industria e Comercio LTDA", "email": "braco@chr-hansen.com", "cidade": "Valinhos/SP", "segmento": "Industria de culturas e ingredientes"},
        {"nome": "Pronutrition", "empresa": "Pronutrition do Brasil Industria de Suplementos", "email": "compras@pronutrition.com.br", "cidade": "Valinhos/SP", "segmento": "Industria de suplementos alimentares"},
        {"nome": "Ultrapan", "empresa": "Ultrapan Industria e Comercio LTDA", "email": "marketing@ultrapan.com.br", "cidade": "Valinhos/SP", "segmento": "Industria de produtos alimenticios"},
        # --- NOVAS EMPRESAS (adicionadas 21/09 - reposição de fila) ---
        # Supermercados que mais convertem - região
        {"nome": "Delta Supermercados", "empresa": "Delta Supermercados LTDA", "email": "admgeneral@deltasuper.com.br", "cidade": "Piracicaba/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Boa Supermercados", "empresa": "Supermercado Boa LTDA", "email": "atendimento@smboa.com.br", "cidade": "Jundiai/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Supermercado Irmaos Barrera", "empresa": "Supermercado Irmaos Barrera LTDA", "email": "social@irmaosbarrera.com.br", "cidade": "Elias Fausto/SP", "segmento": "Supermercado"},
        {"nome": "Supermercados Real", "empresa": "Supermercados Real LTDA", "email": "contato@supermercadosreal.com.br", "cidade": "Tatui/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Beira Rio Supermercados", "empresa": "Beira Rio Supermercados LTDA", "email": "contato@beirariosm.com.br", "cidade": "Piracicaba/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Supermercado Infanger", "empresa": "Supermercado Infanger LTDA", "email": "contato@infanger.com.br", "cidade": "Vinhedo/SP", "segmento": "Supermercado"},
        {"nome": "GoodBom Supermercados", "empresa": "GoodBom Supermercados LTDA", "email": "contato@goodbom.com.br", "cidade": "Tatui/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Covabra Supermercados", "empresa": "Covabra Supermercados LTDA", "email": "sac@covabra.com.br", "cidade": "Limeira/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Atacado Diniz", "empresa": "Atacado Diniz LTDA", "email": "sac@atacadodiniz.com.br", "cidade": "Louveira/SP", "segmento": "Atacado e distribuicao de alimentos"},
        {"nome": "Oba Hortifruti", "empresa": "Oba Hortifruti SA", "email": "ouvidoria@redeoba.com.br", "cidade": "Sumare/SP", "segmento": "Varejo de hortifruti (rede)"},
        {"nome": "Mania de Churrasco", "empresa": "Mania de Churrasco LTDA", "email": "sac@maniadechurrasco.com", "cidade": "Limeira/SP", "segmento": "Restaurantes (rede steak house)"},
        {"nome": "SupraFoods", "empresa": "SupraFoods Comercio de Alimentos LTDA", "email": "comercial@suprafoods.com.br", "cidade": "Americana/SP", "segmento": "Industria de alimentos"},
        {"nome": "Supermercado Pague Menos", "empresa": "Supermercados Pague Menos SA", "email": "falecom@supermercadospaguemenos.com.br", "cidade": "Campinas/SP", "segmento": "Supermercados (rede)"},
        {"nome": "Supermercados Sao Judas Tadeu", "empresa": "Supermercados Sao Judas Tadeu LTDA", "email": "faleconosco@supersaojudas.com.br", "cidade": "Bauru/SP", "segmento": "Supermercados (rede)"},
        # --- NOVAS EMPRESAS (adicionadas 22/09 - reposicao de fila, MX verificado) ---
                # Oleos e gorduras - alta prioridade
                {"nome": "Unigra Brasil", "empresa": "Unigra Brasil Industria e Comercio de Produtos Alimenticios LTDA", "email": "sac.br@mastermartini.com", "cidade": "Sorocaba/SP", "segmento": "Industria de oleos, gorduras e margarinas"},
                {"nome": "AAK do Brasil", "empresa": "AAK do Brasil Industria e Comercio de Oleos Vegetais LTDA", "email": "marketing.sola@aak.com", "cidade": "Jundiai/SP", "segmento": "Industria de oleos e gorduras especiais"},
                # Industrias de alimentos
                {"nome": "Perfetti Van Melle Brasil", "empresa": "Perfetti Van Melle Brasil LTDA", "email": "contato@perfettivanmelle.com.br", "cidade": "Vinhedo/SP", "segmento": "Industria de balas e guloseimas"},
                {"nome": "Bakels Brasil", "empresa": "Bakels Brasil Ingredientes para Panificacao LTDA", "email": "brazil@bakels.com.br", "cidade": "Vinhedo/SP", "segmento": "Industria de ingredientes para panificacao"},
                {"nome": "Kemin do Brasil", "empresa": "Kemin Industria e Comercio LTDA", "email": "marketing.foodlatam@kemin.com", "cidade": "Valinhos/SP", "segmento": "Industria de ingredientes alimenticios"},
                {"nome": "Theoto S/A", "empresa": "Theoto S/A Industria e Comercio", "email": "sac@theoto.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de produtos alimenticios"},
                {"nome": "Marquespan", "empresa": "Marquespan Industria de Alimentos LTDA", "email": "sac@marquespan.com.br", "cidade": "Tatui/SP", "segmento": "Industria de panificacao (paes congelados)"},
                {"nome": "Flamboia Alimentos", "empresa": "Flamboia Alimentos LTDA", "email": "comercial@flamboia.com.br", "cidade": "Cabreuva/SP", "segmento": "Industria de alimentos"},
                {"nome": "Agrana Fruit Brasil", "empresa": "Agrana Fruit Brasil Industria e Comercio LTDA", "email": "atendimento@agrana.com", "cidade": "Cabreuva/SP", "segmento": "Industria de frutas e ingredientes"},
                {"nome": "Moinho Potenza", "empresa": "Industria Moageira Nova Odessa LTDA", "email": "contato@moinhopotenza.com.br", "cidade": "Hortolandia/SP", "segmento": "Industria de farinhas e moagem"},
                {"nome": "Bem Casado", "empresa": "Bem Casado Industria de Alimentos e Bebidas LTDA", "email": "sac@arrozbemcasado.com.br", "cidade": "Nova Odessa/SP", "segmento": "Industria de arroz e alimentos"},
                {"nome": "Penina Alimentos", "empresa": "Penina Alimentos LTDA", "email": "contato@penina.com.br", "cidade": "Boituva/SP", "segmento": "Industria de alimentos (temperos e especiarias)"},
                # Frigorificos - nicho prioritario (gordura animal + oleo de fritura)
                {"nome": "Frigorifico Cowpig", "empresa": "Frigorifico Cowpig LTDA", "email": "contato@cowpig.com.br", "cidade": "Boituva/SP", "segmento": "Frigorifico (cortes nobres de carne)"},
                # Refeicoes coletivas
                {"nome": "CBR Refeicoes", "empresa": "C.B.R. Fornecedora de Refeicoes LTDA", "email": "fiscal@cbr-refeicoes.com.br", "cidade": "Hortolandia/SP", "segmento": "Refeicoes coletivas"},
                # Frutas processadas
                                {"nome": "Only Fruit", "empresa": "Only Fruit Industria de Alimentos LTDA", "email": "contato@onlyfruit.com.br", "cidade": "Nova Odessa/SP", "segmento": "Industria de alimentos (frutas)"},
                                # --- NOVAS EMPRESAS (adicionadas 24/09 - Melhorador Contínuo #27, MX verificado) ---
                                # Encapsulados/farmaceuticas - Salto mesmo (nicho oleo vegetal limpeza maquinas)
                                {"nome": "Cap-Lab", "empresa": "Cap-Lab", "email": "marketing@cap-lab.com.br", "cidade": "Salto/SP", "segmento": "Laboratorio de encapsulados"},
                                {"nome": "Cellera Farma", "empresa": "Cellera Farma Industria Farmaceutica", "email": "sac@cellerafarma.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria farmaceutica (medicamentos e suplementos)"},
                                {"nome": "Farmoterapica", "empresa": "Farmoterapica", "email": "atendimento@farmoterapica.com.br", "cidade": "Indaiatuba/SP", "segmento": "Industria farmaceutica (solucoes estereis e nutricao parenteral)"},
                                {"nome": "Hero Suplementos", "empresa": "Hero Suplementos", "email": "contato@herosuplementos.com.br", "cidade": "Indaiatuba/SP", "segmento": "Suplementos e encapsulados"},
                                {"nome": "Sorocaps", "empresa": "Sorocaps Industria Farmaceutica LTDA", "email": "comercial@sorocaps.com.br", "cidade": "Sorocaba/SP", "segmento": "Industria farmaceutica (encapsulados)"},
                                # Suplementos/nutraceuticos - Jundiai
                                {"nome": "Hile", "empresa": "Hile Industria de Alimentos (fabrica de suplementos)", "email": "contato@hile.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de suplementos e nutraceuticos (encapsulados, capsulas, gomas)"},
                                {"nome": "WBM", "empresa": "WBM Industria de Suplementos", "email": "contato@wbm.com.br", "cidade": "Jundiai/SP", "segmento": "Industria de suplementos e nutraceuticos (encapsulados)"},
                                # Supermercados - alta conversao
                                {"nome": "Supermercados Sao Vicente", "empresa": "Supermercados Sao Vicente (rede)", "email": "atendimento@svicente.com.br", "cidade": "Piracicaba/SP e regiao", "segmento": "Supermercados (rede)"},
                                # Farmaceutica oleo limpeza maquinas - Sorocaba
                                {"nome": "Ekobe", "empresa": "Ekobe Industria de Nutraceuticos e Cosmeticos LTDA", "email": "contato@ekobe.ind.br", "cidade": "Capela do Alto/SP", "segmento": "Industria de nutraceuticos e cosmeticos (gomas, capsulas, terceirizacao) - NICHO PRIORITARIO"},
                                # Refeicoes coletivas - Campinas/Sorocaba
                                {"nome": "Zuhan Refeicoes", "empresa": "Zuhan Refeicoes Corporativas", "email": "contato@zuhan.com.br", "cidade": "Campinas/SP", "segmento": "Refeicoes coletivas e cozinhas industriais"},
                                {"nome": "Lollos Refeicoes", "empresa": "Lollos Refeicoes Empresariais", "email": "sac@lollos.com.br", "cidade": "Sorocaba/SP", "segmento": "Refeicoes empresariais e cozinha central"},
                                # Rede frango assado - fritura alto volume
                                {"nome": "Rede Frango Assado", "empresa": "Pimenta Verde Alimentos Ltda (Rede Frango Assado)", "email": "sac@redefrangoassado.com.br", "cidade": "Louveira/SP", "segmento": "Rede de restaurantes rotisserie (fritura alto volume)"},
                                # Industria de maioneses/gorduras - vencidos >40%
                                {"nome": "Mareia (Conrail)", "empresa": "Conrail Industria e Comercio de Produtos Alimenticios Ltda", "email": "sac@mareia.com.br", "cidade": "Campo Limpo Paulista/SP", "segmento": "Industria de maioneses e condimentos (food service) - NICHO PRIORITARIO (vencidos >40% gordura)"},
                            ]

def now_iso():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def load_config():
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)

def read_leads():
    if not os.path.exists(LEADS_PATH):
        return []
    with open(LEADS_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_leads(leads):
    with open(LEADS_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(leads)

# --- Lock de arquivo + merge: evita perder linhas em escrita concorrente ---
# (Prospector/Atendente/Estrategista rodam em paralelo; sem lock, o último
#  que grava sobrescreve as linhas dos outros — 5 leads já foram perdidos)
def _acquire_lock(path, timeout=20):
    deadline = time.time() + timeout
    while True:
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            return True
        except FileExistsError:
            if time.time() > deadline:
                return False
            time.sleep(0.3)
        except OSError:
            return False

def _release_lock(path):
    try:
        os.remove(path)
    except OSError:
        pass

def merge_write_leads(novos_em_memoria):
    """Grava leads.csv com lock, mesclando com o que estiver em disco.
    Deduplica por email e renumera ids sequencialmente."""
    lock = LEADS_PATH + ".lock"
    if _acquire_lock(lock):
        try:
            atuais = read_leads()
            existentes = {l.get("email", "").strip().lower() for l in atuais}
            a_adicionar = [l for l in novos_em_memoria
                           if l.get("email", "").strip().lower() not in existentes]
            base_id = max((int(l.get("id") or 0) for l in atuais), default=0)
            for i, l in enumerate(a_adicionar, start=base_id + 1):
                l["id"] = str(i)
            write_leads(atuais + a_adicionar)
            return len(a_adicionar)
        finally:
            _release_lock(lock)
    # Falha ao obter lock: grava direto mesmo assim (melhor que perder o lote)
    write_leads(novos_em_memoria)
    return len(novos_em_memoria)

def find_lead(leads, email_addr):
    for l in leads:
        if l.get("email","").strip().lower() == email_addr.strip().lower():
            return l
    return None

def _plain_from_html(html):
    """Converte HTML em texto puro com quebras de linha preservadas."""
    import re
    t = re.sub(r"<br\s*/?>", "\n", html)
    t = re.sub(r"</p>", "\n\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return t.strip()

def tpl_apresentacao(cfg, lead):
    """Template de apresentação B2B otimizado: <80 palavras, 1 CTA, argumentos em 1 linha cada.
    V2 (19/08): versão curta — cold email longo derruba resposta (1% no lote 1).
    V3 (19/08): ângulo por segmento — indústrias de gorduras/laticínios usam discurso de vencidos.
    V4 (07/09): ângulo SUPERMERCADOS/ATACAREJO — nicho que mais converteu (Savegnago, Sumerbol,
    GoodBom, Rede Boa = 4 dos 7 respondidos reais). Contrato de rede + prova social Madero."""
    g = cfg["empresa"]
    cidade = lead.get("cidade") or "região"
    segmento = (lead.get("segmento") or "alimentação").lower()
    # Ângulo específico: supermercados/atacarejo — padaria+rotisserie+açougue = óleo toda semana
    if any(k in segmento for k in ["supermercado", "supermercados", "atacarejo",
                                        "atacado", "varejo"]):
            return {
                "subject": f"Oleo de fritura da {lead.get('empresa','')} vira renda — coleta na rede toda",
                "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
        <p>Ola, {lead.get('nome','')}.</p>
        <p>Cada loja com padaria, rotisserie e acougue gera <b>oleo de fritura toda semana</b> — e o que sai de graca virou commodity: o mercado global de oleo usado vale <b>US$ 11 bi</b> e deve dobrar com a demanda por biodiesel (Fortune Business Insights).</p>
        <p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinacao correta do oleo de fritura</b> de redes inteiras: coleta programada por loja (semana fixa), bombonas fornecidas, <b>certificado de destinacao (PNRS)</b> e <b>relatorio ESG mensal</b> para a rede — a rede zera o passivo ambiental e ainda recebe pelo material. Pagamos de <b>R$ 1,00 a 2,50 por litro</b>, a vista (PIX) na coleta: cada supermercado com padaria e rotisserie gera de <b>400 a 600 L/mes</b>. Uma rede com 5 lojas como a {lead.get('empresa','')} pode estar gerando <b>2.000 a 3.000 L/mes = R$ 48 mil a R$ 72 mil/ano</b> so com o oleo de fritura.</p>
        <p>Urgencia: a <b>Portaria MME/MMA no 3/2026</b> obriga >=1% de oleo residual no biodiesel a partir de <b>jan/2028</b> — quem fecha contrato agora garante prioridade.</p>
        <p><b>Quantas lojas a rede tem?</b> Com esse numero enviamos o calculo exato. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
        <p>Abraco,<br><b>{g['nome']}</b> · Compra de oleo e gordura vegetal usados · {cidade}</p>
        </div>"""
        }
    # Ângulo específico: ÓLEO VEGETAL VENCIDO — produto carro-chefe (indústrias,
    # distribuidoras, atacadistas, supermercados com estoque de óleo vencido)
    if any(k in segmento for k in ["oleo", "óleo", "oleos", "óleos", "soja", "girassol",
                                    "canola", "milho", "azeite", "refino", "esmagamento"]):
        return {
            "subject": f"Óleo vegetal vencido parado no estoque? Destinamos com certificado ({cidade})",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Estoque de <b>óleo vegetal vencido</b> (garrafas, potes, tambores) é passivo: ocupa espaço, vira prejuízo e precisa de destinação segura — sem risco de desvio e com comprovação legal.</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta de óleo vegetal vencido</b> para <b>biodiesel</b>, com <b>descaracterização completa (cortesia)</b>, <b>certificado de destinação</b> (ANVISA/Receita) e coleta programada. Você zera o passivo e ainda recebe pelo material — <b>pagamento à vista (PIX) na coleta</b>, sem burocracia.</p>
<p><b>Quanto de óleo vencido vocês têm parado hoje?</b> Mande o volume (litros) que avaliamos e retornamos com a proposta. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Destinação de óleo vegetal vencido · {cidade}</p>
</div>"""
        }
    # Ângulo específico V8: FÁBRICAS DE BATATA — fritura industrial em volume (>200L/mês)
    if any(k in segmento for k in ["batata", "chips", "salgadinho", "congelada",
                                    "palha", "fritas", "batata frita", "snack"]):
        return {
            "subject": f"Óleo de fritura da {lead.get('empresa','')} vira receita contínua — coleta programada",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Fábricas que fritam batata em escala industrial geram <b>centenas a milhares de litros de óleo usado por mês</b> — e esse óleo, que hoje sai de graça, virou commodity energética: o mercado global de óleo de cozinha usado (UCO) vale <b>US$ 8 bi</b> e deve dobrar com a demanda por biodiesel e SAF.</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta do óleo de fritura industrial</b> de fábricas de batata: coleta programada (semana fixa), bombonas fornecidas, <b>certificado de destinação (PNRS)</b> e relatório de impacto ambiental. Sua fábrica zera o passivo e ainda recebe mensalmente pelo material.</p>
<p>E há urgência: a <b>Portaria MME/MMA nº 3/2026</b> obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b> — a demanda por óleo usado vai disparar. Quem fecha contrato agora garante prioridade e preço estável.</p>
<p><b>Quantos litros de óleo de fritura sua produção gera por mês?</b> Com esse número enviamos a avaliação. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Destinação de óleo de fritura industrial · {cidade}</p>
</div>"""
        }
    # Ângulo específico: indústrias que geram vencidos com >40% de gordura (material oleoso)
    if any(k in segmento for k in ["margarina", "manteiga", "maionese", "gordura",
                                    "laticinio", "creme vegetal", "oleos vegetais",
                                    "laticínios", "gorduras"]):
        return {
            "subject": f"Destinação de vencidos com gordura — resolvemos seu passivo ({cidade})",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Indústrias de {segmento} têm um problema caro: <b>produtos vencidos</b> (margarina, manteiga, maionese, gordura vegetal) que precisam de destinação segura — sem voltar ao mercado e sem passivo no CNPJ.</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta de resíduos com &gt;40% de gordura</b> para <b>biodiesel</b>, com <b>descaracterização completa (cortesia)</b> e <b>certificado de destinação</b> (ANVISA/Receita). Você zera o passivo e ainda recebe um valor pelo material.</p>
<p><b>O que vocês têm disponível hoje?</b> Mande a relação do material (tipo e volume) que avaliamos e retornamos com a proposta. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Destinação de resíduos com &gt;40% de gordura · {cidade}</p>
</div>"""
        }
    # Ângulo específico: indústrias que lavam/lubrificam máquinas com óleo vegetal
    # (encapsulados, farmacêuticas, nutracêuticos, suplementos, cosméticos, manipuladoras)
    # — case real Catalent (Indaiatuba/Sorocaba) como prova social
    if any(k in segmento for k in ["farmaceutica", "farmacêutica", "encapsulad", "nutraceutic",
                                    "nutracêutic", "suplemento", "cosmetico", "cosmético",
                                    "manipula", "farmaco", "pharma", "capsula"]):
        return {
            "subject": f"Óleo vegetal usado na limpeza das máquinas da {lead.get('empresa','')} — compramos",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Indústrias de {segmento} usam <b>óleo vegetal na limpeza e lubrificação das máquinas</b> de produção — e esse óleo, depois de usado, tem valor. Já coletamos para a <b>Catalent</b> (unidades de Indaiatuba e Sorocaba), uma das maiores fabricantes de cápsulas do mundo.</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta do óleo vegetal usado de limpeza de máquinas</b>, com coleta programada, bombonas fornecidas e <b>certificado de destinação + MTR</b> para a auditoria da Anvisa. Já coletamos para a <b>Catalent</b> (Indaiatuba e Sorocaba), uma das maiores fabricantes de cápsulas do mundo.</p>
<p><b>Quanto de óleo vegetal a produção usa por mês?</b> Com esse número enviamos a avaliação. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Compra de óleo vegetal usado industrial · {cidade}</p>
</div>"""
        }
    # Ângulo específico: HOTÉIS/RESORTS/POUSADAS — cozinha industrial de pensão completa
    # (café da manhã + almoço + jantar todos os dias = fritura constante o ano todo)
    # V6 (12/09): 5 hotéis-fazenda de Itu/região adicionados à fila — nicho sub-coberto,
    # contrato único de coleta + sensibilidade ESG do setor hoteleiro.
    if any(k in segmento for k in ["hotel", "resort", "pousada", "pensao", "pensão",
                                    "hospedagem", "spa"]):
        return {
            "subject": f"Óleo de fritura do {lead.get('empresa','')} vira receita — coleta programada",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Cozinha de hotel com pensão completa é <b>fritura todos os dias</b> (café da manhã, almoço e jantar) — e o óleo usado, que hoje sai de graça, virou commodity: o mercado global de óleo de cozinha usado (UCO) vale <b>US$ 8,6 bi</b> e dobra com a demanda por biodiesel (Fortune Business Insights).</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta</b> do óleo de fritura de hotéis: coleta programada (semana fixa), bombonas fornecidas, <b>certificado de destinação (PNRS)</b> e relatório ESG mensal — argumento forte para o setor de hospitalidade, que presta contas de sustentabilidade. O hotel zera o passivo ambiental e ainda recebe pelo material.</p>
<p>Urgência: a <b>Portaria MME/MMA nº 3/2026</b> obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b> — quem fecha contrato agora garante prioridade.</p>
<p><b>Quanto a cozinha gera por mês (litros)?</b> Com esse número enviamos a avaliação. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {cidade}</p>
</div>"""
        }
    # Ângulo específico: HOSPITAIS/CLÍNICAS/SAÚDE — cozinha hospitalar (nutrição
    # de pacientes + refeitório) frita todos os dias; setor presta contas de
    # sustentabilidade (certificações ONA/Green Hospital) e auditoria de resíduos.
    # V7 (16/09): HSV Jundiaí + Unimed Sorocaba adicionados à fila — nicho novo,
    # canal ouvidoria/sustentabilidade responde gente (lição Oba/Arcor invertida).
    if any(k in segmento for k in ["hospital", "hospitais", "saude", "saúde", "clinica",
                                    "clínica", "unimed", "maternidade", "sanatorio",
                                    "sanatório", "oncologia", "pronto socorro",
                                    "assistencia medica", "assistência médica"]):
        return {
            "subject": f"Óleo de fritura da cozinha do {lead.get('empresa','')} — coleta com certificado e relatório ESG",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
<p>Olá, {lead.get('nome','')}.</p>
<p>Cozinha hospitalar é <b>fritura todos os dias</b> (nutrição de pacientes + refeitório) — e o óleo usado, que hoje sai de graça, virou commodity: o mercado global de óleo de cozinha usado (UCO) vale <b>US$ 8,6 bi</b> e dobra com a demanda por biodiesel (Fortune Business Insights).</p>
<p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta do óleo de fritura</b> de hospitais: coleta programada (semana fixa), bombonas fornecidas, <b>certificado de destinação (PNRS) + MTR</b> e <b>relatório ESG mensal</b> — argumento forte para o setor de saúde, que presta contas em auditorias de sustentabilidade e licenciamento. O hospital zera o passivo ambiental e ainda recebe pelo material.</p>
<p>Urgência: a <b>Portaria MME/MMA nº 3/2026</b> obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b> — quem fecha contrato agora garante prioridade.</p>
<p><b>Quanto a cozinha gera por mês (litros)?</b> Com esse número enviamos a avaliação. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
<p>Abraço,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {cidade}</p>
</div>"""
        }
    return {
            "subject": f"Óleo usado da {lead.get('empresa','')} vale dinheiro — até R$ 14,4 mil/ano",
            "html": f"""<div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#1c2a21">
    <p>Olá, {lead.get('nome','')}.</p>
    <p>O óleo de fritura da <b>{lead.get('empresa','')}</b> hoje sai de graça — mas virou commodity: o mercado global de óleo de cozinha usado (UCO) vale <b>US$ 11 bi</b> e deve dobrar até 2030 com a demanda por biodiesel e combustível de aviação.</p>
    <p>A <b>{g['nome']}</b>, de {cidade}, faz a <b>destinação correta desse material</b> — coleta programada, bombonas fornecidas e <b>certificado de destinação (PNRS)</b>: você zera o passivo ambiental e ainda recebe pelo óleo. Um estabelecimento que gera <b>600 L/mês recebe R$ 14,4 mil/ano</b> (R$ 2,00/L) — sem custo de logística. Redes grandes já tratam isso como receita: o Grupo Madero fechou contrato de <b>55 mil L/mês</b> com coletora (270 restaurantes).</p>
    <p>E há urgência: a <b>Portaria MME/MMA nº 3/2026</b> obriga ≥1% de óleo residual no biodiesel a partir de <b>jan/2028</b> — o Brasil já exporta óleo usado para os EUA (1,4 mi t importadas em 2023) e quem fecha contrato agora garante prioridade antes da corrida pela matéria-prima.</p>
    <p><b>Quanto vocês geram por mês (litros ou kg)?</b> Com esse número enviamos a avaliação ainda esta semana. WhatsApp: <b>{g['telefone_whatsapp']}</b>.</p>
    <p style="font-size:12px;color:#888">PS: Simulador em <a href="{g.get('site','https://masteroleo.eco.br')}#calculadora" style="color:#1a6b3c">masteroleo.eco.br/#calculadora</a> — descubra quanto seu resíduo vale em 30 segundos.</p>
    <p>Abraço,<br><b>{g['nome']}</b> · Compra de óleo e gordura vegetal usados · {cidade}</p>
    </div>"""}

def prospecao(args):
    cfg = load_config()
    e = cfg["email"]
    if "COLOQUE" in str(e.get("usuario","")):
        sys.exit("ERRO: configure bot/config.json com email e senha de app (Gmail).")
    
    leads = read_leads()
    existing = {l.get("email","").strip().lower() for l in leads}
    
    ctx = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL(e["smtp_host"], e["smtp_port"], context=ctx, timeout=30)
    smtp.login(e["usuario"], e["senha_app"].replace(" ",""))
    
    enviados = 0
    for lead_info in EMPRESAS:
        email_addr = lead_info["email"].strip().lower()
        if args.list:
            status = "✅ já cadastrado" if email_addr in existing else "⬜ novo"
            print(f"{status} | {lead_info['empresa']:40s} | {email_addr:35s} | {lead_info['cidade']}")
            continue
        
        if email_addr in existing and not args.force:
            # verifica se o lead existente deu bounce — não reenviar para inválidos
            existente = find_lead(leads, email_addr)
            if existente and existente.get("status") == "bounce":
                print(f"⏭️  Bounce anterior: {lead_info['empresa']} <{email_addr}> — pulando")
            else:
                print(f"⏭️  Já existe: {lead_info['empresa']} <{email_addr}>")
            continue
        
        if args.dry_run:
            print(f"[DRY-RUN] Enviaria para {lead_info['empresa']} <{email_addr}>")
            enviados += 1
            continue
        
        # Envia email
        tpl = tpl_apresentacao(cfg, lead_info)
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr((str(Header(cfg["email"]["remetente_nome"], "utf-8")), e["usuario"]))
        msg["To"] = email_addr
        msg["Subject"] = Header(tpl["subject"], "utf-8")
        msg["Message-ID"] = make_msgid()
        msg.attach(MIMEText(_plain_from_html(tpl["html"]).strip(), "plain", "utf-8"))
        msg.attach(MIMEText(tpl["html"], "html", "utf-8"))
        
        try:
            smtp.sendmail(e["usuario"], [email_addr], msg.as_string())
            print(f"✅ Enviado: {lead_info['empresa']} <{email_addr}>")
            
            # Adiciona ao leads.csv
            new_lead = {"id": str(len(leads)+1), "nome": lead_info["nome"],
                        "empresa": lead_info["empresa"], "email": email_addr,
                        "tipo": "industria" if "industria" in lead_info["segmento"].lower() else "outro",
                        "volume": "", "segmento": lead_info.get("segmento",""),
                        "cidade": lead_info.get("cidade",""),
                        "fonte": "prospeccao", "status": "novo",
                        "criado_em": now_iso(), "boas_vindas_em": "",
                        "follow1_em": "", "follow2_em": "", "follow3_em": "",
                        "apresentacao_msgid": msg["Message-ID"],
                        "ultima_resposta": "", "respondido_em": "", "respondido_por": ""}
            leads.append(new_lead)
            existing.add(email_addr)
            enviados += 1
            time.sleep(5)  # rate limit
        except Exception as ex:
            print(f"❌ Falha: {lead_info['empresa']} <{email_addr}> — {str(ex)[:120]}")
    
    if not args.dry_run and not args.list and enviados > 0:
        gravados = merge_write_leads(leads)
        print(f"\n{enviados} email(s) enviado(s); {gravados} registrado(s) no leads.csv (merge com lock).")
    elif args.dry_run:
        print(f"\nDRY-RUN — {enviados} envio(s) simulado(s) (nada foi enviado).")
    
    smtp.quit()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Prospecção ativa Master Óleo")
    ap.add_argument("--dry-run", action="store_true", help="simula sem enviar")
    ap.add_argument("--list", action="store_true", help="lista empresas e emails candidatos")
    ap.add_argument("--force", action="store_true", help="reenvia mesmo se já cadastrado")
    args = ap.parse_args()
    prospecao(args)