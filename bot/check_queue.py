#!/usr/bin/env python3
"""Check queue status"""
import json

with open('fila_prospeccao_extra.json', 'r') as f:
    data = json.load(f)

print(f"Total entries: {len(data)}")

emails = [e['email'] for e in data]
print(f"Unique emails: {len(set(emails))}")

# Check last 5 entries
for e in data[-5:]:
    print(f"  {e.get('nome','?')} <{e['email']}> - {e.get('segmento','?')}")