# FFNN Volume-Profile Klassifikation

← [Zurück zur ML-Übersicht](../README.md)

---

> **Quelle:** Serafini, G. (2019). *Trade Chart Pattern Recognition: Statistical and Deep Learning Approaches by Means of Technical Indicators.* Master Thesis, Politecnico di Milano.
> **Datensatz:** E-mini S&P 500 Futures (ES), 2016–2017, 1-Stunden-Kerzen

---

## Grundidee

Statt rohe Preissequenzen zu vergleichen (wie DTW), werden aus jeder Kerze **strukturelle Volume-Profile-Features** extrahiert — und ein Feed-Forward Neural Network (FFNN) klassifiziert daraus direkt BUY / SELL.

Das Modell lernt, welche Volumen-Verteilungsmuster (b-shape, p-shape) statistisch auf Trendfortsetzung oder -umkehr hindeuten.

**Kernaussage:** Die Form der Volumenverteilung innerhalb einer Kerze enthält mehr Informationsgehalt für die Trendrichtung als der Kursverlauf allein.

---

## Methode: Feature-basierte Klassifikation

Im Gegensatz zu DTW (ähnlichkeitsbasiert, keine vordefinierten Features) werden hier diskrete, interpretierbare Features je Kerze berechnet:

| Feature | Typ | Bedeutung |
|---------|-----|-----------|
| `new_min` | Boolean | Neues Tief im Datensatz? → Bearish-Indiz |
| `new_max` | Boolean | Neues Hoch im Datensatz? → Bullish-Indiz |
| `delta` | Kategorisch | Kerze bullish (Close > Open) oder bearish |
| `shape` | Kategorisch | Volumenverteilung: b-shape / p-shape / undefined |
| `candlestick_tick` | Numerisch | Verhältnis Körper zu Gesamtlänge der Kerze |

→ Details zum Volume-Profile-Feature: [03b_features/volume_profile.md](../03b_features/volume_profile.md)

---

## Algorithmus (5 Schritte)

```
OHLCV-Daten (Futures, stündlich)
         │
         ▼
[Step 1]  Walk-Forward Split (chronologisch, 4 Blöcke à 70/30)
         │
         ▼
[Step 2]  Feature-Extraktion je Kerze:
          new_min, new_max, delta, shape, candlestick_tick
         │
         ▼
[Step 3]  Labelling: BUY / SELL
          Einstieg: 1 Tick über/unter Eröffnung nächste Kerze
          CRV 3:1  (TP = 3× SL)
          Trailing Stop
         │
         ▼
[Step 4]  FFNN-Training auf Trainingsblock
          Input: Feature-Vektor je Kerze
          Output: BUY / SELL
         │
         ▼
[Step 5]  Testblock: Vorhersage → Handelssignal
```

---

### Schritt 1: Walk-Forward Split

- **4 Blöcke**, jeweils 70 % Training / 30 % Test
- Chronologisch — kein Random-Split (Zeitreihen-Integrität)
- Testblöcke überlappen nicht; Trainingsblöcke erweitern sich mit jedem Block

```
Block 1: [████████████░░░░░░░░]
Block 2: [█████████████████░░░]
Block 3: [█████████████████████░░░]
Block 4: [███████████████████████████░░░]
          ← Training →    ← Test →
```

---

### Schritt 2: Feature-Extraktion

Aus jeder OHLCV-Kerze werden die 5 Volume-Profile-Features berechnet (siehe [volume_profile.md](../03b_features/volume_profile.md)).

---

### Schritt 3: Labelling (CRV 3:1)

```
Entry: 1 Tick über dem Open der nächsten Kerze (BUY)
       1 Tick unter dem Open der nächsten Kerze (SELL)

Trailing Stop: folgt dem Kurs mit festem Abstand

TP = 3 × SL   →   CRV 3:1
```

**Wichtig:** Dieses CRV-Schema ist identisch mit dem TA-Modul unseres Projekts (CRV ≥ 3:1 als Pflicht-Constraint). Das bestätigt die Konsistenz unserer Labelling-Strategie.

---

### Schritt 4: FFNN-Architektur

```
Input Layer:  5 Features (one-hot-encoded kategorische Features)
Hidden Layer: [empirisch optimiert — Paper gibt keine genaue Anzahl an]
Output Layer: 2 Neuronen → BUY / SELL (Softmax)
Optimizer:    Adam
Loss:         Cross-Entropy
```

**Warum FFNN, nicht LSTM/CNN?**

Volume-Profile-Features sind **nicht sequenziell** — jede Kerze ist ein eigenständiger Datenpunkt ohne zeitliches Gedächtnis. LSTM und CNN benötigen Sequenzstruktur für ihren Vorteil; hier bringt ein einfaches MLP bessere Ergebnisse.

---

## Ergebnisse (E-mini S&P 500 Futures, 2016–2017)

### Modellvergleich

| Modell | WWR | PPC ($/Contract) | Ø MDD ($) |
|--------|-----|-----------------|-----------|
| Baseline (Random) | 50 % | — | — |
| White-Box Min-Max | ~52 % | — | — |
| White-Box Volume-Profile | ~60 % | — | — |
| **FFNN (best)** | **80,4 %** | **78,41** | **128,53** |
| RNN | ~70 % | — | — |
| CNN | ~65 % | — | — |

**FFNN dominiert deutlich** — Volume-Profile-Features sind gut für MLP geeignet.

### Metriken-Erklärung

| Metrik | Definition |
|--------|------------|
| **WWR** | Weighted Win Ratio — gewichtetes Verhältnis Gewinne/Verluste (berücksichtigt Höhe der Gewinne) |
| **PPC** | Profit Per Contract — Durchschnittsgewinn pro Trade in Dollar |
| **MDD** | Maximum Drawdown — maximaler kumulierter Verlust im Testzeitraum |

→ Vollständige Metrik-Definitionen: [03d_backtesting.md](../03d_backtesting.md)

---

## Ableitung für unser Projekt

### Einordnung im Algorithmus

```
Feature Store (OHLCV)
         │
         ▼
Volume-Profile Feature-Extraktion
(new_min, new_max, delta, shape, candlestick_tick)
         │
         ▼
FFNN-Klassifikation: BUY / SELL
         │
         ▼
ML-Score → numerischer Wert für Gesamt-Aggregation
```

### Abgrenzung zum DTW-Modul

| Aspekt | DTW (Tsinaslanidis 2021) | FFNN (Serafini 2019) |
|--------|--------------------------|---------------------|
| Signal-Grundlage | Historische Ähnlichkeit (Shape der Preissequenz) | Strukturelle Features je Kerze |
| Musterdefinition | Generisch / emergent | Volume-Profile (vordefiniert) |
| Zeitfenster | Sequenz (Q.length Tage) | Einzelne Kerze + Kontext |
| Lernfähigkeit | Implizit (Trainingshistorie) | Explizit (NN-Gewichte) |
| Feature-Aufwand | Nur Schlusskurse | OHLCV + Volume-Profil-Berechnung |

→ Keine Überlappung: DTW und FFNN verwenden unterschiedliche Feature-Typen und Signal-Logiken. Kombination beider Scores reduziert Fehlsignale überproportional.

### Empfohlene Implementierungsparameter

| Parameter | Empfehlung | Begründung |
|-----------|-----------|------------|
| Walk-Forward-Blöcke | **4** | Serafini-Design; genug Trainingsdaten pro Block |
| Train/Test-Split | **70/30** | Chronologisch pro Block |
| FFNN-Architektur | **2–3 Hidden Layer, 64–128 Neuronen** | Standard-Ausgangspunkt; per Grid Search optimieren |
| Labelling-CRV | **3:1** | Identisch mit TA-Modul — Konsistenz |
| Input-Features | **5 Volume-Profile-Features** | Serafini-Paper |

---

## Wichtige Designentscheidungen

1. **FFNN vor LSTM/CNN bevorzugen:** Volume-Profile-Features sind nicht sequenziell — FFNN reicht und übertrifft komplexere Modelle
2. **Labelling: CRV 3:1 mit Trailing Stop** — kompatibel mit TA-Modul-Logik
3. **Walk-Forward CV zwingend:** Keine zufällige Aufteilung bei Zeitreihen
4. **Klassifikation vor Regression:** Serafini zeigt explizit: Preisvorhersage (Regression) ist schwächer als Trendklassifikation

---

## Offene Fragen für Implementierung

- [ ] Volume-Profile-Berechnung: Eigene Implementierung oder Library (z.B. `market-profile`)?
- [ ] Timeframe: Stündliche Kerzen (wie Paper) oder Tageskerzen (wie unser TA-Modul)?
- [ ] Feature-Normalisierung: Numerische Features (candlestick_tick) z-normalisieren?
- [ ] FFNN-Hyperparameter: Grid Search oder Bayesian Optimization?
- [ ] Kombinations-Score: Wie DTW-Score und FFNN-Score zu einem Gesamt-ML-Score aggregieren?
