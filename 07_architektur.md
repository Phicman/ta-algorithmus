# 07 – Algorithmus-Architektur

← [Zurück zum Index](../claude.md)

---

## Systemübersicht

```
[Ticker-Liste]
     ↓
[OHLCV-Daten laden]          (API / yfinance)
     ↓
[Langfrist-Kontext]          (Wochen-/Monatschart-Trend)
     ↓
[ADX Regime-Filter]          (Trend vs. Range erkennen)
     ↓
[Indikator-Berechnung]       (RSI, MACD, Bollinger, MA, Volumen, OBV)
     ↓
[Muster-Scanner]             (je Muster eine Funktion)
     ↓
[Signal-Filter]              (Trendrichtung, Volumen, CRV, Timeframe)
     ↓
[Output-Liste]               (Ticker, Muster, Signal, Stärke, Datum, Kursziel, Stop)
```

---

## Datenquellen

| Quelle | Typ | Notizen |
|--------|-----|---------|
| Yahoo Finance (yfinance) | Python-Bibliothek | Kostenlos; geeignet für Prototyp |
| Alpha Vantage | REST API | Kostenlose Tier; Ratenlimit beachten |
| Polygon.io | REST API | Umfangreicher; kostenpflichtig |

**Benötigt:** Open, High, Low, Close, Volume – mind. 2 Jahre Historie

---

## Indikator-Module (geplant)

| Modul | Indikatoren | Status |
|-------|-------------|--------|
| Gleitende Durchschnitte | SMA, EMA, Double/Triple Crossover | 🔲 |
| Bollinger Bänder | 20 Tage, ±2σ; Bandbreite | 🔲 |
| Oszillatoren | RSI, Stochastik (langsam), MACD, Momentum, ROC, %R, CCI | 🔲 |
| Volumen | OBV, Volumen-Divergenz, Blowoff-Erkennung | 🔲 |
| ADX / DMI | Regime-Filter, DI-Kreuzung, Parabolic SAR | 🔲 |
| Fibonacci | Retracements (38/50/62 %), Zeitziele | 🔲 |

---

## Muster-Scanner (geplant)

| Muster | Typ | Status |
|--------|-----|--------|
| Kopf-Schulter (normal + invers) | Umkehr | 🔲 |
| Doppel-/Dreifachtop/-boden | Umkehr | 🔲 |
| Symmetrisches Dreieck | Fortsetzung | 🔲 |
| Aufsteigendes / Absteigendes Dreieck | Fortsetzung | 🔲 |
| Flagge / Wimpel | Fortsetzung | 🔲 |
| Keil (steigend/fallend) | Fortsetzung/Umkehr | 🔲 |
| Rechteck / Trading Range | Fortsetzung | 🔲 |
| Trendlinien-Ausbruch | Trend | 🔲 |
| Gap-Erkennung (3 Typen) | Kontext | 🔲 |
| Umkehrtag / Selling Climax | Warnsignal | 🔲 |
| Trendkanal | Kontext | 🔲 |
| Retracement-Level | S/R | 🔲 |
| Speedlines | S/R | 🔲 |
| Candlestick-Muster (20+) | Kurzfristig | 🔲 |
| P&F B-1 / S-1 Signale | Präzise S/R | 🔲 |

---

## Signal-Output Format

```
--------------------------------------------------
Ticker:    AAPL
Name:      Apple Inc.
Muster:    Kopf-Schulter (Bearish)
Signal:    SELL
Stärke:    STARK
Timeframe: Daily
Datum:     2026-02-21
Kurs:      195.40
Kursziel:  178.00
Stop:      199.50
CRV:       3.5:1
--------------------------------------------------
```

---

## Backtest-Framework (geplant)

- Walk-Forward Testing (In-Sample / Out-of-Sample)
- Gleiche Parameter für alle Märkte (gegen Over-Fitting)
- Bewertungsmetriken: Sharpe Ratio, Max Drawdown, Win Rate, Ø CRV

---

## Technologie-Stack (Vorschlag)

| Komponente | Technologie |
|------------|-------------|
| Datenabruf | Python + yfinance / requests |
| Indikator-Berechnung | pandas-ta / ta-lib |
| Muster-Erkennung | Eigene Funktionen |
| Output | CSV / JSON / Dashboard |
| Visualisierung | matplotlib / plotly |
