# -*- coding: utf-8 -*-
"""IndexNow ping — envia URLs novas do site masteroleo.eco.br para indexação rápida."""
import json
import urllib.request

KEY = open(r"C:/Users/julio/master-oleo-site/deploy-vercel/indexnow-key.txt", encoding="utf-8").read().strip()
HOST = "masteroleo.eco.br"
URLS = [
    "https://masteroleo.eco.br/blog/vender-oleo-cozinha-usado.html",
]

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/indexnow-key.txt",
    "urlList": URLS,
}
body = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=body,
    headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "Mozilla/5.0"},
    method="POST",
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("HTTP", r.status, "- IndexNow aceito (202 esperado)")
        print(r.read().decode("utf-8", "replace")[:500])
except urllib.error.HTTPError as e:
    print("HTTP ERRO", e.code)
    print(e.read().decode("utf-8", "replace")[:500])
except Exception as e:
    print("FALHA:", e)