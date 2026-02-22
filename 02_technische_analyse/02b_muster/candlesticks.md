# Japanische Candlestick-Charts

← [Zurück zur TA-Übersicht](../README.md)

---

## Grundlagen

**Konstruktion:** Open, High, Low, Close
- **Weißer/Leerer Körper:** Schlusskurs > Eröffnungskurs (bullish)
- **Schwarzer/Gefüllter Körper:** Schlusskurs < Eröffnungskurs (bearish)
- **Dochte / Schatten:** Linien ober- und unterhalb des Körpers = High und Low

**Voraussetzung:** Trendrichtung VOR der Formation bestimmen (~10 Perioden)
- Bullishe Umkehrformation nur nach Abwärtstrend möglich
- Bearishe Umkehrformation nur nach Aufwärtstrend möglich

---

## Einzel-Kerzen

| Muster | Typ | Bedingung |
|--------|-----|-----------|
| **Hammer** | Bullish | Langer unterer Schatten (≥2× Körper), kleiner Körper oben; nach Abwärtstrend |
| **Hanging Man** | Bearish | Wie Hammer, aber nach Aufwärtstrend; Bestätigung nötig |
| **Gravestone Doji** | Bearish | Langer oberer Schatten, kein unterer; Open ≈ Close ≈ Low |
| **Dragonfly Doji** | Bullish | Langer unterer Schatten, kein oberer; Open ≈ Close ≈ High |
| **Long-legged Doji** | Neutral/Umkehr | Lange Schatten oben und unten; Open ≈ Close; starke Unentschlossenheit |
| **Shooting Star** | Bearish | Langer oberer Schatten, kleiner Körper unten; nach Aufwärtstrend |
| **Inverted Hammer** | Bullish | Gleiche Form wie Shooting Star, aber nach Abwärtstrend; Bestätigung zwingend |
| **Spinning Top** | Neutral | Kleiner Körper, Schatten länger als Körper; Unentschlossenheit |
| **Belt Hold (Bullish)** | Bullish | Langer weißer Körper; Eröffnung = Tief |
| **Belt Hold (Bearish)** | Bearish | Langer schwarzer Körper; Eröffnung = Hoch |

---

## Zwei-Kerzen-Muster

| Muster | Typ | Bedingung |
|--------|-----|-----------|
| **Bullish Engulfing** | Bullish | Weißer Körper umschließt vollständig vorherigen schwarzen Körper; nach Abwärtstrend |
| **Bearish Engulfing** | Bearish | Schwarzer Körper umschließt vollständig vorherigen weißen Körper; nach Aufwärtstrend |
| **Dark Cloud Cover** | Bearish | Langer weißer Körper + zweite Kerze öffnet über Vortages-Hoch, schließt unter Körpermitte |
| **Piercing Line** | Bullish | Langer schwarzer Körper + zweite Kerze öffnet unter Vortages-Tief, schließt über Körpermitte |
| **Harami (Bullish)** | Bullish | Kleiner weißer Körper vollständig im vorherigen schwarzen Körper |
| **Harami (Bearish)** | Bearish | Kleiner schwarzer Körper vollständig im vorherigen weißen Körper |
| **Harami Cross** | Stärker | Zweiter Körper = Doji → stärkeres Signal als normales Harami |
| **Meeting Lines** | Bullish/Bearish | Gleicher Schlusskurs an beiden Tagen trotz gegenläufiger Körper |

---

## Drei-Kerzen-Muster

| Muster | Typ | Bedingung |
|--------|-----|-----------|
| **Morning Star** | Bullish | Langer schwarzer Körper + kleiner Körper/Doji (Gap) + langer weißer Körper |
| **Evening Star** | Bearish | Langer weißer Körper + kleiner Körper/Doji (Gap) + langer schwarzer Körper |
| **Three White Soldiers** | Bullish | Drei aufsteigende lange weiße Kerzen; starkes Umkehrsignal nach Abwärtstrend |
| **Three Black Crows** | Bearish | Spiegelbild; starkes Warnsignal an Marktgipfeln |
| **Abandoned Baby** | Sehr stark | Doji mit Gap auf BEIDEN Seiten; extrem selten |
| **Tri-Star** | Sehr stark | Drei aufeinanderfolgende Dojis; mittlerer mit Gap; extrem selten |

---

## Fortsetzungsformationen (Candlestick)

| Formation | Kerzen | Typ | Beschreibung |
|-----------|--------|-----|--------------|
| Rising Three Methods | 5 | Bullish | Langer weißer Körper + 3 kleine schwarze (innerhalb) + langer weißer Abschluss |
| Falling Three Methods | 5 | Bearish | Spiegelbild im Abwärtstrend |
| Upside Tasuki Gap | 3 | Bullish | Gap + zweite Kerze in Trendrichtung + dritte schließt Gap teilweise |
| Downside Tasuki Gap | 3 | Bearish | Spiegelbild |
| On Neck Line | 2 | Bearish | Zweite Kerze schließt nahe Tief der ersten |
| Three Line Strike | 4 | Fortsetzung | 3 Kerzen in Trendrichtung + große Gegenkerze |
| Side by Side White Lines | 3 | Bullish | Gap + zwei weiße Kerzen mit gleichem Open |

---

## Morris-Filter (Candle Pattern Filtering)

> **Algorithmisch wichtig (Greg Morris, 1991)**

**Regel:** Candlestick-Formationen NUR beachten, wenn gleichzeitig:
- Stochastik-%D > 80 (überkauft) für bearishe Muster
- Stochastik-%D < 20 (überverkauft) für bullishe Muster

Bei neutralem %D → Formation ignorieren.

Gleiche Filtertechnik auch mit RSI, CCI, Williams %R möglich.

**Fazit:** Eliminiert Früh- und Fehlsignale erheblich; verbessert Trefferquote signifikant.

---

## Implementierungshinweise

- ~40 bekannte Candlestick-Umkehrformationen
- Immer mit anderen technischen Signalen kombinieren (S/R-Niveau, RSI, Volumen)
- Auf Tages- und Wochencharts einsetzbar
- Candlestick-Signale zeitlich oft VOR anderen kursbasierten Indikatoren
- Als Bestätigung anderer technischer Signale am wirkungsvollsten
