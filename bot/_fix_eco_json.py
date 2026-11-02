#!/usr/bin/env python3
"""Fix the ecossistema.json files by reading, parsing, and re-writing with valid JSON."""
import json, os, copy

BASE = os.path.dirname(os.path.abspath(__file__))

paths = [
    os.path.join(BASE, '..', 'equipe', 'ecossistema.json'),
    os.path.join(BASE, 'ecossistema.json'),
    os.path.join(BASE, 'equipe', 'ecossistema.json'),
]

# Find first valid file with tick_162
for p in paths:
    p = os.path.normpath(p)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"{p} loaded OK ({len(data)} keys)")
        except json.JSONDecodeError as e:
            print(f"{p}: invalid JSON - {e}")
            # Read raw, try to extract data
            with open(p, 'r', encoding='utf-8') as f:
                raw = f.read()
            # Extract tick_162 as text between quotes
            if 'ciclo_2026_11_02_atendente_tick_162' in raw:
                # Try to fix by re-parsing from last valid position
                # Find the last valid position before corruption
                for split_pos in range(len(raw), 5000, -100):
                    try:
                        json.loads(raw[:split_pos] + '\n}')
                        print(f"  Can recover first {split_pos} chars")
                        break
                    except:
                        pass