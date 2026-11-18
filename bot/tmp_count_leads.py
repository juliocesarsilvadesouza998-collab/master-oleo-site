import csv
stats = {'novo':0, 'respondido':0, 'bounce':0, 'encerrado':0, 'descartado':0}
with open('leads.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        s = row.get('status','').strip().lower()
        if s in stats: stats[s] += 1
total = sum(stats.values())
print(f'total: {total}')
print(f'novo: {stats["novo"]}')
print(f'respondido: {stats["respondido"]}')
print(f'bounce: {stats["bounce"]}')
print(f'encerrado: {stats["encerrado"]}')
print(f'descartado: {stats["descartado"]}')