#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Melhorador Continuo 28/10: registra tick no ecossistema.json (prepend) e insights.md."""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ECOSSISTEMA = os.path.join(BASE, "..", "equipe", "ecossistema.json")
INSIGHTS = os.path.join(BASE, "..", "equipe", "insights.md")

now = datetime.datetime.now().astimezone().isoformat(timespec="minutes")

tick = {
    "ciclo_2026_10_28_melhorador_tick_1400": {
        "timestamp": "2026-10-28 14:00 (Melhorador Continuo - cron diario)",
        "acoes": [
            "✅ Diagnóstico: fila de prospecção ZERADA (421 empresas, 359 contatados, 89 bounce, 2 pendentes AMBOS sem MX) — pipeline de envio parado",
            "✅ _reabastecer_fila.py — corrigiu Unialimentar para unialimentar@gmail.com (email publicado no site oficial; domínio .com.br sem MX)",
            "✅ _reabastecer_fila.py — removeu NUF Farmacêutica (domínio sem MX, inenviável, segmento farma fora do core)",
            "✅ _reabastecer_fila.py — adicionou 10 empresas novas com MX validado via nslookup: Supermercado Stabilê, M&M, Tiãozinho, Tiba, Potiguara, Ponto Certo, TBS (Tietê), Mercado Atual (Itu), Boi na Brasa (Sorocaba), União Supermercados 14 lojas (Itu)",
            "✅ enviar_lote.py --status — fila 430, 359 contatados, 89 bounce, 11 PENDENTES ENVIÁVEIS (era 2 inenviáveis)",
        ],
        "diagnostico": {
            "fila_total": 430,
            "fila_contatados": 359,
            "fila_bounce": 89,
            "fila_pendentes_enviáveis": 11,
            "fila_pendentes_antes": 2,
            "respostas": 20,
            "taxa_resposta": "6.3% (meta >3% — OK)",
            "bounce_rate": "~26-29% (acima da meta 15% — atenção)",
            "observacao": "Fila REABASTECIDA. Aprendizado do dia: emails com MX verificados 15+ dias antes podem perder MX (caso Unialimentar/NUF — domínio saiu do ar ou nunca teve servidor de email). Sempre revalidar MX na hora do envio (enviar_lote já faz). Segmentos novos: churrascarias (Boi na Brasa) e supermercados locais de Tietê/Cerquilho/Itu — municípios vizinhos ainda pouco explorados."
        },
        "leads_quentes": [
            "🔴🔴🔴 SAVEGNAGO (R$7,98bi) — WhatsApp (11) 96785-9631. AÇÃO HUMANA pendente ~29 dias.",
            "🔴🔴🔴 PAGUE MENOS (R$4,33bi) — ticket 407470 (Josiane Marinho). 14 dias sem retorno.",
            "🔴🔴🔴 REDE CONFIANÇA (Sorocaba) — proposta 2.500 L/mês; aguardando.",
            "🔴🔴🔴 COVABRA — cadastro fornecedor no portal Ivrim (ação humana).",
            "🔴🔴 BRASFRIGO / QUEIJOS ITUPEVA — agendar coleta-teste.",
            "🟡 SONDA — ligar (11) 2145-6200. 🟡 TAUSTE — ligar (15) 3324-4680. 🟡 ICT FARMACÊUTICA — WhatsApp em 3 dias se silêncio."
        ]
    }
}

# ecossistema.json — prepend
with open(ECOSSISTEMA, encoding="utf-8") as f:
    eco = json.load(f)
merged = dict(tick)
merged.update(eco)  # tick novo primeiro (dict preserva ordem de inserção)
with open(ECOSSISTEMA, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)
print(f"ecossistema.json atualizado: {len(merged)} ciclos registrados")

# insights.md — prepend bloco
entrada = """## 2026-10-28 14:00 (Melhorador Contínuo - cron diário)

### Diagnóstico do dia
- **Fila de prospecção ZERADA** — 421 empresas, 359 contatados, 89 bounce, 2 pendentes AMBOS sem MX (Unialimentar, NUF Farmacêutica) → pipeline de envio parado há ~4 dias.
- Taxa de resposta 6.3% (meta >3% ✅); bounce ~26-29% (meta 15% ⚠️).
- 29 dias sem resposta humana real — gargalo agora é AÇÃO HUMANA nos leads quentes (Savegnago, Pague Menos, Covabra, Rede Confiança), não prospecção.

### Melhorias implementadas
- ✅ **Reabasteceu a fila**: +10 empresas novas com MX validado via nslookup (Tietê: Stabilê, M&M, Tiãozinho, Tiba, Potiguara, Ponto Certo, TBS; Itu: Mercado Atual, União Supermercados 14 lojas; Sorocaba: Churrascaria Boi na Brasa). Fontes: lista oficial de credenciados da Prefeitura de Tietê (gov.br) + sites oficiais.
- ✅ **Corrigiu Unialimentar**: comercial@unialimentar.com.br (sem MX) → unialimentar@gmail.com (publicado no site oficial). Lead volta a ser enviável.
- ✅ **Removeu NUF Farmacêutica**: domínio sem servidor de email (Cloudflare sem MX), inenviável e segmento fora do core.
- Resultado: `enviar_lote.py --status` → **11 pendentes enviáveis** (era 2 inenviáveis). Próximo lote do Prospector volta a enviar.

### Lições
- **MX não é permanente**: domínios com MX verificado há 15+ dias podem perder o servidor de email (ou ter sido verificados por engano). Sempre confiar na revalidação do `enviar_lote.py` na hora do envio — ele já faz isso.
- **Fonte de leads de ouro**: PDFs oficiais de "rede credenciada" das prefeituras regionais (Tietê, e há similares em Itu/Boituva/Cerquilho/Porto Feliz) listam empresas locais com emails REAIS — melhor fonte para reabastecer a fila sem fabricar contatos. Buscar no site da prefeitura: `site:tiete.sp.gov.br rede credenciada`.
- **Municípios vizinhos pouco explorados**: Tietê, Cerquilho, Porto Feliz, Capivari, Elias Fausto têm dezenas de mercados/padarias com fritura contínua e óleo vencido — fila para próximos ciclos.
- Segmentos novos validados: churrascarias (fritura alto volume) + supermercados locais de cidades pequenas.

---

"""

with open(INSIGHTS, encoding="utf-8") as f:
    atual = f.read()
with open(INSIGHTS, "w", encoding="utf-8") as f:
    f.write(entrada + atual)
print("insights.md atualizado")