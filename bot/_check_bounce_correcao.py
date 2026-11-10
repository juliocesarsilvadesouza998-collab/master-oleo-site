import json

with open('bounces.json') as f:
    bounces = json.load(f)

with open('correcoes_emails.json') as f:
    raw = f.read().strip()
    correcoes = json.loads(raw) if raw else {}

nao_tentados = [e for e in bounces if e not in correcoes]
print(f"Total bounces: {len(bounces)}")
print(f"Com correcao: {len(correcoes)}")
print(f"Sem tentativa: {len(nao_tentados)}")
if nao_tentados:
    print(f"Lista: {nao_tentados}")
else:
    print("Nenhum bounce sem tentativa de correcao")