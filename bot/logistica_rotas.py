#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — RENTABILIDADE DE ROTAS E REGIÕES
==============================================
Analisa a rentabilidade por região/fornecedor antes de fechar contrato,
evitando coleta que não cobre o custo de deslocamento.

Regras comerciais preservadas (fonte: política comercial):
  - Compra de óleo coletado: R$ 2,00/L
  - Retirada de água com soda: óleo recuperável abate o serviço
  - Material <20% de óleo: avaliar como retirada de resíduo a R$ 1,50/L,
    descontando o óleo recuperável

Uso:
  python logistica_rotas.py --regioes          # lista regiões conhecidas
  python logistica_rotas.py --calcular REGIAO VOLUME_MENSAL_L --distancia KM
  python logistica_rotas.py --tabela           # tabela de referência por distância
"""
import argparse, os

# Custo de deslocamento (referência: caminhonete/van — diesel R$ 6,30/L, 9 km/L)
CUSTO_KM = 0.70          # R$ por km rodado (combustível + manutenção)
TEMPO_H = 45.0           # custo hora (operação) em R$ — ajustável
VELOC_MEDIA = 45.0       # km/h em área urbana/interior

REGIOES = {
    "Salto (base)": 0,
    "Itu": 12,
    "Indaiatuba": 22,
    "Sorocaba": 45,
    "Campinas": 55,
    "Jundiaí": 40,
    "Piracicaba": 62,
    "Americana": 45,
    "Hortolândia": 40,
    "Valinhos": 48,
    "Vinhedo": 42,
    "Capivari": 25,
    "Cerquilho": 35,
    "Tietê": 42,
    "Salto de Pirapora": 60,
    "Itapetininga": 110,
    "São José do Rio Preto": 380,  # desmoldante (viagem dedicada)
}


def rentabilidade(regiao, volume_l, distancia_km, preco_l=2.00, ida_volta=True):
    """Calcula margem de uma coleta na região."""
    km_total = distancia_km * 2 if ida_volta else distancia_km
    custo_km_total = km_total * CUSTO_KM
    horas = km_total / VELOC_MEDIA + 1.0  # +1h para carga/descarga/documentação
    custo_tempo = horas * TEMPO_H
    custo_total = custo_km_total + custo_tempo

    receita = volume_l * preco_l
    margem = receita - custo_total
    margem_pct = margem / receita * 100 if receita else 0

    return {
        "regiao": regiao, "distancia_km": distancia_km, "km_total": round(km_total),
        "custo_km": round(custo_km_total, 2), "custo_tempo": round(custo_tempo, 2),
        "custo_total": round(custo_total, 2), "volume_l": volume_l,
        "receita": round(receita, 2), "margem": round(margem, 2),
        "margem_pct": round(margem_pct, 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regioes", action="store_true")
    ap.add_argument("--tabela", action="store_true")
    ap.add_argument("--calcular", nargs=3, metavar=("REGIAO", "VOLUME_L", "DIST_KM"))
    args = ap.parse_args()

    if args.regioes:
        print("=== DISTÂNCIAS DE REFERÊNCIA (km de Salto/SP) ===")
        for reg, km in sorted(REGIOES.items(), key=lambda x: x[1]):
            bar = "#" * min(int(km / 5), 30)
            print(f"  {reg:28s} {km:3d} km {bar}")
        return

    if args.tabela:
        print("=== MARGEM POR DISTÂNCIA (400 L, R$ 2,00/L) ===")
        for km in [10, 25, 45, 60, 90, 120, 200]:
            r = rentabilidade("—", 400, km)
            print(f"  {km:3d} km: custo R$ {r['custo_total']:5.2f} | "
                  f"receita R$ {r['receita']:6.2f} | margem R$ {r['margem']:7.2f} "
                  f"({r['margem_pct']:+.1f}%)")
        return

    if args.calcular:
        regiao, volume, dist = args.calcular[0], int(args.calcular[1]), int(args.calcular[2])
        r = rentabilidade(regiao, volume, dist)
        print(f"=== RENTABILIDADE — {r['regiao']} ===")
        print(f"  Distância (ida)       : {r['distancia_km']} km")
        print(f"  KM total (ida e volta): {r['km_total']} km")
        print(f"  Custo deslocamento    : R$ {r['custo_km']:.2f}")
        print(f"  Custo tempo (operação): R$ {r['custo_tempo']:.2f}")
        print(f"  Custo total           : R$ {r['custo_total']:.2f}")
        print(f"  Volume coletado       : {r['volume_l']} L")
        print(f"  Receita (R$ 2,00/L)   : R$ {r['receita']:.2f}")
        print(f"  MARGEM               : R$ {r['margem']:.2f} ({r['margem_pct']:+.1f}%)")
        if r["margem"] < 0:
            print("  ⚠️  COLETA PREJUDICIA — renegociar valor, agrupar com outra ou passar serviço.")
        elif r["margem_pct"] < 20:
            print("  ⚠️  Margem apertada — agrupar coleta na região para diluir custo.")
        else:
            print("  ✅ Margem saudável.")
        return

    print("Uso: --regioes | --tabela | --calcular REGIAO VOLUME_L DIST_KM")


if __name__ == "__main__":
    main()
