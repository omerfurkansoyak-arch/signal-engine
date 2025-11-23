import websocket
import json

TV_WS = "wss://data.tradingview.com/socket.io/websocket"

SYMBOL = "BINANCE:BTCUSDT"
INTERVAL = "1"


def send(ws, msg):
    ws.send(msg + "\n")


def on_message(ws, message):
    if "timescale_update" in message:
        try:
            payload = message.split("~")[-1]
            data = json.loads(payload)
            candles = data["series"]["s1"]["data"]
            if len(candles) > 0:
                c = candles[-1]["v"]
                print("------ 1m Candle ------")
                print("Time:", c[0])
                print("Open:", c[1])
                print("High:", c[2])
                print("Low:", c[3])
                print("Close:", c[4])
                print("Volume:", c[5])
                print("------------------------")
        except:
            pass


def on_open(ws):
    print("Connected to TradingView WebSocket!")
    send(ws, "set_auth_token,unauthorized_user_token")
    send(ws, "chart_create_session,s1")
    send(ws, f"chart_set_symbol,s1,{SYMBOL}")
    send(ws, f"chart_set_resolution,s1,{INTERVAL}")
    send(ws, "chart_request_data,s1")


def on_error(ws, error):
    print("Error:", error)


def on_close(ws):
    print("WebSocket closed")


def run():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        TV_WS,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()


if __name__ == "__main__":
    print("Starting TradingView collector...")
    run()
