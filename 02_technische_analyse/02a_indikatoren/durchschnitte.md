# Gleitende Durchschnitte & Bollinger Bänder

← [Zurück zur TA-Übersicht](../README.md)

---

## Typen gleitender Durchschnitte

| Typ | Beschreibung | Empfehlung |
|-----|-------------|------------|
| **SMA** | Arithmetisches Mittel; jeder Tag gleich gewichtet | Bewährt, einfach |
| **Linear gewichtet** | Jüngere Kurse stärker gewichtet | Selten verwendet |
| **EMA** | Gibt jüngstem Kurs mehr Gewicht + bezieht alle historischen Kurse ein | Präzisere Signale |

> Kein eindeutiger Beweis, dass EMA besser als SMA performt – beim bewährten SMA bleiben und Experimente minimieren.

---

## Bewährte MA-Kombinationen

| Kombination | Markt | Anwendung |
|------------|-------|-----------|
| 5 + 20 Tage | Futures/Aktien | Double Crossover, kurzfristig |
| 10 + 50 Tage | Aktien | Double Crossover, mittelfristig |
| 4 + 9 + 18 Tage | Futures | Triple Crossover (Allen-System) |
| 9 + 18 Tage | Futures | Double Crossover |
| 50 + 200 Tage | Aktien | Golden/Death Cross, langfristig |
| 10 + 40 Wochen | Aktien/Futures | Primärtrend-Verfolgung |
| 20 Tage | Alle | Bollinger-Basis |
| 13 Wochen / 21 Tage | Alle | Fibonacci-MAs (bewährt) |

---

## Triple Crossover – Allen-System (4-9-18 Tage)

- **Aufwärtstrend:** 4-Tage-Linie > 9-Tage-Linie > 18-Tage-Linie
- **Abwärtstrend:** Reihenfolge umgekehrt (18 > 9 > 4)
- **Vorbereitendes Verkaufssignal:** 4-Tage-Linie fällt unter 9- UND 18-Tage-Linie
- **Bestätigendes Signal:** 9-Tage-Linie kreuzt unter 18-Tage-Linie
- Umgekehrt für Kaufsignale

---

## Bollinger Bänder

**Parameter:** 20 Tage (täglich), 20 Wochen (wöchentlich), ±2 Standardabweichungen

| Signal | Beschreibung |
|--------|-------------|
| Oberes Band | Überkauft-Ziel; Abprall möglich |
| Unteres Band | Überverkauft-Ziel; Abprall möglich |
| Enge Bänder (Squeeze) | Volatilitätskompression → neuer Trend beginnt bald |
| Kurs berührt unteres Band | Kursziel = oberes Band (und umgekehrt) |

---

## Prozentbänder (Alternative zu Bollinger)

| Zeitrahmen | Parameter |
|------------|-----------|
| Kurzfristig | 3 %-Bänder um 21-Tage-MA |
| Langfristig | 5 %-Bänder um 10-Wochen-MA |
| Sehr langfristig | 10 %-Bänder um 40-Wochen-MA |

Kurs erreicht Bandgrenze → Trend als überdehnt betrachten.

---

## 4-Wochen-Regel (Donchian)

- **Kaufsignal:** Kurs übersteigt Hoch der letzten 4 vollen Kalenderwochen
- **Verkaufssignal:** Kurs unterschreitet Tief der letzten 4 vollen Kalenderwochen
- Bewährtestes einfaches Trendfolgesystem; geringe Transaktionskosten
- Direkte Ableitung des 28-Tage-Handelszyklus
- **Modifizierbar:** 1- oder 2-Wochen-Ausstiegsregel für sensibleres System

---

## MA als Oszillator (MACD-Basis)

- Differenz zwischen kurzem und langem MA als Histogramm darstellen
- Histogramm dreht vor Signallinie → Frühindikator
- In Aufwärtstrend: Histogramm an Nulllinie = Kaufzone

---

## Wichtige Einschränkungen

- Gleitende Durchschnitte funktionieren gut in **Trendmärkten**, schlecht in **Seitwärtsphasen** (1/3 bis 1/2 der Zeit)
- Lösung: ADX-Filter einsetzen → bei fallendem ADX Oszillatoren bevorzugen
- Optimierung von MAs nützlich, aber kein Heiliger Gral; Out-of-sample-Testing zwingend

---

## Zeitrahmen-Konvention (Murphy)

| Chart | Abdeckung |
|-------|-----------|
| Intraday | ab 5-Minuten-Perioden |
| Tages-Chart | 6–9 Monate |
| Wochen-Chart | bis zu 5 Jahre |
| Monats-Chart | bis zu 20 Jahre |

---

## Empirische Evidenz & Einschränkungen *(Han, Liu, Zhou, Zhu 2022)*

> Quelle: *Technical Analysis in the Stock Market: A Review* – akademischer Review-Artikel, der Studien von 1897 bis 2020 auswertet.

### MA-Crossover auf Marktebene: seit 1987 nicht mehr zuverlässig

Einfache MA-Crossover-Strategien (Variable-Length MA, Fixed-Length MA, Trading Range Breakout) waren von 1897 bis 1986 nachweislich profitabel. **Seit 1987 ist diese Profitabilität auf Indexebene praktisch verschwunden.** In der Periode 1987–2020 zeigen alle getesteten Crossover-Regeln negative oder statistisch insignifikante Buy-Sell-Differenzen.

Hauptursache: **Publication Effect** – sobald eine Strategie bekannt und weit verbreitet ist, wird sie vom Markt eingepreist und arbitriert.

**Konsequenz für den Algorithmus:**
- MA-Crossover-Signale **nicht als eigenständiges Kaufsignal** verwenden
- MAs bleiben sinnvoll als **Trendfilter** (Richtungsbestimmung) und als **Kontextindikator** (Kurs über/unter MA)
- Eigenständige Crossover-Signale nur in Kombination mit weiteren Bestätigungen werten

### MA-Timing auf Einzeltitelebene: weiterhin robust

Im Gegensatz zur Marktebene bleibt MA-Timing auf **Einzelaktien** nachweislich wirksam – besonders bei volatileren Titeln. Die Strategie "Kurs > MA → investiert, Kurs < MA → aus dem Markt" zeigt auf Einzeltitelebene deutlich höhere Sharpe Ratios als Buy-and-Hold, und das auch nach Veröffentlichung der Studie (Han, Yang, Zhou 2013).

**Konsequenz für den Algorithmus:**
- MA-basierte Signale auf Einzeltitelebene sind valide und sollen genutzt werden
- Volatilität eines Titels kann als verstärkender Faktor für MA-Signale berücksichtigt werden

### Multi-Horizont-Ansatz: empirisch überlegen

Der sogenannte **Trend-Faktor** (Han, Zhou, Zhu 2016) verwendet MAs über viele Zeithorizonte gleichzeitig: 3, 5, 10, 20, 50, 100, 200, 400, 600, 800 und 1.000 Tage. Dieser Multi-Horizont-Ansatz erzielte historisch einen Sharpe Ratio von 0,46 – deutlich höher als Momentum, Value oder Marktfaktor.

**Konsequenz für den Algorithmus:**
- Unser Top-Down-Ansatz (Monthly / Weekly / Daily) hat eine solide empirische Grundlage
- MAs über **mehrere Zeithorizonte gleichzeitig** auswerten, nicht nur einen
- Übereinstimmung über mehrere Horizonte = stärkeres Signal

### Buy-Signal robuster als Sell-Signal *(Wong, Manzur, Chew 2002)*

Eine Studie am Singapore Stock Exchange (1974–1994) zeigt: MA-basierte **Buy-Signale sind konsistent stärker und statistisch zuverlässiger als Sell-Signale**. Sell-Signale waren häufig insignifikant, besonders in kürzeren Testperioden. Buy-Signale hingegen waren über alle MA-Varianten (Single, Dual, Triple) und alle Subperioden hinweg auf dem 5–10%-Niveau signifikant.

**Konsequenz für den Algorithmus:**
- Fokus auf Kaufsignale (entspricht unserem aktuellen Scope) ist empirisch gut begründet
- Sell-Signale aus MA-Crossovern mit deutlich niedrigerem Vertrauen behandeln
- Ergebnis wird robuster, je länger der Beobachtungszeitraum nach dem Signal ist (5 → 30 Tage)
