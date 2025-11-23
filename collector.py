import websocket
import json

def on_message(ws, message):
    try:
        data = json.loads(message)

        # kline datası mesajda var mı?
        if "k" in data:
            k = data["k"]
            print("------ 1m Candle ------")
            print("Time:", k['t'])
            print("Open:", k['o'])
            print("High:", k['h'])
            print("Low:", k['l'])
            print("Close:", k['c'])
            print("Volume:", k['v'])
            print("-----------------------")
    except:
        pass

def on_error(ws, error):
    print("HATA:", error)

def on_close(ws, close_status_code, close_msg):
    print("Bağlantı kapandı:", close_status_code, close_msg)

def on_open(ws):
    print("Binance WS bağlantısı açıldı.")

symbol = "btcusdt"

ws = websocket.WebSocketApp(
    f"wss://stream.binance.com:9443/ws/{symbol}@kline_1m",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
