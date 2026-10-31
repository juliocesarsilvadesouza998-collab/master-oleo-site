# -*- coding: utf-8 -*-
"""IndexNow ping — envia URLs novas do site masteroleo.eco.br para indexação rápida."""
import json
import re
import sys
import urllib.error
import urllib.request

KEY = open(r"C:/Users/julio/master-oleo-site/deploy-vercel/indexnow-key.txt", encoding="utf-8").read().strip()
SITEMAP = r"C:/Users/julio/master-oleo-site/deploy-vercel/sitemap.xml"
HOST = "masteroleo.eco.br"

# Pega TODAS as URLs do sitemap (antes o script enviava só 1 URL fixa).
URLS = [u.strip() for u in re.findall(r"<loc>(.*?)</loc>", open(SITEMAP, encoding="utf-8").read())
        if u.strip().startswith("https://")]
for extra in sys.argv[1:]:
    if extra not in URLS:
        URLS.append(extra)
print(f"IndexNow: {len(URLS)} URLs do host {HOST}")

enviadas, falhas = 0, []
for i in range(0, len(URLS), 50):  # blocos de 50 por POST
    lote = URLS[i:i + 50]
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/indexnow-key.txt",
        "urlList": lote,
    }
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    n = i // 50 + 1
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            print(f"  lote {n}: HTTP {r.status} — {len(lote)} URLs aceitas")
            enviadas += len(lote)
    except urllib.error.HTTPError as e:
        print(f"  lote {n}: HTTP ERRO {e.code} — {e.read().decode('utf-8', 'replace')[:300]}")
        falhas.append(e.code)
    except Exception as e:
        print(f"  lote {n}: FALHA {e}")
        falhas.append(str(e))

print(f"\nResumo: {enviadas}/{len(URLS)} URLs enviadas, {len(falhas)} lote(s) com falha")
if falhas:
    sys.exit(1)