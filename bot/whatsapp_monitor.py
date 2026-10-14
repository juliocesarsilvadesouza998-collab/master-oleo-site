#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — MONITOR DE RESPOSTAS DO WHATSAPP
==============================================
Lê as conversas não lidas do WhatsApp Web (via CDP) e identifica respostas
de leads — para o Atendente responder ou gerar alerta de lead quente.

Uso:
  python whatsapp_monitor.py            # lista conversas não lidas
  python whatsapp_monitor.py ler <num>  # lê o texto da conversa do número

Integração: o Atendente IA roda este script e, ao encontrar resposta,
responde com a persona (destinação/certificado/coleta-teste) ou pede o
volume mensal — levando o lead para fechamento.
"""
import argparse, json, re, sys, time
import websocket, requests

CDP_PORT = 9222


def get_ws_url():
    targets = requests.get(f"http://localhost:{CDP_PORT}/json", timeout=5).json()
    for t in targets:
        if t.get("type") == "page" and "web.whatsapp.com" in t.get("url", ""):
            return t["webSocketDebuggerUrl"]
    raise RuntimeError("Sem aba do WhatsApp Web na porta 9222")


def eval_js(ws, expr):
    ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                        "params": {"expression": expr, "returnByValue": True}}))
    while True:
        m = json.loads(ws.recv())
        if m.get("id") == 1:
            return m["result"]["result"].get("value")


def conversas_não_lidas(n=12):
    ws_url = get_ws_url()
    ws = websocket.create_connection(ws_url, timeout=30)
    try:
        # Pega as conversas da lista com título e timestamp
        js = """
        (() => {
          const rows = [...document.querySelectorAll('div[role="listitem"]')];
          if (rows.length > 0) {
            return rows.slice(0, %d).map(r => {
              const txt = r.innerText || '';
              const first = (txt.split('\\n')[0] || '').slice(0, 40);
              return {first, txt: txt.slice(0, 120)};
            });
          }
          // fallback: árvore do painel esquerdo
          const pane = document.querySelector('#side, div[data-testid="chat-list"]');
          return pane ? [{first: '_fallback', txt: pane.innerText.slice(0, 300)}] : [];
        })()
        """ % n
        return eval_js(ws, js) or []
    finally:
        ws.close()


def ler_conversa(numero):
    """Abre a conversa do número e retorna o texto dos últimos blocos (via CDP.nav, igual ao envio)."""
    import importlib
    wb = importlib.import_module("whatsapp_bot")
    cdp = wb.CDP(wb.get_whatsapp_ws()[0])
    try:
        cdp.nav(f"https://web.whatsapp.com/send?phone={numero}")
        time.sleep(6)
        txt = ""
        for _ in range(3):
            txt = cdp.eval("""
              (() => {
                const p = document.querySelector('div[data-testid="conversation-panel-messages"]');
                return p ? p.innerText.slice(-1000) : '';
              })()
            """)
            if txt:
                break
            time.sleep(2)
        return txt
    finally:
        cdp.close()


def main():
    ap = argparse.ArgumentParser(description="Monitor WhatsApp")
    ap.add_argument("comando", choices=["conversas", "ler"])
    ap.add_argument("numero", nargs="?", default=None)
    args = ap.parse_args()

    if args.comando == "conversas":
        conv = conversas_não_lidas()
        print(json.dumps(conv, ensure_ascii=False, indent=2))
    elif args.comando == "ler":
        txt = ler_conversa(args.numero)
        print(txt[-800:] if txt else "(vazio)")


if __name__ == "__main__":
    main()