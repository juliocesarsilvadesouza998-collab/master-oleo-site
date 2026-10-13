import json

with open('fila_prospeccao_extra.json', encoding='utf-8') as f:
    data = json.load(f)

emails = set()
for item in data:
    if item.get('email'):
        emails.add(item['email'].strip().lower())

with open('bounces.json', encoding='utf-8') as f:
    bounces = json.load(f)
bounce_set = set(e.strip().lower() for e in bounces if e)

print(f"Total emails in fila: {len(emails)}")
print(f"Total bounces: {len(bounce_set)}")
print("=== EMAILS IN FILA ===")
for e in sorted(emails):
    print(e)
print("=== BOUNCES ===")
for e in sorted(bounce_set):
    print(e)