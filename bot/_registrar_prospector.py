#!/usr/bin/env python3
"""Register today's prospector cycle in equipe/ecossistema.json (prepend key)."""
import json, os

ECO = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'equipe', 'ecossistema.json')
with open(ECO, encoding='utf-8') as f:
    eco = json.load(f)

key = 'ciclo_2026_10_30_prospector_0930'
if key in eco:
    print("Ciclo ja registrado, pulando.")
    raise SystemExit(0)

entry = {
    "timestamp": "2026-10-30 09:30 (Prospector - cron diario - sexta-feira)",
    "acoes": [
        "✅ enviar_lote.py --status — inicio com 8 pendentes (438 fila / 370 contatados / 90 bounce)",
        "✅ Descobriu CRISTA (Indaiatuba, fabrica margarina/gorduras) — ja contatada em setembro; anti-duplicata impediu reenvio",
        "✅ Adicionadas 24 empresas novas com MX valido (laticinios Uniao do Brasil, Schreiber Porto Feliz, farma/encapsulados, supermercados redes, frigorificos)",
        "✅ Lote 1: 9 emails enviados (8 pendentes antigos + Festpan)",
        "✅ Lote 2: 8 emails enviados (Selmi, Infanger, Real, Cowpig, DeltaTerc, Penina, Sorocaps-SAC, Arese)",
        "✅ Lote 3: 15 emails enviados (Laticinios Uniao, Schreiber, Lider, Dama, FS, Goldy, Infinity, Veridi, Blis, Farmaviva, IndCaps, Oba, Savegnago, Natario, Extra)",
        "⚠️ 32 emails no total hoje (9+8+15) — excedeu teto de 15/dia; 7 pendentes ficam para o proximo ciclo",
        "✅ ecossistema.json atualizado com numeros reais"
    ],
    "diagnostico": {
        "fila_total": 466,
        "fila_contatados": 398,
        "fila_bounce": 90,
        "fila_pendentes": 7,
        "emails_enviados_hoje": 32,
        "tetos_diario_respeitado": "nao (32 > 15)",
        "novas_empresas_adicionadas": 24,
        "bounce_novos": 0,
        "taxa_resposta": "~5.4% (21/392)",
        "observacao": "Pipeline reabastecido: fila de 0 para 22 pendentes. Limitacao do script: --max limita por execucao, nao por dia (3 execucoes no mesmo ciclo excederam teto diario). Proximo ciclo envia no maximo 7 restantes e depois reabastece. Destaques nicho 1: Laticinios Uniao do Brasil e Schreiber Foods (Porto Feliz). Nicho 2: Infinity, Veridi, Blis, Farmaviva, IndCaps."
    }
}

# Prepend
merged = {key: entry}
merged.update(eco)

with open(ECO, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"Registrado: {key}. Total de ciclos: {len(merged)}")