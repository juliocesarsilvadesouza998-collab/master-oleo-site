import json
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)
print(f'Total items in fila_extra: {len(fila)}')
for e in fila:
    if 'crista' in e.get('nome','').lower() or 'crista' in e.get('empresa','').lower():
        print(f'FOUND: {e["nome"]} - {e["email"]}')
        
with open('leads.csv', 'r', encoding='utf-8') as f:
    import csv
    reader = csv.DictReader(f)
    leads = list(reader)
    crista_leads = [l for l in leads if 'crista' in l.get('email','').lower()]
    print(f'Crista in leads: {len(crista_leads)}')
    if crista_leads:
        print(crista_leads[0])
    
# Count pendentes in fila_extra (not in leads, not bounced)
with open('bounces.json', 'r') as f:
    bounces = json.load(f)
bounce_set = {b.strip().lower() for b in bounces}
leads_emails = {l.get('email','').strip().lower() for l in leads}
extra_emails = {e.get('email','').strip().lower() for e in fila if e.get('email')}
pendentes = extra_emails - leads_emails - bounce_set
print(f'\nPendentes validos na fila_extra: {len(pendentes)}')
for e in sorted(pendentes):
    print(f'  {e}')

# Also check what's pending from the full combined queue
# by running the status again indirectly