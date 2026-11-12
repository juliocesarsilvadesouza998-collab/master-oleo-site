#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Filtro de QUALIFICACAO de alvo da Master Oleo (fonte unica da verdade).

Regra do negocio (Julio, 12/11/2026): a Master Oleo coleta SOMENTE material
oleoso separavel — oleo vegetal/fritura usado, gordura vegetal, manteiga,
margarina, maionese (vencidos ou nao). Quem nao gera esse material esta fora do
alvo, por melhor que seja o porte da empresa.

Excluidos por decisao explicita:
  * LATICINIOS (12/11/2026): o residuo de laticinio e' soro/queijo/finos, nao
    oleo separavel; e o ticket de vencido e' baixo. Aplicado a fabricas,
    queijarias e distribuidoras de laticinios/frios.
  * Doces pastosos / nao separaveis (requeijao, doce de leite, creme).

NAO excluir (falsos positivos ja vistos): chocolate/cacau (tem manteiga de cacau
e gordura vegetal), sorvetes (gordura vegetal), industrias de OLEOS E GORDURAS
(manteigas vegetais), atacadistas/supermercados de alimentos em geral.

Retorna string com o motivo quando o alvo DEVE ser descartado, ou "" quando serve.
"""
import re

# Assinatura de laticinio no nome/empresa (peso alto)
_NOME_LACTEO = re.compile(
    r"latic[ií]n|queijaria|queijo|leiteria|leiteir|lactic[ií]nio|l[aá]cteos?\b|"
    r"iogurte|requeij|mussarela|ricota|catupiry|bufala|b[uú]fala|dairy|"
    r"\bleite\b|\bmanteiga\b|derivados do leite|creme de leite|doce de leite", re.I)

# Assinatura no segmento (peso alto) — "NICHO PRIORITARIO (vencidos >40% gordura)" etc.
_SEG_LACTEO = re.compile(
    r"latic[ií]n|queijos?\b|derivados l[aá]cteos|bebidas? l[aá]cteas|"
    r"ind[uú]stria de manteiga|f[áa]brica(ç|c)[aã]o de latic[ií]nios|"
    r"creme de leite|doce de leite|fracionamento de queijos", re.I)

# Empresas que contem palavra lactea mas NAO sao laticinio (mantidas no alvo)
_NAO_LACTEO = re.compile(
    r"chocolate|chocolates|cacau|kopenhagen|cacau show|"
    r"sorvete|sorvetes|picole|picol[ée]|"
    r"[óo]leos? (e gorduras|vegetais)|gordura vegetal|manteigas? vegetais|"
    r"refinadora|agropalma|"
    r"supermercado|atacadista|hipermercado|"
    r"p[ãa]o de queijo|salgado", re.I)


def motivo_exclusao(nome="", empresa="", segmento=""):
    """Retorna o motivo (str) se o alvo for laticinio/nao-oleoso; "" se servir."""
    nome = nome or ""
    empresa = empresa or ""
    segmento = segmento or ""
    ident = "%s %s" % (nome, empresa)
    if _NAO_LACTEO.search(ident) or _NAO_LACTEO.search(segmento):
        return ""
    if _NOME_LACTEO.search(ident):
        return "laticinio (identificado no nome da empresa)"
    if _SEG_LACTEO.search(segmento):
        return "laticinio (identificado no segmento)"
    return ""
