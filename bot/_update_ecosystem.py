#!/usr/bin/env python3
"""Update equipe/ecossistema.json with current real numbers"""
import csv, json, datetime, os

BASE = r'C:\Users\julio\master-oleo-site\bot'
LEADS_PATH = os.path.join(BASE, 'leads.csv')
ECO_PATH = r'C:\Users\julio\master-oleo-site\equipe\ecossistema.json'

with open(LEADS_PATH, newline='', encoding='utf-8-sig') as f:
    leads = list(csv.DictReader(f))

total = len(leads)
by_status = {}
by_fonte = {}
respondidos = []
for r in leads:
    s = r.get('status','').strip() or 'novo'
    by_status[s] = by_status.get(s, 0) + 1
    f = r.get('fonte','').strip() or 'desconhecida'
    by_fonte[f] = by_fonte.get(f, 0) + 1
    if r.get('respondido_em',''):
        respondidos.append(r)

eco = {
    "atualizado_em": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
    "leads": {
        "total": total,
        "por_status": by_status,
        "por_fonte": by_fonte
    },
    "respondidos": {
        "total": len(respondidos),
        "lista": [{"empresa": r.get('empresa','?'), "contato": r.get('contato',''), "email": r.get('email',''), "cidade": r.get('cidade',''),
                    "respondido_em": r.get('respondido_em',''), "ultima_resposta": (r.get('ultima_resposta','') or '')[:100]} 
                  for r in sorted(respondidos, key=lambda x: x.get('respondido_em','') or '', reverse=True)[:30]]
    },
    "bounces_cache": 130,
    "prospeccao_lote_enviados": sum(1 for r in leads if r.get('apresentacao_em','')),
    "sequencia_ativa": True,
    "ultima_execucao": datetime.datetime.now().astimezone().isoformat(timespec="seconds")
}

with open(ECO_PATH, 'w', encoding='utf-8') as f:
    json.dump(eco, f, ensure_ascii=False, indent=2)

print(f"Ecossistema atualizado: {total} leads, {len(respondidos)} respondidos")
print(f"Status: {json.dumps(by_status, ensure_ascii=False)}")
print(f"Fontes: {json.dumps(by_fonte, ensure_ascii=False)}")