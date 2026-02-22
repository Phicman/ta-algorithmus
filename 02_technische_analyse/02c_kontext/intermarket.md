# Intermarket-Analyse

← [Zurück zur TA-Übersicht](../README.md)

---

## Kernthese (Murphy, Kap. 17)

Alle Finanzmärkte sind miteinander verbunden. Vollständiges Verständnis eines Marktes erfordert Kenntnis der anderen.

**Sequenz:** Dollar → Rohstoffe → Anleihen → Aktien

---

## Die vier zentralen Beziehungen

| Beziehung | Korrelation | Beschreibung |
|-----------|-------------|-------------|
| **Dollar ↔ Rohstoffe** | Invers | Steigender Dollar → Rohstoffpreise fallen |
| **Rohstoffe ↔ Anleihen** | Invers | Steigende Rohstoffe → Inflation → Anleihen fallen |
| **Anleihen ↔ Aktien** | Positiv (normal) | Steigende Anleihen (fallende Zinsen) → Aktien steigen |
| **Deflations-Ausnahme** | Anleihen ↑, Aktien ↓ | Positive Korrelation Anleihen/Aktien bricht zusammen |

### Vollständige Kausalkette

**Inflationär:** Dollar ↓ → Rohstoffe ↑ → Inflation ↑ → Anleihen ↓ → Zinsen ↑ → Aktien ↓

**Deflationär:** Dollar ↑ → Rohstoffe ↓ → Anleihen ↑ → Aktien möglicherweise ↓

---

## Frühindikatoren

| Indikator | Läuft voraus für |
|-----------|-----------------|
| Gold / Goldminen | Goldminen drehen VOR Goldpreis |
| Versorger (Utilities) | Drehen VOR T-Bonds → Frühwarnsystem für Zinsrichtung |
| T-Bond-Futures | Führender Indikator für Aktienmärkte |

---

## Sektorrotation

### Zinssensitive Sektoren (outperformen bei schwachen Rohstoffen)
- Versorger (Utilities)
- Finanzwerte (Financials)
- Konsum-Basistitel (Consumer Staples)

### Inflationssensitive Sektoren (outperformen bei starken Rohstoffen)
- Goldminen
- Energie (Oil & Gas)
- Zykliker (Materials, Industrials)

---

## Dollar & Marktkapitalisierung

| Dollar | Begünstigt |
|--------|-----------|
| Stark | Small-Caps / Inlandswerte (Russell 2000) |
| Schwach | Large-Caps / Multinationale (DJIA, S&P 500) |

---

## Relative Stärke-Analyse (RS-Ratio)

**Konstruktion:** Preisserie A ÷ Preisserie B → Ratio-Chart
- Steigendes Verhältnis = Zähler stärker
- Fallendes Verhältnis = Nenner stärker
- Alle Standard-TA-Tools auf Ratio-Charts anwendbar (Trendlinien, MAs, Formationen)

**Anwendungen:**
- CRB/T-Bond-Ratio für Asset-Klassen-Entscheidung
- Sektoren gegen S&P für Sektorauswahl
- RS-Linie eines Einzelwerts dreht nach oben → frühes Einstiegssignal

---

## Top-Down-Aktienauswahl

1. Übergeordneten Markttrend bestimmen (S&P 500, DAX)
2. Sektoren nach relativer Stärke ranken (RS gegen Index)
3. Stärkste Sektoren auswählen (Intermarket-Kontext berücksichtigen)
4. Einzelwerte mit stärkster RS innerhalb der besten Sektoren
5. Kaufen wenn RS-Linie eines Einzelwerts gerade nach oben dreht

---

## Algorithmus-Implikationen

- **Makro-Filter:** Dollar-Trend und Rohstoff-Trend als übergeordnete Filterebene
- **Sektor-Scoring:** RS-Ratio jedes Sektors vs. Gesamtmarkt berechnen; nur Aktien aus Top-Sektoren scannen
- **Anleihen als Vorläufer:** T-Bond-Trend für übergeordnete Marktrichtung einbeziehen
- **Relative Stärke automatisch berechnen:** Für jeden Titel RS vs. Index; steigende RS = Kaufkandidat
