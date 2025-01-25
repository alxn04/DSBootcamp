import sys


def print_info(item):
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
        if key_company.lower() == item.lower():
            company = COMPANIES[key_company]
            for key_stock in STOCKS:
                if key_stock.lower() == company.lower():
                    print(f"{item.capitalize()} stock price is {STOCKS[key_stock]}")
                    return
    for key_stock in STOCKS:
        if key_stock.lower() == item.lower():
            stock = key_stock
            for key_company in COMPANIES:
                if COMPANIES[key_company].lower() == stock.lower():
                    print(f"{item.upper()} is a ticker symbol for {key_company}")
                    return
    print(f"{item} is an unknown company or an unknown ticker symbol")


def main():
    try:
        if len(sys.argv) == 2:
            stroke_list = [i.strip(" ") for i in sys.argv[1].split(",")]
            is_empty = [1 if i == "" else 0 for i in stroke_list]
            if sum(is_empty) == 0:  # нет подряд идущих запятых
                for item in stroke_list:
                    print_info(item)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
