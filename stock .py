import yfinance as yf
from tabulate import tabulate

# Portfolio stored as dictionary: symbol -> shares
portfolio = {}

def add_stock(symbol, shares):
    symbol = symbol.upper()
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares
    print(f"✅ Added {shares} shares of {symbol}")

def remove_stock(symbol):
    symbol = symbol.upper()
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"❌ Removed {symbol} from portfolio")
    else:
        print("⚠️ Stock not found in portfolio")

def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    if data.empty:
        return None
    price = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = price - prev_close
    percent_change = (change / prev_close) * 100 if prev_close else 0
    return {
        "symbol": symbol,
        "price": price,
        "change": change,
        "percent_change": percent_change
    }

def display_portfolio():
    table = []
    total_value = 0

    for symbol, shares in portfolio.items():
        stock = get_stock_data(symbol)
        if stock:
            value = stock['price'] * shares
            total_value += value
            table.append([
                symbol,
                shares,
                f"${stock['price']:.2f}",
                f"${stock['change']:.2f}",
                f"{stock['percent_change']:.2f}%",
                f"${value:.2f}"
            ])
        else:
            table.append([symbol, shares, "N/A", "N/A", "N/A", "N/A"])

    print(tabulate(table, headers=["Symbol", "Shares", "Price", "Change", "% Change", "Value"], tablefmt="pretty"))
    print(f"\n📊 Total Portfolio Value: ${total_value:.2f}\n")

def main():
    while True:
        print("\n--- Stock Portfolio Tracker ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Show Portfolio")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            symbol = input("Enter stock symbol (e.g. AAPL): ")
            shares = int(input("Enter number of shares: "))
            add_stock(symbol, shares)

        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ")
            remove_stock(symbol)

        elif choice == "3":
            display_portfolio()

        elif choice == "4":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
