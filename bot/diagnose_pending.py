import json
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)
print(f"Total items: {len(fila)}")
# Count unique emails
emails = [e.get('email','').lower() for e in fila if e.get('email')]
print(f"Unique emails: {len(set(emails))}")
# Check which emails are in leads.csv vs not
import csv
leads_emails = set()
try:
    with open('leads.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            e = row.get('email','').strip().lower()
            if e:
                leads_emails.add(e)
except:
    pass
print(f"Leads CSV emails: {len(leads_emails)}")
not_in_leads = set(emails) - leads_emails
print(f"Fila emails NOT in leads (pendentes): {len(not_in_leads)}")
for e in sorted(not_in_leads):
    print(f"  {e}")