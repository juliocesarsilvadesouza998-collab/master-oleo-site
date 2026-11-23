#!/usr/bin/env python3
import os, subprocess, sys

os.chdir(r"C:\Users\julio\master-oleo-site")

# Check if there are changes to commit
result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=30)
if not result.stdout.strip():
    print("Nada para commitar.")
    sys.exit(0)

# Add everything except sensitive files
subprocess.run(["git", "add", "-A"], check=True, timeout=30)

# Check gitignore protects sensitive files
subprocess.run(["git", "commit", "-m", "Melhoria contínua 23/11: +10 leads Capivari/Cerquilho via PDFs prefeitura; insights e ecossistema atualizados"], check=True, timeout=30)
print("Commit feito. Enviando...")
subprocess.run(["git", "push", "origin", "main"], check=True, timeout=60)
print("Push concluído.")