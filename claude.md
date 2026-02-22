# Handelsalgorithmus – Projekt-Dokumentation

> Zentrale Dokumentation zum Aufbau eines modularen, signalbasierten Handelsalgorithmus.
> Projektphase: Konzeption
> Letzte Aktualisierung: 2026-02-21

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
| ML-Analyse | [03_ml_analyse/README.md](./03_ml_analyse/README.md) | 🔲 Konzept |
| Sentiment-Analyse | [04_sentiment_analyse/README.md](./04_sentiment_analyse/README.md) | 🔲 Konzept |
| Market Regime | [05_market_regime/README.md](./05_market_regime/README.md) | 🔲 Konzept |
| Geldmanagement | [06_geldmanagement.md](./06_geldmanagement.md) | 🔲 Konzept |
| Architektur | [07_architektur.md](./07_architektur.md) | 🔲 Konzept |
| TODO / Backlog | [08_todo.md](./08_todo.md) | ✅ Aktiv |

---

## Aggregation

Wie die einzelnen Modul-Scores zu einem Gesamt-Score zusammengeführt werden (z.B. Summe, gewichteter Score, Meta-Modell) ist noch offen und wird im Verlauf des Projekts definiert.

---

## Projektphasen

| Phase | Beschreibung | Status |
|-------|--------------|--------|
| 1 | Konzeption & Dokumentation | 🔄 Laufend |
| 2 | Aufbau Modul für Modul (Code) | 🔲 Ausstehend |
| 3 | Integration & Aggregation | 🔲 Ausstehend |
| 4 | Backtesting & Validierung | 🔲 Ausstehend |
| 5 | Live-Betrieb US-Markt | 🔲 Ausstehend |
| 6 | Erweiterung Europa / Optionen | 🔲 Ausstehend |

---

## Wissensquellen & Inputs

| # | Quelle | Typ | Verwendet in |
|---|--------|-----|--------------|
| 1 | John J. Murphy – *Technische Analyse der Finanzmärkte* | Buch | Technische Analyse |
