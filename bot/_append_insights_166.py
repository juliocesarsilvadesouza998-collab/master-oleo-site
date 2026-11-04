# -*- coding: utf-8 -*-
import io, os

path = r"C:\Users\julio\master-oleo-site\equipe\insights.md"

texto = """
## Ciclo 02/11/2026 18:57 — Atendente IA (tick #166)

### O que rodou
| Ação | Resultado |
|------|-----------|
| `sync_formspree.py` | 120 bounces em cache, **0 notificação nova** do Formspree |
| `corrigir_emails.py` | **0 bounce novo** — todos os 120 já tentados |
| `prospecao_followup.py` | **3 follow-ups** com thread: Liofoods (FP2), Poly Blends (FP2), Juvis (FP1) |
| `bot_oleo.py send_sequence` | Sequência processada — nenhum envio pendente |
| `bot_oleo.py check-replies` | **0 resposta pendente** |
| `scan_inbox.py --dias 2` | 0 mensagem não lida (438 leads, 356 msgids) |
| `proposta_contrato.py` / `relatorio_esg.py` | Não executados — nenhum lead informou volume, nenhum pedido ESG |

### Diagnóstico
- Base: **438 leads** — 308 novo, 92 bounce, 23 respondido, 14 encerrado, 1 sequência.
- Bounce rate ~21% (92/438), taxa de resposta ~5,3%.
- Caixa zerada: nenhuma resposta humana nova. **33 dias sem resposta humana real** (última: Tauste, 30/09).
- Fila de prospecção continua sem pendentes MX-válidos — o cold email está no teto até repor leads (lista CNPJ/Leadjet ou catálogo CIESP).

### Leitura do ciclo
1. O motor automático está saudável (SMTP/IMAP OK, follow-ups saindo no prazo), mas **não há nada para responder** — o funil de entrada está seco.
2. Todo o valor agora está em **ação humana nos leads que já abriram canal**: Sanofi Medley (follow-up recomendado 03/11), Pastifício Selmi (ticket 91322 aberto), Savegnago, Pague Menos, Rede Confiança, Covabra (cadastro Ivrim).
3. Nenhuma proposta de contrato gerada: para emitir a tabela escalonada (R$1,20→R$2,20/L) é preciso um lead informar volume — nenhum informou neste ciclo.

---
"""

with io.open(path, "a", encoding="utf-8", newline="") as f:
    f.write(texto.replace("\n", "\r\n"))

print("ok", os.path.getsize(path))
