"""
Gleitende Durchschnitte, Bollinger Bänder & Donchian-Kanal
──────────────────────────────────────────────────────────
Trendfilter und Kontextindikatoren für den Handelsalgorithmus.

Spalten die add_moving_averages() hinzufügt:
    ema_9, ema_21, ema_50, ema_200 : Exponentiell gewichtete Durchschnitte
    price_vs_ema50                 : 'above' | 'below'
    price_vs_ema200                : 'above' | 'below'
    ma_alignment                   : 'bullish' | 'bearish' | 'mixed'

Spalten die add_bollinger_bands() hinzufügt:
    bb_mid     : SMA-20-Mittellinie
    bb_upper   : Oberes Band (Überkauft-Ziel)
    bb_lower   : Unteres Band (Überverkauft-Ziel)
    bb_width   : Relative Bandbreite = (upper - lower) / mid
    bb_pct     : %B – Position des Kurses im Band (0 = unten, 1 = oben)
    bb_squeeze : True = Volatilitätskompression; neuer Trend wahrscheinlich

Spalten die add_donchian() hinzufügt:
    donchian_high     : Höchstes Hoch der letzten 20 Tage (exkl. heute)
    donchian_low      : Niedrigstes Tief der letzten 20 Tage (exkl. heute)
    donchian_breakout : 'up' | 'down' | None

Hinweis:
    EMAs verwenden k = 2 / (period + 1), Startwert = erster gültiger Kurs.
    SMA 20 wird intern für Bollinger Bänder berechnet, aber nicht ausgegeben.
"""

import numpy as np
import pandas as pd


# ── Interne Hilfsfunktionen ──────────────────────────────────────────────────

def _ema(series: pd.Series, period: int) -> pd.Series:
    """
    Exponentiell gewichteter Durchschnitt mit k = 2 / (period + 1).
    Pandas ewm(adjust=False) entspricht exakt der klassischen EMA-Formel.
    """
    return series.ewm(span=period, adjust=False).mean()


# ── Gleitende Durchschnitte (EMA) ────────────────────────────────────────────

def add_moving_averages(
    df: pd.DataFrame,
    periods: list[int] = None,
) -> pd.DataFrame:
    """
    Berechnet EMAs und MA-Kontext-Spalten.

    Parameter:
        df      : DataFrame mit Spalte Close
        periods : EMA-Perioden (Standard: [9, 21, 50, 200])

    Rückgabe:
        DataFrame mit zusätzlichen Spalten:
            ema_9, ema_21, ema_50, ema_200
            price_vs_ema50  : 'above' | 'below'  (mittelfristiger Trendkontext)
            price_vs_ema200 : 'above' | 'below'  (langfristiger Trendkontext)
            ma_alignment    : 'bullish' wenn EMA9 > EMA21 > EMA50 > EMA200,
                              'bearish' wenn umgekehrt, sonst 'mixed'
    """
    if periods is None:
        periods = [9, 21, 50, 200]

    df = df.copy()
    close = df["Close"]

    for p in periods:
        df[f"ema_{p}"] = _ema(close, p).round(4)

    df["price_vs_ema50"]  = np.where(close > df["ema_50"],  "above", "below")
    df["price_vs_ema200"] = np.where(close > df["ema_200"], "above", "below")

    bullish = (
        (df["ema_9"]  > df["ema_21"]) &
        (df["ema_21"] > df["ema_50"]) &
        (df["ema_50"] > df["ema_200"])
    )
    bearish = (
        (df["ema_9"]  < df["ema_21"]) &
        (df["ema_21"] < df["ema_50"]) &
        (df["ema_50"] < df["ema_200"])
    )
    df["ma_alignment"] = np.select(
        [bullish, bearish],
        ["bullish", "bearish"],
        default="mixed",
    )

    return df


# ── Bollinger Bänder ──────────────────────────────────────────────────────────

def add_bollinger_bands(
    df: pd.DataFrame,
    period: int = 20,
    std_dev: float = 2.0,
    squeeze_lookback: int = 126,
) -> pd.DataFrame:
    """
    Bollinger Bänder (SMA-Basis, ±2 Standardabweichungen).

    Parameter:
        df               : DataFrame mit Spalte Close
        period           : Glättungsperiode (Standard: 20 Tage)
        std_dev          : Multiplikator für Standardabweichung (Standard: 2.0)
        squeeze_lookback : Lookback für Squeeze-Erkennung in Tagen (Standard: 126 ≈ 6 Monate)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten:
            bb_mid, bb_upper, bb_lower, bb_width, bb_pct, bb_squeeze
    """
    df = df.copy()
    close = df["Close"]

    mid   = close.rolling(period).mean()
    std   = close.rolling(period).std(ddof=1)
    upper = mid + std_dev * std
    lower = mid - std_dev * std

    df["bb_mid"]   = mid.round(4)
    df["bb_upper"] = upper.round(4)
    df["bb_lower"] = lower.round(4)
    df["bb_width"] = ((upper - lower) / mid).round(4)
    df["bb_pct"]   = ((close - lower) / (upper - lower)).round(4)

    # Squeeze: aktuelle Bandbreite ≤ Minimum der letzten `squeeze_lookback` Tage
    bb_width = df["bb_width"]
    rolling_min = bb_width.rolling(squeeze_lookback, min_periods=squeeze_lookback // 2).min()
    df["bb_squeeze"] = bb_width <= rolling_min

    return df


# ── Donchian-Kanal ────────────────────────────────────────────────────────────

def add_donchian(
    df: pd.DataFrame,
    period: int = 20,
) -> pd.DataFrame:
    """
    Donchian-Kanal – 4-Wochen-Regel nach Park & Irwin (2004).

    Der Kanal basiert auf den letzten `period` Tagen OHNE den aktuellen Tag
    (shift(1)), um Look-Ahead-Bias zu vermeiden.

    Parameter:
        df     : DataFrame mit Spalten High, Low, Close
        period : Kanalbreite in Handelstagen (Standard: 20 ≈ 4 Wochen)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten:
            donchian_high     : Höchstes Hoch der letzten `period` Tage (exkl. heute)
            donchian_low      : Niedrigstes Tief der letzten `period` Tage (exkl. heute)
            donchian_breakout : 'up' | 'down' | None
    """
    df = df.copy()

    df["donchian_high"] = df["High"].shift(1).rolling(period).max().round(4)
    df["donchian_low"]  = df["Low"].shift(1).rolling(period).min().round(4)

    conditions = [
        df["Close"] > df["donchian_high"],
        df["Close"] < df["donchian_low"],
    ]
    df["donchian_breakout"] = np.select(conditions, ["up", "down"], default="")

    return df


# ── Convenience ───────────────────────────────────────────────────────────────

def add_all(df: pd.DataFrame) -> pd.DataFrame:
    """
    Wendet alle Durchschnitts-Indikatoren auf einmal an.
    Reihenfolge: MAs → Bollinger Bänder → Donchian-Kanal
    """
    df = add_moving_averages(df)
    df = add_bollinger_bands(df)
    df = add_donchian(df)
    return df
