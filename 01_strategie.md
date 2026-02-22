# 01 – Strategie & Ziel

← [Zurück zum Index](../claude.md)

---

## Ziel

Aufbau eines modularen Algorithmus zur automatisierten Analyse von Aktiendaten. Jedes Modul liefert einen numerischen Score. Überschreitet der aggregierte Gesamt-Score einen definierten Schwellenwert, wird ein **Kaufsignal** ausgegeben.

**Output:** Signal-Liste mit Ticker, Name, Modul-Scores, Gesamt-Score und Kaufsignal.

---

## Scope

| Parameter | Beschreibung |
|-----------|--------------|
| **Signaltyp** | Kaufsignale (Verkauf/Short folgt später) |
| **Instrumente** | Aktien (Optionen/Zertifikate folgen später) |
| **Märkte** | US-Aktien (europäische Märkte folgen später) |
| **Timeframe** | Swing bis positionsorientiert (Tage bis Monate) |
| **Standard-Kerze** | 1 Tag (Daily) |
| **Kontext-Timeframes** | Weekly / Monthly (Langfrist-Kontext) |

---

## Modularer Aufbau

Jedes Modul analysiert die Aktiendaten aus einer eigenen Perspektive und gibt einen Score zurück. Die Scores werden aggregiert — die Aggregationsmethode wird im Projektverlauf definiert.

| Modul | Beschreibung |
|-------|--------------|
| Technische Analyse | Chartmuster, Trends, Indikatoren |
| ML-Analyse | Datengetriebene Mustererkennung |
| Sentiment-Analyse | Marktstimmung, News, Social Signals |
| Market Regime | Marktumfeld (Trend, Seitwärts, Krise) |
| Weitere | Offen für Erweiterung |

---

## Kaufsignal-Logik

```
Modul 1 Score + Modul 2 Score + ... + Modul N Score
                        │
               Aggregation (TBD)
                        │
           Gesamt-Score > Schwellenwert?
                 │               │
                JA              NEIN
                 │
          KAUFSIGNAL
```

Schwellenwert und Gewichtung der Module werden nach Abschluss der Konzeptionsphase und ersten Backtests definiert.

---

## Ticker-Universum

> Noch nicht final definiert. Kandidaten:

- S&P 500 Komponenten (500 Titel)
- Nasdaq 100
- DAX 40
- Eigene Watchlist

---

## Trendbestimmung

- **Aufwärtstrend:** Höhere Hochs UND höhere Tiefs
- **Abwärtstrend:** Niedrigere Hochs UND niedrigere Tiefs
- **Seitwärtstrend:** Gleiche Hochs und Tiefs (~1/3 der Zeit) → Trendfolgeindikatoren funktionieren hier schlecht
- **Trendwechsel** erst bei Bruch des Musters (z.B. Unterschreiten des letzten Tiefs im Aufwärtstrend)

### Drei Trendklassen

| Klasse | Dauer | Fokus |
|--------|-------|-------|
| Primär | > 1 Jahr | Kontext |
| Sekundär / mittelfristig | Wochen bis Monate | ✅ Primärer Fokus dieses Algorithmus |
| Kurzfristig | < 2–3 Wochen | Kontext |

---

## Analysemethodik: Top-Down

1. **Monatschart** (Langfrist): primäre Trendlinien, Support/Resistance, wichtige Chartformationen
2. **Wochenchart:** mittelfristige Strukturen, gleiche Analyse wiederholen
3. **Tageschart:** Feintuning, kurzfristige Strukturen, Entry-Vorbereitung

---

## Datenquellen & APIs

| Quelle | Typ | Notizen |
|--------|-----|---------|
| Yahoo Finance (yfinance) | Python-Bibliothek | Kostenlos, geeignet für Prototyp |
| Alpha Vantage | REST API | Kostenlose Tier verfügbar, Ratenlimit beachten |
| Polygon.io | REST API | Umfangreicher, kostenpflichtig |

**Benötigt:** Open, High, Low, Close, Volume; mind. 2 Jahre Historie
