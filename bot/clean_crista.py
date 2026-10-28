import json, csv

# Load fila_extra
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)

# Remove the Crista entry since it already exists in the main queue
fila = [e for e in fila if 'crista' not in e.get('email','').lower()]
with open('fila_prospeccao_extra.json', 'w') as f:
    json.dump(fila, f, indent=2, ensure_ascii=False)
print(f'Cleaned. Total fila_extra: {len(fila)}')