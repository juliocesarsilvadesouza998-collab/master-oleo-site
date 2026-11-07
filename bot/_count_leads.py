import csv, json
with open('leads.csv', newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
print('Total leads:', len(rows))
statuses = {}
for r in rows:
    s = r.get('status', '?')
    statuses[s] = statuses.get(s, 0) + 1
for k,v in sorted(statuses.items()):
    print(f'  {k}: {v}')
try:
    with open('bounces.json') as f:
        b = json.load(f)
    print(f'Bounces cache: {len(b)}')
except: print('No bounces.json')
try:
    with open('replies_pending.json') as f:
        rp = json.load(f)
    print(f'Replies pending: {len(rp)}')
except: print('No replies_pending.json')