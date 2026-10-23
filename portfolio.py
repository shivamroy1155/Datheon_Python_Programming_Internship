"""Stock Portfolio Performance Tracker.
Install dependency: python -m pip install yfinance
Run: python portfolio.py

Fetches the latest available quote from Yahoo Finance when available, calculates
portfolio returns, and appends timestamped records to portfolio_summary.csv.
Data availability/timing depends on the provider. Educational use only.
"""
import csv
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path(__file__).with_name("portfolio_summary.csv")


def positive_number(prompt):
    while True:
        try:
            value = float(input(prompt).strip().replace(",", ""))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a number greater than zero, e.g. 125.50.")


def latest_price(ticker):
    import yfinance as yf
    stock = yf.Ticker(ticker)
    price = stock.fast_info.get("last_price")
    if price is None:
        history = stock.history(period="5d", interval="1d")
        if history.empty:
            raise ValueError(f"No price data found for {ticker}.")
        price = history["Close"].dropna().iloc[-1]
    price = float(price)
    if price <= 0:
        raise ValueError(f"Invalid price returned for {ticker}.")
    return price


def make_position(ticker, buy, quantity, current):
    invested = buy * quantity
    value = current * quantity
    pnl = value - invested
    return {
        "ticker": ticker, "buy_price": round(buy, 4),
        "quantity": round(quantity, 4), "current_price": round(current, 4),
        "invested": round(invested, 2), "market_value": round(value, 2),
        "profit_loss": round(pnl, 2),
        "return_pct": round(pnl / invested * 100, 2),
    }


def append_csv(positions):
    fields = ["timestamp", "ticker", "buy_price", "quantity", "current_price",
              "invested", "market_value", "profit_loss", "return_pct"]
    has_data = OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with OUTPUT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if not has_data:
            writer.writeheader()
        for position in positions:
            writer.writerow({"timestamp": timestamp, **position})


def main():
    print("\n=== Stock Portfolio Performance Tracker ===")
    print("Examples: AAPL (US), INFY.NS or TCS.NS (India)")
    print("Prices are the latest available from Yahoo Finance, if provided.")
    positions = []

    while True:
        ticker = input("\nTicker, or DONE to finish: ").strip().upper()
        if ticker == "DONE":
            break
        if not ticker or not all(c.isalnum() or c in ".-^=" for c in ticker):
            print("Invalid ticker format.")
            continue

        buy = positive_number("Purchase price per share: ")
        quantity = positive_number("Number of shares: ")
        print(f"Fetching latest available price for {ticker}...")
        try:
            current = latest_price(ticker)
        except ImportError:
            print("Install the required package: python -m pip install yfinance")
            return
        except Exception as error:
            print(f"Could not fetch price: {error}")
            if input("Enter price manually instead? (y/n): ").strip().lower() == "y":
                current = positive_number("Current price per share: ")
            else:
                print("Holding skipped.")
                continue

        positions.append(make_position(ticker, buy, quantity, current))
        print(f"Added {ticker} at price {current:.2f}")

    if not positions:
        print("No holdings entered; nothing saved.")
        return

    invested = sum(p["invested"] for p in positions)
    value = sum(p["market_value"] for p in positions)
    pnl = value - invested
    return_pct = pnl / invested * 100 if invested else 0

    print("\n" + "-" * 90)
    print(f"{'TICKER':<14}{'BUY':>10}{'QTY':>10}{'LATEST':>12}"
          f"{'VALUE':>12}{'P/L':>12}{'RETURN':>12}")
    print("-" * 90)
    for p in positions:
        print(f"{p['ticker']:<14}{p['buy_price']:>10.2f}{p['quantity']:>10.2f}"
              f"{p['current_price']:>12.2f}{p['market_value']:>12.2f}"
              f"{p['profit_loss']:>12.2f}{p['return_pct']:>11.2f}%")
    print("-" * 90)
    print(f"Total invested: {invested:,.2f}")
    print(f"Current value:  {value:,.2f}")
    print(f"Total P/L:      {pnl:,.2f} ({return_pct:.2f}%)")

    try:
        append_csv(positions)
        print(f"\nSaved results to: {OUTPUT_FILE}")
    except OSError as error:
        print(f"Could not write CSV: {error}")


if __name__ == "__main__":
    main()
