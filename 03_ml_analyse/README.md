# 03 – ML-Analyse

← [Zurück zum Index](../claude.md)

---

## Modulübersicht

| Untermodul | Datei | Inhalt |
|------------|-------|--------|
| Modelle | [03a_modelle/](./03a_modelle/) | Algorithmen & ML-Methoden je Quelle |
| Features | [03b_features/](./03b_features/) | Feature Engineering, Input-Aufbereitung |
| Signal-Logik | [03c_signal_logik.md](./03c_signal_logik.md) | Score-Berechnung, Schwellenwerte, Integration |
| Backtesting | [03d_backtesting.md](./03d_backtesting.md) | Evaluierungsmetriken, Validierungsdesign |

---

## Methoden-Übersicht

| Methode | Kategorie | Datei | Quelle | Status |
|---------|-----------|-------|--------|--------|
| DTW Generic Pattern Recognition | Ähnlichkeitsbasiert | [03a_modelle/dtw_generic_pattern.md](./03a_modelle/dtw_generic_pattern.md) | Tsinaslanidis & Guijarro (2021) | ✅ Dokumentiert |
| FFNN Volume-Profile Klassifikation | Feature-basiert (NN) | [03a_modelle/ffnn_volume_profile.md](./03a_modelle/ffnn_volume_profile.md) | Serafini (2019) | ✅ Dokumentiert |
| PRML Candlestick + Random Forest | Feature-basiert (Ensemble) | [03a_modelle/prml_candlestick_rf.md](./03a_modelle/prml_candlestick_rf.md) | Lin et al. (2021) | ✅ Dokumentiert |

---

## Kernerkenntnis (Modulebene)

Das ML-Modul kombiniert **ähnlichkeitsbasierte und feature-basierte Mustererkennung** — kein klassisches regelbasiertes Supervised Learning.

| Ansatz | Methode | Grundlage | Modell |
|--------|---------|-----------|--------|
| Ähnlichkeitsbasiert | DTW Generic Pattern | Historische Preissequenz-Ähnlichkeit | UCR Suite / stumpy |
| Feature-basiert (NN) | FFNN Volume-Profile | Strukturelle Volumen-Features je Kerze | FFNN / MLP |
| Feature-basiert (Ensemble) | PRML Candlestick | Shape + Loc + 9 TA-Indikatoren je Kerze | Random Forest |

Anstatt bekannte TA-Muster zu codieren, leiten diese Methoden Handelssignale aus **historischem Nachfolgeverhalten** (DTW), **strukturellen Volumenmustern** (FFNN) oder **formal klassifizierten Candlestick-Kontexten** (PRML/RF) ab.

Diese Philosophie ist **komplementär zum TA-Modul**:

| Aspekt | TA-Modul | ML-Modul |
|--------|----------|----------|
| Grundlage | Regelbasiert (Indikatoren) | Datengetrieben (Ähnlichkeit / Modell) |
| Musterdefinition | Vorab kodiert (ADX, RSI, etc.) | Generisch / gelernt |
| Lernfähigkeit | Statisch | Implizit oder explizit |
| Fehlersignal-Schutz | Regime-Filter (ADX) | Consensus-Voting / Modell-Konfidenz |

---

## Implementierungsstand

| Datei | Status |
|-------|--------|
| Code-Implementierung | 🔲 Ausstehend |
| Backtesting-Framework | 🔲 Ausstehend |
| Feature Store Integration | 🔲 Ausstehend |
