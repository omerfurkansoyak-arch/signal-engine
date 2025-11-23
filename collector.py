import websocket
import json
import time

SYMBOLS = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"]

def on_open(ws):
    print("TradingView bağlantısı açıldı.")
    for s in SYMBOLS:
        msg = {
            "session_id": "session1",
            "timestamp": int(time.time()),
            "events": [
                {"name": "chart_create_session", "params": ["cs_1"]},
                {"name": "resolve_symbol", "params": ["cs_1", "symbol_1", s]},
                {"name": "create_series", "params": ["cs_1", "s_1", "symbol_1", "1", 1]}
            ]
        }
        ws.send(json.dumps(msg))

def on_message(ws, message):
    print("Gelen veri:")
    print(message)

def on_error(ws, error):
    print("Hata:", error)

def on_close(ws, close_status_code, close_msg):
    print("Bağlantı kapandı:", close_status_code, close_msg)

def run():
    ws = websocket.WebSocketApp(
        "wss://data.tradingview.com/socket.io/websocket",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

if __name__ == "__main__":
    run()
