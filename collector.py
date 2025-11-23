import json
import time
from websocket import WebSocketApp

SYMBOLS = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"]

def on_open(ws):
    print("TradingView bağlantısı açıldı.")
    for s in SYMBOLS:
        session = "cs_1"

        msg = {
            "session_id": "session1",
            "timestamp": int(time.time()),
            "events": [
                {"name": "chart_create_session", "params": [session]},
                {"name": "resolve_symbol", "params": [session, "symbol_1", s]},
                {"name": "create_series", "params": [session, "s_1", "symbol_1", "1", 1]}
            ]
        }

        ws.send(json.dumps(msg))

def on_message(ws, message):
    print("Gelen veri:")
    print(message)

def on_error(ws, error):
    print("Hata:", error)

def on_close(ws, code, msg):
    print("Bağlantı kapandı:", code, msg)

def run():
    ws = WebSocketApp(
        "wss://data.tradingview.com/socket.io/websocket?from=chart",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever()

if __name__ == "__main__":
    run()

