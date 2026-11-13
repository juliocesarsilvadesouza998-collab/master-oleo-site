#!/usr/bin/env python3
import json, os

base = r'C:\Users\julio\master-oleo-site\bot'
os.chdir(base)

# Fila status
if os.path.exists('fila_leads.json'):
    with open('fila_leads.json') as f:
        fila = json.load(f)
    print(f'FILA: {len(fila)} leads')
    status = {}
    for l in fila:
        s = l.get('status', 'unknown')
        status[s] = status.get(s, 0) + 1
    for s in sorted(status.keys()):
        print(f'  [{s}] {status[s]} leads')
        items = [l for l in fila if l.get('status')==s][:2]
        for it in items:
            vol = it.get('volume_est', '?')
            email = it.get('email', '?')[:30]
            print(f'    {it.get("nome_empresa","?")} | {email} | vol: {vol}')
else:
    print('No fila_leads.json')

# Correcoes
if os.path.exists('correcoes_emails.json'):
    with open('correcoes_emails.json') as f:
        corr = json.load(f)
    if corr:
        print(f'\nÚltimas 3 correções:')
        for c in corr[-3:]:
            print(json.dumps(c, ensure_ascii=False, default=str))
else:
    print('\nNo correcoes_emails.json')

# Check bounces_file count
if os.path.exists('bounces_cache.json'):
    with open('bounces_cache.json') as f:
        b = json.load(f)
    print(f'\nBounces: {len(b)} emails cached')
else:
    print('\nNo bounces_cache.json')

# Check replies_pending
if os.path.exists('replies_pending.json'):
    with open('replies_pending.json') as f:
        rp = json.load(f)
    print(f'Replies pending: {len(rp)}')
else:
    print('replies_pending.json: empty/absent')

# Log file last lines
logpath = r'C:\Users\julio\master-oleo-site\bot\bot.log'
if os.path.exists(logpath):
    with open(logpath) as f:
        lines = f.readlines()
    print(f'\nÚltimas 10 linhas do bot.log:')
    for line in lines[-10:]:
        print(line.rstrip())
else:
    print('\nNo bot.log')