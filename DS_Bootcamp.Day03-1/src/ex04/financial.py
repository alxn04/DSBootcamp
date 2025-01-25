import re
import sys
import time

import requests
from bs4 import BeautifulSoup


def get_response(ticker):
    html_content = ""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    path = f"https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker}"
    response = requests.get(path, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        if "noData yf-wnifss" in html_content:
            raise Exception("Unknown ticker")
    else:
        raise requests.RequestException(f"Error HTTP request: {e}")
    return html_content


def parse_page(html, breakdown):
    soup = BeautifulSoup(html, "html.parser")
    breakdowns = soup.find_all("div", class_="row lv-0 yf-t22klz")
    breakdown_flag = 0
    res = []
    for item in breakdowns:
        title = item.find("div", class_="rowTitle yf-t22klz").text
        if title == breakdown:
            breakdown_flag = 1
            res.append(title)
            stats = item.find_all("div", class_=re.compile(r"column yf-t22klz( alt)?"))
            for stat in stats:
                res.append(stat.text.strip(" "))
            print(tuple(res))
            break
    if not breakdown_flag:
        raise Exception("Breakdown or ticker not found")
    return tuple(res)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 3:
            breakdown = sys.argv[2]
            ticker = sys.argv[1]
            path = f"https://finance.yahoo.com/quote/{ticker}/financials/?p={ticker}"
        else:
            raise Exception(
                "Incorrect count of arguments. Try [py_script] [ticker] [breakdown]"
            )
        html_content = get_response(ticker)
        # time.sleep(5)
        parse_page(html_content, breakdown)

    except Exception as e:
        print(f"Error: {e}")
