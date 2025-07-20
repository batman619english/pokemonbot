import requests
from bs4 import BeautifulSoup

URL = "https://www.bestbuy.com/site/searchpage.jsp?st=pokemon+cards"

def check_bestbuy():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = []

    cards = soup.select(".sku-item")
    for card in cards:
        title_tag = card.select_one(".sku-header a")
        status_tag = card.select_one(".fulfillment-fulfillment-summary")

        if not title_tag or not status_tag:
            continue

        title = title_tag.text.strip()
        link = "https://www.bestbuy.com" + title_tag["href"]

        if "sold out" not in status_tag.text.lower():
            items.append(f"{title}\n{link}")

    return items

