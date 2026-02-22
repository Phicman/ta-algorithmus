# Zeitzyklen & Saisonalität

← [Zurück zur TA-Übersicht](../README.md)

---

## Grundprinzip (Kap. 14)

Zyklen beantworten **WANN** dreht der Markt – als Ergänzung zu Kurs- und Indikatoranalyse.

**Drei Parameter eines Zyklus:**
- **Amplitude:** Höhe (in Preis-Einheiten, Tal zu Kamm)
- **Länge:** Zeitspanne zwischen zwei Tälern (Tief zu Tief = zuverlässiger als Gipfel zu Gipfel)
- **Phase:** Zeitpunkt des letzten Wellentals (für Projektion des nächsten)

---

## Vier Zyklische Prinzipien

| Prinzip | Beschreibung |
|---------|-------------|
| **Summation** | Jede Kursbewegung = Summe aller aktiven Zyklen |
| **Harmonizität** | Benachbarte Zyklen stehen in Verhältnis 2:1 (z.B. 20 → 10 und 40 Tage) |
| **Synchronizität** | Wellen verschiedener Länge bilden oft gleichzeitig Böden |
| **Proportionalität** | Längere Zyklen haben proportional größere Amplituden |

---

## Nominales Zyklusmodell (Hurst)

| Einheit | Länge |
|---------|-------|
| Jahre | 18 / 9 |
| Monate | 54 / 18 |
| Wochen | 40 / 20 |
| Tage | 80 / 40 / 20 / 10 / 5 |

> Die Standard-Perioden 5, 10, 20, 40 Tage für MAs und Oszillatoren spiegeln dominante Marktzyklen wider – kein Zufall!

---

## Klassifikation der Zyklen

| Typ | Länge | Handelsbedeutung |
|-----|-------|-----------------|
| Langfristiger Zyklus | 2+ Jahre | Übergeordneter Trend |
| Saisonaler Zyklus | ~1 Jahr | Jahreszeitmuster |
| **Primärer/Mittelfristiger Zyklus** | 9–26 Wochen | **Am nützlichsten für Trading** |
| Trading-Zyklus | 4 Wochen | Einstieg/Ausstieg in Primärtrendrichtung |
| Alpha/Beta-Zyklus | ~2 Wochen | Feintuning |

**Nutzung:**
- Primärzyklus = Seite des Marktes (long oder short)
- Trading-Zyklus = Tiefpunkte für Käufe nutzen (wenn Primärtrend aufwärts)

---

## Linke und rechte Translation

| Translation | Zyklus-Gipfel | Bedeutung |
|-------------|---------------|-----------|
| **Rechte Translation** | Rechts des idealen Mittelpunkts | Bullenmarkt-Kennzeichen |
| **Linke Translation** | Links des Mittelpunkts | Bärenmarkt-Kennzeichen |

---

## Saisonale Zyklen – Rohstoffe

| Markt | Typisches Hoch | Typisches Tief |
|-------|---------------|----------------|
| Sojabohnen | Apr–Jun | Aug–Okt |
| Gold | — | Aug (Saisontief) |
| Rohöl | Okt | — |
| T-Bonds | Jan | Okt |

---

## Aktienmarkt-Saisonalität

| Muster | Detail |
|--------|--------|
| Stärkste 3 Monate | November–Januar |
| Schwächster Monat | September |
| Stärkster Monat | Dezember |
| "Sell in May" | Mai–Oktober schwächer als Oktober–April; historisch belegt |

---

## Januar-Barometer (Yale Hirsch)

- Wie der Januar endet, so endet das Jahr
- **Verschärfte Variante:** Erste 5 Handelstage des Januars als Indikator
- Als jährlicher Bias-Filter verwenden (nicht als alleiniges Signal)

---

## Präsidentschaftszyklus (4-Jahres-Zyklus, USA)

| Jahr | Phase | Ø-Rendite kumuliert |
|------|-------|---------------------|
| Vorwahljahr (4) | Stärkste Phase | +217 % |
| Wahljahr (1) | Stimulierung | +224 % |
| Nachwahljahr (2) | Unpopuläre Maßnahmen | +72 % |
| Midterm-Jahr (3) | Schwächste Phase | +63 % |

**Stärkste Periode:** Letztes Quartal des Midterm-Jahres + erstes Quartal des Vorwahljahres

---

## Zyklen-Kombination mit Indikatoren (Bressert)

- Oszillator-Periode = halbe Zykluslänge
  - 20-Tage-Zyklus → 10-Tage-Oszillator
  - 40-Tage-Zyklus → 20-Tage-Oszillator
- MA-Periode = Zykluslänge

---

## Algorithmus-Implikationen

- **28-Tage-Zyklus-Filter:** Kaufsignale bevorzugen wenn Zyklusboden naht
- **Primärzyklus-Filter (9–26 Wochen):** Wochenchart-Trend als übergeordneter Zyklusfilter
- **Saisonale Filter:** Bekannte saisonale Muster als optionalen Filter einbauen
- **Translation-Erkennung:** Zyklus-Gipfel-Position → Bullen-/Bärenmarkt-Heuristik
- **Standard-MA-Perioden sind bereits zyklusoptimiert** → keine weiteren Experimente nötig
