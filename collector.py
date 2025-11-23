import ccxt
import time
from datetime import datetime

# İzleyeceğimiz semboller (Bybit spot)
SYMBOLS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
TIMEFRAME = "1m"

def fetch_latest_candle(exchange, symbol):
    try:
        candles = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=1)
        if not candles:
            return None

        ts, o, h, l, c, v = candles[0]
        return {
            "symbol": symbol,
            "timestamp": ts,
            "datetime": datetime.utcfromtimestamp(ts / 1000).isoformat(),
            "open": o,
            "high": h,
            "low": l,
            "close": c,
            "volume": v,
        }
    except Exception as e:
        print(f"Fetch error for {symbol}: {e}")
        return None


def main_loop():
    # Bybit borsasını kullan
    exchange = ccxt.bybit({
        "enableRateLimit": True,
    })

    print("Collector started on Bybit. Fetching 1m candles...")

    while True:
        for symbol in SYMBOLS:
            data = fetch_latest_candle(exchange, symbol)
            if data:
                print(
                    f"[{data['datetime']}] {data['symbol']} "
                    f"O:{data['open']} H:{data['high']} "
                    f"L:{data['low']} C:{data['close']} V:{data['volume']}"
                )
        # 1 dakikada bir tekrar et
        time.sleep(60)


if __name__ == "__main__":
    main_loop()
