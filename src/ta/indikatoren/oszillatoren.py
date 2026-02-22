"""
Oszillatoren: RSI, MACD, Stochastik
──────────────────────────────────
Impuls- und Momentumindikatoren für den Handelsalgorithmus.

Spalten die add_rsi() hinzufügt:
    rsi         : RSI-Wert (0–100), Wilder's Smoothing (com = period−1)
    rsi_zone    : 'overbought' | 'oversold' | 'neutral'
    rsi_above50 : True = RSI > 50 → empirisch bestätigtes Aufwärtsmomentum-Signal

Spalten die add_macd() hinzufügt:
    macd          : MACD-Linie (EMA12 − EMA26)
    macd_signal   : Signallinie (EMA9 der MACD-Linie)
    macd_hist     : Histogramm (MACD − Signal)
    macd_hist_dir : 'rising' | 'falling' → dreht VOR Signallinie-Kreuzung (Frühwarnung)

Spalten die add_stochastik() hinzufügt:
    stoch_k    : Langsame %K-Linie (geglättet)
    stoch_d    : Langsame %D-Linie = Signallinie (wichtiger als %K)
    stoch_zone : 'overbought' | 'oversold' | 'neutral' → Grundlage Morris-Filter

Quellen:
    RSI-50-Crossover empirisch bestätigt: Wong, Manzur, Chew (2002)
    MACD nur als Bestätigung, nicht als Trigger: Pramudya & Ichsani (2020)
    Stochastik-Parameter und Morris-Filter: Murphy (Kap. 10)
"""

import numpy as np
import pandas as pd


# ── RSI ───────────────────────────────────────────────────────────────────────

def add_rsi(
    df: pd.DataFrame,
    period: int = 14,
    overbought: float = 70.0,
    oversold: float = 30.0,
) -> pd.DataFrame:
    """
    RSI nach Wilders Methode (com = period−1 → alpha = 1/period).

    Wichtig: RSI-Extremzonen sind nur in Seitwärtsmärkten (ADX < 25) zuverlässig.
    In Trendmärkten bleibt RSI dauerhaft überkauft/überverkauft → Fehlsignale.
    rsi_above50 ist regime-unabhängig nutzbar als Momentum-Bestätigung. (Wong 2002)

    Parameter:
        df         : DataFrame mit Spalte Close
        period     : Glättungsperiode (Standard: 14 = halber 28-Tage-Zyklus)
        overbought : Schwellenwert Überkauft (Standard: 70)
        oversold   : Schwellenwert Überverkauft (Standard: 30)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: rsi, rsi_zone, rsi_above50
    """
    df = df.copy()
    close = df["Close"]

    delta = close.diff()
    gain  = delta.clip(lower=0)
    loss  = (-delta).clip(lower=0)

    # Wilders Glättung: com = period-1 entspricht alpha = 1/period
    avg_gain = gain.ewm(com=period - 1, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, adjust=False, min_periods=period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = (100 - 100 / (1 + rs)).round(2)

    df["rsi_zone"] = np.select(
        [df["rsi"] >= overbought, df["rsi"] <= oversold],
        ["overbought", "oversold"],
        default="neutral",
    )
    df["rsi_above50"] = df["rsi"] > 50

    return df


# ── MACD ──────────────────────────────────────────────────────────────────────

def add_macd(
    df: pd.DataFrame,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """
    MACD – Moving Average Convergence/Divergence.

    Nur als Bestätigung und Trendfilter, nicht als alleinigen Trigger verwenden.
    macd_hist_dir erkennt Wendepunkte des Histogramms – dieser Richtungswechsel
    erscheint VOR der Signallinie-Kreuzung und dient als Frühwarnung. (Pramudya 2020)

    Beste Signale: Kaufsignal unter der Nulllinie; Verkaufssignal über der Nulllinie.

    Parameter:
        df     : DataFrame mit Spalte Close
        fast   : Periode schnelle EMA (Standard: 12)
        slow   : Periode langsame EMA (Standard: 26)
        signal : Periode Signallinie  (Standard: 9)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: macd, macd_signal, macd_hist, macd_hist_dir
    """
    df = df.copy()
    close = df["Close"]

    ema_fast    = close.ewm(span=fast,   adjust=False).mean()
    ema_slow    = close.ewm(span=slow,   adjust=False).mean()
    macd_line   = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist        = macd_line - signal_line

    df["macd"]        = macd_line.round(4)
    df["macd_signal"] = signal_line.round(4)
    df["macd_hist"]   = hist.round(4)

    # Richtung des Histogramms: steigend = Kaufdruck nimmt zu
    df["macd_hist_dir"] = np.where(hist > hist.shift(1), "rising", "falling")

    return df


# ── Stochastik ────────────────────────────────────────────────────────────────

def add_stochastik(
    df: pd.DataFrame,
    k_period: int = 14,
    smooth: int = 3,
    d_period: int = 3,
    overbought: float = 80.0,
    oversold: float = 20.0,
) -> pd.DataFrame:
    """
    Langsame Stochastik (%K und %D geglättet).

    Konstruktion:
        Fast %K  = 100 × (Close − Low14) / (High14 − Low14)
        Slow %K  = SMA(smooth) der Fast %K  → stoch_k
        Slow %D  = SMA(d_period) der Slow %K → stoch_d  (Signallinie)

    Slow %D (stoch_d) ist die wichtigere Linie für Handelssignale.
    stoch_zone ist die Grundlage für den Morris-Candlestick-Filter:
        Candlestick-Formationen nur auswerten wenn stoch_d > 80 oder < 20.

    Parameter:
        df         : DataFrame mit Spalten High, Low, Close
        k_period   : Lookback-Periode für %K (Standard: 14)
        smooth     : Glättung für Slow %K (Standard: 3)
        d_period   : Glättung für Slow %D (Standard: 3)
        overbought : Schwellenwert Überkauft (Standard: 80)
        oversold   : Schwellenwert Überverkauft (Standard: 20)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: stoch_k, stoch_d, stoch_zone
    """
    df = df.copy()

    low_k  = df["Low"].rolling(k_period).min()
    high_k = df["High"].rolling(k_period).max()
    fast_k = 100 * (df["Close"] - low_k) / (high_k - low_k)

    slow_k = fast_k.rolling(smooth).mean()
    slow_d = slow_k.rolling(d_period).mean()

    df["stoch_k"] = slow_k.round(2)
    df["stoch_d"] = slow_d.round(2)

    df["stoch_zone"] = np.select(
        [df["stoch_d"] >= overbought, df["stoch_d"] <= oversold],
        ["overbought", "oversold"],
        default="neutral",
    )

    return df


# ── Convenience ───────────────────────────────────────────────────────────────

def add_all(df: pd.DataFrame) -> pd.DataFrame:
    """
    Wendet alle Oszillatoren auf einmal an.
    Reihenfolge: RSI → MACD → Stochastik
    """
    df = add_rsi(df)
    df = add_macd(df)
    df = add_stochastik(df)
    return df
