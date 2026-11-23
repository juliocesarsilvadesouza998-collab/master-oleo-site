#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — PROSPECÇÃO INTELIGENTE
====================================
Expande a prospecção para segmentos não explorados usando diretórios
públicos (ABCP/ABCIC/ABF etc.) e fontes gratuitas. Gera fila de leads
segmentada, classifica por potencial e registra no CRM.

Uso:
  python prospect_inteligencia.py --status        # mostra estado da fila
  python prospect_inteligencia.py --novos N       # sugere/registra N novos leads de um segmento
  python prospect_inteligencia.py --sugerir SEG   # busca empresas de um segmento
"""
import argparse, csv, json, os, re, sqlite3, sys, time
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "crm_masteroleo.db")
FILA = os.path.join(BASE, "fila_prospeccao_extra.json")
LEADS_CSV = os.path.join(BASE, "leads.csv")

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Segmentos industriais que geram os materiais que compramos
SEGMENTOS = {
    "oleos-gorduras": {
        "desc": "Fábricas de óleos vegetais, gorduras, margarinas",
        "cnpa": ["1041-4", "1043-1", "1052-0", "1042-2"],
        "material": "óleo vencido/fora de especificação, margarina, gordura",
        "potencial": "A",
        "buscas": [
            "fábrica óleos vegetais margarina email contato",
            "indústria gorduras vegetais processamento email",
        ],
    },
    "laticinios-queijos": {
        "desc": "Laticínios, manteiga, queijos, cremes",
        "cnpa": ["1051-1", "1052-0"],
        "material": "manteiga/creme vencidos >40% gordura",
        "potencial": "A",
        "buscas": [
            "fábrica laticínios manteiga email contato compras",
            "laticínio queijo manteiga SP email",
        ],
    },
    "restaurantes-cadeias": {
        "desc": "Redes de restaurantes, fast food, cozinhas industriais",
        "cnpa": ["5611-2", "5620-1"],
        "material": "óleo de fritura usado (grande volume)",
        "potencial": "A",
        "buscas": [
            "rede restaurantes fast food cozinha industrial email contato",
            "franquia restaurante Brasil email compras",
        ],
    },
    "hoteis-hospitalidade": {
        "desc": "Rede de hotéis com restaurantes",
        "cnpa": ["5510-8", "5590-6"],
        "material": "óleo de fritura usado",
        "potencial": "B",
        "buscas": [
            "rede hotéis Brasil email contato compras",
            "hotel rede restaurante óleo email",
        ],
    },
    "farmacos-encapsulados": {
        "desc": "Indústrias farmacêuticas (óleo de limpeza de máquinas)",
        "cnpa": ["2121-1", "2110-6"],
        "material": "óleo vegetal industrial usado",
        "potencial": "A",
        "buscas": [
            "indústria farmacêutica óleo vegetal limpeza máquina email",
            "laboratório encapsulados óleo email contato",
        ],
    },
    "distribuidoras-alimentos": {
        "desc": "Distribuidoras de alimentos (produtos vencidos)",
        "cnpa": ["4631-1", "4633-8", "4691-5"],
        "material": "alimentos vencidos >40% gordura",
        "potencial": "B",
        "buscas": [
            "distribuidora alimentos vencidos descarte email contato",
            "atacado alimentos distribuição email",
        ],
    },
    "frigorificos-abatedouros": {
        "desc": "Frigoríficos e abatedouros (gorduras animais)",
        "cnpa": ["1011-2", "1012-1"],
        "material": "gorduras animais, resíduos oleosos",
        "potencial": "A",
        "buscas": [
            "frigorífico gordura animal resíduo email contato",
            "abatedouro indústria carne email compras",
        ],
    },
    "biodiesel-residuos": {
        "desc": "Indústrias de biodiesel e gestão de resíduos",
        "cnpa": ["1932-2", "3811-4"],
        "material": "parceria: compra de óleo usado para revenda/processo",
        "potencial": "A",
        "buscas": [
            "indústria biodiesel produção óleo usado email",
            "empresa coleta resíduos óleo vegetal email",
        ],
    },
    "supermercados-regionais": {
        "desc": "Redes regionais de supermercados fora do eixo atual",
        "cnpa": ["4711-3", "4712-1"],
        "material": "óleo de fritura das praças de alimentação",
        "potencial": "A",
        "buscas": [
            "supermercado regional rede email compras contato",
            "atacadista supermercados interior SP email",
        ],
    },
}


def ja_existe(email, fila):
    for item in fila:
        if item.get("email") and email.lower() in str(item.get("email")).lower():
            return True
    return False


def buscar_empresas(segmento, n=8):
    """Busca empresas de um segmento usando DuckDuckGo."""
    cfg = SEGMENTOS.get(segmento)
    if not cfg:
        print(f"Segmento {segmento} não existe. Opções: {list(SEGMENTOS.keys())}")
        return []
    encontrados = []
    for q in cfg["buscas"]:
        url = "https://html.duckduckgo.com/html/?q=" + q.replace(" ", "+")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=12).read().decode("utf-8", errors="ignore")
            emails = EMAIL_RE.findall(data)
            vistos = set()
            for e in emails:
                if e.lower() in vistos:
                    continue
                vistos.add(e.lower())
                # Remove emails de provedores genéricos/plataformas
                if any(x in e.lower() for x in ["example", "facebook", "wix", "google",
                                                "youtube", "duckduckgo", "github"]):
                    continue
                dominio = e.split("@")[1].lower()
                if dominio in ("gmail.com", "hotmail.com", "outlook.com", "yahoo.com",
                               "terra.com.br", "uol.com.br", "ig.com.br"):
                    continue  # tentamos preferir emails corporativos
                # Acha o nome da empresa próximo ao email
                ctx = data[max(0, data.find(e) - 120): data.find(e) + 80]
                ctx = re.sub(r"<[^>]+>", " ", ctx)
                ctx = re.sub(r"\s+", " ", ctx).strip()
                encontrados.append({
                    "empresa": ctx[:60] or dominio.split(".")[0],
                    "email": e,
                    "segmento": segmento,
                    "material": cfg["material"],
                    "potencial": cfg["potencial"],
                })
                if len(encontrados) >= n:
                    return encontrados
        except Exception:
            continue
    return encontrados


def status_fila():
    if not os.path.exists(FILA):
        print("Fila não existe.")
        return
    fila = json.load(open(FILA, encoding="utf-8"))
    from collections import Counter
    por_seg = Counter(i.get("segmento", "?") for i in fila)
    total = len(fila)
    print(f"=== FILA DE PROSPECÇÃO ({total} empresas) ===")
    for seg, n in por_seg.most_common():
        print(f"  {seg}: {n}")


def sugerir(segmento, n=8, salvar=True):
    fila = []
    if os.path.exists(FILA):
        fila = json.load(open(FILA, encoding="utf-8"))
    novos = buscar_empresas(segmento, n)
    adicionados = 0
    for item in novos:
        if ja_existe(item["email"], fila):
            continue
        # Confere se já está no leads.csv
        if os.path.exists(LEADS_CSV):
            with open(LEADS_CSV, newline="", encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    if item["email"].lower() == str(r.get("email", "")).lower():
                        break
                else:
                    fila.append(item)
                    adicionados += 1
        else:
            fila.append(item)
            adicionados += 1
    if salvar:
        with open(FILA, "w", encoding="utf-8") as f:
            json.dump(fila, f, ensure_ascii=False, indent=2)
    print(f"Segmento {segmento}: {adicionados} novos adicionados à fila")
    for i in novos[:5]:
        print(f"  → {i['email']} ({i['empresa'][:40]})")
    return adicionados


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--sugerir", default=None)
    ap.add_argument("--n", type=int, default=8)
    args = ap.parse_args()

    if args.status:
        status_fila()
    elif args.sugerir:
        sugerir(args.sugerir, args.n)
    else:
        print("Uso: --status | --sugerir <segmento> [--n N]")
        print("Segmentos:", list(SEGMENTOS.keys()))


if __name__ == "__main__":
    main()
