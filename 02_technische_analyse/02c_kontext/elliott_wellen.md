# Elliott-Wellen-Theorie & Fibonacci

← [Zurück zur TA-Übersicht](../README.md)

---

> Elliott-Wellen liefern Kontext für Kursziele und Wellenzählung. Komplex → als Filter/Zusatzinformation, nicht als primäres Signal. IMMER mit anderen TA-Tools kombinieren.

---

## Grundprinzip

**Vollständiger Hausse-Zyklus:** 5 Impulswellen aufwärts + 3 Korrekturwellen abwärts = 8 Wellen

- **Impulswellen (1, 3, 5):** Steigende Wellen in Trendrichtung
- **Korrekturwellen (2, 4):** Fallende Wellen gegen den Aufwärtstrend
- **Korrekturphase (a, b, c):** Drei Wellen; a und c in Korrekturtrendrichtung, b gegen die Korrektur
- **Wichtigste Regel:** Eine Korrektur kann NIEMALS aus fünf Wellen bestehen

**Drei Aspekte (Priorität absteigend):**
1. Wellenform (Form) – wichtigster Aspekt
2. Ratio-Analyse (Fibonacci-Verhältnisse) – für Kursziele
3. Zeit (Zeitliche Beziehungen) – am wenigsten zuverlässig

---

## Wellenhierarchie

- 9 Ränge von *Grand Supercycle* (200 Jahre) bis *Subminuette* (Stunden)
- Fibonacci-Grundlage: 5 + 3 = 8 Wellen; unterteilen sich in 34 + 144 = Fibonacci-Zahlen

---

## Korrekturwellen – 3 Typen

### Zick-Zack (5-3-5 Sequenz)
- Schärfste Korrekturform
- Welle A = 5 Unterwellen; Welle B = 3; Welle C = 5
- Welle B erreicht NICHT den Ausgangspunkt der Welle A
- Welle C läuft deutlich über das Ende von Welle A hinaus

### Flat (3-3-5 Muster)
- Eher Konsolidierung; in Hausse = Zeichen von Stärke
- Welle B: Rallye bis zum Ausgangspunkt der Welle A
- Welle C endet am oder knapp unter dem Endpunkt der Welle A

### Dreieck (5 Wellen, je 3 Unterwellen)
- Taucht **typischerweise in Welle 4** auf → letzte Korrektur vor finaler Impulswelle 5
- 4 Varianten: Aufsteigend, absteigend, symmetrisch, expandierend
- **Kursziel:** Abstand nach Ausbruch = breiteste Dreiecksbreite
- **Timing:** Spitze des Dreiecks markiert oft den Zeitpunkt des Welle-5-Endes

---

## Regel der Alternation

Wenn Welle 2 einfach (a-b-c) war → Welle 4 wird komplex (Dreieck) sein, und umgekehrt.
Sagt nicht was passiert, sondern was wahrscheinlich NICHT passiert → wertvoller Filter.

---

## Welle 4 als Unterstützungszone

Nach abgeschlossenem 5-Wellen-Aufwärtstrend fällt Bärenmarkt normalerweise NICHT unter die vorangegangene Welle 4 des nächst niedrigeren Rangs.
→ **Welle 4 = maximales Korrekturziel und Stop-Niveau**

---

## Fibonacci-Zahlen & Ratios

**Fibonacci-Sequenz:** 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144 ...

**Wichtigste Ratios:**

| Ratio | Herkunft |
|-------|----------|
| 0,382 | Kehrwert von 2,618 |
| 0,500 | 1/2 |
| 0,618 | Goldener Schnitt |
| 1,618 | Kehrwert des Goldenen Schnitts |
| 2,618 | 1,618² |

### Fibonacci-Retracements (Algorithmus-Standard)

| Niveau | Bedeutung |
|--------|-----------|
| 38,2 % | Minimum-Retracement in starkem Trend |
| 50,0 % | Häufigstes Standard-Retracement |
| 61,8 % | Maximum-Retracement in schwächerem Trend |

### Wellen-Kursziele

| Berechnung | Formel |
|-----------|--------|
| Welle 3 Minimum | Länge Welle 1 × 1,618 + Tiefpunkt Welle 2 |
| Welle 5 | Länge Welle 1 × 3,236 + Hoch/Tief Welle 2 |
| Zick-Zack Welle c | Länge Welle a (oder × 1,618) |
| Unregelmäßige Flat Welle c | ≈ 1,618 × Welle a |
| Dreieck (jede Welle) | ≈ 0,618 × vorherige Welle |

### Fibonacci-Zeitziele

- Zähle Handelstage vom letzten wichtigen Drehpunkt
- Erwarte neue Umkehr an Fibonacci-Tagen: **13, 21, 34, 55, 89**
- Gleich auf Wochen- und Monatscharts anwendbar

---

## Aktien vs. Commodities

| Merkmal | Aktien | Commodities |
|---------|--------|-------------|
| Welle 3 | Tendiert zur Extension | — |
| Welle 5 | — | Tendiert zur Extension |
| Welle 4 | Darf NIEMALS mit Welle 1 überlappen | Weniger streng |
| Eignung | Breite Indizes besser als Einzelaktien | Besonders nach langen Bodenbildungen |

---

## Algorithmus-Prioritäten

1. **Fibonacci-Retracement-Scan** (38/50/62 %) als S/R-Bestätigung → leicht implementierbar
2. **Dreieck in Welle 4 erkennen** → Signal: letzte Impulswelle steht bevor
3. **Welle-4-Niveau markieren** → maximales Bären-Kursziel nach 5-Wellen-Hausse
4. **Fibonacci-Zeitziele** (13/21/34/55/89 Tage) als Timing-Bestätigung
5. **5-Wellen-Zählung** → komplex; manuell oder als Zusatzmodul
