"""
Handelsalgorithmus – Einstiegspunkt
────────────────────────────────────
Führt die TA-Analyse für alle Ticker aus tickers.txt durch.

Verwendung:
    python main.py
"""

from src.data.feature_store import get_features
from src.data.price_fetcher import load_tickers
from src.ta.TA_run import run, print_signal


def main():
    tickers = load_tickers()
    print(f"Analysiere {len(tickers)} Ticker...\n")

    for ticker in tickers:
        df = get_features(ticker)
        result = run(df, ticker=ticker)
        print_signal(result)


if __name__ == "__main__":
    main()
