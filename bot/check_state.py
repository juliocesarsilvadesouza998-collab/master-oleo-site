#!/usr/bin/env python3
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, "bounces.json")) as f:
    b = json.load(f)
print(f"bounces.json: {len(b)} entries")

with open(os.path.join(BASE, "replies_pending.json")) as f:
    r = json.load(f)
print(f"replies_pending.json: {len(r)} entries")