# -*- coding: utf-8 -*-
# Investigacao dos Nao_Marcados (leitura apenas)
import csv, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'leads.csv'), encoding='utf-8')))
bj = json.load(open(os.path.join(BASE, 'bounces.json'), encoding='utf-8'))
bj_emails = {e.lower() for e in bj}

alvos = ['contato@eixorestaurantes.co', 'contato@organalimentos.com.br', 'info@kelcopetcare.com.br']
print('--- busca exata por email no CSV ---')
idx = {}
for i, r in enumerate(rows):
    e = (r.get('email') or '').strip()
    idx.setdefault(e.lower(), []).append((i, r))
for a in alvos:
    hits = idx.get(a, [])
    for i, r in hits:
        print('%d | id=%s | empresa=%r | email=%r | status=%r | boas_vindas=%r' % (
            i, r.get('id'), r.get('empresa'), r.get('email'), r.get('status'), r.get('boas_vindas_em')))
    if not hits:
        print('%s => NAO_EXISTE_COMO_EMAIL_DE_LEAD' % a)

print()
print('--- todos os 26 nao marcados: existe como email de lead? ---')
bl = {r.get('email','').strip().lower() for r in rows if (r.get('status') or '').strip() == 'bounce'}
bounce_st = {(r.get('email','').strip().lower()) for r in rows}
for e in sorted(bj_emails - bl):
    if e in idx:
        for i, r in idx[e]:
            print('%-45s EXISTE status=%s id=%s nome=%r' % (e, r.get('status'), r.get('id'), (r.get('nome') or '')[:20]))
    else:
        print('%-45s ORFAO' % e)