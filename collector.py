import time
import requests
import datetime

SYMBOLS = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"]
RESOLUTION = "1"  # 1 dakika
INTERVAL = 10     # 10 saniyede bir güncelleme


def get_unix():
    return int(time.time())


def fetch_tv_candle(symbol):
    now = get_unix()
    url = (
        f"https://data.tradingview.com/v3/history?"
        f"symbol={symbol}&resolution={RESOLUTION}&from={now-500}&to={now}"
    )

    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"TradingView error: {r.status_code}")

    data = r.json()

    if "t" not in data or len(data["t"]) == 0:
        raise Exception("Empty candle data")

    i = -1  # son mum
    return {
        "symbol": symbol,
        "timestamp": datetime.datetime.utcfromtimestamp(data["t"][i]).isoformat(),
        "open": data["o"][i],
        "high": data["h"][i],
        "low": data["l"][i],
        "close": data["c"][i],
        "volume": data["v"][i]
    }


def main():
    print("TradingView JSON Collector başlatıldı...")

    while True:
        for s in SYMBOLS:
            try:
                c = fetch_tv_candle(s)
                print(
                    f"{c['symbol']} | {c['timestamp']} | "
                    f"O:{c['open']} H:{c['high']} L:{c['low']} C:{c['close']} V:{c['volume']}"
                )

            except Exception as e:
                print("HATA:", e)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
