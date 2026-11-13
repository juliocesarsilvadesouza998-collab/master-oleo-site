#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prospector de reposição — Master Óleo (Atendente IA, 02/11/2026)

Motivo: fila_prospeccao_extra.json zerou (0 pendentes). Este script descobre
empresas NOVAS por busca web (Bing), extrai email do site oficial, valida MX
(descartando self-hosted, regra do projeto), deduplica contra leads/bounces/fila
e grava em fila_prospeccao_extra.json.

Uso: python prospectar_novos.py [--max-por-query 6] [--queries N]
"""
import argparse, csv, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")
LEADS = os.path.join(BASE, "leads.csv")
BOUNCES = os.path.join(BASE, "bounces.json")

# Filtro de qualificação de alvo (fonte única: filtros_oleo.py).
# Laticínios/queijarias estão fora do alvo (sem óleo separável) — decisão 12/11/2026.
sys.path.insert(0, BASE)
from filtros_oleo import motivo_exclusao  # noqa: E402

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# (query, cidade, segmento)
ALVOS = [
    ("supermercado Taubate SP site oficial contato", "Taubate/SP", "Supermercados (rede/mix - padaria, rotisserie, acougue: fritura continua + oleo vencido)"),
    ("supermercado Sao Jose dos Campos contato", "Sao Jose dos Campos/SP", "Supermercados (rede/mix - padaria, rotisserie: fritura continua + oleo vencido)"),
    ("supermercado Jacarei SP contato", "Jacarei/SP", "Supermercado local (padaria/rotisserie - fritura continua)"),
    ("supermercado Mogi das Cruzes contato", "Mogi das Cruzes/SP", "Supermercados (rede/mix - padaria, rotisserie: fritura continua)"),
    ("supermercado Botucatu contato", "Botucatu/SP", "Supermercado local (padaria/rotisserie - fritura continua)"),
    ("supermercado Itapetininga contato", "Itapetininga/SP", "Supermercado local (padaria/rotisserie - fritura continua)"),
    ("supermercado Limeira SP contato", "Limeira/SP", "Supermercados (rede/mix - padaria, rotisserie: fritura continua)"),
    ("supermercado Americana SP contato", "Americana/SP", "Supermercados (rede/mix - padaria, rotisserie: fritura continua)"),
    ("supermercado Rio Claro SP contato", "Rio Claro/SP", "Supermercados (rede/mix - padaria, rotisserie: fritura continua)"),
    ("atacadista distribuidora de alimentos Campinas contato", "Campinas/SP", "Distribuidora/atacadista de alimentos (estoque de oleo vegetal vencido + fritura)"),
    ("industria de margarina e gordura vegetal Sao Paulo contato", "Sao Paulo/SP", "Industria de margarinas/gorduras vegetais (vencidos >40% gordura - descaracterizacao)"),
    ("fabrica de maionese e molhos contato comercial", "Sao Paulo/SP", "Industria de maionese/molhos (vencidos emulsionados - descaracterizacao)"),
    ("empresa de alimentacao coletiva refeitorio industrial Campinas", "Campinas/SP", "Alimentacao coletiva/refeitorio industrial (cozinha industrial - fritura alto volume)"),
    ("cozinha industrial refeicoes coletivas Sorocaba", "Sorocaba/SP", "Alimentacao coletiva/refeitorio industrial (cozinha industrial - fritura alto volume)"),
    ("hotel fazenda eventos Campinas contato", "Campinas/SP", "Hotel fazenda (cozinha industrial - fritura continua)"),
    ("padaria industria panificacao Campinas contato comercial", "Campinas/SP", "Panificacao industrial (fritura continua + oleo/margarina vencida)"),
    ("frigorifico industria de carnes Sorocaba contato", "Sorocaba/SP", "Frigorifico (gordura animal/vegetal residual)"),
    ("industria de alimentos Piracicaba contato comercial", "Piracicaba/SP", "Industria de alimentos (oleo vegetal vencido + fritura)"),
    ("industria de alimentos Jundiai contato comercial", "Jundiai/SP", "Industria de alimentos (oleo vegetal vencido + fritura)"),
    ("distribuidora de oleos e gorduras vegetais contato comercial", "Sao Paulo/SP", "Industria/distribuidora de oleos e gorduras (nicho prioritario)"),
    ("fabrica de biscoitos e salgadinhos Campinas contato", "Campinas/SP", "Industria de biscoitos/snacks (fritura industrial - alto volume)"),
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
BAD_DOM = ("sentry.io", "wixpress.com", "example.com", "dominio.com", "seudominio",
           "domain.com", "email.com", "site.com.br", "exemplo.com", "teste.com",
           "googlemail.com", "cloudflare", "w3.org", "schema.org")
BAD_LOCAL = ("noreply", "no-reply", "naoresponda", "postmaster", "abuse", "webmaster",
             "privacidade", "lgpd", "rh@", "curriculo", "curriculum", "trabalheconosco")
PREF = ("comercial", "contato", "vendas", "sac", "atendimento", "fale", "info",
        "administrativo", "compras", "financeiro", "adm")
SKIP_DOM = ("facebook", "instagram", "linkedin", "youtube", "twitter", "mercadolivre",
            "reclameaqui", "solutudo", "apontador", "encontrapadarias", "ifood",
            "wikipedia", "gov.br", "sebrae", "guiasp", "telelistas", "tripadvisor",
            "booking", "cnpj.biz", "econodata", "jusbrasil", "glassdoor", "infojobs",
            "vagas", "glass", "guiamais", "b2w", "amazon", "shopee", "magazineluiza",
            "sitemercado", "tudocelular", "blog", "noticias", "g1.", "uol.com.br",
            "estadao", "folha", "terra.com.br", "olx", "zapimoveis",
            # diretórios/agregadores: nunca têm o e-mail do comercial
            "maiscnpj", "buscadeempresas", "mapaindustrial", "pesquisaempresas",
            "guiatelefone", "eguias", "guiaja", "guiataubate", "paginaamarela",
            "applocal", "encontraempresas", "cnpjservices", "casadosdados",
            "hoteis.com", "decolar", "hotels.com", "hotel.com.br", "skyscanner",
            "trivago", "hotelinsite", "cnpq.br", "lattes", "ifood.com.br",
            "olhonocnpj", "empresascnpj", "consulteempresas", "sociais")


def get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "pt-BR,pt;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read(700000)
        ctype = r.headers.get("Content-Type", "")
    enc = "utf-8"
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    if m:
        enc = m.group(1)
    return raw.decode(enc, "replace")


def serper_domains(query, n=20):
    """Busca via Serper.dev (Google). Ativa quando existe SERPER_API_KEY (env) ou
    "serper_api_key" no config.json. Plano gratuito: 2.500 buscas — é a via que
    devolve resultado regional correto (DDG/Mojeek bloqueiam este IP e o Bing
    entrega cache de outra região)."""
    key = os.environ.get("SERPER_API_KEY", "")
    if not key:
        try:
            with open(os.path.join(BASE, "config.json"), encoding="utf-8") as f:
                key = (json.load(f).get("serper_api_key") or "").strip()
        except Exception:
            key = ""
    if not key:
        return []
    body = json.dumps({"q": query, "gl": "br", "hl": "pt-br", "num": n}).encode()
    req = urllib.request.Request("https://google.serper.dev/search", data=body,
                                 headers={"X-API-KEY": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            data = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        print(f"  (serper falhou: {type(e).__name__})")
        return []
    out = []
    for item in data.get("organic", []):
        h = re.sub(r"^https?://", "", item.get("link", "")).split("/")[0].lower().replace("www.", "")
        if h and h not in out and not any(s in h for s in SKIP_DOM):
            out.append(h)
    return out


def bing_domains(query):
    """Retorna domínios (hosts) dos resultados orgânicos — Serper > DDG > Bing."""
    serper = serper_domains(query)
    if serper:
        return serper[:12]
    already = set()
    out = []
    for name, urlfmt, cite_re in [
        ("DDG", "https://html.duckduckgo.com/html/?q={q}&kl=br-pt", r'uddg=([^&"]+)'),
        ("Bing", "https://www.bing.com/search?q={q}&mkt=pt-BR&setmkt=pt-BR&cc=br", r'<cite[^>]*>(.*?)</cite>'),
    ]:
        try:
            html = get(urlfmt.replace("{q}", urllib.parse.quote(query)), 25)
        except Exception:
            continue
        if name == "DDG":
            for l in re.findall(cite_re, html):
                u = urllib.parse.unquote(l)
                h = re.sub(r"^https?://", "", u).split("/")[0].lower().replace("www.", "")
                if h and h not in already and not any(s in h for s in SKIP_DOM):
                    already.add(h)
                    out.append(h)
        else:
            for c in re.findall(cite_re, html, re.S):
                txt = re.sub(r"<[^>]+>", "", c).replace(" ", "").strip()
                hh = re.sub(r"^https?://", "", txt).split("/")[0].lower().replace("www.", "")
                if hh and hh not in already and not any(s in hh for s in SKIP_DOM):
                    already.add(hh)
                    out.append(hh)
        if out:
            break  # DDG usually better; para se achou algo
    return out[:12]


def _norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def _extrair(html):
    out = []
    for em in EMAIL_RE.findall(html):
        em = em.strip(".,;:()<>\"'").lower()
        if em.startswith("//"):
            continue
        local, _, dom = em.partition("@")
        if not dom or any(b in dom for b in BAD_DOM):
            continue
        if any(b.strip("@") in local for b in BAD_LOCAL):
            continue
        if re.search(r"\.(png|jpe?g|gif|webp|svg|css|js)$", dom):
            continue
        if em not in out:
            out.append(em)
    return out


def site_emails(host, cidade=""):
    """Crawl homepage + páginas de contato buscando e-mails.

    Só aceita e-mail quando o site confirma a cidade-alvo (evita pegar empresa
    de outro estado — o Bing geolocaliza mal e devolve resultado fora da região).
    Retorna (emails, cidade_confirmada).
    """
    base = "https://" + host
    found = []
    html_all = ""
    cidade_n = _norm(cidade.split("/")[0])
    cidade_ok = False
    pages = ["", "/contato", "/contato/", "/fale-conosco", "/faleconosco",
             "/quem-somos", "/sobre", "/institucional", "/atendimento"]
    for p in pages:
        try:
            html_all += get(base + p, 15)
        except Exception:
            continue
        if cidade_n and cidade_n in _norm(html_all):
            cidade_ok = True
        for em in _extrair(html_all):
            if em not in found:
                found.append(em)
        # já achou e-mail "comercial" e confirmou a cidade -> não precisa seguir
        if cidade_ok and any(em.startswith(PREF) for em in found):
            break
        if len(html_all) > 900000:
            break
    # ordena por preferência de prefixo comercial
    def score(em):
        for i, p in enumerate(PREF):
            if em.startswith(p):
                return i
        return 99
    found.sort(key=score)
    return found, cidade_ok


def tem_mx(dominio):
    try:
        r = subprocess.run(["nslookup", "-type=MX", dominio], capture_output=True, timeout=25)
        out = (r.stdout + r.stderr).decode("latin-1", "replace")
        mxs = re.findall(r"mail exchanger = (\S+)", out, re.I)
        if not mxs:
            return False, ""
        mx = mxs[0].rstrip(".")
        # self-hosted (MX = próprio domínio) rejeita SMTP externo -> risco de bounce
        if mx.lower().endswith(dominio.lower()):
            return False, mx
        return True, mx
    except Exception:
        return False, ""


def nome_empresa(host):
    n = host.split(".")[0]
    n = n.replace("-", " ").replace("_", " ").strip()
    return " ".join(w.capitalize() for w in n.split())


def carregar_conhecidos():
    conhecidos = set()
    if os.path.exists(LEADS):
        with open(LEADS, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                e = (r.get("email") or "").strip().lower()
                if e:
                    conhecidos.add(e)
    for path in (FILA, os.path.join(BASE, "emails_existentes.txt")):
        if not os.path.exists(path):
            continue
        try:
            if path.endswith(".json"):
                for it in json.load(open(path, encoding="utf-8-sig")):
                    e = (it.get("email") or "").strip().lower()
                    if e:
                        conhecidos.add(e)
            else:
                for line in open(path, encoding="utf-8-sig", errors="replace"):
                    line = line.strip().lower()
                    if "@" in line:
                        conhecidos.add(line)
        except Exception:
            pass
    bounces = set()
    if os.path.exists(BOUNCES):
        try:
            bounces = {b.strip().lower() for b in json.load(open(BOUNCES, encoding="utf-8"))}
        except Exception:
            bounces = set()
    return conhecidos, bounces


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-por-query", type=int, default=5)
    ap.add_argument("--max-queries", type=int, default=len(ALVOS))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    conhecidos, bounces = carregar_conhecidos()
    print(f"Conhecidos: {len(conhecidos)} emails | bounces: {len(bounces)}")

    tarefas = []  # (host, cidade, segmento)
    vistos = set()
    for query, cidade, seg in ALVOS[:args.max_queries]:
        hosts = bing_domains(query)[:args.max_por_query]
        print(f"[busca] {query[:52]:<52} -> {len(hosts)} dominios")
        for h in hosts:
            if h in vistos:
                continue
            vistos.add(h)
            tarefas.append((h, cidade, seg))
        time.sleep(1.5)

    print(f"\nCrawl de {len(tarefas)} sites...")
    with ThreadPoolExecutor(max_workers=8) as ex:
        emails_por_host = list(ex.map(lambda t: (t, site_emails(t[0], t[1])), tarefas))

    novas, sem_email, sem_mx, ja, fora_cidade, fora_alvo = [], 0, 0, 0, 0, 0
    for (host, cidade, seg), (emails, cidade_ok) in emails_por_host:
        if not emails:
            sem_email += 1
            continue
        if not cidade_ok:
            fora_cidade += 1
            print(f"  ✖ fora da cidade: {host} [{cidade}] — {emails[0]} descartado")
            continue
        escolhido = None
        for em in emails:
            if em in bounces:
                continue
            if em in conhecidos:
                continue
            escolhido = em
            break
        if not escolhido:
            ja += 1
            continue
        ok, mx = tem_mx(escolhido.split("@")[-1])
        if not ok:
            sem_mx += 1
            print(f"  ⚠️  sem MX/self-hosted: {escolhido} ({mx or 'sem registro'})")
            continue
        reg = {"nome": nome_empresa(host), "empresa": nome_empresa(host) + " (" + host + ")",
               "email": escolhido, "cidade": cidade, "segmento": seg,
               "fonte": "prospector-web-2026-11-02"}
        _fora = motivo_exclusao(reg["nome"], reg["empresa"], reg["segmento"])
        if _fora:
            fora_alvo += 1
            print(f"  ⛔ fora do alvo ({_fora}): {host} — não entra na fila")
            continue
        novas.append(reg)
        conhecidos.add(escolhido)
        print(f"  ✅ {reg['empresa'][:48]:<48} <{escolhido}> MX={mx}")

    print(f"\nResumo: {len(novas)} novas | {sem_email} sem email no site | "
          f"{fora_cidade} fora da cidade | {sem_mx} sem MX valido | {ja} ja conhecidas | "
          f"{fora_alvo} fora do alvo (laticinio/nao-oleoso)")

    if not novas:
        return
    if args.dry_run:
        print("[DRY-RUN] nada gravado")
        return
    fila = json.load(open(FILA, encoding="utf-8")) if os.path.exists(FILA) else []
    fila.extend(novas)
    with open(FILA, "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=2)
    print(f"fila_prospeccao_extra.json: {len(fila)} registros (+{len(novas)})")


if __name__ == "__main__":
    main()
