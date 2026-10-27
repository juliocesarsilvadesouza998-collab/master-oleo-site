import json
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)
emails = [e.get('email','').lower() for e in fila if e.get('email')]
for e in sorted(emails):
    print(e)
print(f'---TOTAL: {len(emails)}---')