from flask import Flask
from checker import run_checker
import threading
import time
from datetime import datetime, timedelta
import pytz

app = Flask(__name__)

def daily_scheduler():
    pst = pytz.timezone("America/Los_Angeles")

    while True:
        now = datetime.now(pst)
        start_time = now.replace(hour=5, minute=55, second=0, microsecond=0)
        end_time = now.replace(hour=11, minute=0, second=0, microsecond=0)

        if now < start_time:
            sleep_sec = (start_time - now).total_seconds()
            print(f"[WAIT] Sleeping until 5:55 AM PST ({int(sleep_sec)} seconds)")
            time.sleep(sleep_sec)
        elif start_time <= now <= end_time:
            print(f"[RUN] Running bot at {now.strftime('%Y-%m-%d %H:%M:%S')}")
            run_checker()
            time.sleep(30)  # Adjust frequency as needed
        else:
            next_day = start_time + timedelta(days=1)
            sleep_sec = (next_day - now).total_seconds()
            print(f"[DONE] Bot finished for the day. Sleeping {int(sleep_sec)} seconds until next run.")
            time.sleep(sleep_sec)

@app.route('/')
def home():
    return "Pokémon TCG Restock Bot is running."

# Start scheduler thread
threading.Thread(target=daily_scheduler, daemon=True).start()

