import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from flask import Flask

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "FMdc1Tf+Y5DBWIx95pLL0h6y1gkruCbGPRqm/iURHKXUISmM0N3OLRL3IWNnadCpVtdob2i+bZkZEF4j2XZ1O3CQ6JQoTkiqERpwv6lzkeaKJOx0djh3UOdR3xQnvj491MJAsywfBT6TI9a1cVxiDwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U4dbc4dee4747e4f8ce6fe6a03d481667"

URLS = [
    "https://www.pokemoncenter.com/category/trading-card-game",
    "https://www.pokemoncenter.com/category/new-releases",
    "https://www.pokemoncenter.com/category/trading-card-game/elite-trainer-boxes",
    "https://www.pokemoncenter.com/category/trading-card-game/booster-packs-boxes"
]

# Used to store sent items to avoid duplicate alerts
sent_items = set()

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
                if title not in sent_items:
                    found_items.append(f"{title}\n{link}")
                    sent_items.add(title)

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

def should_check():
    now = datetime.now(pytz.timezone("US/Pacific"))
    return now.hour == 5 and now.minute >= 50 or 6 <= now.hour < 11

def check_loop():
    while True:
        if should_check():
            print("Checking for Pokémon Center stock...")
            items = get_in_stock_items()
            if items:
                send_line_message("🟢 Pokémon Restock:\n\n" + "\n\n".join(items[:5]))
            else:
                print("❌ No in-stock Pokémon TCG items found.")
        else:
            print("⏳ Outside of check window. Sleeping...")

        time.sleep(20)  # Adjust to 15–30 sec depending on how aggressive you want

@app.route("/", methods=["GET"])
def home():
    return "✅ Pokémon Center Restock Bot Running"

if __name__ == "__main__":
    import threading
    threading.Thread(target=check_loop).start()
    app.run(host="0.0.0.0", port=10000)
