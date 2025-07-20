import requests
import os

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_LINE_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID", "YOUR_LINE_USER_ID")

def notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": LINE_USER_ID,
        "messages": [{
            "type": "text",
            "text": message
        }]
    }
    res = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)
    print("🔔 LINE Push:", res.status_code, res.text)

