import time
import requests
from datetime import datetime

# Hangi pariteleri takip edeceğiz
SYMBOLS = ["BTCUSDT", "ETHUSDT"]  # istersen buraya başka USDT pariteleri ekleyebilirsin
INTERVAL = "1m"                   # 1 dakikalık mum
API_URL = "https://api.binance.com/api/v3/klines"


def get_latest_candle(symbol: str):
    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "limit": 1,
    }
    resp = requests.get(API_URL, params=params, timeout=5)
    resp.raise_for_status()
    k = resp.json()[0]  # tek mum istedik, o yüzden [0]

    return {
        "symbol": symbol,
        "open_time": datetime.utcfromtimestamp(k[0] / 1000).isoformat(),
        "open": float(k[1]),
        "high": float(k[2]),
        "low": float(k[3]),
        "close": float(k[4]),
        "volume": float(k[5]),
    }


def main_loop():
    print("Binance REST collector başlıyor...")
    while True:
        for s in SYMBOLS:
            try:
                c = get_latest_candle(s)
                print(
                    f"[{c['symbol']}] {c['open_time']} "
                    f"O:{c['open']} H:{c['high']} L:{c['low']} C:{c['close']} V:{c['volume']}"
                )
            except Exception as e:
                print(f"HATA ({s}): {e}")

        # 60 saniyede bir yeni mum gelir
        time.sleep(60)


if __name__ == "__main__":
    main_loop()
