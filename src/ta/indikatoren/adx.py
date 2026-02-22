"""
ADX / DMI & Parabolic SAR
─────────────────────────
Regime-Filter: Bestimmt ob Trend- oder Oszillator-Logik gilt.

Spalten die add_adx() hinzufügt:
    adx      : Trendstärke (0–100), richtungsunabhängig
    di_plus  : Stärke der Aufwärtsbewegungen
    di_minus : Stärke der Abwärtsbewegungen
    regime   : 'ranging' | 'weak_trend' | 'trending' | 'exhaustion'

Spalten die add_parabolic_sar() hinzufügt:
    psar      : Dynamischer Trailing Stop
    psar_bull : True = Kurs über SAR (Aufwärtstrend)
"""

import numpy as np
import pandas as pd


# ── Interne Hilfsfunktionen ──────────────────────────────────────────────────

def _wilder_smooth(values: np.ndarray, period: int) -> np.ndarray:
    """
    Wilders kumulierte Glättung – für TR und DM.
    Erster Wert = Summe der ersten `period` Werte.
    Folgewerte:  S[i] = S[i-1] - S[i-1]/period + values[i]

    Hinweis: Die Division in di_plus/di_minus (smooth_dm / smooth_tr)
    hebt die fehlende Normalisierung auf – das Ergebnis ist identisch
    mit dem auf Durchschnitten basierenden Ansatz.
    """
    result = np.full(len(values), np.nan)
    result[period - 1] = np.nansum(values[:period])
    for i in range(period, len(values)):
        result[i] = result[i - 1] - result[i - 1] / period + values[i]
    return result


def _wilder_smooth_avg(values: np.ndarray, period: int) -> np.ndarray:
    """
    Wilders Durchschnitts-Glättung – für DX → ADX.
    Erster Wert = Durchschnitt der ersten `period` gültigen Werte.
    Folgewerte:  S[i] = (S[i-1] × (period-1) + values[i]) / period
    """
    result = np.full(len(values), np.nan)
    valid = np.where(~np.isnan(values))[0]
    if len(valid) < period:
        return result
    start = valid[0]
    result[start + period - 1] = np.nanmean(values[start : start + period])
    for i in range(start + period, len(values)):
        if not np.isnan(values[i]):
            result[i] = (result[i - 1] * (period - 1) + values[i]) / period
    return result


# ── ADX / DMI ────────────────────────────────────────────────────────────────

def add_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Berechnet ADX, +DI, -DI und Regime-Klassifikation nach Wilders Methode.

    Parameter:
        df     : DataFrame mit Spalten High, Low, Close
        period : Glättungsperiode (Standard: 14 nach Wilder)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: adx, di_plus, di_minus, regime
    """
    df = df.copy()
    high  = df["High"].to_numpy(dtype=float).flatten()
    low   = df["Low"].to_numpy(dtype=float).flatten()
    close = df["Close"].to_numpy(dtype=float).flatten()

    # True Range: Maximum aus drei Spannweiten
    prev_close = np.concatenate([[np.nan], close[:-1]])
    tr = np.maximum.reduce([
        high - low,
        np.abs(high - prev_close),
        np.abs(low  - prev_close),
    ])
    tr[0] = np.nan

    # Directional Movement
    up   = high - np.concatenate([[0.0], high[:-1]])
    down = np.concatenate([[0.0], low[:-1]]) - low
    up[0] = 0.0
    down[0] = 0.0

    dm_plus  = np.where((up > down)  & (up   > 0), up,   0.0)
    dm_minus = np.where((down > up)  & (down > 0), down, 0.0)

    # Wilders Glättung (Index 0 ist NaN/0, daher ab Index 1)
    smooth_tr    = _wilder_smooth(tr[1:],       period)
    smooth_plus  = _wilder_smooth(dm_plus[1:],  period)
    smooth_minus = _wilder_smooth(dm_minus[1:], period)

    # Directional Indicators
    with np.errstate(invalid="ignore", divide="ignore"):
        di_plus  = np.where(smooth_tr > 0, 100 * smooth_plus  / smooth_tr, np.nan)
        di_minus = np.where(smooth_tr > 0, 100 * smooth_minus / smooth_tr, np.nan)

    # DX → ADX
    with np.errstate(invalid="ignore", divide="ignore"):
        dx_sum = di_plus + di_minus
        dx = np.where(dx_sum > 0, 100 * np.abs(di_plus - di_minus) / dx_sum, np.nan)

    adx = _wilder_smooth_avg(dx, period)

    # Auf Originallänge auffüllen (Index 0 wurde übersprungen)
    pad = np.array([np.nan])
    df["di_plus"]  = np.round(np.concatenate([pad, di_plus]),  2)
    df["di_minus"] = np.round(np.concatenate([pad, di_minus]), 2)
    df["adx"]      = np.round(np.concatenate([pad, adx]),      2)
    df["regime"]   = _classify_regime(df["adx"])

    return df


def _classify_regime(adx: pd.Series) -> pd.Series:
    """
    Klassifiziert das Marktregime anhand ADX-Wert und -Richtung.

    ranging    : ADX < 20            → Oszillatoren verwenden
    weak_trend : ADX 20–25           → abwarten / vorsichtig
    trending   : ADX > 25, steigend  → Trendfolgeindikatoren
    exhaustion : ADX > 40, fallend   → keine neuen Positionen
    """
    adx_rising = adx > adx.shift(1)
    conditions = [
        (adx > 40) & ~adx_rising,
        adx >= 25,
        adx >= 20,
    ]
    choices = ["exhaustion", "trending", "weak_trend"]
    return pd.Series(
        np.select(conditions, choices, default="ranging"),
        index=adx.index,
        dtype="object",
    )


# ── Parabolic SAR ────────────────────────────────────────────────────────────

def add_parabolic_sar(
    df: pd.DataFrame,
    af_start: float = 0.02,
    af_step:  float = 0.02,
    af_max:   float = 0.20,
) -> pd.DataFrame:
    """
    Parabolic SAR (Stop and Reverse) nach Wilder.

    Nur in Trendmärkten sinnvoll (regime == 'trending'). Mit add_adx()
    kombinieren und psar nur ausgeben wenn ADX > 25.

    Parameter:
        df       : DataFrame mit Spalten High, Low
        af_start : Startwert Beschleunigungsfaktor (Standard: 0.02)
        af_step  : Erhöhung pro neuem Extrempunkt  (Standard: 0.02)
        af_max   : Maximum Beschleunigungsfaktor   (Standard: 0.20)

    Rückgabe:
        DataFrame mit zusätzlichen Spalten: psar, psar_bull
    """
    df   = df.copy()
    high = df["High"].to_numpy(dtype=float).flatten()
    low  = df["Low"].to_numpy(dtype=float).flatten()
    n    = len(df)

    psar = np.full(n, np.nan)
    bull = np.ones(n, dtype=bool)
    ep   = high[0]
    af   = af_start
    psar[0] = low[0]

    for i in range(1, n):
        if bull[i - 1]:
            # Aufwärtstrend: SAR bewegt sich aufwärts Richtung EP
            psar[i] = psar[i - 1] + af * (ep - psar[i - 1])
            # SAR darf nicht über die letzten zwei Tiefs hinausragen
            psar[i] = min(psar[i], low[i - 1])
            if i >= 2:
                psar[i] = min(psar[i], low[i - 2])

            if low[i] <= psar[i]:
                # Kurs durchbricht SAR → Wechsel zu Abwärtstrend
                bull[i] = False
                psar[i] = ep
                ep       = low[i]
                af       = af_start
            else:
                bull[i] = True
                if high[i] > ep:
                    ep = high[i]
                    af = min(af + af_step, af_max)

        else:
            # Abwärtstrend: SAR bewegt sich abwärts Richtung EP
            psar[i] = psar[i - 1] + af * (ep - psar[i - 1])
            # SAR darf nicht unter die letzten zwei Hochs fallen
            psar[i] = max(psar[i], high[i - 1])
            if i >= 2:
                psar[i] = max(psar[i], high[i - 2])

            if high[i] >= psar[i]:
                # Kurs durchbricht SAR → Wechsel zu Aufwärtstrend
                bull[i] = True
                psar[i] = ep
                ep       = high[i]
                af       = af_start
            else:
                bull[i] = False
                if low[i] < ep:
                    ep = low[i]
                    af = min(af + af_step, af_max)

    df["psar"]      = np.round(psar, 4)
    df["psar_bull"] = bull
    return df


# ── Convenience ──────────────────────────────────────────────────────────────

def get_regime(df: pd.DataFrame, period: int = 14) -> str:
    """
    Gibt das aktuelle Marktregime zurück (letzter Wert im DataFrame).

    Returns:
        'ranging' | 'weak_trend' | 'trending' | 'exhaustion'
    """
    if "regime" not in df.columns:
        df = add_adx(df, period=period)
    return df["regime"].iloc[-1]
