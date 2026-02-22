import os
import requests
import pandas as pd
from datetime import date
from dotenv import load_dotenv

load_dotenv()

NEWS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "news")
ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"


def _csv_path(ticker: str, fetch_date: str) -> str:
    return os.path.join(NEWS_DIR, f"{ticker}_{fetch_date}_news.csv")


def _load_cache(ticker: str, fetch_date: str) -> pd.DataFrame | None:
    path = _csv_path(ticker, fetch_date)
    if not os.path.exists(path):
        return None
    return pd.read_csv(path)


def fetch_news(ticker: str, fetch_date: str = None) -> pd.DataFrame | None:
    """
    Gibt Finanznachrichten mit Sentiment-Score für einen Ticker zurück.
    Benötigt einen Alpha Vantage API-Key in der .env Datei (ALPHA_VANTAGE_KEY).
    Prüft zuerst den lokalen CSV-Cache.

    Parameter:
        ticker:     z.B. "AAPL"
        fetch_date: Datum im Format "YYYY-MM-DD" (Standard: heute)

    Rückgabe:
        DataFrame mit Spalten: title, summary, time_published, sentiment_score, sentiment_label
        None wenn kein API-Key vorhanden oder Fehler aufgetreten
    """
    if fetch_date is None:
        fetch_date = date.today().strftime("%Y-%m-%d")

    cached = _load_cache(ticker, fetch_date)
    if cached is not None:
        return cached

    api_key = os.getenv("ALPHA_VANTAGE_KEY")
    if not api_key:
        print("[news_fetcher] Kein ALPHA_VANTAGE_KEY in .env gefunden. News-Abruf übersprungen.")
        return None

    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ticker,
        "time_from": fetch_date.replace("-", "") + "T0000",
        "time_to": fetch_date.replace("-", "") + "T0930",
        "apikey": api_key,
        "sort": "EARLIEST",
        "limit": 50,
    }

    response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    if "feed" not in data:
        print(f"[news_fetcher] Keine News für {ticker} am {fetch_date}.")
        return None

    rows = []
    for article in data["feed"]:
        for ts in article.get("ticker_sentiment", []):
            if ts["ticker"] == ticker:
                rows.append({
                    "title": article.get("title"),
                    "summary": article.get("summary"),
                    "time_published": article.get("time_published"),
                    "sentiment_score": float(ts.get("ticker_sentiment_score", 0)),
                    "sentiment_label": ts.get("ticker_sentiment_label"),
                })

    if not rows:
        return None

    df = pd.DataFrame(rows)
    os.makedirs(NEWS_DIR, exist_ok=True)
    df.to_csv(_csv_path(ticker, fetch_date), index=False)

    return df
