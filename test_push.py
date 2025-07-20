import requests
import json

LINE_CHANNEL_ACCESS_TOKEN = "FMdc1Tf+Y5DBWIx95pLL0h6y1gkruCbGPRqm/iURHKXUISmM0N3OLRL3IWNnadCpVtdob2i+bZkZEF4j2XZ1O3CQ6JQoTkiqERpwv6lzkeaKJOx0djh3UOdR3xQnvj491MJAsywfBT6TI9a1cVxiDwdB04t89/1O/w1cDnyilFU="
LINE_USER_ID = "U4dbc4dee4747e4f8ce6fe6a03d481667"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
}

data = {
    "to": LINE_USER_ID,
    "messages": [
        {
            "type": "text",
            "text": "👋 Hello! This is a test message from your LINE bot."
        }
    ]
}

response = requests.post("https://api.line.me/v2/bot/message/push",
                         headers=headers, data=json.dumps(data))

print("Status:", response.status_code)
print("Response:", response.text)

