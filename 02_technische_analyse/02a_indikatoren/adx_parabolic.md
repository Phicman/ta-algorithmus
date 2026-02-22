# ADX / DMI & Parabolic SAR

← [Zurück zur TA-Übersicht](../README.md)

---

## ADX / DMI – Directional Movement Index

### Konstruktion

| Größe | Formel | Bedeutung |
|-------|--------|-----------|
| +DM | Heutiges Hoch − gestriges Hoch (wenn positiv) | Aufwärtsbewegungsstärke |
| −DM | Gestriges Tief − heutiges Tief (wenn positiv) | Abwärtsbewegungsstärke |
| +DI | Geglättetes +DM / ATR × 100 | Stärke der Aufwärtsbewegungen |
| −DI | Geglättetes −DM / ATR × 100 | Stärke der Abwärtsbewegungen |
| ADX | Geglättete abs. Differenz (+DI − −DI) / (+DI + −DI) × 100 | Trendstärke (ohne Richtung) |

---

## ADX-Interpretation (Regime-Filter)

| ADX | Bedeutung | Empfohlene Indikatoren |
|-----|-----------|----------------------|
| < 20, dann **steigend** | Neuer Trend beginnt → Frühsignal | Trendfolgeindikatoren aktivieren |
| > 25, steigend | Trend bestätigt | Trendfolgeindikatoren bevorzugen |
| > 40, dann **fallend** | Trenderschöpfung, Vorsicht | Vorsicht mit neuen Positionen |
| Fallend | Seitwärtsmarkt / Trendabschwächung | Oszillatoren bevorzugen |

> **ADX zeigt NICHT die Richtung, nur die Stärke.**

---

## DI-Handelssignale

| Signal | Bedingung |
|--------|-----------|
| **Kaufsignal** | +DI kreuzt über −DI |
| **Verkaufssignal** | +DI kreuzt unter −DI (= −DI übernimmt Führung) |

**Extreme Point Rule:** Am Kreuzungstag das Extrem markieren (Hoch bei Kauf, Tief bei Verkauf) → nur handeln wenn Kurs dieses Niveau über-/unterschreitet.

---

## Parabolic SAR (Stop and Reverse)

### Konstruktion

- **Aufwärtstrend:** SAR-Punkte erscheinen unterhalb der Kurse (Trailing Stop)
- **Abwärtstrend:** SAR-Punkte erscheinen oberhalb der Kurse
- System ist immer im Markt (long oder short); bei Kurs = SAR → Positionswechsel

**Formel:**
`SARt+1 = SARt + AF × (EP − SARt)`

- EP = Extrempunkt (höchster Kurs im Aufwärtstrend / niedrigster im Abwärtstrend)
- AF = Beschleunigungsfaktor: beginnt bei 0,02; steigt um 0,02 bei jedem neuen EP; Maximum: 0,20

### Eigenschaften

| Marktphase | Verhalten |
|------------|-----------|
| Trendmarkt | Exzellent; präzise Trailing-Stops |
| Seitwärtsmarkt | Versagt; häufige Fehlsignale (~70 % laut Wilder) |

> **Parabolic SAR MUSS mit DMI-Filter kombiniert werden.**

---

## Kombination: Parabolic SAR + DMI

**Regel:** Parabolic SAR nur handeln wenn:
1. DI-Kreuzung in Signalrichtung bestätigt
2. ADX steigt (Trendmarkt bestätigt)

→ Filtert ~70 % der Fehlsignale in Seitwärtsphasen heraus.

---

## Algorithmus-Implikationen

- **ADX als Marktregime-Filter:** Vor jedem Signal ADX-Status prüfen
- **ADX < 20:** Trendfolgesignale unterdrücken; Oszillatoren aktivieren
- **ADX > 25:** Trendfolgesignale bevorzugen
- **ADX > 40:** Vorsicht mit neuen Positionen; mögliche Erschöpfung
- **Parabolic SAR:** Als dynamischen Trailing-Stop im Output anzeigen (nur bei steigendem ADX)
- **DI-Kreuzungen:** Als zusätzliches Trendsignal (objektiv, aber schwächer als Kursformation)
