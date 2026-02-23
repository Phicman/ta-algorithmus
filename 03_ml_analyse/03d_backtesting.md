# Backtesting – Evaluierungsmetriken & Validierungsdesign

← [Zurück zur ML-Übersicht](./README.md)

---

## Validierungsdesign: Walk-Forward Cross Validation

**Grundprinzip:** Zeitreihen dürfen nicht zufällig gesplittet werden — zukünftige Daten dürfen nie im Training enthalten sein.

### Schema

```
Block 1: [████████████░░░░░░░░░░░░░░░░░░░]
Block 2: [████████████████████░░░░░░░░░░░]
Block 3: [████████████████████████████░░░]
Block 4: [████████████████████████████████░░░]
          ←──── Training ────→  ←─ Test ─→
```

| Parameter | Wert | Quelle |
|-----------|------|--------|
| Anzahl Blöcke | 4 | Serafini (2019) |
| Train/Test-Ratio | 70 / 30 | Serafini (2019) |
| Split-Art | Chronologisch (expandierend) | Beide Paper |

**Expandierender vs. rollierender Ansatz:**
- **Expandierend (default):** Trainingsset wächst mit jedem Block an — mehr Daten, aber ältere Muster gewichtet
- **Rollierend:** Trainingsset hat feste Länge (z.B. letzte 4 Jahre) — neuere Muster dominieren

→ Für **Modell-Validierung**: expandierend bevorzugt (mehr Datenbasis für stabile Schätzungen)
→ Für **Parameter-Selektion** (SL/TP-Kalibrierung): rollierend / quartalweise bevorzugt — neuere Marktregimes sind relevanter

### Walk-Forward als Live-Parametrierungsmechanismus *(Arévalo et al. 2017)*

> Erweiterung: Walk-Forward nicht nur zur Validierung, sondern aktiv zur Parameterauswahl im Live-Betrieb.

**Schema (quartalweise):**
```
Quartal 1  →  Training: Beste SL/TP-Konfiguration ermitteln
Quartal 2  →  Test mit Q1-Parametern + gleichzeitig Training für Q3
Quartal 3  →  Test mit Q2-Parametern + gleichzeitig Training für Q4
...
```

- Je Quartal werden alle SL/TP-Kombinationen auf dem Trainingsquartal evaluiert
- Die profitabelste Konfiguration wird automatisch auf das Folge-Quartal angewendet
- **Resultat:** Kein manuelles Parameter-Raten; System adaptiert sich an Marktregimes
- **Vorteil gegenüber statischen Parametern:** Schlägt statische Konfigurationen konsistent (empirisch belegt für 52 Testquartale)

**Wichtig:** SL/TP werden dynamisch ermittelt; alle anderen Parameter (FV-Threshold, Range-Filter, EMA-Perioden) werden separat via Reality Check validiert — sie sind nicht Teil des dynamischen Quartals-Loops, um Data Snooping zu vermeiden.

---

## Metriken-Übersicht

### 1. WWR – Weighted Win Ratio

> Quelle: Serafini (2019)

```
WWR = Ø(Gewinn-Trades × Gewinn-Betrag) / Ø(Verlust-Trades × Verlust-Betrag)

WWR > 1  →  profitabel (Gewinne überwiegen gewichtet)
WWR = 1  →  Break-Even
WWR < 1  →  Verlustbringend
```

**Unterschied zu Win-Rate:** WWR berücksichtigt die **Höhe** der Gewinne und Verluste, nicht nur ihre Anzahl. Ein Algorithmus mit 40 % Win-Rate kann WWR > 1 haben, wenn die Gewinne deutlich größer sind als die Verluste.

*Serafini-Referenz: FFNN erreicht WWR = 80,4 %*

---

### 2. PPC – Profit Per Contract

> Quelle: Serafini (2019)

```
PPC = Summe aller Gewinne und Verluste / Anzahl Trades
    (in Dollar oder Prozent je nach Instrument)
```

**Bedeutung:** Absoluter Durchschnittsgewinn pro Trade. Negatives PPC = System verliert im Schnitt.

*Serafini-Referenz: FFNN erreicht PPC = 78,41 $/Contract*

---

### 3. MDD – Maximum Drawdown

> Quelle: Serafini (2019)

```
MDD = max(Peak - Trough) über den gesamten Testzeitraum

Kumulierte Equity-Kurve:
  Peak ──────┐
             │ ← Drawdown
  Trough     └──── (tiefster Punkt nach einem Peak)

MDD = größter dieser Abstände
```

**Bedeutung:** Worst-Case-Verlust, den ein Trader hätte aushalten müssen. Niedrigerer MDD = bessere Risikokontrolle.

*Serafini-Referenz: FFNN erreicht Ø MDD = 128,53 $/Contract*

---

### 4. Return per Trade (Ø Return/Trade)

> Quelle: Tsinaslanidis & Guijarro (2021)

```
Ø Return/Trade = Summe aller Trade-Returns / Anzahl Trades
                 (in Prozent des Einsatzes)
```

*Paper-Referenz: Beste DTW-Konfiguration erreicht +0,763 % Ø Return/Trade*

---

### 5. Profitable Experiment Rate

> Quelle: Tsinaslanidis & Guijarro (2021)

```
Profitable Experiments = Anteil der Konfigurationen mit positivem Gesamt-Return

91,03 % aller 1.126 Konfigurationen → positiver Gesamt-Return (DTW, NYSE, 2006–2015)
```

**Bedeutung für Parameterrobustheit:** Hohe Rate bedeutet, dass das System über viele Parameterkombinationen hinweg stabil profitabel ist — kein Data-Snooping-Artefakt.

---

### 6. Sharpe Ratio

> Quelle: Lin et al. (2021) — formale Definition

```
SharpeRatio = (μ(R_t) - r_f) / σ(R_t)

μ(R_t) = Durchschnittlicher kumulierter Return bis Datum t
r_f    = Risikofreier Zinssatz (z.B. US Treasury 3M)
σ(R_t) = Standardabweichung des Returns R_t
```

Höherer Sharpe = bessere risikoadjustierte Performance.

| Sharpe | Bewertung |
|--------|-----------|
| < 0 | Schlechter als risikofreier Zins |
| 0 – 0,5 | Schwach |
| 0,5 – 1,0 | Akzeptabel |
| > 1,0 | Gut |
| > 2,0 | Sehr gut (PRML TOP10 erreicht 0,81) |

*Paper-Referenz: Lin et al. PRML TOP10 = 0,81; Information Ratio = 2,37*

---

### 7. Average Annual Return

> Quelle: Lin et al. (2021)

```
AverageAnnualReturn = (Π_{i=1}^{N} (1 + r_i))^(1/N) - 1

r_i = Return des Jahres i
N   = Anzahl Jahre im Testzeitraum
```

Geometrischer Jahres-Durchschnittsreturn (berücksichtigt Compounding). Besser als arithmetisches Mittel für multi-jährige Perioden.

*Paper-Referenz: Lin et al. PRML TOP10 = +36,73 % p.a. vs. Benchmark -0,66 % p.a.*

---

### 8. Information Ratio

> Quelle: Lin et al. (2021)

```
InformationRatio = (R_t - R_b) / σ_t

R_t = Return des Portfolios im Zeitraum t
R_b = Return des Benchmarks (z.B. S&P 500) im gleichen Zeitraum
σ_t = Tracking Error (Standardabweichung der Excess-Returns)
```

**Bedeutung:** Misst die Outperformance gegenüber dem Benchmark pro Einheit Tracking-Risiko.

| Information Ratio | Bewertung |
|-------------------|-----------|
| < 0 | Underperformance |
| 0 – 0,5 | Schwache Outperformance |
| 0,5 – 1,0 | Gute Outperformance |
| > 1,0 | Sehr gute Outperformance |
| > 2,0 | Exzellent (PRML TOP10 erreicht 2,37) |

*Paper-Referenz: Lin et al. PRML TOP10 = 2,37 (vs. Benchmark IR = 0)*

---

### 9. Accuracy / Precision / Recall / F-Measure

> Quelle: Lin et al. (2021) — für Pattern-Screening

```
Accuracy  = (TP + TN) / (TP + TN + FP + FN)
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F-Measure = 2 * Precision * Recall / (Precision + Recall)
```

| Term | Bedeutung im Trading-Kontext |
|------|------------------------------|
| TP (True Positive) | Kaufsignal korrekt → Preis stieg |
| TN (True Negative) | Kein Signal korrekt → Preis fiel |
| FP (False Positive) | Kaufsignal falsch → Preis fiel (Fehlsignal) |
| FN (False Negative) | Kein Signal obwohl Preis stieg (verpasste Chance) |

**Verwendung im PRML-Framework:** Accuracy-Threshold = 55 % als Selektionskriterium für Pattern-Pool.

---

## Benchmark-Vergleiche

| Benchmark | Beschreibung | Referenz |
|-----------|-------------|---------|
| **Buy & Hold** | Passives Halten des Index (NYSE, S&P 500) | Standard |
| **Random-Baseline** | Zufällige BUY/SELL-Entscheidungen (WWR ≈ 50 %) | Serafini (2019) |
| **White's Reality Check** | Data-Snooping-bereinigter Signifikanztest | Tsinaslanidis (2021), White (2000) |
| **Sullivan et al. (1999)** | Technische Handelssysteme: Ø +0,29 % / Trade | Historische Benchmark |
| **Hsu & Kuan (2005)** | TA-Systeme: Ø +0,186 % / Trade | Historische Benchmark |

---

## Transaktionskosten

| Kostenart | Wert | Markt | Quelle |
|-----------|------|-------|--------|
| Floor-Trader-Kosten | 0,05 % je Seite (0,1 % Round-Trip) | US | Fama/Blume (1966) nach Tsinaslanidis |
| Kommission + Stamp-Duty | 0,2 % total | China | Bessembinder & Chan nach Lin et al. |
| Bid-Ask Spread (US) | 0,1 % – 0,39 % | US | Bessembinder & Chan (1998) |
| Slippage | Nicht explizit modelliert | — | Konservativ via Entry-Timing |

**Konsequenz für unser Projekt (US):** System muss > 0,1–0,2 % Return pro Trade erzielen (je nach Broker). DTW: +0,12 % Ø → positiv nach Kosten (knapp).

---

## Sliding Window Validation

> Quelle: Lin et al. (2021) — als Robustheitstest

Ergänzend zur Walk-Forward-CV: 4 überlappende Trainingsfenster mit je anderem Startpunkt.

```
Fenster 1: Training Jan 2001–Dez 2015 | Test Jan 2016–Okt 2020
Fenster 2: Training Jan 2002–Dez 2016 | Test Jan 2017–Okt 2020
Fenster 3: Training Jan 2003–Dez 2017 | Test Jan 2018–Okt 2020
Fenster 4: Training Jan 2004–Dez 2018 | Test Jan 2019–Okt 2020
```

**Zweck:** Wenn das System in allen 4 Fenstern profitabel ist, ist es nicht von einer einzelnen Marktphase abhängig.

**Unterschied zur Walk-Forward-CV:** Sliding Window hat überlappende Trainingsdaten und deckt verschiedene Marktphasen ab; Walk-Forward testet inkrementell.

---

## Statistische Tests

| Test | Zweck | Paper |
|------|-------|-------|
| **White's Reality Check** | Testet ob Performance signifikant oder Data-Snooping-Artefakt | Tsinaslanidis (2021), Arévalo et al. (2017) |
| **Hansen SPA** | Superior Predictive Ability — weniger konservativ als Reality Check; korrigiert für schwache Vergleichsstrategien | Arévalo et al. (2017) |
| **Spearman-Korrelation** | Nicht-parametrischer Zusammenhang Parameter ↔ Return | Tsinaslanidis (2021) |
| **Logit-Regression** | Welche Parameter treiben Profitabilität? | Tsinaslanidis (2021) |
| **Walk-Forward CV** | Overfitting-Schutz durch Out-of-Sample-Validierung | Serafini (2019) |
| **Walk-Forward Parametrierung** | Dynamische SL/TP-Selektion pro Quartal (Live-Adaptierung) | Arévalo et al. (2017) |
| **Sliding Window** | Robustheit über verschiedene Marktphasen | Lin et al. (2021) |
| **Accuracy-Threshold-Test** | Pattern-Screening: Nur Muster > 55 % Accuracy ins Portfolio | Lin et al. (2021) |

---

## Evaluierungsrahmen für unser Projekt

### Primäre Metriken (Pflicht)

| # | Metrik | Einheit | Mindest-Ziel | Quelle |
|---|--------|---------|-------------|--------|
| 1 | **Ø Return/Trade** | % | > 0,2 % (nach Kosten) | DTW Paper |
| 2 | **Average Annual Return** | % p.a. | > Buy&Hold | Lin et al. |
| 3 | **MDD** | % | < Benchmark MDD | Alle Paper |
| 4 | **Sharpe Ratio** | — | > 0,5 | Lin et al. |
| 5 | **Information Ratio** | — | > 1,0 | Lin et al. |

### Sekundäre Metriken (ergänzend)

| # | Metrik | Einheit | Quelle |
|---|--------|---------|--------|
| 6 | **Win-Rate** | % | Alle |
| 7 | **WWR** | — | Serafini |
| 8 | **PPC** | $/% | Serafini |
| 9 | **Profitable Experiment Rate** | % | Tsinaslanidis |
| 10 | **Accuracy je Pattern** | % | Lin et al. |
| 11 | **F-Measure** | — | Lin et al. |
| 12 | **Profit / MDD Ratio** | — | Arévalo et al. (2017) |

**Profit / MDD Ratio:**
```
Profit/MDD = Gesamtprofit / Maximum Drawdown
```
Misst wie viel Gewinn pro Einheit maximalem Risiko erzielt wurde. Hoher Wert = günstigeres Risiko-Ertrags-Profil. Referenzwert Arévalo et al.: **13,2** bei optimalem FV-Setting.

### Benchmark

- Primär: **Buy & Hold S&P 500** (passiver Vergleich) → Information Ratio
- Sekundär: **Random Baseline** (Signifikanztest, WWR ≈ 50 %)
- Tertiär: **Sullivan et al. (1999)** historische TA-Benchmark (+0,29 % / Trade)

---

## Offene Fragen für Backtesting-Design

- [x] Expandierendes oder rollierendes Trainingsfenster? → **Beide, je nach Zweck:** Expandierend für Modell-Validierung; rollierend/quartalweise für dynamische SL/TP-Parametrierung (Arévalo et al. 2017)
- [ ] Wie viele Walk-Forward-Blöcke? (4 wie Serafini oder anpassen?)
- [ ] White's Reality Check implementieren oder vereinfachter Permutationstest?
- [ ] Kombinierter ML+TA-Score: Wie separate vs. kombinierte Evaluation?
- [ ] Slippage-Modellierung: Welcher Annahme? (0,05 % je Seite als Ausgangspunkt)
- [ ] Sliding Window: Wie viele Fenster? Gleiche Länge wie Paper (15 Jahre Training)?
- [ ] Risikofreier Zins für Sharpe: US 3M Treasury (aktuell ~5 %) oder langfristiger Durchschnitt (2–3 %)?
- [ ] Accuracy-Threshold für Pattern-Screening: 55 % wie Paper oder konservativer?
