#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista nomes+emails de todas as empresas conhecidas (base + extra) para conferencia anti-duplicata."""
import json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
from prospecao import EMPRESAS as BASE_EMPRESAS

extra = json.load(open(os.path.join(BASE, "fila_prospeccao_extra.json"), encoding="utf-8"))
todas = list(BASE_EMPRESAS) + extra
for p in sorted(todas, key=lambda x: x.get("empresa", "").lower()):
    print(f"{p.get('empresa','')} | {p.get('email','')} | {p.get('cidade','')} | {p.get('segmento','')}")