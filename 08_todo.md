# 08 – TODO & Backlog

← [Zurück zum Index](../claude.md)

---

## Infrastruktur

- [ ] Ticker-Universum festlegen
- [ ] API / Datenquelle wählen und testen
- [ ] Output-Format finalisieren (CSV, JSON, Dashboard?)
- [ ] Backtest-Logik planen (Walk-Forward, In-Sample/Out-of-Sample)
- [ ] Timeframe-Hierarchie definieren (Daily primär, Weekly zur Bestätigung)

---

## Indikatoren implementieren

### Gleitende Durchschnitte
- [ ] SMA, EMA, linear gewichtet implementieren
- [ ] Double-Crossover-Logik (5/20, 10/50, 9/18 Tage)
- [ ] Triple-Crossover-Logik (4/9/18 Tage, Allen-System)
- [ ] Prozentbänder (3 % um 21-Tage, 5 % um 10-Wochen)
- [ ] 4-Wochen-Regel / Price-Channel-Ausbruch (dynamische S/R)
- [ ] Fibonacci-MA-Perioden testen (13 Wochen, 21 Tage, 34, 55)

### Oszillatoren
- [ ] RSI: Formel, Failure Swings, Divergenz, Trendlinien auf RSI
- [ ] Stochastik (langsam): %K/%D-Formel, Extremzonen, Kreuzungssignal
- [ ] Larry Williams %R (invertierte Stochastik)
- [ ] MACD-Histogramm-Wendepunkt-Detektion (Frühwarnsignal)
- [ ] Wochen-MACD als Richtungsfilter für Tages-MACD
- [ ] Momentum-Oszillator (10 + 40 Tage)
- [ ] ROC-Berechnung (Formel: 100 × V/Vx)
- [ ] Nulllinienkreuzung Momentum/ROC als Signal (nur in Trendrichtung)
- [ ] Kombinations-Signal RSI + Stochastik (beide in Extremzone)

### Volumen & Marktbreite
- [ ] OBV-Berechnung + Divergenz-Detektion (OBV vs. Kurs)
- [ ] Blowoff/Selling-Climax-Detektion (hohes Volumen + starke Bewegung)
- [ ] COT-Report-Integration für Futures prüfen
- [ ] Contrary-Opinion-Daten integrieren (Bullish Consensus API prüfen)

### ADX / Parabolic SAR
- [ ] ADX/DMI implementieren: +DI/-DI; Kreuzungssignal mit Extreme-Point-Rule
- [ ] Parabolic SAR: Beschleunigungsfaktor 0,02–0,20; nur bei steigendem ADX ausgeben
- [ ] ADX-Schwellenwerte als Signalfilter (<20 / 20-25 / >25 / >40)

---

## Muster-Scanner implementieren

### Umkehrformationen
- [ ] Kopf-Schulter (bearish + bullish inverse)
- [ ] Fehlgeschlagene KS-Formation erkennen
- [ ] Komplexe KS-Formation
- [ ] Doppeltop / Doppelboden
- [ ] Dreifachtop / Dreifachboden

### Fortsetzungsformationen
- [ ] Symmetrisches Dreieck (Ausbruch zwischen 2/3 und 3/4)
- [ ] Aufsteigendes / Absteigendes Dreieck
- [ ] Flagge / Wimpel (Halbmast-Regel implementieren)
- [ ] Keil-Erkennung (fallend = bullish, steigend = bearish)
- [ ] Rechteck / Trading-Range-Erkennung
- [ ] Broadening-Top-Erkennung (divergierende Trendlinien + steigendes Volumen)

### Weitere Muster
- [ ] Gap-Erkennung (3 Typen: Ausbruch, Fortsetzung, Erschöpfung)
- [ ] Umkehrtag-Erkennung (inkl. Selling Climax)
- [ ] Trendkanal-Erkennung (Basislinie + parallele Rückkehrlinie)
- [ ] Retracement-Berechnung (33/50/66 % + Fibonacci 38/62 %)
- [ ] Speedline-Berechnung (1/3 und 2/3)
- [ ] Measured-Move-Kursziel-Berechnung
- [ ] Fächerprinzip (3-Linien-Sequenz nach Trendbruch)

### Trendlinien & S/R
- [ ] Trendlinien-Ausbruch (3-Prozent-Regel, 2-Tage-Regel)
- [ ] Unterstützung / Widerstand (Role Reversal)
- [ ] Runde Zahlen als psychologische S/R markieren

---

## Candlestick-Erkennung

- [ ] Basis: Hammer, Hanging Man, Doji-Typen, Engulfing, Morning/Evening Star
- [ ] Erweitert: Dark Cloud Cover, Piercing Line, Harami, Shooting Star
- [ ] Drei-Kerzen: Three White Soldiers, Three Black Crows, Abandoned Baby
- [ ] Fortsetzungen: Rising/Falling Three Methods, Tasuki Gap
- [ ] **Morris-Filter implementieren:** Stochastik %D > 80 / < 20 als Pflicht-Bedingung

---

## Kontext-Module

- [ ] Fibonacci-Retracements (38/50/62 %) automatisch von jedem Swing-Hoch/-Tief
- [ ] Fibonacci-Zeitziele (13, 21, 34, 55, 89 Tage vom letzten Drehpunkt)
- [ ] Elliott-Wellen-Modul (Phase 2): Dreieck als Welle-4-Erkennung
- [ ] Welle-4-Unterstützungszone markieren
- [ ] Langfrist-Top-Down-Filter: Wochenchart-Trend als übergeordneten Filter
- [ ] Saisonale Filter (Jahresmonat als Gewichtungsfaktor)
- [ ] Präsidentschaftszyklus-Filter (US-Markt)
- [ ] 28-Tage-Zyklus-Filter

---

## Signal-Logik & Output

- [ ] Bestätigungs-/Divergenz-Logik zwischen Indikatoren
- [ ] Kursziel-Anpassung an nahe S/R-Niveaus (automatische Korrektur)
- [ ] RS-Ratio-Berechnung (Kurs / Indexkurs) für jeden Titel
- [ ] Sektor-Scoring-Modul (RS jedes Sektors vs. Gesamtmarkt)
- [ ] Intermarket-Makro-Filter (Dollar + CRB + T-Bond)
- [ ] Stop-Distanz automatisch berechnen (Chart-Stop)
- [ ] Chance/Risiko-Filter: < 3:1 CRV → SCHWACH markieren
- [ ] Trailing-Stop-Ausgabe (Parabolic-SAR-Wert im Output)

---

## P&F-Charts

- [ ] P&F-Chart-Generierung aus OHLC-Daten (3-Punkt-Umkehr, Kästchengröße auto)
- [ ] Einfache Signale (B-1/S-1) automatisch erkennen
- [ ] 45-Grad-Trendlinien implementieren
- [ ] Horizontal Count Kursziel berechnen

---

## Erledigt ✅

- [x] Kapitel 3–17 aus Murphy einarbeiten (Kap. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)
- [x] RSI vollständig dokumentieren (Failure Swings, Divergenz, 50er-Linie)
- [x] Stochastik vollständig dokumentieren (langsam, %K/%D, Morris-Filter)
- [x] MACD vollständig dokumentieren (Histogramm-Wendepunkte, Wochen-Filter)
- [x] Contrary-Opinion-Logik einarbeiten
- [x] Candlestick-Charts vollständig einarbeiten (Kap. 12)
- [x] Elliott-Wellen-Theorie einarbeiten (Kap. 13)
- [x] Zeitzyklen einarbeiten (Kap. 14)
- [x] ADX/DMI, Parabolic SAR dokumentieren (Kap. 15)
- [x] Geldmanagement & Handelstaktiken dokumentieren (Kap. 16)
- [x] Intermarket-Analyse dokumentieren (Kap. 17)
- [x] Wissensbasis in modulare Dateistruktur aufgeteilt
