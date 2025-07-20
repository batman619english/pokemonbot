import requests
from bs4 import BeautifulSoup

URLS = [
    "https://www.pokemoncenter.com/category/trading-card-game",
    "https://www.pokemoncenter.com/category/new-releases",
    "https://www.pokemoncenter.com/category/trading-card-game/elite-trainer-boxes",
    "https://www.pokemoncenter.com/category/trading-card-game/booster-packs-boxes"
]

def check_pokemoncenter():
    headers = {"User-Agent": "Mozilla/5.0"}
    found = []

    for url in URLS:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        products = soup.select("li.product-grid-tile")

        for product in products:
            title_tag = product.select_one("a[data-productname]")
            stock_tag = product.select_one(".product-availability-message")

            if not title_tag:
                continue

            title = title_tag["data-productname"].strip()
            link = "https://www.pokemoncenter.com" + title_tag["href"]

            if not stock_tag or "out of stock" not in stock_tag.text.lower():
                found.append(f"{title}\n{link}")

    return found

