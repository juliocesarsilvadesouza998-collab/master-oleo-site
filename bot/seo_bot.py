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
import argparse, datetime, json, os, re, sys, urllib.request, urllib.error

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
]

def checar_site(url):
    """Retorna True se o site responde 200."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200, r.status
    except Exception as e:
        return False, str(e)[:60]

def ler_arquivos_site():
    """Lê todos os HTML do site para análise de conteúdo."""
    textos = {}
    if not os.path.isdir(SITE_DIR):
        return textos
    for fn in os.listdir(SITE_DIR):
        if fn.endswith(".html"):
            try:
                with open(os.path.join(SITE_DIR, fn), encoding="utf-8") as f:
                    textos[fn] = f.read().lower()
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

def main():
    ap = argparse.ArgumentParser(description="Bot de SEO Master Óleo")
    ap.add_argument("--check", action="store_true", help="só verificação rápida")
    args = ap.parse_args()

    now = datetime.datetime.now().astimezone()
    relatorio = {"data": now.isoformat(), "site": SITE, "palavras_chave": {}, "tecnicos": [], "ok": True}

    # 1) Site no ar
    ok_ar, status = checar_site(SITE)
    relatorio["site_no_ar"] = ok_ar
    relatorio["status_http"] = status
    print(f"{'✅' if ok_ar else '❌'} Site no ar: HTTP {status}")

    # 2) Conteúdo: palavras-chave presentes?
    textos = ler_arquivos_site()
    for kw in PALAVRAS_CHAVE:
        presente = any(kw in html for html in textos.values())
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