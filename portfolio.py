"""Stock Portfolio Performance Tracker.
Run: python portfolio.py

Enter the latest prices you have checked from a trusted market source.
This version calculates returns and logs results to portfolio_summary.csv;
it does not fetch live prices automatically.
"""
import csv
from datetime import datetime
from pathlib import Path

OUTPUT_FILE = Path(__file__).with_name("portfolio_summary.csv")


def ask_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt).strip().replace(",", ""))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid number greater than zero, e.g. 125.50.")


def calculate_position(ticker, buy_price, quantity, current_price):
    invested = buy_price * quantity
    market_value = current_price * quantity
    profit_loss = market_value - invested
    return {
        "ticker": ticker,
        "buy_price": buy_price,
        "quantity": quantity,
        "current_price": current_price,
        "invested": invested,
        "market_value": market_value,
        "profit_loss": profit_loss,
        "return_pct": profit_loss / invested * 100,
    }


def save_csv(positions):
    fields = [
        "timestamp", "ticker", "buy_price", "quantity", "current_price",
        "invested", "market_value", "profit_loss", "return_pct",
    ]
    file_exists = OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    with OUTPUT_FILE.open("a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        if not file_exists:
            writer.writeheader()
        for position in positions:
            writer.writerow({"timestamp": timestamp, **position})


def main():
    print("\n=== Stock Portfolio Performance Tracker ===")
    print("Use latest prices checked from a trusted market source.")
    print("Note: this version does not fetch live quotes automatically.")
    positions = []

    while True:
        ticker = input("\nTicker (e.g. INFY.NS) or DONE to finish: ").strip().upper()
        if ticker == "DONE":
            break
        if not ticker or not all(char.isalnum() or char in ".-^" for char in ticker):
            print("Enter a valid ticker symbol, or DONE.")
            continue

        buy_price = ask_positive_number("Buy price per share: ")
        quantity = ask_positive_number("Quantity of shares: ")
        current_price = ask_positive_number("Latest/current price per share: ")
        positions.append(calculate_position(ticker, buy_price, quantity, current_price))
        print(f"Added {ticker}.")

    if not positions:
        print("No holdings entered; nothing to save.")
        return

    total_invested = sum(item["invested"] for item in positions)
    total_value = sum(item["market_value"] for item in positions)
    total_pnl = total_value - total_invested

    print("\n" + "-" * 82)
    print(f"{'TICKER':<14}{'BUY':>10}{'QTY':>10}{'CURRENT':>12}{'VALUE':>12}{'P/L':>12}{'RETURN':>10}")
    print("-" * 82)
    for item in positions:
        print(
            f"{item['ticker']:<14}{item['buy_price']:>10.2f}{item['quantity']:>10.2f}"
            f"{item['current_price']:>12.2f}{item['market_value']:>12.2f}"
            f"{item['profit_loss']:>12.2f}{item['return_pct']:>9.2f}%"
        )
    print("-" * 82)
    print(f"Total invested: {total_invested:,.2f}")
    print(f"Current value:  {total_value:,.2f}")
    print(f"Total P/L:      {total_pnl:,.2f} ({total_pnl / total_invested * 100:.2f}%)")

    try:
        save_csv(positions)
        print(f"\nSaved results to: {OUTPUT_FILE}")
    except OSError as error:
        print(f"Could not save CSV: {error}")


if __name__ == "__main__":
    main()
