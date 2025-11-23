import ccxt
import time
from datetime import datetime

# ================== AYARLAR ==================

# 1 dakikalık mum verisi
TIMEFRAME = "1m"

# İzlenecek pariteler (Bybit formatı: BTC/USDT gibi)
SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "TIA/USDT",
    "LINK/USDT",
    "AVAX/USDT",
    "NEAR/USDT",
    "OP/USDT",
    "CRV/USDT",
    "DOT/USDT",
]

# Her döngü arasında kaç saniye beklesin
SLEEP_SECONDS = 60

# ================== YARDIMCI FONKSİYONLAR ==================


def ts_to_utc_iso(ts_ms: int) -> str:
    """Unix timestamp (ms) -> ISO UTC string."""
    return datetime.utcfromtimestamp(ts_ms / 1000).isoformat()


def fetch_latest_candle(exchange: ccxt.Exchange, symbol: str):
    """
    Bybit'ten son 1 dakikalık mumu çeker.
    Başarılı olursa bir dict döner, hata/boş olursa None.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=1)
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] HATA fetch_ohlcv({symbol}): {e}")
        return None

    if not ohlcv:
        print(f"[{datetime.utcnow().isoformat()}] UYARI: {symbol} için OHLCV boş döndü.")
        return None

    t, o, h, l, c, v = ohlcv[0]

    return {
        "symbol": symbol,
        "timestamp": t,
        "datetime": ts_to_utc_iso(t),
        "open": float(o),
        "high": float(h),
        "low": float(l),
        "close": float(c),
        "volume": float(v),
    }


# ================== ANA DÖNGÜ ==================


def main_loop():
    # Bybit borsasına bağlan
    exchange = ccxt.bybit(
        {
            "enableRateLimit": True,  # ccxt'nin rate limit koruması
        }
    )

    # Marketleri yükle (seçtiğimiz pariteler mevcut mu diye emin olmak için)
    try:
        markets = exchange.load_markets()
        print(f"[{datetime.utcnow().isoformat()}] Marketler yüklendi. Toplam: {len(markets)}")
    except Exception as e:
        print(f"[{datetime.utcnow().isoformat()}] HATA load_markets: {e}")
        return

    print(
        f"[{datetime.utcnow().isoformat()}] Collector started on BYBIT. "
        f"Timeframe={TIMEFRAME}, Symbols={', '.join(SYMBOLS)}"
    )

    while True:
        loop_start = datetime.utcnow().isoformat()
        print(f"\n[{loop_start}] ----- Yeni tarama başlıyor -----")

        for symbol in SYMBOLS:
            # Sembol borsada var mı?
            if symbol not in exchange.markets:
                print(f"[{datetime.utcnow().isoformat()}] UYARI: {symbol} Bybit'te bulunamadı, atlanıyor.")
                continue

            data = fetch_latest_candle(exchange, symbol)
            if not data:
                continue

            # Basit log çıktısı – ileride burayı sinyal/DB/Telegram için kullanacağız
            print(
                f"[{data['datetime']}] {data['symbol']} "
                f"O:{data['open']:.4f} H:{data['high']:.4f} "
                f"L:{data['low']:.4f} C:{data['close']:.4f} "
                f"V:{data['volume']:.4f}"
            )

        # Döngüler arası bekleme
        print(
            f"[{datetime.utcnow().isoformat()}] Döngü bitti, {SLEEP_SECONDS} saniye uyuyor..."
        )
        try:
            time.sleep(SLEEP_SECONDS)
        except KeyboardInterrupt:
            print(f"[{datetime.utcnow().isoformat()}] Manuel durdurma alındı. Çıkılıyor.")
            break


# ================== ÇALIŞTIRMA ==================

if __name__ == "__main__":
    main_loop()
