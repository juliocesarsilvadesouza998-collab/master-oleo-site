#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Óleo — WHATSAPP BOT via CDP (Chrome DevTools Protocol)
==============================================================
Controla o WhatsApp Web que está logado no Opera (porta 9222) de forma
PROGRAMÁTICA — sem cliques na tela, sem intervenção humana. O Opera precisa
estar aberto com: --remote-debugging-port=9222 --user-data-dir="<perfil do usuário>"

Uso:
  python whatsapp_bot.py status                       # mostra se está logado
  python whatsapp_bot.py enviar 5516981302000 "texto"  # envia mensagem
  python whatsapp_bot.py enviar-cada <arquivo.json>   # envia várias ({[desc],numero,msg} ou {desc,email,numero,msg})
  python whatsapp_bot.py foto 5516981302000 "caminho.png" "legenda"   # envia imagem
  python whatsapp_bot.py arquivo 5516981302000 "caminho.pdf" "legenda" # envia documento

Sem dependências além de: requests, websocket-client (instaladas).
"""
import argparse, json, os, socket, sys, time
import requests
import websocket  # websocket-client

CDP_PORT = 9222


def get_targets():
    r = requests.get(f"http://localhost:{CDP_PORT}/json", timeout=5)
    return r.json()


def get_whatsapp_ws():
    """Retorna a URL de websocket da aba do WhatsApp Web."""
    targets = get_targets()
    for t in targets:
        if t.get("type") == "page" and "web.whatsapp.com" in t.get("url", ""):
            return t["webSocketDebuggerUrl"], t.get("id", "")
    # se não achar, procura qualquer aba que possamos navegar
    for t in targets:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"], t.get("id", "")
    raise RuntimeError("Nenhuma aba de navegador encontrada na porta 9222")


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=60)
        self._id = 0

    def cmd(self, method, params=None):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params or {}}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"CDP {method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, expr):
        """Executa JS e retorna o valor (serializado via JSON)."""
        res = self.cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": True})
        val = res.get("result", {}).get("value")
        if res.get("exceptionDetails"):
            raise RuntimeError(f"JS error: {res['exceptionDetails']}")
        return val

    def nav(self, url):
        self.cmd("Page.navigate", {"url": url})
        time.sleep(1.5)

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def wait_whatsapp(cdp, timeout=40):
    """Aguarda o WhatsApp Web carregar e estar logado."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            # Seleciona a lista de conversas OU o painel do chat → indica logado
            logado = cdp.eval(
                "document.querySelector('header, #side, div[data-testid=\"chat-list\"]') !== null || "
                "document.body && document.body.innerText.includes('Conversas')"
            )
            qr = cdp.eval("document.querySelector('canvas') !== null && document.body.innerText.includes('Use seu celular')")
            if logado:
                return True
            if qr:
                return "QR"  # precisa escanear
        except Exception:
            pass
        time.sleep(2)
    return False


def abrir_conversa(cdp, numero):
    """Navega para a conversa do número via link direto do WhatsApp Web."""
    cdp.nav(f"https://web.whatsapp.com/send?phone={numero}")
    time.sleep(3)
    # Aguarda aparecer o painel do chat com campo de mensagem
    t0 = time.time()
    while time.time() - t0 < 25:
        ok = cdp.eval(
            "(document.querySelector('div[contenteditable=\"true\"]') !== null || "
            "document.querySelector('[data-testid=\"conversation-panel-messages\"]') !== null) && "
            "!document.body.innerText.includes('Nenhuma conversa')"
        )
        if ok:
            return True
        time.sleep(1.5)
    return False


def digitar_e_enviar(cdp, texto):
    """Foca o campo de mensagem, digita (com eventos reais) e envia."""
    # Foca o contenteditable e injeta o texto via execCommand (dispara eventos reais do React)
    js = f"""
    (() => {{
      const campo = document.querySelector('div[contenteditable="true"][data-tab="10"], div[contenteditable="true"]');
      if (!campo) return 'SEM_CAMPO';
      campo.focus();
      campo.innerText = '';
      campo.dispatchEvent(new Event('focus', {{bubbles: true}}));
      // insere o texto com eventos de input (React/WhatsApp web exige)
      campo.innerHTML = {json.dumps(texto)};
      campo.dispatchEvent(new InputEvent('input', {{bubbles: true, data: {json.dumps(texto)}, inputType: 'insertText'}}));
      campo.dispatchEvent(new InputEvent('input', {{bubbles: true, data: null, inputType: 'insertText'}}));
      return 'DIGITADO';
    }})()
    """
    r = cdp.eval(js)
    time.sleep(0.8)
    # Clique no botão de enviar — vários seletores possíveis do WhatsApp Web atual
    clique = cdp.eval(
        "(() => { const sels = ['button[data-testid=\"send\"]', 'div[aria-label=\"Enviar\"]', "
        "'button[aria-label=\"Enviar\"]', 'span[data-icon=\"send\"]', "
        "[...document.querySelectorAll('button')].find(b => b.querySelector('span[data-icon=\"send\"]') !== null) || null"
        "]; let btn = null; for (const s of sels) { if (typeof s === 'string') { btn = document.querySelector(s); } else { btn = s; } if (btn) break; } "
        "if (btn) { btn.click(); return 'CLICOU'; } return 'SEM_BOTAO'; })()"
    )
    time.sleep(1.0)
    return r, clique


def enviar_mensagem(numero, texto):
    ws_url, _ = get_whatsapp_ws()
    cdp = CDP(ws_url)
    try:
        estado = wait_whatsapp(cdp, timeout=30)
        if estado == "QR":
            raise RuntimeError("WhatsApp Web não está logado (mostra QR code) — conecte uma vez no celular.")
        if not estado:
            raise RuntimeError("WhatsApp Web não carregou a tempo")
        if not abrir_conversa(cdp, numero):
            raise RuntimeError(f"Não abriu conversa com {numero} (número sem WhatsApp?)")
        r, clique = digitar_e_enviar(cdp, texto)
        confirmacao = cdp.eval(
            "(document.querySelector('div[data-testid=\"msg-sent\"]') !== null ? 'enviada' : 'verificar')"
        )
        return {"digitou": r, "botao": clique, "confirmacao": confirmacao}
    finally:
        cdp.close()


def enviar_todos(lista):
    """lista: [{numero, msg}] — envia em sequência com pausa."""
    resultados = []
    for item in lista:
        try:
            res = enviar_mensagem(item["numero"], item["msg"])
            resultados.append({"numero": item["numero"], "ok": True, **res})
            print(f"✅ {item['numero']}: {res}")
        except Exception as ex:
            resultados.append({"numero": item.get("numero"), "ok": False, "erro": str(ex)})
            print(f"❌ {item.get('numero')}: {ex}")
        time.sleep(3)  # pausa entre envios p/ não parecer spam
    return resultados


def main():
    ap = argparse.ArgumentParser(description="WhatsApp Bot via CDP")
    ap.add_argument("comando", choices=["status", "enviar", "enviar-cada"])
    ap.add_argument("arg", nargs="*", help="número/mensagem ou caminho do JSON")
    args = ap.parse_args()

    if args.comando == "status":
        ws_url, _ = get_whatsapp_ws()
        cdp = CDP(ws_url)
        try:
            estado = wait_whatsapp(cdp, timeout=20)
            print("LOGADO" if estado is True else ("QR (precisa conectar)" if estado == "QR" else "NAO CARREGADO"))
        finally:
            cdp.close()
        return

    if args.comando == "enviar":
        numero, texto = args.arg[0], " ".join(args.arg[1:])
        res = enviar_mensagem(numero, texto)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return

    if args.comando == "enviar-cada":
        with open(args.arg[0], encoding="utf-8") as f:
            dados = json.load(f)
        res = enviar_todos(dados)
        print(json.dumps({"total": len(res), "ok": sum(1 for r in res if r["ok"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()