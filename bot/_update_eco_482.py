#!/usr/bin/env python3
"""Update ecossistema.json with latest lead numbers."""
import json, datetime, os, sys

path = os.path.join(os.path.dirname(__file__), 'ecossistema.json')

with open(path, 'r', encoding='utf-8') as f:
    eco = json.load(f)

now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y-%m-%dT%H:%M:%S-03:00')
eco['atualizado_em'] = now
eco['leads']['total'] = 482
eco['leads']['por_status']['novo'] = 295
eco['leads']['por_status']['bounce'] = 95
eco['leads']['por_status']['respondido'] = 24
eco['leads']['por_status']['descartado'] = 53
eco['leads']['por_status']['encerrado'] = 15
eco['bounces_cache'] = 133
eco['ultima_execucao'] = now
eco['respondidos']['total'] = 20

with open(path, 'w', encoding='utf-8') as f:
    json.dump(eco, f, ensure_ascii=False, indent=2)

print(f'ecossistema.json atualizado: 482 leads em {now}')