#!/usr/bin/env python3
import csv, json, os

BASE = r'C:\Users\julio\master-oleo-site\bot'
with open(os.path.join(BASE,'leads.csv'),newline='',encoding='utf-8-sig') as f:
    reader = list(csv.DictReader(f))

ids = ['9672890944','59','9672890911','9672890890','9672890888','ARTEMA20261028']
for r in reader:
    if r.get('id') in ids:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        print('---')