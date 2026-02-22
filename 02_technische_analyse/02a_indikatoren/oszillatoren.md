# Oszillatoren

← [Zurück zur TA-Übersicht](../README.md)

---

## Allgemeine Interpretationsregeln (Kap. 10)

1. **Extremzone erreicht** → Überkauft/Überverkauft-Signal
2. **Divergenz in Extremzone** → wichtigstes Warnsignal
3. **Nulllinienkreuzung** → Handelssignal in Trendrichtung

> **Kritisch:** Oszillator-Signale IMMER in Richtung des übergeordneten Trends handeln.

---

## RSI – Relative Strength Index

**Formel:** RSI = 100 − 100 / (1 + RS)
RS = Ø steigende Schlusskurse über x Tage / Ø fallende Schlusskurse über x Tage

### Parameter

| Periode | Anwendung |
|---------|-----------|
| 9 Tage | Sensitiv, kurzfristiges Trading |
| 14 Tage | Standard (= halber 28-Tage-Zyklus) |
| 21 / 28 Tage | Geglättet |
| 14 Wochen | Wochenchart |

### Signale (Priorität absteigend)

| Signal | Beschreibung |
|--------|-------------|
| **Divergenz** | RSI über 70 / unter 30 + 2. Bewegung bestätigt Kursniveau nicht → stärkstes Signal |
| **Failure Swing (Top)** | RSI über 70, dann 2. Gipfel tiefer als 1. bei noch steigenden Kursen → Bruch des Zwischentiefs = Verkaufssignal |
| **Failure Swing (Bottom)** | RSI unter 30, dann 2. Tief höher als 1. bei noch fallenden Kursen → Überschreitung des Zwischenhochs = Kaufsignal |
| **50er-Linie** | Unterstützung (Aufwärtstrend) / Widerstand (Abwärtstrend); Kreuzung als Signal nutzbar |
| **Trendlinienbrüche auf RSI** | Erscheinen oft früher als auf Kurschart → Frühwarnsystem |

### Extremzonen

| Marktphase | Überkauft | Überverkauft |
|------------|-----------|--------------|
| Normal | > 70 | < 30 |
| Starker Bullenmarkt | > 80 | < 20 |

---

## Stochastik-Oszillator (langsam bevorzugt)

**Formel %K:** `%K = 100 × (C − L14) / (H14 − L14)`
C = letzter Schlusskurs, L14 = Tiefstes Tief 14 Perioden, H14 = Höchstes Hoch 14 Perioden

**%D** = 3-Perioden-MA der %K-Linie (die wichtigere Linie)

**Langsame Stochastik:** Zusätzlicher 3-Perioden-MA beider Linien → geglättet, zuverlässiger

### Signale

| Signal | Beschreibung |
|--------|-------------|
| **Vorbereitendes Signal** | %D in Extremzone (> 80 / < 20) + Divergenz zur Kursbewegung |
| **Eigentliches Handelssignal** | %K kreuzt %D in Extremzone |
| **Kombination Wochen + Tage** | Wochensignal = Trendrichtung; Tagessignal = Timing |

### Candle Pattern Filtering (Morris 1991)

> Candlestick-Formationen NUR beachten wenn Stochastik-%D in Extremzone (> 80 oder < 20). Eliminiert Früh- und Fehlsignale erheblich.

---

## MACD – Moving Average Convergence/Divergence

**Konstruktion:**
- MACD-Linie: Differenz 12-EMA minus 26-EMA
- Signallinie: 9-EMA der MACD-Linie
- Histogramm: MACD-Linie minus Signallinie

### Signale (Priorität absteigend)

| Priorität | Signal | Beschreibung |
|-----------|--------|-------------|
| 1 | **Histogramm-Wendepunkt** | Dreht VOR Signallinie-Kreuzung → Frühwarnung |
| 2 | **Signallinie-Kreuzung** | MACD kreuzt Signallinie nach oben = Kauf; nach unten = Verkauf |
| 3 | **Nulllinienkreuzung** | Ähnlich Momentum-Technik |
| 4 | **Divergenz** | MACD über Null + beginnt zu fallen während Kurse steigen → bearish |

**Beste Signale:** Kaufsignale unter der Nulllinie; Verkaufssignale über der Nulllinie

**Wochen-MACD als Tagesfilter:** Tagessignale nur handeln wenn mit Wochen-MACD-Richtung übereinstimmend

---

## Momentum & Rate of Change (ROC)

| Indikator | Formel | Nulllinie |
|-----------|--------|-----------|
| Momentum | M = V − Vx | 0 |
| ROC | ROC = 100 × (V / Vx) | 100 |

**Parameter:** 10 Tage (kurzfristig), 40 Tage (mittelfristig)

**Interpretation:**
- Über Nulllinie und steigend → Aufwärtstrend beschleunigt
- Über Nulllinie und flachend → Trend verlangsamt, aber noch intakt
- Unter Nulllinie → kurzfristiger Abwärtstrend in Kraft
- **Momentum läuft Kursbewegung voraus** → Trendlinienbrüche früher als auf Kurschart

---

## Larry Williams %R

**Formel:** Invertierte Stochastik
**Parameter:** 20 Tage (Standard)
**Extremzonen:** > 80 oder < 20

Gleiche Interpretationsprinzipien wie RSI und Stochastik (Divergenz, Überkauft/Überverkauft).

---

## Commodity Channel Index (CCI)

**Parameter:** 20 Perioden

| Signal | Bedingung |
|--------|-----------|
| Kaufsignal | CCI über +100 |
| Verkaufssignal | CCI unter −100 |

---

## Kombinations-Signale

- **RSI + Stochastik:** Signal nur ausgeben wenn BEIDE Oszillatoren im überkauften/überverkauften Bereich
- **Candlestick + Stochastik %D:** Candlestick-Formation nur wenn %D > 80 oder < 20 (Morris-Filter)
- **Wochen-MACD + Tages-MACD:** Tagessignal nur in Richtung des Wochen-MACD

---

## Zeitperioden & Marktzyklen (Kap. 10)

- Oszillator-Längen sind auf Marktzyklen bezogen: Stützzeitraum = halbe Zykluslänge
- 28-Tage-Handelszyklus (20 Handelstage) → 14-Tage-RSI, 10-Tage-Momentum
- Alle Standardparameter (5, 10, 14, 20) stehen in harmonischer Beziehung zum 28-Tage-Zyklus

---

## Empirische Evidenz: RSI *(Wong, Manzur, Chew 2002)*

> Quelle: *How Rewarding Is Technical Analysis? Evidence From Singapore Stock Market* – empirische Studie am Singapore Straits Times Industrial Index, 1974–1994.

### RSI 50-Crossover: zuverlässigste RSI-Methode

Von vier getesteten RSI-Methoden (Touch, Peak, Retracement, 50 Crossover) lieferte ausschließlich die **50-Crossover-Methode** konsistent signifikante Ergebnisse. Die anderen drei Methoden produzierten gemischte oder insignifikante Resultate.

**50-Crossover-Regel:**
- **Kaufsignal:** RSI steigt über 50
- **Verkaufssignal:** RSI fällt unter 50

Für den Gesamtzeitraum waren sowohl Buy- als auch Sell-Statistiken auf dem 1%-Niveau signifikant. Buy-Sell-Differenz durchgehend hoch signifikant.

**Konsequenz für den Algorithmus:**
- RSI-50-Crossover als ergänzendes Trendsignal verwenden (RSI > 50 = Aufwärtsmomentum bestätigt)
- Touch/Peak/Retracement-Methoden nur in Kombination mit ADX-Regime-Filter einsetzen
- Die 50er-Linie als Unterstützung/Widerstand (bereits in Murphy dokumentiert) hat damit auch empirische Bestätigung

### ADX als Pflicht-Filter für RSI: empirisch bestätigt

Die Autoren weisen explizit darauf hin, dass RSI primär für **nicht-trendende Märkte** konzipiert ist. In Trendmärkten liefert RSI häufig Fehlsignale, weil er dauerhaft in einer Extremzone verweilt. Die empfohlene Lösung (LeBeau/Lucas 1992): **RSI nur einsetzen wenn ADX einen nicht-trendenden Markt anzeigt.**

Da in der Studie kein ADX-Filter angewendet werden konnte (fehlende Daten), wurden RSI-Signale auf alle Marktphasen angewendet – was die gemischten Ergebnisse bei Touch/Peak/Retracement erklärt.

**Konsequenz für den Algorithmus:**
- RSI-Extremzonen-Signale (< 30 / > 70) nur ausgeben wenn ADX < 25 (Seitwärtsmarkt)
- RSI-50-Crossover kann auch in Trendmärkten als Trendbestätigung genutzt werden
- Dies ist deckungsgleich mit unserem bestehenden ADX-Regime-Filter (Signalfilter Nr. 2)

### Buy-Signal robuster als Sell-Signal

Über alle RSI-Varianten hinweg waren Buy-Signale konsistent stärker und statistisch zuverlässiger als Sell-Signale. Das deckt sich mit dem Befund aus den MA-Studien und bestätigt: **Kaufsignale sind generell robuster als Verkaufssignale bei technischen Indikatoren.**

**Konsequenz für den Algorithmus:**
- Entspricht unserem aktuellen Scope (nur Kaufsignale) – empirisch gut begründet
- Wenn später Sell-Signale ergänzt werden: mit deutlich höheren Anforderungen an Bestätigung
