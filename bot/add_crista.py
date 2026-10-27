import json
with open('fila_prospeccao_extra.json', 'r') as f:
    fila = json.load(f)

existing_emails = {e.get('email','').lower() for e in fila if e.get('email')}

new_entry = {
    "nome": "Crista Indústria (Grupo Lins)",
    "empresa": "Crista Indústria (Grupo Lins)",
    "email": "faleconosco@cristamargarina.com.br",
    "cidade": "Indaiatuba/SP (fábrica: Marginal Norte, Indaiatuba - ~20km de Salto)",
    "segmento": "industria de oleos vegetais, margarinas e gorduras vegetais (70 anos, Grupo Lins) - NICHO PRIORITARIO (vencidos >40% gordura); MX Locaweb valido 27/10"
}

if new_entry['email'].lower() not in existing_emails:
    fila.append(new_entry)
    with open('fila_prospeccao_extra.json', 'w') as f:
        json.dump(fila, f, indent=2, ensure_ascii=False)
    print(f"ADDED: {new_entry['nome']}")
else:
    print("ALREADY EXISTS")

# Count
print(f"Total in fila now: {len(fila)}")