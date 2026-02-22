import os
import pandas as pd
import yfinance as yf
from datetime import date, timedelta

PRICES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "prices")
TICKERS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "tickers.txt")
ALL_TICKERS_CSV = os.path.join(PRICES_DIR, "all_daily.csv")


def _csv_path(ticker: str) -> str:
    return os.path.join(PRICES_DIR, f"{ticker}_daily.csv")


def _load_cache(ticker: str) -> pd.DataFrame | None:
    path = _csv_path(ticker)
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path, index_col="Date", parse_dates=True)
    return df


def _is_up_to_date(df: pd.DataFrame) -> bool:
    last_cached = df.index.max().date()
    expected = date.today() - timedelta(days=1)
    # Wochenenden überspringen
    while expected.weekday() >= 5:
        expected -= timedelta(days=1)
    return last_cached >= expected


def _fetch_from_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    df = yf.download(ticker, start=start, end=end, interval="1d", auto_adjust=True, progress=False)
    # yfinance 1.x gibt MultiIndex-Spalten zurück → auf einfache Spaltennamen reduzieren
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df.index.name = "Date"
    return df


def _get_company_name(ticker: str) -> str:
    try:
        info = yf.Ticker(ticker).info
        return info.get("longName", ticker)
    except Exception:
        return ticker


def fetch_prices(ticker: str, start: str = "2019-01-01", end: str = None) -> pd.DataFrame:
    """
    Gibt OHLCV-Tagesdaten für einen Ticker zurück.
    Prüft zuerst den lokalen CSV-Cache, ruft yfinance nur bei Bedarf ab.

    Parameter:
        ticker: z.B. "AAPL"
        start:  Startdatum im Format "YYYY-MM-DD"
        end:    Enddatum im Format "YYYY-MM-DD" (Standard: heute)

    Rückgabe:
        DataFrame mit Spalten: Open, High, Low, Close, Volume
    """
    if end is None:
        end = date.today().strftime("%Y-%m-%d")

    cached = _load_cache(ticker)

    if cached is not None and _is_up_to_date(cached):
        return cached

    if cached is not None:
        # Nur fehlende Daten nachladen
        fetch_start = (cached.index.max() + timedelta(days=1)).strftime("%Y-%m-%d")
        new_data = _fetch_from_yfinance(ticker, start=fetch_start, end=end)
        if not new_data.empty:
            df = pd.concat([cached, new_data])
            df = df[~df.index.duplicated(keep="last")]
        else:
            df = cached
    else:
        df = _fetch_from_yfinance(ticker, start=start, end=end)

    os.makedirs(PRICES_DIR, exist_ok=True)
    df.to_csv(_csv_path(ticker))

    return df


def load_tickers(path: str = None) -> list[str]:
    """
    Liest Ticker-Symbole aus tickers.txt ein.
    Leerzeilen und Kommentare (#) werden ignoriert.

    Parameter:
        path: Pfad zur tickers.txt (Standard: Projektroot/tickers.txt)

    Rückgabe:
        Liste von Ticker-Symbolen, z.B. ["AAPL", "MSFT", "NVDA"]
    """
    path = path or TICKERS_FILE
    with open(path, "r") as f:
        return [line.strip().upper() for line in f if line.strip() and not line.startswith("#")]


def fetch_all(tickers: list[str] = None, start: str = "2019-01-01") -> pd.DataFrame:
    """
    Lädt OHLCV-Daten für alle Ticker und speichert sie kombiniert in all_daily.csv.

    Parameter:
        tickers: Liste von Ticker-Symbolen (Standard: aus tickers.txt)
        start:   Startdatum im Format "YYYY-MM-DD"

    Rückgabe:
        DataFrame mit Spalten: Ticker, Name, Open, High, Low, Close, Volume
    """
    if tickers is None:
        tickers = load_tickers()

    frames = []
    for ticker in tickers:
        print(f"[fetch_all] Lade {ticker}...")
        df = fetch_prices(ticker, start=start).copy()
        df.insert(0, "Name", _get_company_name(ticker))
        df.insert(0, "Ticker", ticker)
        frames.append(df)

    combined = pd.concat(frames).sort_values(["Date", "Ticker"])

    os.makedirs(PRICES_DIR, exist_ok=True)
    combined.to_csv(ALL_TICKERS_CSV)
    print(f"[fetch_all] Gespeichert: {ALL_TICKERS_CSV}")

    return combined
