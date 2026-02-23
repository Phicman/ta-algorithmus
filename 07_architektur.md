# 07 – Algorithmus-Architektur

← [Zurück zum Index](../claude.md)

---

## Systemübersicht

```
                    [Ticker-Liste]
                          │
                   [Data Fetcher]
                  /               \
           [yfinance]        [Alpha Vantage]
          (OHLCV CSV)          (News CSV)
                  \               /
                   ───────────────
                          │
          ┌───────────────┼───────────────┐
          │               │               │
    [TA-Analyse]   [Market Regime]    [ML-Analyse]   [Sentiment-Analyse]
    Indikatoren    Volatilität &      XGBoost        FinBERT
    Muster         Return-Umfeld      Signale        News-Scoring
    Signal-Logik
          │               │               │               │
          └───────────────┴───────────────┴───────────────┘
                                  │
                          [Signal-Logik]
                          Filterung & CRV
                                  │
                        [Geldmanagement]
                        Positionsgröße & Stop
                                  │
                             [Output]
                     Ticker, Signal, Stärke, CRV
```

---

## Technologie-Stack

| Komponente         | Technologie                        |
|--------------------|------------------------------------|
| Sprache            | Python                             |
| Datenabruf Kurse   | yfinance                           |
| Datenabruf News    | Alpha Vantage REST API             |
| Datenspeicherung   | CSV (OHLCV) + Parquet (Features/Indikatoren, via pyarrow) |
| Indikator-Berechnung | pandas, pandas-ta / ta-lib       |
| Muster-Erkennung   | Eigene Python-Funktionen           |
| ML-Signalgenerierung | XGBoost                          |
| Generic Pattern Recognition | DTW / UCR Suite (tslearn / rucrdtw) |
| Sentiment-Analyse  | FinBERT (HuggingFace Transformer)  |
| Visualisierung     | matplotlib / plotly                |
| Output             | CSV / JSON / Dashboard             |

---

## Projektstruktur

```
ta-algorithmus/
├── main.py                      # Einstiegspunkt — analysiert alle Ticker
├── src/
│   ├── data/
│   │   ├── price_fetcher.py     # yfinance → OHLCV CSV
│   │   ├── news_fetcher.py      # Alpha Vantage → News CSV
│   │   └── feature_store.py     # Parquet-Cache; FEATURE_PIPELINE orchestriert alle Module
│   ├── ta/
│   │   ├── indikatoren/         # EMA, RSI, MACD, Bollinger, OBV, ADX...
│   │   ├── muster/              # Candlesticks, Formationen, Umkehr/Fortsetzung
│   │   └── TA_run.py            # TA-Scoring & Signal-Output
│   ├── ml/                      # XGBoost + DTW Generic Pattern Recognition
│   ├── sentiment/               # FinBERT Pipeline & Scoring
│   ├── market_regime/           # Regime-Erkennung (Trend/Range/Volatilität)
│   └── geldmanagement.py        # Positionsgröße, Stop-Platzierung
├── data/
│   ├── prices/                  # OHLCV CSVs je Ticker (gitignored)
│   ├── features/                # Parquet-Cache mit Indikatoren je Ticker (gitignored)
│   └── news/                    # News CSVs je Ticker & Datum (gitignored)
├── tests/
├── requirements.txt
└── .env                         # API-Keys (nicht im Repo)
```

---

## Datenquellen

| Quelle | Typ | Verwendung |
|--------|-----|------------|
| Yahoo Finance (yfinance) | Python-Bibliothek | OHLCV Tagesdaten, kostenlos |
| Alpha Vantage | REST API | News + Sentiment, kostenloser Tier |

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

## ML-Modul: Zwei Ansätze (geplant)

Das ML-Modul (`src/ml/`) kombiniert zwei komplementäre Methoden:

### 1. XGBoost — Signalgenerierung aus Features
- Technische Indikatoren als Input-Features (RSI, MACD, ADX, Bollinger, Volumen...)
- Vorhersage: BUY / SELL / NEUTRAL
- Trainiert auf historischen Daten mit Walk-Forward-Validierung

### 2. DTW Generic Pattern Recognition — Mustererkennung
> Quelle: Tsinaslanidis & Guijarro (2021) — getestet auf 560 NYSE-Aktien, Tagesdaten 2006–2015

**Grundprinzip:** Statt nur vordefinierte Chartmuster (Kopf-Schulter, Flaggen etc.) zu suchen, findet DTW **beliebige historische Preismuster**, die in der Vergangenheit profitabel waren — ohne vorher zu wissen wie das Muster aussieht.

**Wissenschaftlich belegte Parameterrichtlinien:**

| Parameter | Empfohlener Bereich | Begründung |
|-----------|--------------------|----|
| Musterlänge | **15–25 Handelstage** | Längere Muster = höhere Signifikanz (Pring 2002) |
| Anzahl Referenzmuster | **10–15** | Weniger = selektiver = besser |
| Take-Profit | **10–16%** | Stärkste positive Korrelation mit Performance (0.701) |
| Stop-Loss | **< Take-Profit** | SL nicht signifikant — TP/SL-Verhältnis entscheidend |
| Konsens-Schwelle | **Hoch** | Nur handeln wenn Mehrheit der Referenzen übereinstimmt |

**Verhältnis zu klassischen Mustern:**

| Ansatz | Modul | Beschreibung |
|--------|-------|-------------|
| Klassische Chartmuster | `src/ta/muster/` | Regelbasiert, vordefinierte Formen |
| DTW Generic Patterns | `src/ml/` | Datengetrieben, findet unbekannte Muster |

Beide Ansätze ergänzen sich: Klassische Muster liefern interpretierbare Signale, DTW erkennt Muster die der Mensch nicht sieht.

---

## Backtest-Framework (geplant)

- Walk-Forward Testing (In-Sample / Out-of-Sample)
- Gleiche Parameter für alle Märkte (gegen Over-Fitting)
- Bewertungsmetriken: Sharpe Ratio, Max Drawdown, Win Rate, Ø CRV
