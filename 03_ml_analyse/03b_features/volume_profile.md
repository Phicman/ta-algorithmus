# Volume-Profile Features

← [Zurück zur ML-Übersicht](../README.md)

---

> **Quelle:** Serafini, G. (2019). *Trade Chart Pattern Recognition: Statistical and Deep Learning Approaches by Means of Technical Indicators.* Master Thesis, Politecnico di Milano.

---

## Grundidee

Das Volume-Profile beschreibt die **Volumenverteilung entlang des Preisbereichs einer Kerze** — also: Bei welchem Preisniveau innerhalb der Kerze wurde wie viel gehandelt?

Diese Verteilung ist ein direktes Abbild von Angebots- und Nachfragezonen innerhalb eines Zeitraums. Sie liefert strukturelle Information, die in OHLCV-Aggregaten verloren geht.

---

## Volumen-Shape: b-shape vs. p-shape

Der wichtigste Feature aus dem Volume-Profile ist die **Form der Volumenverteilung**:

### b-shape (Volumen konzentriert im unteren Bereich)

```
Preis  │
 High  │    ░
       │   ░░
       │  ░░░
       │ ░░░░░░
  Low  │░░░░░░░░░░░░
       └──────────────→ Volumen
```

- Volumen häuft sich im **unteren Preisbereich**
- Interpretation: Der Markt hat zu tiefen Preisen stark gekauft → **Unterstützungszone** gebildet
- Signal: **Bullish** (Käufer kontrollieren die Zone)

### p-shape (Volumen konzentriert im oberen Bereich)

```
Preis  │
 High  │░░░░░░░░░░░░
       │░░░░░░░░
       │░░░░░
       │░░░
  Low  │░
       └──────────────→ Volumen
```

- Volumen häuft sich im **oberen Preisbereich**
- Interpretation: Der Markt hat zu hohen Preisen stark verkauft → **Widerstandszone** gebildet
- Signal: **Bearish** (Verkäufer kontrollieren die Zone)

### undefined (gleichmäßig / neutral)

- Keine klare Konzentration — keine strukturelle Information
- Feature-Wert: `shape = undefined`

---

## Feature-Übersicht (Serafini 2019)

| Feature | Typ | Berechnung | Interpretation |
|---------|-----|------------|----------------|
| **`shape`** | Kategorisch (b / p / undef.) | Volumen-Schwerpunkt: untere Hälfte → b, obere → p | Strukturelles Marktregime |
| **`delta`** | Kategorisch (bullish / bearish) | Close > Open → bullish; Close < Open → bearish | Kerzen-Richtung |
| **`new_min`** | Boolean (0/1) | Close < min(Close[-lookback:]) → 1 | Neues Tief im Betrachtungszeitraum |
| **`new_max`** | Boolean (0/1) | Close > max(Close[-lookback:]) → 1 | Neues Hoch im Betrachtungszeitraum |
| **`candlestick_tick`** | Numerisch [0,1] | (Close - Open) / (High - Low) | Verhältnis Körper zu Gesamtlänge |

---

## Berechnung: Volume-Profile Shape

### Konzept

Die Kerze wird vertikal in **n Bins** aufgeteilt (z.B. n=10). Für jeden Bin wird das anteilige Volumen berechnet. Der Schwerpunkt des Volumens bestimmt die Shape.

```
Schwerpunkt = Σ(Bin-Index × Volumen-Anteil) / Σ(Volumen-Anteil)

Schwerpunkt < 0.5 (untere Hälfte) → b-shape
Schwerpunkt > 0.5 (obere Hälfte) → p-shape
Schwerpunkt ≈ 0.5 (±Toleranz)   → undefined
```

**Voraussetzung:** Tick-Daten oder intra-Kerzen Volumendaten nötig.
Für Tageskerzen-Näherung: VWAP-Position relativ zu (High+Low)/2 als Proxy.

### Näherung mit Tageskerzen (OHLCV)

Ohne Tick-Daten kann der VWAP als Proxy verwendet werden:

```python
# VWAP-Proxy für Tageskerzen
typical_price = (High + Low + Close) / 3
vwap = typical_price  # Approximation

midpoint = (High + Low) / 2

if vwap < midpoint:
    shape = "b"      # Volumen-Schwerpunkt unten → Unterstützung
elif vwap > midpoint:
    shape = "p"      # Volumen-Schwerpunkt oben → Widerstand
else:
    shape = "undefined"
```

**Hinweis:** Dies ist eine Näherung. Echtes Volume-Profile benötigt Intraday-Daten.

---

## Feature `candlestick_tick`

Misst die **relative Körperstärke** einer Kerze:

```
candlestick_tick = (Close - Open) / (High - Low)

Wertebereich: -1 (voller Bearish-Body) bis +1 (voller Bullish-Body)
≈ 0 → Doji / Spinning Top (kein klarer Richtungsentscheid)
```

---

## Features `new_min` / `new_max`

Messen, ob die Kerze ein neues Extremum setzt:

```python
lookback = n  # optimierbarer Parameter

new_min = 1 if Close < min(Close[-lookback:-1]) else 0
new_max = 1 if Close > max(Close[-lookback:-1]) else 0
```

Kombination:
- `new_max=1` + `shape=b` → Starkes Bullish-Signal (Ausbruch mit Käufer-Dominanz)
- `new_min=1` + `shape=p` → Starkes Bearish-Signal (Ausbruch mit Verkäufer-Dominanz)

---

## Kombinations-Logik der Features

| shape | delta | new_max | new_min | Interpretation |
|-------|-------|---------|---------|----------------|
| b | bullish | 1 | 0 | Starkes Bullish-Signal |
| p | bearish | 0 | 1 | Starkes Bearish-Signal |
| b | bearish | 0 | 0 | Widerspruch → schwaches Signal |
| p | bullish | 0 | 0 | Widerspruch → schwaches Signal |
| undefined | — | — | — | Kein struktureller Bias |

---

## Einordnung im Feature Store

```
OHLCV-Rohdaten
         │
         ▼
Volume-Profile Feature-Extraktion
  ├── shape      (b / p / undefined)
  ├── delta      (bullish / bearish)
  ├── new_min    (0 / 1)
  ├── new_max    (0 / 1)
  └── candlestick_tick  (float)
         │
         ▼
Feature Store (Parquet) → Input für FFNN-Klassifikation
```

---

## Implementierungshinweise

- **Tageskerzen:** VWAP-Näherung für Shape (kein Tick-Daten nötig)
- **Stündliche Kerzen:** Näherung besser; echte VP nur mit Tick-Feed
- **Lookback für new_min/new_max:** Optimierbarer Parameter (z.B. 20 Tage = 1 Monat)
- **One-Hot-Encoding:** Kategorische Features (shape, delta) vor FFNN-Input kodieren

---

## Offene Fragen für Implementierung

- [ ] Tageskerzen oder stündliche Kerzen für das ML-Modul?
- [ ] Lookback-Fenster für `new_min`/`new_max`: 20 Tage oder optimieren?
- [ ] Echter Volume-Profile über intra-Tages-Daten oder VWAP-Näherung?
- [ ] Feature-Caching: Volume-Profile-Features im Feature Store (Parquet) vorspeichern?
