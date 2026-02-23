# Handelsalgorithmus – Projekt-Dokumentation

> Zentrale Dokumentation zum Aufbau eines modularen, signalbasierten Handelsalgorithmus.
> Projektphase: Konzeption + Data-Modul + alle TA-Indikatoren implementiert
> Letzte Aktualisierung: 2026-02-23

---

## Projektziel

Aufbau eines modularen Algorithmus zur automatisierten Analyse von Aktiendaten und Generierung von Kaufsignalen. Jedes Modul analysiert die Daten aus einer anderen Perspektive und liefert einen numerischen Output-Wert. Überschreitet der aggregierte Gesamt-Score einen definierten Schwellenwert, wird ein Kaufsignal ausgegeben.

---

## Scope

| Parameter | Beschreibung |
|-----------|--------------|
| **Signaltyp** | Kaufsignale (Verkauf/Short folgt später) |
| **Instrumente** | Aktien (Optionen/Zertifikate folgen später) |
| **Märkte** | US-Aktien (europäische Märkte folgen später) |
| **Timeframe** | Swing bis positionsorientiert (Tage bis Monate) |
| **Standard-Kerze** | 1 Tag (Daily) |

---

## Architektur-Prinzip

```
Aktiendaten
     │
     ├──► Modul 1: Technische Analyse  ──► Score
     ├──► Modul 2: ML-Analyse          ──► Score
     ├──► Modul 3: Sentiment-Analyse   ──► Score
     ├──► Modul 4: Market Regime       ──► Score
     └──► ...weitere Module            ──► Score
                                            │
                                     Aggregation (TBD)
                                            │
                              Score > Schwellenwert?
                                    │           │
                                   JA          NEIN
                                    │
                             KAUFSIGNAL
```

---

## Modulübersicht

| Modul | Datei | Status |
|-------|-------|--------|
| Strategie & Ziel | [01_strategie.md](./01_strategie.md) | 🔲 Konzept |
| Technische Analyse | [02_technische_analyse/README.md](./02_technische_analyse/README.md) | 🔲 Konzept |
| ML-Analyse | [03_ml_analyse/README.md](./03_ml_analyse/README.md) | 🔄 Dokumentation läuft |
| Sentiment-Analyse | [04_sentiment_analyse/README.md](./04_sentiment_analyse/README.md) | 🔲 Konzept |
| Market Regime | [05_market_regime/README.md](./05_market_regime/README.md) | 🔲 Konzept |
| Geldmanagement | [06_geldmanagement.md](./06_geldmanagement.md) | 🔄 Dokumentation läuft |
| Architektur | [07_architektur.md](./07_architektur.md) | ✅ Dokumentiert |
| TODO / Backlog | [08_todo.md](./08_todo.md) | ✅ Aktiv |

---

## Implementierungsstand

| Datei | Beschreibung | Status |
|-------|-------------|--------|
| `src/data/price_fetcher.py` | yfinance → OHLCV CSV, Multi-Ticker, Caching | ✅ Fertig |
| `src/data/news_fetcher.py` | Alpha Vantage News API (benötigt `.env` mit API-Key) | ✅ Fertig |
| `src/data/feature_store.py` | Parquet-Cache für Indikatoren; FEATURE_PIPELINE orchestriert alle Module | ✅ Fertig |
| `src/ta/indikatoren/adx.py` | ADX/DMI (Regime-Filter) + Parabolic SAR | ✅ Fertig |
| `src/ta/indikatoren/durchschnitte.py` | EMA 9/21/50/200, Bollinger Bänder, Donchian-Kanal | ✅ Fertig |
| `src/ta/indikatoren/oszillatoren.py` | RSI (Wilder), MACD, Slow Stochastik | ✅ Fertig |
| `src/ta/indikatoren/volumen.py` | OBV + OBV-Trend, Volumen-Kontext, Kurs/Volumen-Signal | ✅ Fertig |
| `src/ta/TA_run.py` | TA-Scoring, Haupt-Runner; akzeptiert pre-computed df vom Feature Store | ✅ Fertig |
| `main.py` | Einstiegspunkt — analysiert alle Ticker aus `tickers.txt` | ✅ Fertig |
| `tickers.txt` | AAPL, MSFT, NVDA, JPM, BAC | ✅ Fertig |
| `requirements.txt` | yfinance, pandas, requests, python-dotenv, pyarrow | ✅ Fertig |
| `03_ml_analyse/03a_modelle/dtw_generic_pattern.md` | DTW Generic Pattern Recognition — Algorithmus, UCR Suite, Parameter, Ergebnisse | ✅ Fertig |
| `03_ml_analyse/03a_modelle/ffnn_volume_profile.md` | FFNN + Volume-Profile — b/p-Shape, Features, Walk-Forward-CV, Ergebnisse | ✅ Fertig |
| `03_ml_analyse/03a_modelle/prml_candlestick_rf.md` | PRML Candlestick + Random Forest — 13 Shapes, 9 Indikatoren, Pattern-Screening, Ergebnisse | ✅ Fertig |
| `03_ml_analyse/03b_features/volume_profile.md` | Volume-Profile Feature-Definition (b/p-shape, delta, new_min/max, candlestick_tick) | ✅ Fertig |
| `03_ml_analyse/03b_features/candlestick_shape_loc.md` | Candlestick Shape (13 Formen) + Loc (8 relative Positionen) — formal + Python-Implementierung | ✅ Fertig |
| `03_ml_analyse/03d_backtesting.md` | Evaluierungsmetriken (WWR, PPC, MDD, Sharpe, IR, AAR, F-Measure, Profit/MDD), Walk-Forward, Walk-Forward-Parametrierung, Sliding Window, Hansen SPA | ✅ Fertig |

**Schlüssel-Entscheidungen:**
- Datenspeicherung: CSV je Ticker (`{TICKER}_daily.csv`) + kombinierte `all_daily.csv`
- Indikatoren als **Parquet gecacht** (`data/features/{TICKER}_features.parquet`) — `feature_store.py` als Zwischenschicht zwischen OHLCV und allen Analyse-Modulen
- **FEATURE_PIPELINE** in `feature_store.py` — geordnete Liste von Berechnungsfunktionen; jedes neue Modul registriert seine eigene Feature-Funktion dort (kein Modul muss ein anderes kennen)
- `TA_run.run()` überspringt `add_all_indicators()` wenn der df bereits Indikatoren enthält (`rsi`-Spalte als Prüfung) — rückwärtskompatibel
- Ticker-Verwaltung: `tickers.txt` (Kommentare mit `#`, Leerzeilen werden ignoriert)
- Unternehmensname: Spalte `Name` zwischen Ticker und Open (via `yfinance.info`)
- Daily OHLCV ab `2019-01-01` als Standard-Startdatum
- Python-Umgebung: `.venv/` (aktivieren mit `source .venv/bin/activate`)
- yfinance 1.x Fix: MultiIndex-Spalten werden in `_fetch_from_yfinance()` auf einfache Spaltennamen reduziert
- MA-Typ: **EMA** für alle Perioden (9, 21, 50, 200); SMA 20 nur intern als Bollinger-Basis
- Indikatoren selbst berechnet (numpy/pandas built-ins) — keine externe TA-Library
- RSI: Wilders Methode (com = period−1); RSI-50-Crossover als regime-unabhängiges Signal (Wong 2002)
- MACD: nur als Bestätigung/Trendfilter, nicht als alleiniger Trigger (Pramudya 2020)
- Stochastik: langsame Variante (%K geglättet); %D als Morris-Filter-Grundlage
- Donchian: shift(1) auf High/Low → kein Look-Ahead-Bias (Park & Irwin 2004)

**Indikator-Spalten Übersicht:**

| Modul | Spalten |
|-------|---------|
| `adx.py` | `adx`, `di_plus`, `di_minus`, `regime`, `psar`, `psar_bull` |
| `durchschnitte.py` | `ema_9/21/50/200`, `price_vs_ema50/200`, `ma_alignment`, `bb_mid/upper/lower/width/pct/squeeze`, `donchian_high/low/breakout` |
| `oszillatoren.py` | `rsi`, `rsi_zone`, `rsi_above50`, `macd`, `macd_signal`, `macd_hist`, `macd_hist_dir`, `stoch_k`, `stoch_d`, `stoch_zone` |
| `volumen.py` | `obv`, `obv_ema`, `obv_trend`, `vol_sma20`, `vol_ratio`, `vol_above_avg`, `vol_price_signal` |

---

## Aggregation

Wie die einzelnen Modul-Scores zu einem Gesamt-Score zusammengeführt werden (z.B. Summe, gewichteter Score, Meta-Modell) ist noch offen und wird im Verlauf des Projekts definiert.

---

## Projektphasen

| Phase | Beschreibung | Status |
|-------|--------------|--------|
| 1 | Konzeption & Dokumentation | 🔄 Laufend |
| 2 | Aufbau Modul für Modul (Code) | 🔄 Laufend |
| 3 | Integration & Aggregation | 🔲 Ausstehend |
| 4 | Backtesting & Validierung | 🔲 Ausstehend |
| 5 | Live-Betrieb US-Markt | 🔲 Ausstehend |
| 6 | Erweiterung Europa / Optionen | 🔲 Ausstehend |

---

## Wissensquellen & Inputs

| # | Quelle | Typ | Verwendet in |
|---|--------|-----|--------------|
| 1 | John J. Murphy – *Technische Analyse der Finanzmärkte* | Buch | Technische Analyse |
| 2 | Park & Irwin (2004) | Paper | Price Channel / Fortsetzungsformationen |
| 3 | Pramudya & Ichsani (2020) | Paper | Signal-Logik (MACD als Bestätigung, RSI+BB-Kombination) |
| 4 | Tsinaslanidis & Guijarro (2021) | Paper | ML-Modul: DTW Generic Pattern Recognition — 560 NYSE-Aktien, 91 % profitable Konfigurationen |
| 5 | Serafini (2019) | Master-Thesis | ML-Modul: FFNN + Volume-Profile — WWR 80,4 %, CRV 3:1 bestätigt |
| 6 | Lin, Liu, Yang et al. (2021) | Paper | ML-Modul: PRML Candlestick + Random Forest — 13 Shapes, 36,7 % p.a. TOP10 |
| 7 | Arévalo, García, Guijarro & Peris (2017) | Paper | TA-Modul/Backtesting: Flag-Pattern + EMA-Dual-Timeframe-Filter + Dynamic Walk-Forward SL/TP — DJIA 286 % Return, Profit/MDD 13,2, Reality Check bestanden |
