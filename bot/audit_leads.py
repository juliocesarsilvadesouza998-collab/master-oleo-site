import json
import csv

# Carregar leads.csv
leads_status = {}
bounce_with_bv = []
with open('leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        status = row['status']
        email = row['email']
        leads_status[status] = leads_status.get(status, 0) + 1
        if status == 'bounce' and row['boas_vindas_em'].strip():
            bounce_with_bv.append({'id': row['id'], 'email': email, 'boas_vindas_em': row['boas_vindas_em']})

# Carregar bounces.json
with open('bounces.json', 'r') as f:
    bounces = json.load(f)

# Carregar leads e verificar se todos os bounces estão marcados
bounce_emails_in_leads = set()
with open('leads.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] == 'bounce':
            bounce_emails_in_leads.add(row['email'])

# Emails no bounces.json que NÃO estão marcados como bounce no leads.csv
bounces_not_in_csv = set()
for b in bounces:
    if b not in bounce_emails_in_leads:
        bounces_not_in_csv.add(b)

print("=== RESUMO DO DIA ===")
print(f"\nLeads por status:")
for status, count in sorted(leads_status.items()):
    print(f"  {status}: {count}")

print(f"\nTotal de leads: {sum(leads_status.values())}")
print(f"\nBounces no cache (bounces.json): {len(bounces)}")
print(f"Bounces marcados no leads.csv: {len(bounce_emails_in_leads)}")
print(f"Bounces no cache NÃO marcados no leads.csv: {len(bounces_not_in_csv)}")
if bounces_not_in_csv:
    print(f"  Emails problemáticos: {bounces_not_in_csv}")

print(f"\nLeads bounce com boas_vindas_em preenchido (problema): {len(bounce_with_bv)}")
if bounce_with_bv:
    for lead in bounce_with_bv:
        print(f"  - ID {lead['id']}: {lead['email']} (boas_vindas_em: {lead['boas_vindas_em']})")

# Carregar replies_pending.json
with open('replies_pending.json', 'r') as f:
    replies_pending = json.load(f)
print(f"\nRespostas pendentes: {len(replies_pending)}")