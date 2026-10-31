#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — Bot de SEO (ranqueamento no Google)
==================================================
Monitora e melhora o ranqueamento do site masteroleo.eco.br no Google,
com foco em palavras-chave locais do negócio (coleta de óleo usado,
descaracterização de vencidos, compra de margarina vencida etc.).

O que faz em cada execução:
1. Checa o site no ar (HTTP 200)
2. Verifica palavras-chave alvo e sua presença no conteúdo do site
3. Verifica SEO técnico (title, description, canonical, sitemap, robots)
4. Gera relatório de status e registra histórico em equipe/seo.json
5. Recomenda/gera conteúdo novo (blocos de texto otimizados) se necessário

Uso:
  python seo_bot.py          # diagnóstico completo + relatório
  python seo_bot.py --check  # só verificação rápida (exit 0 = ok, 1 = problema)
"""
import argparse, datetime, json, os, re, ssl, sys, time, urllib.request, urllib.error

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
SITE = "https://masteroleo.eco.br"
SITE_DIR = os.path.join(ROOT, "deploy-vercel")
SEO_LOG = os.path.join(BASE, "..", "equipe", "seo.json")

# Palavras-chave alvo (locais, alto intenção de compra) + onde devem aparecer
PALAVRAS_CHAVE = [
    "coleta de óleo usado salto sp",
    "coleta de óleo de cozinha usado salto",
    "compra de óleo usado",
    "descaracterização de alimentos vencidos",
    "margarina vencida",
    "manteiga vencida",
    "maionese vencida",
    "compra de gordura vegetal usada",
    "óleo usado biodiesel",
    "descarte de óleo de cozinha salto",
    # Nicho industrial: limpeza de máquinas com óleo vegetal
    "óleo vegetal limpeza de máquinas",
    "óleo vegetal usado máquinas encapsulados",
    "coleta de óleo vegetal industrial",
    "óleo de limpeza de máquinas farmacêuticas",
    # Blog/artigos (long-tail)
    "quanto vale o óleo de cozinha usado",
    "preço do óleo usado por litro",
    "quem compra margarina vencida",
    "quem compra manteiga vencida",
    "o que é descaracterização de alimentos",
    "destruição de produtos vencidos",
    "vender óleo de cozinha usado",
    "óleo vegetal usado industrial",
]

def checar_site(url):
    """Retorna True se o site responde 200."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200, r.status
    except urllib.error.URLError as e:
        # Certificado válido mas store local desatualizado (Windows) gera
        # falso negativo — refaz sem verificação para não mascarar o status real.
        if isinstance(e.reason, ssl.SSLError):
            ctx = ssl._create_unverified_context()
            try:
                with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                    return r.status == 200, r.status
            except Exception as e2:
                return False, str(e2)[:60]
        return False, str(e)[:60]
    except Exception as e:
        return False, str(e)[:60]

def ler_arquivos_site():
    """Lê todos os HTML do site para análise de conteúdo (recursivo, inclui blog/)."""
    textos = {}
    if not os.path.isdir(SITE_DIR):
        return textos
    for root, _, files in os.walk(SITE_DIR):
        for fn in files:
            if fn.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, fn), SITE_DIR)
                try:
                    with open(os.path.join(root, fn), encoding="utf-8") as f:
                        textos[rel] = f.read().lower()
                except Exception:
                    pass
    return textos

def verificar_seo_tecnico(textos):
    """Checagens técnicas básicas de SEO on-page."""
    problemas = []
    for fn, html in textos.items():
        if "<title>" not in html or "</title>" not in html:
            problemas.append(f"{fn}: sem <title>")
        if 'name="description"' not in html:
            problemas.append(f"{fn}: sem meta description")
        if 'rel="canonical"' not in html:
            problemas.append(f"{fn}: sem canonical")
        if fn == "index.html" and 'application/ld+json' not in html:
            problemas.append("index.html: sem Schema.org (JSON-LD) — relevante para rich snippets")
    return problemas

def gerar_schema_jsonld():
    """Gera Schema.org JSON-LD para o site (LocalBusiness)."""
    return {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Master Óleo",
        "description": "Compra de óleo de cozinha usado, gordura vegetal usada e resíduos vencidos com mais de 40% de gordura (margarina, manteiga, maionese) para biodiesel. Descaracterização e coleta com certificado.",
        "url": "https://masteroleo.eco.br",
        "telephone": "+5511967859631",
        "address": {"@type": "PostalAddress", "addressLocality": "Salto", "addressRegion": "SP", "addressCountry": "BR"},
        "geo": {"@type": "GeoCoordinates", "latitude": -23.2010, "longitude": -47.2939},
        "openingHours": "Mo-Sa 08:00-19:00",
        "priceRange": "$$",
        "sameAs": []
    }

def _normalizar(s):
    """Remove acentos, separa por não-alfanumérico (Salto/SP → 'salto sp') e minúsculas."""
    import unicodedata, re as _re
    s = s.lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = _re.sub(r"[^a-z0-9]+", " ", s)
    return s

def _kw_presente(kw, textos):
    """Busca flexível: todos os tokens da keyword aparecem em ordem, numa janela curta
    (até 3 palavras extras entre o primeiro e o último) no texto normalizado.
    Aceita variações ('de', 'em', plural, Salto/SP) sem exigir substring exata."""
    alvo = _normalizar(kw)
    tokens = alvo.split()
    if not tokens:
        return False
    if len(tokens) == 1:
        return any(alvo in _normalizar(h) for h in textos.values())
    for html in textos.values():
        norm = _normalizar(html).split()
        for i in range(len(norm) - len(tokens) + 1):
            janela = norm[i:i + len(tokens) + 3]
            pos = []
            j = 0
            ok = True
            for t in tokens:
                try:
                    k = janela.index(t, j)
                except ValueError:
                    ok = False
                    break
                pos.append(k)
                j = k + 1
            if ok and pos == sorted(pos):
                return True
    return False

def _bing_resultados(kw, timeout=25):
    """Top 20 do Bing via RSS (mais limpo que raspar o HTML: o HTML devolve
    blocos genéricos quando o Bing detecta acesso automatizado).
    Retorna lista de tuplas (url, titulo)."""
    import urllib.parse as _up
    url = ("https://www.bing.com/search?q=" + _up.quote(kw)
           + "&format=rss&count=20&setlang=pt-BR&cc=BR")
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", "replace")
    itens = []
    for it in re.findall(r"<item>(.*?)</item>", raw, re.S):
        link = re.search(r"<link>(.*?)</link>", it, re.S)
        titulo = re.search(r"<title>(.*?)</title>", it, re.S)
        if link:
            itens.append((link.group(1).strip(), titulo.group(1).strip() if titulo else ""))
    return itens


def _relevante(kw, itens):
    """True se a SERP parece corresponder à keyword (evita falso 'não ranqueia'
    quando o Bing devolve uma SERP genérica)."""
    import unicodedata
    def norm(s):
        s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()
        return s.lower()
    tokens = [t for t in re.findall(r"[a-z0-9]{4,}", norm(kw))]
    if not tokens:
        return True
    texto = norm(" ".join(t for _, t in itens))
    return sum(1 for t in tokens if t in texto) >= max(1, len(tokens) // 2)


def checar_posicao_bing(kw, timeout=25):
    """Retorna dict: pos (1-based ou None), resultados (nº), relevante (bool),
    erro (bool). 'relevante=False' significa SERP suspeita -> inconclusivo."""
    itens = []
    erro = False
    try:
        itens = _bing_resultados(kw, timeout)
    except Exception:
        erro = True
    if not itens:
        return {"pos": None, "resultados": 0, "relevante": False, "erro": erro}
    pos = None
    for i, (link, _t) in enumerate(itens, 1):
        if "masteroleo.eco.br" in link:
            pos = i
            break
    return {"pos": pos, "resultados": len(itens), "relevante": _relevante(kw, itens), "erro": erro}

def main():
    ap = argparse.ArgumentParser(description="Bot de SEO Master Óleo")
    ap.add_argument("--check", action="store_true", help="só verificação rápida")
    ap.add_argument("--rank", action="store_true", help="verifica posição real no Bing para cada keyword")
    ap.add_argument("--max-rank", type=int, default=20, help="máx. keywords checadas no --rank (default 20)")
    args = ap.parse_args()

    now = datetime.datetime.now().astimezone()
    relatorio = {"data": now.isoformat(), "site": SITE, "palavras_chave": {}, "tecnicos": [], "ok": True}

    # 1) Site no ar
    ok_ar, status = checar_site(SITE)
    relatorio["site_no_ar"] = ok_ar
    relatorio["status_http"] = status
    print(f"{'✅' if ok_ar else '❌'} Site no ar: HTTP {status}")

    # 1.5) Posições reais no Bing (--rank)
    if args.rank:
        print("\n📊 POSIÇÃO REAL NO BING (top 20):")
        relatorio["ranking_bing"] = {}
        alvo = PALAVRAS_CHAVE[:args.max_rank]
        for kw in alvo:
            r = checar_posicao_bing(kw)
            relatorio["ranking_bing"][kw] = r
            if r["erro"] and r["resultados"] == 0:
                print(f"  ⚠️  '{kw}': erro na consulta ao Bing")
            elif r["pos"] is not None:
                print(f"  🏆 '{kw}': POSIÇÃO {r['pos']} de {r['resultados']} resultados")
            elif not r["relevante"]:
                print(f"  ❔ '{kw}': INCONCLUSIVO (Bing devolveu SERP genérica — não confirma nem descarta)")
            else:
                print(f"  ⏳ '{kw}': fora do top {r['resultados']} (medido no Bing, SERP relevante)")
            time.sleep(1)
        print()

    # 2) Conteúdo: palavras-chave presentes?
    textos = ler_arquivos_site()
    for kw in PALAVRAS_CHAVE:
        presente = _kw_presente(kw, textos)
        relatorio["palavras_chave"][kw] = "presente" if presente else "AUSENTE"
        if not presente:
            relatorio["ok"] = False
        print(f"  {'✅' if presente else '❌'} '{kw}': {'presente' if presente else 'AUSENTE'}")

    # 3) SEO técnico
    tecnicos = verificar_seo_tecnico(textos)
    relatorio["tecnicos"] = tecnicos
    if tecnicos:
        relatorio["ok"] = False
        for t in tecnicos:
            print(f"  ⚠️  {t}")

    # 4) Sitemap
    sitemap = os.path.join(SITE_DIR, "sitemap.xml")
    if not os.path.exists(sitemap):
        print("  ⚠️  sitemap.xml ausente — recomendado criar")
        relatorio["sitemap"] = "ausente"
        relatorio["ok"] = False
    else:
        relatorio["sitemap"] = "presente"
        print("  ✅ sitemap.xml presente")

    # 5) Registra histórico
    os.makedirs(os.path.dirname(os.path.abspath(SEO_LOG)), exist_ok=True)
    historico = []
    if os.path.exists(os.path.abspath(SEO_LOG)):
        try:
            historico = json.load(open(os.path.abspath(SEO_LOG), encoding="utf-8"))
            if not isinstance(historico, list):
                historico = []
        except Exception:
            historico = []
    historico.append(relatorio)
    with open(os.path.abspath(SEO_LOG), "w", encoding="utf-8") as f:
        json.dump(historico[-60:], f, ensure_ascii=False, indent=2)

    print()
    print(f"{'✅' if relatorio['ok'] else '⚠️'} SEO geral: {'OK' if relatorio['ok'] else 'melhorias necessárias'}")
    print(f"Histórico salvo em equipe/seo.json ({len(historico)} registros)")
    return 0 if relatorio["ok"] else 1

if __name__ == "__main__":
    sys.exit(main())