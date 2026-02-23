"""
Feature Store – persistenter Indikator-Cache
─────────────────────────────────────────────
Zwischenschicht zwischen rohen OHLCV-Daten und allen Analyse-Modulen.

Ablauf:
    get_features("AAPL")
        1. Parquet-Cache prüfen → aktuell? → sofort zurückgeben
        2. Sonst: OHLCV laden → FEATURE_PIPELINE ausführen → Parquet speichern

FEATURE_PIPELINE:
    Geordnete Liste von Berechnungsfunktionen. Jedes Modul registriert hier
    seine eigenen Feature-Funktionen. Der Feature Store orchestriert die
    Ausführung — kein Modul muss ein anderes kennen.

    Neue Features hinzufügen:
        1. Funktion in eigenem Modul implementieren (z.B. src/ml/features.py)
        2. In FEATURE_PIPELINE eintragen → fertig

Verwendung:
    from src.data.feature_store import get_features

    df = get_features("AAPL")          # alle Indikatoren als Spalten
    df = get_features("AAPL", force_refresh=True)  # Cache ignorieren
"""

import os
from datetime import date, timedelta

import pandas as pd

from src.data.price_fetcher import fetch_prices
from src.ta.TA_run import add_all_indicators

FEATURES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "features")


# ── Feature Pipeline ──────────────────────────────────────────────────────────
# Reihenfolge ist relevant: spätere Funktionen können Spalten früherer nutzen.
# Jede Funktion nimmt einen DataFrame entgegen und gibt einen zurück.

FEATURE_PIPELINE = [
    add_all_indicators,        # TA-Indikatoren (ADX, EMA, RSI, MACD, OBV ...)
    # add_regime_features,     # TODO: Market Regime (src/market_regime/features.py)
    # add_ml_features,         # TODO: ML-spezifische Features (src/ml/features.py)
]


# ── Interne Hilfsfunktionen ───────────────────────────────────────────────────

def _parquet_path(ticker: str) -> str:
    return os.path.join(FEATURES_DIR, f"{ticker}_features.parquet")


def _is_up_to_date(df: pd.DataFrame) -> bool:
    """Prüft ob der letzte Eintrag dem letzten Handelstag entspricht."""
    last_cached = df.index.max().date()
    expected = date.today() - timedelta(days=1)
    while expected.weekday() >= 5:
        expected -= timedelta(days=1)
    return last_cached >= expected


def _run_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Führt alle Funktionen der FEATURE_PIPELINE sequentiell aus."""
    for fn in FEATURE_PIPELINE:
        df = fn(df)
    return df


# ── Öffentliche API ───────────────────────────────────────────────────────────

def get_features(ticker: str, force_refresh: bool = False) -> pd.DataFrame:
    """
    Gibt einen DataFrame mit OHLCV-Daten und allen berechneten Indikatoren zurück.

    Beim ersten Aufruf werden die Indikatoren berechnet und als Parquet gespeichert.
    Folgeaufrufe lesen direkt aus dem Cache — kein erneutes Rechnen.

    Parameter:
        ticker        : Ticker-Symbol, z.B. "AAPL"
        force_refresh : True = Cache ignorieren und neu berechnen

    Rückgabe:
        DataFrame mit Spalten: Open, High, Low, Close, Volume + alle Indikatoren
    """
    path = _parquet_path(ticker)

    if not force_refresh and os.path.exists(path):
        cached = pd.read_parquet(path)
        if _is_up_to_date(cached):
            return cached

    df = fetch_prices(ticker)
    df = _run_pipeline(df)

    os.makedirs(FEATURES_DIR, exist_ok=True)
    df.to_parquet(path)
    print(f"[feature_store] {ticker}: Parquet gespeichert ({len(df)} Zeilen, {len(df.columns)} Spalten)")

    return df


def refresh_all(tickers: list[str]) -> None:
    """
    Aktualisiert den Feature-Cache für eine Liste von Tickern.

    Parameter:
        tickers : Liste von Ticker-Symbolen, z.B. ["AAPL", "MSFT"]
    """
    for ticker in tickers:
        print(f"[feature_store] Aktualisiere {ticker}...")
        get_features(ticker, force_refresh=True)
    print(f"[feature_store] Fertig. {len(tickers)} Ticker aktualisiert.")
