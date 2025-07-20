import requests

# Your LINE Notify token
LINE_ACCESS_TOKEN = "ff62166d86df463f496ade82b02f48ee"

def send_line_notify(message):
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "message": message
    }
    response = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    send_line_notify("✅ This is a test message from your LINE Notify bot!")

