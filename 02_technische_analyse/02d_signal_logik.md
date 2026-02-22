# Signal-Logik & Filterregeln

← [Zurück zur TA-Übersicht](../README.md)

---

## Signal-Entscheidungsbaum

```
WENN [Muster erkannt]
  UND [ADX steigt > 25]              ← Trendmarkt bestätigt
  UND [Volumen bestätigt Ausbruch]
  UND [RSI nicht extrem überkauft/verkauft (außer bei Divergenz)]
  UND [Schlusskurs > Ausbruchsniveau (nicht nur Intraday)]
  UND [Signal in Richtung des übergeordneten Wochenchart-Trends]
DANN Signal = BUY / SELL / WATCH
     Stärke = STARK / MITTEL / SCHWACH
```

---

## Stärke-Bewertung

| Stärke | Kriterien |
|--------|-----------|
| **STARK** | Muster + Volumenbestätigung + Indikator-Bestätigung |
| **MITTEL** | Muster + ein weiteres Kriterium |
| **SCHWACH** | Muster alleine / kein Volumen / Gegentrend |

---

## Signalfilter (Priorität absteigend)

### 1. Trendrichtungs-Filter
- Aufwärtstrend: Höhere Hochs UND höhere Tiefs
- Abwärtstrend: Niedrigere Hochs UND niedrigere Tiefs
- **Wochen-MACD als übergeordneter Trendfilter:** Tagessignale nur in Richtung des Wochen-MACD

### 2. ADX-Regime-Filter
| ADX | Aktion |
|-----|--------|
| < 20 | Trendfolgesignale unterdrücken; Oszillatoren bevorzugen |
| 20–25 | Schwacher Trend; Signale mit Vorsicht |
| > 25 steigend | Trendfolgesignale bevorzugen |
| > 40 fallend | Vorsicht; mögliche Trenderschöpfung |

### 3. Volumen-Bestätigung
- Ausbrüche: Volumen über dem Durchschnitt (bestätigt Signal)
- Rückkehrbewegungen: Niedriges Volumen = normales Zeichen
- OBV-Divergenz als Frühwarnung prüfen

### 4. Timeframe-Hierarchie (Top-Down)
- **Monatschart:** Primärtrend bestimmen
- **Wochenchart:** Sekundärtrend; Signalrichtung filtern
- **Tageschart:** Primärer Signal-Timeframe
- **Intraday:** Entry/Exit-Feintuning (optional)

### 5. Candlestick Morris-Filter
- Candlestick-Signal nur ausgeben wenn Stochastik-%D > 80 oder < 20
- Bei neutralem %D → Formation ignorieren

### 6. Kombinations-Signal (verstärkt Signal)
- RSI + Stochastik beide in Extremzone → höhere Signalqualität
- Muster + Fibonacci-Level koinzidieren → höhere Wahrscheinlichkeit

---

## Filterregeln für Formationen

| Regel | Beschreibung |
|-------|-------------|
| **3-Prozent-Regel** | Schlusskurs mind. 3 % jenseits der Trendlinie/Formation |
| **2-Tage-Regel** | Kurse an 2 aufeinanderfolgenden Tagen jenseits des Niveaus |
| **Freitags-Schluss** | Wochensignal erfordert Freitags-Schlusskurs jenseits der Linie |

---

## Chance/Risiko-Verhältnis (CRV)

- **Minimum CRV:** 3:1 (Kursziel mindestens 3× so weit wie Stop-Distanz)
- Signale mit < 3:1 CRV → automatisch als SCHWACH markieren oder verwerfen
- Kursziel-Methoden: Formationshöhe projizieren + Fibonacci-Niveaus + S/R prüfen

---

## Prozentualen Korrekturniveaus als S/R

| Niveau | Bedeutung |
|--------|-----------|
| 33 % | Minimum-Korrektur; erste Unterstützung |
| 50 % | Standard; häufigstes Umkehrniveau |
| 66 % | Maximum; Bruch = vollständige Trendumkehr wahrscheinlich |
| 38,2 % / 61,8 % | Fibonacci-Varianten; weit verbreitet |

---

## Wichtige Grundsätze (Murphy)

- **Trend ist dein Freund** – Signale IN Trendrichtung deutlich höher gewichten
- **Bestätigungsprinzip** – Mehrere Indikatoren in gleicher Richtung = höhere Signalqualität
- **Divergenzprinzip** – Gegenläufige Indikatoren = Warnsignal für Trendwechsel
- **Chartformationen sind Tendenzen, keine Gesetze** – immer mit Wahrscheinlichkeiten arbeiten
- **Voraussetzung für Umkehrformation** – vorhergehender Trend muss existieren
- **Bestätigungs-Volumen** – Bodenformationen brauchen zwingend Volumenanstieg beim Ausbruch

---

## Akademische Grundlagen & Gewichtungsprinzipien *(Han, Liu, Zhou, Zhu 2022)*

> Quelle: *Technical Analysis in the Stock Market: A Review* – akademischer Review-Artikel, der Studien von 1897 bis 2020 auswertet.

### Prinzip 1: Kombinations-Signale sind dem Einzelsignal überproportional überlegen

Die akademische Evidenz zeigt, dass einfache Einzelsignale (MA-Crossover, Trading Range Breakout) auf Marktebene seit 1987 keine konsistente Profitabilität mehr liefern. Was weiterhin funktioniert, sind **Kombinationen mehrerer unabhängiger Signalquellen**.

Der Mehrwert entsteht nicht linear (2 Signale = doppelt so gut), sondern überproportional: Zwei unabhängige Signale in dieselbe Richtung eliminieren gemeinsam einen Großteil der Fehlsignale, die jedes Signal alleine noch produzieren würde.

**Konsequenz für die Stärke-Bewertung:**
- STARK (Muster + Volumen + Indikator) ist nicht dreimal besser als SCHWACH – es ist qualitativ anders
- Einzelsignale ohne Bestätigung sollen im Score niedrig oder gar nicht gewichtet werden
- Die Kombinations-Ebene (Filter 6) ist damit wichtiger als jeder Einzelfilter

### Prinzip 2: Multi-Horizont-Konsistenz erhöht die Signalqualität

Der empirisch stärkste MA-basierte Ansatz (Trend-Faktor, Han/Zhou/Zhu 2016, Sharpe Ratio 0,46) verwendet MAs über viele Zeithorizonte gleichzeitig. Übereinstimmung über mehrere Horizonte ist ein stärkeres Signal als ein Einzelsignal auf einem Timeframe.

**Konsequenz für die Timeframe-Hierarchie (Filter 4):**
- Übereinstimmung Daily + Weekly ist ein Pflichtkriterium für STARK
- Übereinstimmung Daily + Weekly + Monthly ist ein Signal-Verstärker
- Ein Tagessignal gegen den Wochenchart-Trend bleibt maximal SCHWACH, unabhängig von der Indikatorlage

### Prinzip 3: Publication Effect – nicht-triviale Kriterien bevorzugen

Weitverbreitete, einfache Signale (klassische MA-Crossover, bekannte Chartformationen alleine) werden vom Markt zunehmend eingepreist. Weniger offensichtliche Kriterien behalten länger ihre Wirksamkeit.

**Konsequenz für die Gewichtung:**

| Kriterium | Bewertung |
|-----------|-----------|
| Einfacher MA-Crossover alleine | Nicht als eigenständiges Signal werten |
| Klassisches Chartmuster alleine | Maximal SCHWACH |
| Divergenz (RSI/MACD vs. Kurs) | Höher gewichten – weniger trivial, schwerer zu arbitrieren |
| Volumenbestätigung | Höher gewichten – objektiv, weniger subjektiv interpretierbar |
| ADX-Regime-Filter | Höher gewichten – filtert Fehlsignale strukturell heraus |
| Multi-Horizont-Konsistenz | Höher gewichten – empirisch gut belegt |

---

## Ergänzende Evidenz: Buy/Sell-Asymmetrie *(Wong, Manzur, Chew 2002)*

> Quelle: *How Rewarding Is Technical Analysis? Evidence From Singapore Stock Market*

Über alle getesteten Indikatoren (MA, Dual-MA, Triple-MA, RSI) hinweg sind **Buy-Signale konsistent stärker und statistisch signifikanter als Sell-Signale**. Sell-Signale waren in mehreren Subperioden und Indikatorvarianten statistisch insignifikant, während Buy-Signale robust blieben.

Dies bestätigt zwei Designentscheidungen des Algorithmus:

1. **Fokus auf Kaufsignale im aktuellen Scope** ist empirisch gut begründet – Buy-Signale sind das verlässlichere Ende der technischen Analyse
2. **ADX als Pflicht-Filter für RSI** ist empirisch notwendig: RSI in Trendmärkten ohne ADX-Filter führt zu gemischten Ergebnissen; mit Regime-Filter (ADX < 25 für Oszillator-Signale) verbessern sich die Resultate strukturell

Zudem gilt: Die Qualität von MA-Signalen verbessert sich, je länger der Beobachtungszeitraum nach dem Signal ist. Das stärkt die Ausrichtung auf **positionsorientiertes Trading** (Tage bis Wochen) gegenüber sehr kurzfristigen Signalen.
