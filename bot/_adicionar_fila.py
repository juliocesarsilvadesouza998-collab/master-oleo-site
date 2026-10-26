# -*- coding: utf-8 -*-
"""Adiciona novas empresas à fila_prospeccao_extra.json"""
import json, os

novas = [
    {
        "nome": "Sorocaps",
        "empresa": "Sorocaps Industria Farmaceutica Ltda",
        "email": "sorocaps@sorocaps.com.br",
        "cidade": "Sorocaba/SP",
        "segmento": "Industria farmaceutica (capsulas gelatinosas)"
    },
    {
        "nome": "American Factory",
        "empresa": "American Factory LTDA",
        "email": "atendimento@afactory.com.br",
        "cidade": "Bauru/SP",
        "segmento": "Industria nutraceutica (capsulas, comprimidos, pos)"
    },
    {
        "nome": "Conduz Laticinios",
        "empresa": "Conduz Laticinios",
        "email": "contato@conduzlaticinios.com.br",
        "cidade": "Sao Paulo/SP",
        "segmento": "Laticinios e derivados (queijos, manteiga)"
    },
    {
        "nome": "Laticinios PJ",
        "empresa": "Laticinios PJ",
        "email": "sac@laticiniospj.com.br",
        "cidade": "Minas Gerais",
        "segmento": "Laticinios (queijos)"
    },
    {
        "nome": "Laticinios Piramide",
        "empresa": "Laticinios Piramide",
        "email": "latpiramide@gmail.com",
        "cidade": "Sao Paulo/SP",
        "segmento": "Laticinios"
    },
    {
        "nome": "Nutrielen",
        "empresa": "Nutrielen Solucoes em Terceirizacao",
        "email": "nutrielen@nutrielen.com.br",
        "cidade": "Sao Paulo/SP",
        "segmento": "Terceirizacao de encapsulados e nutraceuticos"
    },
    {
        "nome": "NUF Farmaceutica",
        "empresa": "NUF Farmaceutica Ltda",
        "email": "suporte@nuffarmaceutica.com.br",
        "cidade": "Cravinhos/SP",
        "segmento": "Industria de capsulas nutraceuticas e suplementos"
    },
    {
        "nome": "Alemed Nutraceutica",
        "empresa": "Alemed Nutraceutica Ltda",
        "email": "orcamento@alemednutraceutica.com.br",
        "cidade": "Sao Paulo/SP",
        "segmento": "Industria nutraceutica (capsulas, pos, liquidos)"
    }
]

p = os.path.join(os.path.dirname(__file__), 'fila_prospeccao_extra.json')
with open(p, encoding='utf-8') as f:
    fila = json.load(f)

# checar duplicatas por email
existentes = {e.get('email', '').strip().lower() for e in fila if isinstance(e, dict)}
adicionadas = 0
for nova in novas:
    if nova['email'].lower() in existentes:
        print(f"JA EXISTE: {nova['nome']} <{nova['email']}>")
    else:
        fila.append(nova)
        existentes.add(nova['email'].lower())
        adicionadas += 1
        print(f"ADICIONADA: {nova['nome']} <{nova['email']}>")

with open(p, 'w', encoding='utf-8') as f:
    json.dump(fila, f, ensure_ascii=False, indent=2)

print(f"\nTotal adicionadas: {adicionadas}")
print(f"Total na fila: {len(fila)}")

# contar status
from collections import Counter
pendentes = sum(1 for e in fila if isinstance(e, dict) and not e.get('enviado', False))
print(f"Pendentes (sem flag enviado): {pendentes}")
