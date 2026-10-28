# -*- coding: utf-8 -*-
# Analise diaria do Analista de Qualidade (cron) - le apenas, nao modifica
import csv, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'leads.csv'), encoding='utf-8')))
print('TOTAL_LEADS', len(rows))

from collections import Counter
st = Counter((r.get('status') or '').strip() for r in rows)
for k, v in st.most_common():
    print('STATUS %s: %d' % (k, v))

# bounces.json
bj_path = os.path.join(BASE, 'bounces.json')
bj = json.load(open(bj_path, encoding='utf-8'))
if isinstance(bj, dict):
    bj_emails = set(bj.keys())
elif isinstance(bj, list):
    bj_emails = set()
    for e in bj:
        if isinstance(e, str):
            bj_emails.add(e)
        elif isinstance(e, dict):
            bj_emails.add(e.get('email') or e.get('to') or '')
print('BOUNCES_JSON', len(bj_emails))

# de cada lead com status bounce, extrai email
bounce_leads = {}
for r in rows:
    s = (r.get('status') or '').strip()
    e = (r.get('email') or '').strip()
    if s == 'bounce':
        bounce_leads[e.lower()] = e
print('LEADS_STATUS_BOUNCE', len(bounce_leads))

# emails em bounces.json que NAO estao marcados bounce no CSV
bl = {e.lower() for e in bounce_leads.values()}
not_marked = sorted(bj_emails - bl)
print('EM_BOUNCES_JSON_NAO_MARCADOS_CSV', len(not_marked))
for e in not_marked[:20]:
    print('  NAO_MARCADO', e)

# bounce no CSV que nao esta em bounces.json
not_cached = sorted(bl - {e.lower() for e in bj_emails})
print('BOUNCE_CSV_SEM_CACHE', len(not_cached))
for e in not_cached[:20]:
    print('  SEM_CACHE', e)

# leads com status bounce e boas_vindas_em preenchido (anomalia)
anom = []
for r in rows:
    if (r.get('status') or '').strip() == 'bounce' and (r.get('boas_vindas_em') or '').strip():
        anom.append((r.get('empresa'), r.get('email'), r.get('boas_vindas_em')))
print('BOUNCE_COM_BOAS_VINDAS', len(anom))
for a in anom:
    print('  ANOMALIA', a)

# replies_pending
rp_path = os.path.join(BASE, 'replies_pending.json')
if os.path.exists(rp_path):
    rp = json.load(open(rp_path, encoding='utf-8'))
    print('REPLIES_PENDING', len(rp) if isinstance(rp, list) else rp)
else:
    print('REPLIES_PENDING arquivo inexistente')

# ultimos 10 leads adicionados
print('ULTIMOS_LEADS:')
for r in rows[-6:]:
    print('  ', r.get('criado_em'), '|', (r.get('empresa') or '')[:30], '|', r.get('status'))