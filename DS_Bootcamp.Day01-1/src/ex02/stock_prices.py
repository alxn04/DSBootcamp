import sys


def find_price(name):
    price = 0
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
        if key_company.lower() == name.lower():
            company = COMPANIES[key_company]
            for key_stock in STOCKS:
                if key_stock == company:
                    price = STOCKS[key_stock]
    return price


def main():
    try:
        if len(sys.argv) == 2:
            price = find_price(sys.argv[1])
            print(price) if price else print("Unknown company")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
