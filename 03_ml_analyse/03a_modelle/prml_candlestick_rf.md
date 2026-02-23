# PRML – Pattern Recognition mit Machine Learning (Candlestick + Random Forest)

← [Zurück zur ML-Übersicht](../README.md)

---

> **Quelle:** Lin, Y., Liu, S., Yang, H., Wu, H., Jiang, B. (2021). *Improving stock trading decisions based on pattern recognition using machine learning technology.* PLoS ONE 16(8): e0255558.
> **DOI:** 10.1371/journal.pone.0255558
> **Datensatz:** Alle chinesischen Aktien (CCER), tägl. OHLCV, Jan 2000 – Okt 2020
> **Training:** Jan 2000 – Dez 2014 | **Test/Prediction:** Jan 2015 – Okt 2020

---

## Grundidee

PRML (**P**attern **R**ecognition + **M**achine **L**earning) kombiniert zwei Schichten:

1. **Musterschicht:** Jede Kerze wird formal in Shape + Loc klassifiziert. N-Tages-Muster entstehen durch Kombination aufeinanderfolgender Kerzen.
2. **ML-Schicht:** Für jedes der 169 (2-Tage) bzw. 2.197 (3-Tage) Muster wird ein separates ML-Modell trainiert. Nur Muster mit Accuracy > 55 % werden im Portfolio gehalten.

**Kernunterschied zu reinem ML:** Kein einziges Modell klassifiziert alle Muster — stattdessen wird das beste Modell per Muster selektiert. Das reduziert Overfitting strukturell.

**Kernunterschied zu DTW:** Kein Ähnlichkeitsvergleich — stattdessen formale Klassifikation von Shape/Loc + diskrete TA-Features.

---

## Mathematische Grundlagen

### Definition 1: Candlestick (K-Line)

```
k = (o_t, h_t, l_t, c_t)

o_t  = Eröffnungskurs zum Zeitpunkt t
h_t  = Tageshoch
l_t  = Tagestief
c_t  = Schlusskurs
```

### Definition 2: Candlestick Time Series

```
T_n = {k_1, k_2, ..., k_n}     (Sequenz von n Kerzen eines Stocks)

T_in = {k_i1, k_i2, ..., k_in} (i-ter Stock, n Kerzen)
```

### Definition 3: Candlestick Relative Position (Loc)

Die relative Position beschreibt, wie die aktuelle Kerze im Vergleich zur Vorkerze steht:

```
loc_i = f(h_t, h_{t-1}, l_t, l_{t-1}, c_t, c_{t-1})
```

| Loc-Symbol | Bedingung | Bedeutung |
|------------|-----------|-----------|
| BC_h | h_t > h_{t-1}, l_t < l_{t-1}, c_t > c_{t-1} | Outside Bar, bullish Close |
| BC_l | h_t > h_{t-1}, l_t < l_{t-1}, c_t < c_{t-1} | Outside Bar, bearish Close |
| BH_h | h_t > h_{t-1}, l_t > l_{t-1}, c_t > c_{t-1} | Higher High + Higher Low, bullish |
| BH_l | h_t > h_{t-1}, l_t > l_{t-1}, c_t < c_{t-1} | Higher High + Higher Low, bearish |
| BL_h | h_t < h_{t-1}, l_t < l_{t-1}, c_t > c_{t-1} | Lower High + Lower Low, bullish |
| BL_l | h_t < h_{t-1}, l_t < l_{t-1}, c_t < c_{t-1} | Lower High + Lower Low, bearish |
| BM_h | h_t < h_{t-1}, l_t > l_{t-1}, c_t > c_{t-1} | Inside Bar, bullish Close |
| BM_l | h_t < h_{t-1}, l_t > l_{t-1}, c_t < c_{t-1} | Inside Bar, bearish Close |

→ 8 mögliche Loc-Werte. Details zu Shape: [03b_features/candlestick_shape_loc.md](../03b_features/candlestick_shape_loc.md)

### Definition 4: Loc Series

```
LOC_n = {loc_1, loc_2, ..., loc_n}     (Sequenz von n relativen Positionen)
```

### Definition 5: Candlestick Pattern

```
p_j = (T_j, LOC_j)

Beispiel 2-Tages-Muster:
p_2 = (T_2, LOC_2)   mit   T_2 = {k_1, k_2},   LOC_2 = {loc_1, loc_2}
```

---

## Technische Indikatoren als Features

Für jede Kerze werden 9 technische Indikatoren berechnet:

### Moving Average (MA)

```
MA(t) = (1/m) * Σ_{i=0}^{m-1} c_{t-i}

m = Periodenlänge (Paper: 5 Tage)
c = Schlusskurs
```

### Exponential Moving Average (EMA)

```
EMA(t) = (2/(n+1)) * c_t + ((n-1)/(n+1)) * EMA(t-1)

n = Periodenlänge (Paper: 10 Tage)
```

### Volume Rate of Change (ROC)

```
ROC(t) = v_t / ((1/x) * Σ_{i=0}^{x} v_{t-i})

v_t = Volumen zum Zeitpunkt t
x   = Periodenlänge (Paper: 1 Tag)
```

### Commodity Channel Index (CCI)

```
CCI(t) = ((h_t + l_t + c_t)/3 - MA(n)) / (0.015 * (1/n) * Σ_{i=t-n}^{t} |MA(i) - c_i|)

n = Periodenlänge (Paper: 10 Tage)
```

CCI misst die Abweichung des Preises vom gleitenden Durchschnitt. Werte > +100 = überkauft; < -100 = überverkauft.

### Momentum (MOM)

```
MOM(t) = c_t - c_{t-n}

n = Periodenlänge (Paper: 10 Tage)
```

Misst die Preisbeschleunigung / -verlangsamung.

### Chaikin Accumulation/Distribution Line (AD)

```
CLV(t) = (2*c_t - h_t - l_t) / (h_t - l_t)     ← Close Location Value

AD(t) = AD(t-1) + v_t * CLV(t)
```

CLV ∈ [-1, +1]:
- CLV = +1 → Close am High (voller Kauf-Druck)
- CLV = -1 → Close am Low (voller Verkaufs-Druck)
- CLV = 0 → Close in Mitte (neutraler Druck)

### On Balance Volume (OBV)

```
wenn c_t > c_{t-1}: OBV(t) = OBV(t-1) + v_t
wenn c_t < c_{t-1}: OBV(t) = OBV(t-1) - v_t
sonst:              OBV(t) = OBV(t-1)
```

Kumulativer Volumenindikator. OBV-Divergenz (OBV steigt, Kurs fällt) = Bullish-Signal.

### True Range (TR)

```
TR(t) = max(h_t, c_{t-1}) - min(l_t, c_{t-1})
```

Berücksichtigt Gaps über Nacht. Größerer TR = höhere Volatilität.

### Average True Range (ATR)

```
ATR(t) = (1/n) * Σ_{i=1}^{n} TR(t-i+1)

n = Periodenlänge (Paper: 10 Tage)
```

Gleitender Durchschnitt der True Range. Standardmaß für Volatilität.

---

## Feature-Vektor je Kerze

Jede Kerze → 11 Features:

| # | Feature | Typ | Formel |
|---|---------|-----|--------|
| 1 | Shape | Kategorisch (1–13) | Siehe [candlestick_shape_loc.md](../03b_features/candlestick_shape_loc.md) |
| 2 | Loc | Kategorisch (8 Typen) | Siehe oben |
| 3 | MA5 | Numerisch | MA(t), m=5 |
| 4 | EMA10 | Numerisch | EMA(t), n=10 |
| 5 | ROC(1) | Numerisch | ROC(t), x=1 |
| 6 | CCI10 | Numerisch | CCI(t), n=10 |
| 7 | MOM10 | Numerisch | MOM(t), n=10 |
| 8 | AD | Numerisch | AD(t) |
| 9 | OBV | Numerisch | OBV(t) |
| 10 | TR | Numerisch | TR(t) |
| 11 | ATR10 | Numerisch | ATR(t), n=10 |

**Gesamte Features:**
- 2-Tages-Muster: 11 × 2 Tage = **22 Features**
- 3-Tages-Muster: 11 × 3 Tage = **33 Features**
- (+ Result Direction als Zielvariable, wird nicht als Feature genutzt)

---

## Algorithmus (6 Schritte)

```
OHLCV-Daten (alle Aktien)
         │
         ▼
[Step 1]  Chronologischer Split: ML-Lernset | Prediction-Set
         │
         ▼
[Step 2]  Feature-Extraktion je Kerze:
          Shape + Loc + 9 TA-Indikatoren
         │
         ▼
[Step 3]  Pattern-Generierung:
          2-Tages: 13×13 = 169 Kombinationen
          3-Tages: 13×13×13 = 2.197 Kombinationen
         │
         ▼
[Step 4]  ML-Training je Pattern (4 Modelle):
          LR, KNN, RBM, RF → bestes Modell je Pattern merken
         │
         ▼
[Step 5]  Pattern-Screening:
          Max(Accuracy) > 55% → Pattern ins Pool aufnehmen
          Patterns < 1.000 Trainingsdatenpunkte → verwerfen
         │
         ▼
[Step 6]  Strategy Pool → Investment
          All / Adjust / TOP10 / TOP5 / TOP3
```

---

### Schritt 1: Datensatz-Split

```
ML-Lernset:      Jan 2000 – Dez 2014  (15 Jahre Training)
  ├── Training:  80 % (für Modellparameter)
  └── Testing:   20 % (für Accuracy-Bestimmung / Pattern-Screening)

Prediction-Set:  Jan 2015 – Okt 2020  (6 Jahre Out-of-Sample)
```

**Wichtig:** Prediction-Set ist vollständig unberührt während Training. Kein Look-Ahead-Bias.

---

### Schritt 3: Pattern-Generierung

Jedes N-Tages-Muster ist eine Kombination von N aufeinanderfolgenden Kerzen:

```
2-Tages-Pattern: p_2 = (k_{t-1}, k_t)   mit   Shape_{t-1}, Shape_t ∈ {1,...,13}
                 → 13 × 13 = 169 mögliche Kombinationen

3-Tages-Pattern: p_3 = (k_{t-2}, k_{t-1}, k_t)
                 → 13 × 13 × 13 = 2.197 mögliche Kombinationen
```

**Training Balance:** Pro Pattern werden 5.000 zufällige Datenpunkte ausgewählt (50 % steigende Preise, 50 % fallende Preise) — verhindert Class-Imbalance.

---

### Schritt 4: ML-Modelle

#### Pattern Recognition Algorithm

```
Input:  Feature-Daten je Pattern p
Output: Bestes ML-Modell, Accuracy, Pattern p

foreach p in patterns:
    p_data = Generiere Trainingsdaten für p

    lr_model  = LinearClassification(p_data)      → LR mit L2, GridSearchCV
    knn_model = GridSearchCV(KNN, p_data)
    rf_model  = GridSearchCV(RF, p_data)
    rbm_model = BernoulliRBM + LogisticRegression(p_data)

    max_acc = MAX(Accuracy(lr), Accuracy(knn), Accuracy(rf), Accuracy(rbm))

    if max_acc > accuracy_threshold (55%):
        save best_model, max_acc, p
```

#### Modellparameter

| Modell | Parameter |
|--------|-----------|
| **LR** | Regularisierung L2, solver=warn, C=1.0, max_iter=100, tol=0.0001 |
| **KNN** | n_neighbors ∈ [1,10], weights ∈ {uniform, distance}, algorithm ∈ {auto, ball_tree, kd_tree, brute}, GridSearchCV cv=10 |
| **RBM** | learning_rate=0.06, n_iter=10, n_components=100, + Logistic Output Layer |
| **RF** | n_estimators ∈ [10,100,5], criterion ∈ {gini, entropy}, min_samples_leaf ∈ {2,4,6,50}, max_depth ∈ [1,10], GridSearchCV cv=10 |

#### Zusätzliche Validierungsmodelle (Dependence Testing)

| Modell | Architektur |
|--------|-------------|
| **MLP** | 3-Layer: Input(64) → Hidden(64, ReLU) → Output(1), Adam, binary_crossentropy, 20 Epochs, Batch=128 |
| **LSTM** | 3-Layer: Input(64) → LSTM(64) → Output(1), Adam, binary_crossentropy, 10 Epochs, 56.129 Parameter |

---

### Schritt 5: Pattern-Screening

```
Pattern-Pool aufbauen:
  → Alle Patterns mit max(Accuracy) > 55%

Filter Adjust:
  → Aus Pattern-Pool: Patterns mit < 1.000 Trainingsdaten entfernen
  (verhindert, dass seltene Muster mit wenig Datenbasis ins Portfolio kommen)

Strategy Pools:
  All    = Alle Patterns mit Accuracy > 55%
  Adjust = All minus seltene Patterns (< 1.000 Datenpunkte)
  TOP10  = 10 genaueste Patterns aus Adjust
  TOP5   = 5 genaueste Patterns aus Adjust
  TOP3   = 3 genaueste Patterns aus Adjust
```

**Ergebnis (2-Tages-Muster, 1 Tag voraus):**
- 159 von 169 Mustern überschreiten 55%-Schwelle (94 % aller Muster!)
- RF bester Klassifikator: 96 Muster; KNN: 14; RBM: 39; LR: ~10

---

### Schritt 6: Investmentstrategie (Equal Weight Portfolio)

```
Kapital M, N Patterns im Pool, K Aktien je Pattern p_i

Kapital je Pattern:       M/N * (1/P_i)
Kapital je Aktie:         M/N * (1/P_i) * (1/K)

Einstieg: Schlusskurs zum Zeitpunkt t
Ausstieg: Schlusskurs zum Zeitpunkt t+N (N = 1 bis 10 Tage)

Wenn Prediction = Long → investieren
Wenn Prediction = Short → nichts tun (Long-only im Paper)
```

**Anpassung für unser Projekt:** SELL-Signale aus Short-Muster ergänzen (US-Markt erlaubt Short-Selling).

---

## Modellbewertung

### Accuracy

```
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

| Term | Bedeutung |
|------|-----------|
| TP (True Positive) | Modell = Anstieg, Realität = Anstieg |
| TN (True Negative) | Modell = Fallen, Realität = Fallen |
| FP (False Positive) | Modell = Anstieg, Realität = Fallen |
| FN (False Negative) | Modell = Fallen, Realität = Anstieg |

### Precision, Recall, F-Measure

```
Precision   = TP / (TP + FP)                    [Anteil korrekte Kaufsignale]
Recall      = TP / (TP + FN)                    [Anteil erkannter echter Anstiege]
F-Measure   = 2 * Precision * Recall / (Precision + Recall)   [harmonisches Mittel]
```

**Recall** = auch Sensitivity / True Positive Rate. F-Measure steigt, wenn beide gleich wichtig sind.

---

## Ergebnisse

### Performance (2-Tages-Muster, Prediction 1 Tag voraus)

| Strategie | Ø Jahresrendite | Max Drawdown | Sharpe | Information Ratio |
|-----------|----------------|--------------|--------|-------------------|
| SH Index (Benchmark) | -0,66 % | -52,28 % | -0,19 | 0 |
| All (pure ML, kein PRML) | -2,89 % | -75,45 % | -0,25 | 0,41 |
| **PRML2 (All Patterns)** | **+10,75 %** | **-13,81 %** | **0,17** | **2,38** |
| PRML2 – TOP10 | **+36,73 %** | **-16,43 %** | **0,81** | **2,37** |
| PRML2 – TOP5 | +33,76 % | -15,34 % | 0,99 | 2,02 |
| PRML2 – TOP3 | +26,17 % | -27,62 % | 0,62 | 2,26 |

**Mit 0,2% Transaktionskosten (TOP10):** Immer noch +24,45% Jahresrendite, MDD -17,29%

### Performance LSTM/MLP (TOP10, 2-Tages, 1 Tag voraus)

| Modell | Jahresrendite | Max Drawdown | Sharpe | Information Ratio |
|--------|--------------|--------------|--------|-------------------|
| TOP10 MLP | 11,43 % | -20,03 % | 0,04 | 2,16 |
| **TOP10 LSTM** | **21,83 %** | **-16,26 %** | **0,75** | **1,00** |
| TOP10 MLP+LSTM | 14,72 % | -25,10 % | 0,21 | 2,26 |

### Sliding Window Robustheit (TOP10, 2-Tages, 1 Tag voraus)

| Trainings-Fenster | Test-Fenster | Ø Jahresrendite | Max Drawdown |
|-------------------|--------------|----------------|--------------|
| Jan 2001 – Dez 2015 | Jan 2016 – Okt 2020 | 3,97 % | -17,32 % |
| Jan 2002 – Dez 2016 | Jan 2017 – Okt 2020 | 1,12 % | -21,44 % |
| Jan 2003 – Dez 2017 | Jan 2018 – Okt 2020 | 13,06 % | -16,27 % |
| Jan 2004 – Dez 2018 | Jan 2019 – Okt 2020 | **51,92 %** | **-6,92 %** |

→ Alle 4 Sliding Windows profitabel → robuste Strategie (nicht Datensatz-spezifisch).

### Einflussfaktoren

| Befund | Implikation |
|--------|-------------|
| RF > LR, KNN, RBM | Ensemble-Methoden bevorzugen |
| 1-Tag-Ahead >> 2–10-Tage-Ahead | Kürzerer Prediction-Horizont besser |
| PRML >> Pure ML | Pattern-Vorfilterung erhöht Accuracy strukturell |
| TOP10 > TOP3/5 > All | Optimum: 5–10 best-performing Patterns |
| 2-Tages > 3-Tages | Einfachere Muster robuster (weniger Overfitting) |

---

## Ableitung für unser Projekt

### Was direkt übernehmen

1. **Shape + Loc Feature-Extraktion** → in Feature Store integrieren (`03b_features/candlestick_shape_loc.md`)
2. **TA-Indikatoren als Features** (MA, EMA, OBV, ATR, CCI, MOM, AD, TR, ROC) → bereits in TA-Modul berechnet, nur als ML-Features bereitstellen
3. **Pattern-Screening-Prinzip** (TOP N) → bestätigt Consensus-Voting (DTW); hier mit Accuracy statt Mehrheitsvoting
4. **Random Forest als primäres Modell** → robuster als LSTM für strukturierte Features
5. **Information Ratio** → in Backtesting-Modul ergänzen
6. **Sliding Window Validation** → 4 überlappende Trainingsfenster als Robustheitstest

### Anpassungen für US-Markt

| Aspekt | Paper (China) | Unser Projekt (US) |
|--------|---------------|--------------------|
| Short-Selling | Verboten → Long-only | Erlaubt → SELL-Signale aktivieren |
| Transaktionskosten | 0,2 % (Kommission + Stamp-Duty) | 0,1 % (nur Kommission) |
| Prediction-Horizont | 1 Tag (optimal) | 1–5 Tage (Position-Trading) |
| Pattern-Länge | 2–3 Kerzen | 2–5 Kerzen (Wochen-Muster möglich) |
| Accuracy-Schwelle | 55 % | 55–60 % (konservativer) |

### Einordnung im Algorithmus

```
Feature Store (OHLCV)
         │
         ▼
Shape + Loc + 9 TA-Indikatoren berechnen
(11 Features je Kerze → 22 für 2-Tages / 33 für 3-Tages)
         │
         ▼
Pattern-Klassifikation (welche der 169/2.197 Kombinationen liegt vor?)
         │
         ▼
Random Forest: BUY / SELL (per Pattern vortrainiert)
         │
         ▼
Pattern-Screening: Accuracy > 55%? → Pattern aktiv
         │
         ▼
ML-Score → numerischer Wert für Gesamt-Aggregation
```

### Abgrenzung zu DTW und FFNN

| Aspekt | DTW | FFNN (Serafini) | PRML (Lin et al.) |
|--------|-----|-----------------|-------------------|
| Feature-Typ | Rohpreis-Sequenz (z-norm.) | Volume-Profile (5 Features) | Shape/Loc + 9 TA-Indikatoren (11/Kerze) |
| Modell | Ähnlichkeit (kein ML) | Neural Network | Random Forest (Ensemble) |
| Pattern-Def. | Generisch / emergent | Volume-Shape (b/p) | Formale 13er-Klassifikation |
| Screening | Consensus-Voting (N.ref) | Accuracy-Threshold FFNN | Accuracy-Threshold pro Muster |
| Stärke | Sequenz-Ähnlichkeit | Volumen-Struktur | Candlestick-Kontext + TA |

→ Dreifach-Komplementarität: Alle drei Ansätze verwenden verschiedene Informationsquellen.

---

## Offene Fragen für Implementierung

- [ ] Pattern-Generierung: 2-Tages oder auch 3-Tages-Muster? (2-Tages sind robuster laut Paper)
- [ ] Accuracy-Schwelle: 55 % wie im Paper oder konservativer 60 %?
- [ ] Trainingsdaten-Balance: 5.000 Datenpunkte je Pattern (50/50) reproduzieren?
- [ ] RF vs. LSTM: RF als Primärmodell; LSTM als Validierungsmodell?
- [ ] SELL-Signale: Short-Muster symmetrisch zu Long-Mustern definieren?
- [ ] Prediction-Horizont: 1 Tag (Day-Trading) oder 3–5 Tage (Position-Trading)?
- [ ] Kombination mit DTW-Score: Wie PRML-Accuracy-Score und DTW-Konsens aggregieren?
