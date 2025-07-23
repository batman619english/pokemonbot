import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from flask import Flask
import threading
import logging

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "FMdc1Tf+Y5DBWIx95pLL0h6y1gkruCbGPRqm/iURHKXUISmM0N3OLRL3IWNnadCpVtdob2i+bZkZEF4j2XZ1O3CQ6JQoTkiqERpwv6lzkeaKJOx0djh3UOdR3xQnvj491MJAsywfBT6TI9a1cVxiDwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U4dbc4dee4747e4f8ce6fe6a03d481667"

POKEMON_URLS = [
    "https://www.pokemoncenter.com/category/trading-card-game",
    "https://www.pokemoncenter.com/category/new-releases",
    "https://www.pokemoncenter.com/category/trading-card-game/elite-trainer-boxes",
    "https://www.pokemoncenter.com/category/trading-card-game/booster-packs-boxes"
]

BESTBUY_KEYWORDS = ["pokemon elite trainer box", "pokemon booster box"]

sent_items = set()

# ✅ Enable timestamped logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def send_line_message(message):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    logging.info(f"📤 LINE Status: {response.status_code}, Response: {response.text}")

def get_pokemon_center_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    found = []

    for url in POKEMON_URLS:
        try:
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
                        found.append(f"{title}\n{link}")
                        sent_items.add(title)
        except Exception as e:
            logging.warning(f"⚠️ Error checking Pokémon Center URL {url}: {e}")

    return found

def get_bestbuy_items():
    headers = {"User-Agent": "Mozilla/5.0"}
    found = []
    try:
        for keyword in BESTBUY_KEYWORDS:
            search_url = f"https://www.bestbuy.com/site/searchpage.jsp?st={keyword.replace(' ', '+')}"
            res = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.select(".sku-item")

            for item in items:
                title_tag = item.select_one(".sku-header a")
                status_tag = item.select_one(".add-to-cart-button")

                if title_tag and status_tag:
                    title = title_tag.text.strip()
                    link = title_tag["href"]
                    if "sold out" not in status_tag.text.lower():
                        if title not in sent_items:
                            found.append(f"{title}\nhttps://www.bestbuy.com{link}")
                            sent_items.add(title)
    except Exception as e:
        logging.warning(f"⚠️ Error checking Best Buy: {e}")

    return found

def check_and_alert():
    pst = pytz.timezone("US/Pacific")
    now = datetime.now(pst)
    logging.info(f"🕒 Current PST time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    start_time = now.replace(hour=5, minute=55, second=0, microsecond=0)
    end_time = now.replace(hour=11, minute=0, second=0, microsecond=0)

    if start_time <= now <= end_time:
        logging.info("⏰ Running scan...")
        found_items = get_pokemon_center_items() + get_bestbuy_items()
        if found_items:
            send_line_message("🟢 Restock Alert:\n\n" + "\n\n".join(found_items[:10]))
        else:
            logging.info("❌ No in-stock items found.")
    else:
        logging.info("⏳ Outside scan window. Sleeping...")

# ✅ Add logging to scheduler
def scheduler():
    logging.info("🔁 Scheduler thread started.")
    while True:
        logging.info("🔄 Running scheduled check...")
        check_and_alert()
        time.sleep(60)

@app.route("/")
def index():
    return "Pokémon Restock Bot is running."

if __name__ == "__main__":
    threading.Thread(target=scheduler, daemon=True).start()
    logging.info("🚀 Starting Flask app...")
    scheduler_thread = threading.Thread(target=scheduler, daemon=True)
    scheduler_thread.start()
    logging.info("✅ Scheduler started.")
    app.run(host="0.0.0.0", port=10000)
