"""
TA-Modul: Technische Analyse – Hauptmodul
─────────────────────────────────────────
Führt alle Indikator-Module zusammen und berechnet einen TA-Score.

Scoring-Prinzipien (Quellen: siehe 02d_signal_logik.md):
    - Kombinations-Signale sind Einzelsignalen überproportional überlegen (Han et al. 2022)
    - ADX-Regime bestimmt welche Signale auswertbar sind
    - RSI-Extremzonen nur in ranging-Märkten zuverlässig (Wong 2002)
    - MACD nur als Bestätigung, nie als Trigger (Pramudya 2020)
    - Volumen bestätigt; Preis triggert (Murphy)

Gewichtung:
    Alle Signale starten bei 1.0 (binär: Signal feuert → +weight, sonst +0).
    Nach Backtesting können einzelne Weights angepasst werden.
    Die Schwellenwerte sind prozentual zu sum(WEIGHTS) – sie passen sich
    automatisch an wenn Weights geändert werden.

Verwendung (empfohlen — mit Feature Store):
    from src.data.feature_store import get_features
    from src.ta.TA_run import run, print_signal

    df = get_features("AAPL")                      # Indikatoren aus Cache
    result = run(df, ticker="AAPL", name="Apple Inc.")
    print_signal(result)

Verwendung (direkt — ohne Cache):
    from src.data.price_fetcher import fetch_prices
    from src.ta.TA_run import run, print_signal

    df = fetch_prices("AAPL")                      # rohe OHLCV-Daten
    result = run(df, ticker="AAPL", name="Apple Inc.")  # berechnet Indikatoren intern
    print_signal(result)
"""

import pandas as pd
import numpy as np

from .indikatoren.adx import add_adx, add_parabolic_sar
from .indikatoren.durchschnitte import add_moving_averages, add_bollinger_bands, add_donchian
from .indikatoren.oszillatoren import add_rsi, add_macd, add_stochastik
from .indikatoren.volumen import add_obv, add_volume_context


# ── Konfiguration ─────────────────────────────────────────────────────────────
# Alle Weights starten bei 1.0 (binäres Scoring).
# Nach Backtesting können einzelne Werte angepasst werden.
# sum(WEIGHTS) bestimmt automatisch den max. Score für die Schwellenwerte.

WEIGHTS: dict[str, float] = {
    # Gruppe 1: Trend-Kontext
    "ma_alignment":      1.0,   # ema9 > ema21 > ema50 > ema200 (Multi-Horizont)
    "price_vs_ema200":   1.0,   # Kurs über EMA200 (langfristiger Trend)
    "price_vs_ema50":    1.0,   # Kurs über EMA50  (mittelfristiger Trend)
    # Gruppe 2: Regime & Trendstärke
    "regime_trending":   1.0,   # ADX > 25 steigend (Trendmarkt bestätigt)
    "dmi_bullish":       1.0,   # DI+ > DI- (bullishe Trendrichtung)
    "psar_bullish":      1.0,   # SAR unter Kurs (nur trending)
    "donchian_breakout": 1.0,   # Ausbruch über 20-Tage-Hoch (Park & Irwin 2004)
    # Gruppe 3: Momentum
    "rsi_above50":       1.0,   # RSI > 50 – regime-unabhängig (Wong 2002)
    "rsi_oversold":      1.0,   # RSI überverkauft – nur ranging zuverlässig
    "stoch_oversold":    1.0,   # Stochastik überverkauft (Morris-Filter)
    "macd_cross":        1.0,   # MACD > Signal (Bestätigung; Pramudya 2020)
    "macd_hist_rising":  1.0,   # Histogramm steigend (Frühwarnung)
    "macd_above_zero":   1.0,   # MACD > 0 (bullisher Trendkontext)
    # Gruppe 4: Volumen
    "obv_rising":        1.0,   # OBV über EMA (akkumulatives Kaufvolumen)
    "vol_strong_bull":   1.0,   # Kurs ↑ + Volumen ↑ (stärkste Bestätigung)
    "vol_above_avg":     1.0,   # Volumen > SMA20 (Ausbruchs-Bestätigung)
    # Gruppe 5: Bollinger Bänder
    "bb_squeeze":        1.0,   # Squeeze aktiv (Ausbruch wahrscheinlich)
    "bb_pct_low":        1.0,   # %B < 0.2 (Kurs nahe unterem Band)
}

# Schwellenwerte als Anteil von sum(WEIGHTS) – passen sich automatisch an
SCORE_THRESHOLDS: dict[str, float] = {
    "STARK":  0.65,   # ≥ 65% → BUY / STARK
    "MITTEL": 0.40,   # ≥ 40% → BUY / MITTEL
    "WATCH":  0.25,   # ≥ 25% → WATCH / SCHWACH
}


# ── Indikator-Pipeline ────────────────────────────────────────────────────────

def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Wendet alle TA-Indikatoren in der korrekten Reihenfolge an.

    Parameter:
        df : OHLCV DataFrame mit Spalten Open, High, Low, Close, Volume

    Rückgabe:
        DataFrame mit allen Indikator-Spalten (siehe claude.md für Übersicht)
    """
    df = add_adx(df)
    df = add_parabolic_sar(df)
    df = add_moving_averages(df)
    df = add_bollinger_bands(df)
    df = add_donchian(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_stochastik(df)
    df = add_obv(df)
    df = add_volume_context(df)
    return df


# ── Scoring ───────────────────────────────────────────────────────────────────

def _val(row: pd.Series, col: str, default=None):
    """Liest einen Spaltenwert sicher aus; gibt default bei NaN zurück."""
    v = row.get(col, default)
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return default
    return v


def _evaluate_signals(row: pd.Series, regime: str) -> dict[str, bool | None]:
    """
    Wertet alle Signale für den letzten Handelstag aus.

    Rückgabe:
        Dict {signal_name: True | False | None}
        True  = Signal feuert   → +weight
        False = Signal feuert nicht → +0
        None  = Signal im aktuellen Regime nicht auswertbar → n/a
    """
    s: dict[str, bool | None] = {}

    # ── Gruppe 1: Trend-Kontext ───────────────────────────────────────────────
    s["ma_alignment"]    = _val(row, "ma_alignment") == "bullish"
    s["price_vs_ema200"] = _val(row, "price_vs_ema200") == "above"
    s["price_vs_ema50"]  = _val(row, "price_vs_ema50") == "above"

    # ── Gruppe 2: Regime & Trendstärke ───────────────────────────────────────
    s["regime_trending"] = regime == "trending"

    di_plus  = _val(row, "di_plus",  0.0)
    di_minus = _val(row, "di_minus", 0.0)
    s["dmi_bullish"] = di_plus > di_minus

    # PSAR und Donchian: nur in trending zuverlässig; in ranging n/a
    if regime in ("trending", "weak_trend"):
        s["psar_bullish"]      = bool(_val(row, "psar_bull", False))
        s["donchian_breakout"] = _val(row, "donchian_breakout") == "up"
    else:
        s["psar_bullish"]      = None
        s["donchian_breakout"] = None

    # ── Gruppe 3: Momentum ────────────────────────────────────────────────────
    # RSI > 50: regime-unabhängig (Wong 2002)
    s["rsi_above50"] = bool(_val(row, "rsi_above50", False))

    # RSI überverkauft: nur in ranging zuverlässig (in Trends dauerhaft überkauft)
    if regime == "ranging":
        s["rsi_oversold"] = _val(row, "rsi_zone") == "oversold"
    else:
        s["rsi_oversold"] = None

    s["stoch_oversold"]   = _val(row, "stoch_zone") == "oversold"
    s["macd_cross"]       = _val(row, "macd", 0.0) > _val(row, "macd_signal", 0.0)
    s["macd_hist_rising"] = _val(row, "macd_hist_dir") == "rising"
    s["macd_above_zero"]  = _val(row, "macd", 0.0) > 0

    # ── Gruppe 4: Volumen ─────────────────────────────────────────────────────
    s["obv_rising"]     = _val(row, "obv_trend") == "rising"
    s["vol_strong_bull"] = _val(row, "vol_price_signal") == "bullish_strong"
    s["vol_above_avg"]  = bool(_val(row, "vol_above_avg", False))

    # ── Gruppe 5: Bollinger Bänder ────────────────────────────────────────────
    s["bb_squeeze"] = bool(_val(row, "bb_squeeze", False))
    bb_pct = _val(row, "bb_pct", None)
    s["bb_pct_low"] = bb_pct is not None and bb_pct < 0.2

    return s


def _compute_score(
    signals: dict[str, bool | None],
    weights: dict[str, float],
) -> float:
    """
    Berechnet den Score aus den gefeuerten Signalen und den Weights.

    None-Signale (n/a) werden nicht gewertet und auch nicht vom Maximum abgezogen.
    """
    return sum(
        weights[k]
        for k, fired in signals.items()
        if fired is True
    )


def _classify(score: float, weights: dict[str, float]) -> tuple[str, str]:
    """
    Klassifiziert Score prozentual zu sum(weights).

    Returns:
        (signal, staerke)
    """
    score_max = sum(weights.values())
    if score_max == 0:
        return "NEUTRAL", "–"

    pct = score / score_max

    if pct >= SCORE_THRESHOLDS["STARK"]:
        return "BUY", "STARK"
    elif pct >= SCORE_THRESHOLDS["MITTEL"]:
        return "BUY", "MITTEL"
    elif pct >= SCORE_THRESHOLDS["WATCH"]:
        return "WATCH", "SCHWACH"
    else:
        return "NEUTRAL", "–"


# ── Hauptfunktion ─────────────────────────────────────────────────────────────

def run(
    df: pd.DataFrame,
    ticker: str = "",
    name: str = "",
    weights: dict[str, float] | None = None,
) -> dict:
    """
    Führt die vollständige TA-Analyse für einen Ticker durch.

    Ablauf:
        1. Alle Indikatoren berechnen
        2. Letzten Handelstag auswerten
        3. Signale regime-bewusst evaluieren
        4. Score berechnen und klassifizieren

    Parameter:
        df      : OHLCV DataFrame (Spalten: Open, High, Low, Close, Volume)
        ticker  : Ticker-Symbol (z.B. 'AAPL')
        name    : Unternehmensname (optional)
        weights : Eigene Weights (Standard: Modul-WEIGHTS)

    Rückgabe:
        dict mit:
            ticker   : str
            name     : str
            datum    : date
            kurs     : float
            signal   : 'BUY' | 'WATCH' | 'NEUTRAL'
            staerke  : 'STARK' | 'MITTEL' | 'SCHWACH' | '–'
            score    : float
            score_max: float  (sum der aktiven Weights)
            regime   : str
            signals  : dict   {name: True | False | None}
            df       : DataFrame mit allen Indikatoren
    """
    w = weights if weights is not None else WEIGHTS

    if "rsi" not in df.columns:
        df = add_all_indicators(df)
    last   = df.iloc[-1]
    regime = _val(last, "regime", "ranging")

    # Exhaustion: keine neuen Positionen
    if regime == "exhaustion":
        signals = {k: None for k in w}
        idx = df.index[-1]
        return {
            "ticker":    ticker,
            "name":      name,
            "datum":     idx.date() if hasattr(idx, "date") else idx,
            "kurs":      round(float(_val(last, "Close", 0.0)), 2),
            "signal":    "NEUTRAL",
            "staerke":   "–",
            "score":     0.0,
            "score_max": sum(w.values()),
            "regime":    regime,
            "signals":   signals,
            "df":        df,
        }

    signals  = _evaluate_signals(last, regime)
    score    = _compute_score(signals, w)
    signal, staerke = _classify(score, w)

    idx = df.index[-1]
    return {
        "ticker":    ticker,
        "name":      name,
        "datum":     idx.date() if hasattr(idx, "date") else idx,
        "kurs":      round(float(_val(last, "Close", 0.0)), 2),
        "signal":    signal,
        "staerke":   staerke,
        "score":     round(score, 1),
        "score_max": sum(w.values()),
        "regime":    regime,
        "signals":   signals,
        "df":        df,
    }


# ── Ausgabe ───────────────────────────────────────────────────────────────────

# Lesbare Beschreibung je Signal für die Konsolenausgabe
_SIGNAL_LABELS: dict[str, str] = {
    "ma_alignment":      "MA-Alignment bullish (ema9>21>50>200)",
    "price_vs_ema200":   "Kurs über EMA200",
    "price_vs_ema50":    "Kurs über EMA50",
    "regime_trending":   "Regime: trending (ADX > 25 steigend)",
    "dmi_bullish":       "DMI: DI+ > DI-",
    "psar_bullish":      "Parabolic SAR: bullish",
    "donchian_breakout": "Donchian-Ausbruch über 20-Tage-Hoch",
    "rsi_above50":       "RSI > 50 (Aufwärtsmomentum)",
    "rsi_oversold":      "RSI überverkauft (ranging-Signal)",
    "stoch_oversold":    "Stochastik überverkauft (Morris-Filter)",
    "macd_cross":        "MACD über Signallinie",
    "macd_hist_rising":  "MACD-Histogramm steigend",
    "macd_above_zero":   "MACD über Null",
    "obv_rising":        "OBV steigend (Kaufvolumen)",
    "vol_strong_bull":   "Volumen bestätigt Kursanstieg",
    "vol_above_avg":     "Volumen überdurchschnittlich",
    "bb_squeeze":        "Bollinger Squeeze aktiv",
    "bb_pct_low":        "Kurs nahe unterem Bollinger Band (%B < 0.2)",
}


def print_signal(result: dict, show_details: bool = True) -> None:
    """
    Gibt das TA-Signal in lesbarem Format auf der Konsole aus.

    Parameter:
        result       : Rückgabe von run()
        show_details : True = alle Signale mit Status anzeigen
    """
    sep = "─" * 56
    score_max = result["score_max"]
    score     = result["score"]
    pct       = round(score / score_max * 100) if score_max else 0

    print(sep)
    if result["ticker"]:
        print(f"  Ticker:   {result['ticker']}")
    if result["name"]:
        print(f"  Name:     {result['name']}")
    print(f"  Datum:    {result['datum']}")
    print(f"  Kurs:     {result['kurs']:.2f}")
    print(f"  Regime:   {result['regime']}")
    print()
    print(f"  Signal:   {result['signal']}")
    print(f"  Stärke:   {result['staerke']}")
    print(f"  Score:    {score:.0f} / {score_max:.0f}  ({pct}%)")
    print(sep)

    if show_details:
        print("  Signale:")
        for key, fired in result["signals"].items():
            label = _SIGNAL_LABELS.get(key, key)
            if fired is True:
                marker = "✓"
            elif fired is False:
                marker = "✗"
            else:
                marker = "–"
            print(f"    {marker} {label}")
        print(sep)
