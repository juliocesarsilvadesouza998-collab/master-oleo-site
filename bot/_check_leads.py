#!/usr/bin/env python3
import csv, json
from collections import Counter

BASE = "C:/Users/julio/master-oleo-site/bot"
LEADS_PATH = BASE + "/leads.csv"
BOUNCE_PATH = BASE + "/bounces.json"

with open(LEADS_PATH, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

c = Counter(r.get("status","") for r in rows)
print(f"Total leads: {len(rows)}")
for k, v in sorted(c.items()):
    print(f"  {k}: {v}")

with open(BOUNCE_PATH, encoding="utf-8") as f:
    bounces = json.load(f)
print(f"Bounces cache: {len(bounces)}")