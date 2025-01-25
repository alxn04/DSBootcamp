import sys


def find_ticker(name):
    price = 0
    company = ""
    COMPANIES = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Netflix": "NFLX",
        "Tesla": "TSLA",
        "Nokia": "NOK",
    }

    STOCKS = {
        "AAPL": 287.73,
        "MSFT": 173.79,
        "NFLX": 416.90,
        "TSLA": 724.88,
        "NOK": 3.37,
    }
    for key_company in COMPANIES:
        if COMPANIES[key_company].lower() == name.lower():
            company = key_company
            for key_stock in STOCKS:
                if key_stock.lower() == name.lower():
                    price = STOCKS[key_stock]
    return [company, price]


def main():
    try:
        if len(sys.argv) == 2:
            ticker = find_ticker(sys.argv[1])
            print(ticker[0], ticker[1]) if ticker[1] else print("Unknown ticker")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
