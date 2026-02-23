# DTW Generic Pattern Recognition

← [Zurück zur ML-Übersicht](../README.md)

---

> **Quelle:** Tsinaslanidis, P. & Guijarro, F. (2021). *What makes trading strategies based on chart pattern recognition profitable?* Expert Systems, 38(5):1–17.
> **DOI:** 10.1111/exsy.12596
> **Datensatz:** 560 NYSE-Aktien, tägl. OHLC, 2006–2015

---

## Grundidee

Statt bekannte TA-Muster (Flagge, Kopf-Schulter, etc.) algorithmisch zu codieren, sucht dieser Ansatz **generisch** nach historischen Preissequenzen, die dem aktuellen Kursverlauf am ähnlichsten sind — unabhängig davon, ob diese einem definierten technischen Muster entsprechen.

Das Signal entsteht nicht aus Regellogik, sondern aus der Frage: *„Was passierte historisch, wenn der Kurs so aussah wie heute?"*

**TA-Grundprinzip als Fundament:** Geschichte wiederholt sich. Muster sind universell gültig (nicht aktienspezifisch).

---

## Methode: Dynamic Time Warping (DTW)

DTW misst die **Ähnlichkeit zwischen zwei Zeitreihen**, indem es die Zeitachse flexibel streckt und staucht. Im Gegensatz zur euklidischen Distanz (punkt-zu-punkt) erlaubt DTW zeitliche Verschiebungen und Dehnungen — ideal für Kursmuster, die denselben Shape haben, aber unterschiedlich schnell ablaufen.

### Berechnung (3 Schritte)

**Schritt 1 – Distanzmatrix D:**

Für zwei normalisierte Preissequenzen {P} (Länge n) und {S} (Länge m):

```
D(i,j) = (xi - yj)²     für i ∈ [1,n], j ∈ [1,m]
```

**Schritt 2 – DTW-Matrix (akkumulierte Distanz):**

```
DTW(i,j) = D(i,j) + min{ DTW(i-1,j),  DTW(i,j-1),  DTW(i-1,j-1) }
```

**Schritt 3 – Alignment-Kosten (Ähnlichkeitsmaß):**

```
Ähnlichkeit = DTW(n, m)     →     kleiner = ähnlicher (0 = identisch)
```

### UCR Suite – Geschwindigkeitsoptimierung

Standard-DTW auf großen Datensätzen ist rechenzeitintensiv. Die **UCR Suite** (Rakthanmanon et al. 2012) liefert **exakt dasselbe Ergebnis** wie Standard-DTW, jedoch deutlich schneller:

- Z-Normalisierung + inkrementelle euklidische Distanzberechnung
- Pruning: unversprechende Kandidaten werden frühzeitig verworfen (nicht nur Distanz, sondern auch Normalisierungskosten)
- Ermöglicht Durchsuchen von Millionen Subsequenzen in Echtzeit

→ In Python verfügbar über die `stumpy`-Library als direkter Ersatz.

---

## Algorithmus (5 Schritte)

```
Datensatz (OHLCV, alle Aktien)
         │
         ▼
[Step 1]  Train | Test Split  (chronologisch)
         │
         ▼
[Step 2]  Query: aktuelle Preissequenz (letzte $Q.length Schlusskurse)
         │
         ▼
[Step 3]  UCR Suite → $N.ref ähnlichste Subsequenzen aus Trainingsdaten
         │
         ▼
[Step 4a] LABELLING: Jede Referenz → BUY / SELL / Neutral
[Step 4b] DECISION: Consensus-Voting → Handelsempfehlung
         │
         ▼
[Step 5]  Trade: Entry am nächsten Tag → TP oder SL schließt Position
```

---

### Schritt 1: Datensatz-Split (chronologisch)

- **Trainingsdaten:** Erste t₁ Handelstage → Datenbank historischer Referenzmuster
- **Testdaten:** Ab t₁+1 → sequentielle Query-Verarbeitung (Walk-forward)
- Kein zufälliger Split — Zeitreihen-Integrität ist zwingend

*Paper: t₁ = 1.000 Tage (~4 Jahre); Test: 1.517 Tage (~6 Jahre)*

---

### Schritt 2: Query-Auswahl

- Query = aktuelle Preissequenz der letzten **$Q.length** Handelstage
- **Nur Schlusskurse** (kein OHLC) — einfacher zu normalisieren, weniger Rauschen
- Für jeden Stock i und Zeitpunkt t im Testzeitraum wird eine Query extrahiert
- Vor DTW: **Z-Normalisierung** der Query (Mittelwert 0, Standardabweichung 1)

---

### Schritt 3: Referenzmuster-Suche (UCR Suite)

- UCR Suite durchsucht **alle** Trainingssequenzen (alle Aktien, nicht nur der eigene Stock)
- Findet die **$N.ref** ähnlichsten Subsequenzen zur aktuellen Query
- **Cross-Stock-Suche ist Pflicht:** TA-Muster sind universell gültig — ein Doppelboden in AAPL ähnelt einem Doppelboden in MSFT

**Ergebnis:** Referenz-Set = {Ref₁, Ref₂, ..., Ref_N.ref}

---

### Schritt 4a: LABELLING – Referenzen beschriften

Für jede Referenz: Was passierte am Tag **nach** dem Musterendes?

```
Entry-Preis = Schlusskurs am letzten Tag der Referenz

BUY-Take-Profit:   Preis steigt auf Entry × (1 + $TP)  → erreicht vor SL → Label: BUY
BUY-Stop-Loss:     Preis fällt auf Entry × (1 - $SL)   → erreicht vor TP → Label: SELL

SELL-Take-Profit:  Preis fällt auf Entry × (1 - $TP)   → erreicht vor SL → Label: SELL
SELL-Stop-Loss:    Preis steigt auf Entry × (1 + $SL)  → erreicht vor TP → Label: BUY

Keines erreicht:   Label: Neutral
```

**Wichtig:** BUY und SELL schließen sich **nicht** gegenseitig aus. Bei sehr weitem TP und weitem SL können beide Level erreicht werden — dann trägt die Referenz beide Labels.

---

### Schritt 4b: DECISION – Consensus-Voting

```
Zähle BUY-Labels  und  SELL-Labels  unter den $N.ref Referenzen

Wenn BUY-Anteil  ≥ $Consensus-Schwelle  →  BUY-Signal
Wenn SELL-Anteil ≥ $Consensus-Schwelle  →  SELL-Signal (im Projekt: WATCH / ignorieren)
Sonst                                   →  Out-of-market (kein Trade)
```

$Consensus = Anteil der potenziellen Trades, die tatsächlich ausgelöst werden (0,5–10 %).

**Quasi-Unanimität:** Bei strengem $Consensus (z.B. 10 % → alle 10 von 10 Referenzen müssen einig sein) wird der Trade nur selten, aber mit hoher Überzeugung ausgelöst.

---

### Schritt 5: Trade-Ergebnis

- Position wird am **nächsten Tag zum Eröffnungskurs** geöffnet
- Position wird geschlossen wenn TP oder SL erreicht
- Transaktionskosten: 0,05 % je Seite (Floor-Trader-Kosten nach Fama/Blume 1966) als Minimum

---

## Parameter & optimale Werte

| Symbol | Parameter | Getestete Werte | Optimal (TA-aligned) |
|--------|-----------|-----------------|----------------------|
| $Q.length | Query-Länge (Tage) | 10, 15, 20, 25 | **15–25** |
| $N.ref | Anzahl Referenzen | 10, 15, 20, 25 | **10–15** |
| $SL | Stop-Loss (%) | 3, 5, 7, 9, 11 | **< $TP** |
| $TP | Take-Profit (%) | 8, 10, 12, 14, 16 | **12–16** |
| $Consensus | Ausgelöste Trades (%) | 0,5–10 | **0,5–7,5** |

**Hartes Constraint:** $SL < $TP (Stop-Loss immer kleiner als Take-Profit)

---

## Ergebnisse & statistische Evidenz

### Performance (560 NYSE-Aktien, 2006–2015)

| Konfiguration | Profitable Experimente | Ø Return/Trade |
|---------------|------------------------|----------------|
| Alle 1.126 Konfigurationen | **91,03 %** | +0,12 % |
| TA-aligned Parameter (429) | **92,5 %** | +0,12 % |
| TA-aligned nach Transaktionskosten | — | **+0,13 %** |

**Beste Einzelkonfiguration** (Data-snooping-bereinigt):
- $Q.length=10, $N.ref=25, $TP=14 %, $SL=11 % → **+0,763 % Ø Return/Trade**

*Zum Vergleich: Sullivan et al. (1999): 0,29 %; Hsu & Kuan (2005): 0,186 %; Cervelló-Royo et al. (2015): 0,18 %*

---

### Einflussfaktoren auf den Return (Spearman-Korrelation)

| Parameter | Korrelation r | Signifikanz | Richtung |
|-----------|--------------|-------------|----------|
| $TP | **+0,701** | ** (1 %) | Höher = deutlich besser |
| $N.ref | **−0,335** | ** (1 %) | Weniger Referenzen = besser |
| $Q.length | **+0,209** | ** (1 %) | Länger = besser |
| $SL | −0,036 | n.s. | Nicht signifikant |

---

### Logit-Regression: Was treibt Profitabilität?

| Faktor | Koeffizient | Interpretation |
|--------|-------------|----------------|
| $TP | **+73,4 ***| Stärkster Treiber — höheres TP erhöht Profitabilitäts-Odds massiv |
| $Q.length | **+0,148 ***| Längeres Muster = robusteres Signal |
| $SL | **−33,1 ***| Niedrigeres SL = profitabler |
| $N.ref | **−0,202 ***| Weniger Referenzen = schärfere Ähnlichkeit = besser |

Alle Koeffizienten signifikant auf 1 %-Niveau.

---

### Benchmarkvergleich

- Das **Composite Trading System** (Durchschnitt aller Konfigurationen) **dominiert den NYSE-Index** im Mean-Variance-Sinne (höherer Return bei ähnlichem Risiko)
- Ergebnis statistisch signifikant nach **White's Reality Check** (Data-Snooping-Test, White 2000)
- Profitabilität bleibt nach Transaktionskosten positiv (bei TA-aligned Parametern)

---

## Ableitung für unser Projekt

### Einordnung im Algorithmus

```
Feature Store (OHLCV Schlusskurse)
         │
         ▼
DTW-Modul: Query = letzte $Q.length Schlusskurse (z-normalisiert)
         │
         ▼
UCR Suite / stumpy → $N.ref ähnlichste Referenzen aus Trainingshistorie
         │
         ▼
LABELLING → jede Referenz: BUY / SELL / Neutral
         │
         ▼
DECISION: Consensus-Voting
         │
         ▼
ML-Score → numerischer Wert für Gesamt-Aggregation
```

### Empfohlene Implementierungsparameter

| Parameter | Empfehlung | Begründung |
|-----------|-----------|------------|
| $Q.length | **20 Tage** | 4 Handelswochen; starke Korrelation mit Return |
| $N.ref | **10** | Höchste Ähnlichkeit; beste Einzelperformance |
| $TP | **12–15 %** | Stärkster Return-Treiber; TA-aligned |
| $SL | **5–7 %** | Unter $TP; entspricht CRV > 2:1 |
| $Consensus | **1–5 %** | Selektiv aber nicht zu restriktiv |

**Hinweis CRV:** Unser TA-Modul verlangt CRV ≥ 3:1. Für das ML-Modul kann mit CRV ≥ 2:1 gestartet werden ($SL=7 %, $TP=14 %) — Backtesting entscheidet.

### Abgrenzung zum TA-Modul

| Aspekt | TA-Modul | DTW ML-Modul |
|--------|----------|--------------|
| Musterdefinition | Regelbasiert (ADX, RSI, EMA) | Generisch, keine Vorauswahl |
| Signal-Basis | Aktuelle Indikatorwerte | Historische Ähnlichkeit |
| Pattern-Typ | Vordefiniert | Beliebig / emergent |
| Lernfähigkeit | Statisch | Implizit (via Trainingshistorie) |
| Fehlersignal-Schutz | ADX-Regime-Filter | Consensus-Voting |
| Lookback | Keine (nur aktuelle Werte) | Gesamte Trainingshistorie |

→ Kein Overlap: TA liefert regelbasierte Signale, DTW liefert historisch-analoge Signale. Kombination beider Scores reduziert Fehlsignale überproportional (Kombinations-Prinzip aus Han et al. 2022).

---

## Wichtige Designentscheidungen

1. **Cross-Stock-Training:** Referenzen aus allen Aktien suchen, nicht nur aus derselben Aktie — Muster sind universell
2. **Walk-Forward-Split:** Kein Random-Split — Zeitreihen-Integrität (kein Look-Ahead-Bias)
3. **Nur Schlusskurse für Query/Referenzsuche:** OHLC nur für Labelling (TP/SL-Bestimmung)
4. **Z-Normalisierung vor DTW:** Zwingend — sonst dominieren absolute Preisunterschiede die Ähnlichkeit
5. **$SL < $TP als hartes Constraint:** Paper-Evidenz + CRV-Logik

---

## Offene Fragen für Implementierung

- [ ] Python-Library: `stumpy` als UCR Suite Ersatz evaluieren
- [ ] Trainingsfensterlänge: Fix (4 Jahre) oder rollierend (Walk-forward, z.B. letztes Jahr)?
- [ ] Score-Quantifizierung: Wie BUY/SELL/OUT in numerischen Score 0–1 umwandeln? (z.B. BUY-Anteil unter Referenzen)
- [ ] Cache-Strategie: DTW-Ergebnisse im Feature Store (Parquet) speichern?
- [ ] Parameter-Optimierung: Grid Search oder Genetic Algorithm (wie im Paper vorgeschlagen)?
- [ ] Mindest-Trainingshistorie: Wieviele Tage braucht unser Datensatz, bevor DTW sinnvoll startet? (Paper: 1.000 Tage)
