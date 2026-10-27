import json
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)

# Check if Crista is already in
existing_emails = {e.get('email','').lower() for e in fila if e.get('email')}
print(f"Crista already in fila? {'faleconosco@cristamargarina.com.br' in existing_emails}")

# Also check for other potential new ones
new_entries = []
candidates = [
    {
        "nome": "Crista Indústria (Grupo Lins)",
        "empresa": "Crista Indústria (Grupo Lins)",
        "email": "faleconosco@cristamargarina.com.br",
        "cidade": "Indaiatuba/SP (fábrica: Marginal Norte, Indaiatuba)",
        "segmento": "industria de oleos vegetais, margarinas e gorduras vegetais - NICHO PRIORITARIO (vencidos >40% gorduras)"
    }
]

for c in candidates:
    if c['email'].lower() not in existing_emails:
        new_entries.append(c)
        print(f"NEW: {c['nome']} - {c['email']}")
    else:
        print(f"EXISTS: {c['nome']}")

print(f"\nTotal new to add: {len(new_entries)}")