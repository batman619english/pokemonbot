import requests
from bs4 import BeautifulSoup

LINE_CHANNEL_ACCESS_TOKEN = "FMdc1Tf+Y5DBWIx95pLL0h6y1gkruCbGPRqm/iURHKXUISmM0N3OLRL3IWNnadCpVtdob2i+bZkZEF4j2XZ1O3CQ6JQoTkiqERpwv6lzkeaKJOx0djh3UOdR3xQnvj491MJAsywfBT6TI9a1cVxiDwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U4dbc4dee4747e4f8ce6fe6a03d481667"

URLS = [
    "https://www.pokemoncenter.com/category/trading-card-game",
    "https://www.pokemoncenter.com/category/new-releases",
    "https://www.pokemoncenter.com/category/trading-card-game/elite-trainer-boxes",
    "https://www.pokemoncenter.com/category/trading-card-game/booster-packs-boxes"
]

def get_in_stock_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    found_items = []

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
                found_items.append(f"{title}\n{link}")

    return found_items

def send_line_message(message):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    items = get_in_stock_items()
    if items:
        send_line_message("🟢 Pokémon Restock:\n\n" + "\n\n".join(items[:5]))
    else:
        print("❌ No in-stock Pokémon TCG items found.")

