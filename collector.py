import time
from datetime import datetime
import ccxt

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
TIMEFRAME = "1m"

def fetch_latest_candle(exchange, symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=1)
    if not ohlcv:
        return None
    t, o, h, l, c, v = ohlcv[0]
    return {
        "symbol": symbol,
        "timestamp": t,
        "datetime": datetime.utcfromtimestamp(t/1000).isoformat(),
        "open": o,
        "high": h,
        "low": l,
        "close": c,
        "volume": v
    }

def main_loop():
    exchange = ccxt.binance({"enableRateLimit": True})
    print("Collector started…")

    while True:
        for symbol in SYMBOLS:
            try:
                data = fetch_latest_candle(exchange, symbol)
                if data:
                    print(
                        f"{data['datetime']} {symbol} "
                        f"O={data['open']} H={data['high']} "
                        f"L={data['low']} C={data['close']} V={data['volume']}"
                    )
            except Exception as e:
                print("Error:", e)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
