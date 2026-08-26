# -*- coding: utf-8 -*-
"""Hexdump da linha do telephone para ver os bytes exatos."""
p = r"C:\Users\julio\master-oleo-site\deploy-vercel\index.html"

with open(p, "rb") as f:
    data = f.read()

for i, line in enumerate(data.split(b"\n")):
    if b"telephone" in line:
        print("linha", i + 1, "bytes:")
        print(line.hex(" "))
        print("repr:", repr(line))
        # mostra cada char como int
        print("chars:", [hex(c) for c in line])
        # conta asteriscos ascii 0x2a
        print("count 0x2a:", line.count(b"*"))
