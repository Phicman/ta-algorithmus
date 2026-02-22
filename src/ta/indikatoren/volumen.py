"""
Volumen & OBV
─────────────
Volumen als sekundärer Bestätigungsindikator. Kurs ist primär, Volumen bestätigt.

Spalten die add_obv() hinzufügt:
    obv       : On-Balance-Volume (kumulativ; Richtung entscheidend, nicht Absolutwert)
    obv_ema   : EMA(20) des OBV → glättet den Trend für maschinelle Auswertung
    obv_trend : 'rising' | 'falling' → OBV über oder unter seiner EMA

Spalten die add_volume_context() hinzufügt:
    vol_sma20        : 20-Tage-Durchschnittsvolumen (Referenzwert)
    vol_ratio        : Heutiges Volumen / vol_sma20 (> 1.0 = überdurchschnittlich)
    vol_above_avg    : True wenn vol_ratio > 1.0
    vol_price_signal : Kurs/Volumen-Kombination nach Murphy:
                       'bullish_strong' | 'bullish_weak' |
                       'bearish_strong' | 'bearish_weak'

Quelle: Murphy (Kap. 7) – Granville OBV (1963), Volumen-Interpretationsregeln
"""

import numpy as np
import pandas as pd


# ── OBV ───────────────────────────────────────────────────────────────────────

def add_obv(
    df: pd.DataFrame,
    ema_period: int = 20,
) -> pd.DataFrame:
    """
    On-Balance-Volume nach Granville (1963).

    Konstruktion:
        Kurs höher als Vortag → Tagesvolumen addieren
        Kurs tiefer als Vortag → Tagesvolumen subtrahieren
        Kurs unverändert      → OBV bleibt gleich

    Die Richtung der OBV-Linie ist entscheidend, nicht der absolute Wert.
    OBV steigt während Kurs stagniert → bullishes Vorzeichen (OBV läuft voraus).
    OBV fällt während Kurs steigt    → bearishes Warnsignal.

    Parameter:
        df         : DataFrame mit Spalten Close, Volume
        ema_period : EMA-Periode für OBV-Glättung (Standard: 20)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: obv, obv_ema, obv_trend
    """
    df = df.copy()
    close  = df["Close"]
    volume = df["Volume"]

    direction = np.sign(close.diff()).fillna(0)
    obv = (direction * volume).cumsum()

    obv_ema = obv.ewm(span=ema_period, adjust=False).mean()

    df["obv"]       = obv.astype(int)
    df["obv_ema"]   = obv_ema.round(0).astype(float)
    df["obv_trend"] = np.where(obv >= obv_ema, "rising", "falling")

    return df


# ── Volumen-Kontext ───────────────────────────────────────────────────────────

def add_volume_context(
    df: pd.DataFrame,
    sma_period: int = 20,
    high_ratio: float = 1.5,
) -> pd.DataFrame:
    """
    Volumen-Kontext: Durchschnitt, Ratio und Kurs/Volumen-Kombination.

    vol_price_signal basiert direkt auf der Murphy-Interpretationstabelle:
        Kurs steigt + Volumen steigt → bullish_strong  (Trend wird bestätigt)
        Kurs steigt + Volumen fällt  → bullish_weak    (Kaufdruck lässt nach)
        Kurs fällt  + Volumen steigt → bearish_strong  (Verkaufsdruck steigt)
        Kurs fällt  + Volumen fällt  → bearish_weak    (Abgabe ohne Panik)

    Parameter:
        df         : DataFrame mit Spalten Close, Volume
        sma_period : Lookback für Durchschnittsvolumen (Standard: 20)
        high_ratio : Schwellenwert für vol_above_avg (Standard: 1.0 = Durchschnitt)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten:
            vol_sma20, vol_ratio, vol_above_avg, vol_price_signal
    """
    df = df.copy()
    volume = df["Volume"]
    close  = df["Close"]

    vol_sma  = volume.rolling(sma_period).mean()
    vol_ratio = volume / vol_sma

    df["vol_sma20"]     = vol_sma.round(0)
    df["vol_ratio"]     = vol_ratio.round(3)
    df["vol_above_avg"] = vol_ratio >= 1.0

    price_up   = close > close.shift(1)
    price_down = close < close.shift(1)
    vol_up     = volume > vol_sma
    vol_down   = volume <= vol_sma

    conditions = [
        price_up   & vol_up,
        price_up   & vol_down,
        price_down & vol_up,
        price_down & vol_down,
    ]
    choices = ["bullish_strong", "bullish_weak", "bearish_strong", "bearish_weak"]
    df["vol_price_signal"] = np.select(conditions, choices, default="")

    return df


# ── Convenience ───────────────────────────────────────────────────────────────

def add_all(df: pd.DataFrame) -> pd.DataFrame:
    """
    Wendet alle Volumen-Indikatoren auf einmal an.
    Reihenfolge: OBV → Volumen-Kontext
    """
    df = add_obv(df)
    df = add_volume_context(df)
    return df
