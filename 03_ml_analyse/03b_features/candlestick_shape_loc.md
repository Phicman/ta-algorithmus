# Candlestick Shape & Loc – Formale Feature-Definition

← [Zurück zur ML-Übersicht](../README.md)

---

> **Quelle:** Lin, Y., Liu, S., Yang, H., Wu, H., Jiang, B. (2021). *Improving stock trading decisions based on pattern recognition using machine learning technology.* PLoS ONE 16(8): e0255558.
> **Verwendung in:** [03a_modelle/prml_candlestick_rf.md](../03a_modelle/prml_candlestick_rf.md)

---

## Grunddefinitionen

Eine Kerze (K-Line) besteht aus vier Preisen:

```
k = (o_t, h_t, l_t, c_t)

o_t = Open   (Eröffnungskurs)
h_t = High   (Tageshoch)
l_t = Low    (Tagestief)
c_t = Close  (Schlusskurs)
```

Daraus entstehen zwei diskrete Features:
- **Shape:** Absolutform der Kerze (13 Typen) — basiert auf o, h, l, c
- **Loc:** Relative Position zur Vorkerze (8 Typen) — basiert auf Vergleich mit h_{t-1}, l_{t-1}, c_{t-1}

---

## Feature 1: Shape — 13 Candlestick-Formen

### Visuelles Schema

```
        High ────────── h_t
          │
Upper     │  (Oberer Schatten)
Shadow    │
          │
  Open ── ┤ ←── o_t (bearish) oder c_t (bullish)
          │
Real      │  (Kerzenkörper = |c_t - o_t|)
Body      │
          │
  Close ──┤ ←── c_t (bearish) oder o_t (bullish)
          │
Lower     │  (Unterer Schatten)
Shadow    │
          │
         Low ────────── l_t
```

### Klassifikationsregeln (13 Formen)

Das Paper klassifiziert nach OHLC-Verhältnissen. Die 13 Formen entstehen aus der Kombination von:
- Körperposition (Close > Open = bullish / Close < Open = bearish / Close = Open = Doji)
- Schattenlängen (kein Schatten / kurzer Schatten / langer Schatten)
- Körperlänge (kurz / mittel / lang)

| Shape-ID | Form | c vs o | Oberer Schatten | Unterer Schatten | Beschreibung |
|----------|------|--------|-----------------|------------------|-------------|
| 1 | Daily Limit (Bullish) | c >> o | Keiner | Keiner | Voller Bullish-Body, keine Schatten (chinesisches Limit-Up) |
| 2 | Langer Bullish-Body | c > o | Kurz | Kurz | Starker Aufwärtstag |
| 3 | Mittlerer Bullish-Body | c > o | Mittel | Mittel | Normaler Aufwärtstag |
| 4 | Kurzer Bullish-Body | c > o | Lang | Lang | Schwacher Aufwärtstag mit langen Schatten |
| 5 | Doji (Long) | c ≈ o | Lang | Lang | Entscheidungslosigkeit, hohe Volatilität |
| 6 | Doji (Short) | c ≈ o | Kurz | Kurz | Entscheidungslosigkeit, enge Range |
| 7 | Doji (Gravestone) | c ≈ o | Lang | Keiner | Bearish-Warnung (schloss am Tief) |
| 8 | Doji (Dragonfly) | c ≈ o | Keiner | Lang | Bullish-Warnung (schloss am Hoch) |
| 9 | Kurzer Bearish-Body | c < o | Lang | Lang | Schwacher Abwärtstag |
| 10 | Mittlerer Bearish-Body | c < o | Mittel | Mittel | Normaler Abwärtstag |
| 11 | Langer Bearish-Body | c < o | Kurz | Kurz | Starker Abwärtstag |
| 12 | Daily Limit (Bearish) | c << o | Keiner | Keiner | Voller Bearish-Body, keine Schatten (chinesisches Limit-Down) |
| 13 | Spinning Top | c ≈ o | Mittel | Mittel | Kleiner Körper, ausgeglichene Schatten |

**Hinweis:** Die genauen Schwellenwerte für "kurz/mittel/lang" werden relativ zur Average True Range (ATR) oder zum historischen Durchschnitt bestimmt.

### Implementierungsansatz (Python)

```python
def classify_shape(o, h, l, c, atr):
    body    = abs(c - o)
    upper   = h - max(o, c)
    lower   = min(o, c) - l
    range_  = h - l

    body_rel  = body / atr    # Körper relativ zur ATR
    upper_rel = upper / atr
    lower_rel = lower / atr

    bullish = c > o
    bearish = c < o
    doji    = body < 0.1 * atr  # Doji wenn Körper < 10% ATR

    if doji:
        if upper_rel > 1.5 and lower_rel < 0.1:
            return 7   # Gravestone Doji
        elif lower_rel > 1.5 and upper_rel < 0.1:
            return 8   # Dragonfly Doji
        elif upper_rel > 1.0 and lower_rel > 1.0:
            return 5   # Long Doji
        else:
            return 6   # Short Doji / Spinning Top ähnlich
    elif bullish:
        if body_rel > 2.0 and upper_rel < 0.1 and lower_rel < 0.1:
            return 1   # Daily Limit Bullish
        elif body_rel > 1.5:
            return 2   # Langer Bullish
        elif body_rel > 0.7:
            return 3   # Mittlerer Bullish
        else:
            return 4   # Kurzer Bullish
    else:  # bearish
        if body_rel > 2.0 and upper_rel < 0.1 and lower_rel < 0.1:
            return 12  # Daily Limit Bearish
        elif body_rel > 1.5:
            return 11  # Langer Bearish
        elif body_rel > 0.7:
            return 10  # Mittlerer Bearish
        else:
            return 9   # Kurzer Bearish
```

---

## Feature 2: Loc — 8 Relative Positionstypen

### Mathematische Definition

```
loc_i = f(h_t, h_{t-1}, l_t, l_{t-1}, c_t, c_{t-1})
```

| Loc-Symbol | Bedingungen | Visualisierung | Interpretation |
|------------|-------------|----------------|----------------|
| **BC_h** | h_t > h_{t-1} AND l_t < l_{t-1} AND c_t > c_{t-1} | Outside Bar, bullish Close | Markt testet beide Seiten, Käufer gewinnen |
| **BC_l** | h_t > h_{t-1} AND l_t < l_{t-1} AND c_t < c_{t-1} | Outside Bar, bearish Close | Markt testet beide Seiten, Verkäufer gewinnen |
| **BH_h** | h_t > h_{t-1} AND l_t > l_{t-1} AND c_t > c_{t-1} | Higher High + Higher Low, bullish | Klarer Aufwärtstrend bestätigt |
| **BH_l** | h_t > h_{t-1} AND l_t > l_{t-1} AND c_t < c_{t-1} | Higher High + Higher Low, bearish | Trend-Stärke nachlassend (bullish Gap aber bearish Close) |
| **BL_h** | h_t < h_{t-1} AND l_t < l_{t-1} AND c_t > c_{t-1} | Lower High + Lower Low, bullish | Abwärtstrend mit Erholung am Tagesende |
| **BL_l** | h_t < h_{t-1} AND l_t < l_{t-1} AND c_t < c_{t-1} | Lower High + Lower Low, bearish | Klarer Abwärtstrend bestätigt |
| **BM_h** | h_t < h_{t-1} AND l_t > l_{t-1} AND c_t > c_{t-1} | Inside Bar, bullish Close | Konsolidierung mit bullischem Bias |
| **BM_l** | h_t < h_{t-1} AND l_t > l_{t-1} AND c_t < c_{t-1} | Inside Bar, bearish Close | Konsolidierung mit bearischem Bias |

### Visualisierung der 8 Loc-Typen

```
BC_h (Outside Bull)    BC_l (Outside Bear)    BH_h (Higher Bull)
  h ─────────────        h ─────────────        h ─────────────
  │   ↑ höher            │   ↑ höher            h₋₁─────────
  │                      │                      │
  │         [====]   Vortag    [====]            │         [====]
  │                      │                      │
  │  [=====]             │  [=====]         l₋₁─────────
  l ─────────────        l ─────────────        l ─────────────
    ↓ tiefer               ↓ tiefer               ↑ höher

BH_l (Higher Bear)     BL_h (Lower Bull)      BL_l (Lower Bear)
  h ─────────────        h₋₁─────────          h₋₁─────────
  h₋₁─────────           h ─────────────        h ─────────────
  │         [====]        │  [====]              │
  l₋₁─────────            l ─────────────        │         [====]
  l ─────────────         l₋₁─────────           l ─────────────
                                                  l₋₁─────────

BM_h (Inside Bull)     BM_l (Inside Bear)
  h₋₁─────────          h₋₁─────────
  h ─────────────        h ─────────────
  │   [====]             │
  l ─────────────        │         [====]
  l₋₁─────────           l ─────────────
                          l₋₁─────────
```

### Implementierungsansatz (Python)

```python
def classify_loc(h, l, c, h_prev, l_prev, c_prev):
    high_up   = h > h_prev
    low_up    = l > l_prev
    close_up  = c > c_prev

    if high_up and not low_up:
        return "BC_h" if close_up else "BC_l"    # Outside Bar
    elif high_up and low_up:
        return "BH_h" if close_up else "BH_l"   # Higher High + Higher Low
    elif not high_up and not low_up:
        return "BL_h" if close_up else "BL_l"   # Lower High + Lower Low
    else:  # not high_up and low_up
        return "BM_h" if close_up else "BM_l"   # Inside Bar
```

---

## Kombination Shape + Loc = Pattern-Feature

Für ein 2-Tages-Muster:

```
Pattern p_2 = (Shape_{t-1}, Shape_t, Loc_{t-1}, Loc_t, TA_{t-1}..., TA_t...)

Mögliche Kombinationen:
  Shape: 13 × 13 = 169
  Loc:   8 × 8 = 64 (aber durch Shape-Kombination implizit eingeschränkt)
```

Der Feature-Vektor für ein 2-Tages-Muster hat **22 Spalten** (11 je Kerze):

```
[Shape_1, Loc_1, MA5_1, EMA10_1, ROC1_1, CCI10_1, MOM10_1, AD_1, OBV_1, TR_1, ATR10_1,
 Shape_2, Loc_2, MA5_2, EMA10_2, ROC1_2, CCI10_2, MOM10_2, AD_2, OBV_2, TR_2, ATR10_2]
```

---

## Encoding für ML-Modelle

Kategorische Features müssen für Modelle kodiert werden:

| Feature | Kodierung |
|---------|-----------|
| Shape (1–13) | Integer (direkt nutzbar für RF/KNN) oder One-Hot (für LR/NN) |
| Loc (BC_h, ..., BM_l) | Integer (0–7) oder One-Hot (8 Spalten) |
| Numerische Features | Standardisierung empfohlen (Z-Normalisierung) |

**Für Random Forest:** Integer-Encoding ausreichend (RF ist skalierungsinvariant).

---

## Einordnung im Feature Store

```
OHLCV-Rohdaten
         │
         ├── Shape-Klassifikation (13 Formen)    ← je Kerze
         ├── Loc-Klassifikation (8 Typen)         ← je Kerze (relativ zur Vorkerze)
         ├── MA5, EMA10                            ← je Kerze
         ├── ROC(1), CCI10, MOM10                 ← je Kerze
         ├── AD, OBV, TR, ATR10                   ← je Kerze
         │
         ▼
Feature Store (Parquet) → 11 Features je Kerze
```

---

## Offene Fragen

- [ ] ATR-Schwellenwerte für Shape-Klassifikation: Welche Grenzen für "kurz/mittel/lang"?
- [ ] Tageskerzen (unser Standard) oder stündliche Kerzen? (Shape-Klassifikation timeframe-agnostisch)
- [ ] Loc für ersten Tag in Datensatz: Keine Vorkerze vorhanden → NaN oder eigene Klasse?
- [ ] Daily-Limit Shape (1 und 12): Im US-Markt gibt es keine harten Limit-Up/Down → Shape 1 und 12 ggf. weglassen oder als "sehr starke Bewegung" umdefinieren
