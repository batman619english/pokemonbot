import requests
from bs4 import BeautifulSoup

LINE_CHANNEL_ACCESS_TOKEN = "FMdc1Tf+Y5DBWIx95pLL0h6y1gkruCbGPRqm/iURHKXUISmM0N3OLRL3IWNnadCpVtdob2i+bZkZEF4j2XZ1O3CQ6JQoTkiqERpwv6lzkeaKJOx0djh3UOdR3xQnvj491MJAsywfBT6TI9a1cVxiDwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U4dbc4dee4747e4f8ce6fe6a03d481667"

TCG_URL = "https://www.pokemoncenter.com/category/trading-card-game"

def get_in_stock_tcg():
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(TCG_URL, headers=headers)
    res.raise_for_status()
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

        # If product not marked "out of stock", consider it available
        if not stock_tag or "out of stock" not in stock_tag.text.lower():
            found.append(f"{title}\n{link}")

    return found

def send_line_push_message(message):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=data)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    restocked_items = get_in_stock_tcg()
    if restocked_items:
        message = "🚨 TCG Product(s) Restocked!\n\n" + "\n\n".join(restocked_items)
        send_line_push_message(message)
    else:
        print("No restocks found.")

