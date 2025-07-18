import requests
from bs4 import BeautifulSoup
import os

LINE_ACCESS_TOKEN = os.getenv("LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

TCG_URL = "https://www.pokemoncenter.com/category/trading-card-game"

def get_in_stock_tcg():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(TCG_URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    products = soup.select("li.product-grid-tile")
    found = []

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

def send_line_notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)

if __name__ == "__main__":
    restocked_items = get_in_stock_tcg()
    if restocked_items:
        msg = "🚨 TCG Product(s) Restocked!\n\n" + "\n\n".join(restocked_items)
        send_line_notify(msg)
    else:
        print("No restocks found.")

