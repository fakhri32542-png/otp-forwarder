import requests
import time
import re
from datetime import datetime

PANEL_URL = "http://139.99.68.231/ints/agent/SMSCDRStats"

PHPSESSID = "c2968f7f9c1f60162e478310d0dc5318"

BOT_TOKEN = "8705044326:AAG4HZjHJ0JThaMc0BCkqFJ1yakyus_JraQ"
CHAT_ID = "-1003824926404"

CHECK_INTERVAL = 5

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:
        requests.post(url, data=data, timeout=15)
        print("Sent To Telegram")

    except Exception as e:
        print("Telegram Error:", e)

session = requests.Session()

session.cookies.set(
    "PHPSESSID",
    PHPSESSID
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

sent_otps = set()

print("OTP Forwarder Started...")

while True:

    try:

        response = session.get(
            PANEL_URL,
            headers=headers,
            timeout=20
        )

        html = response.text

        otp_matches = re.findall(r"\b\d{4,8}\b", html)

        otp_matches = list(set(otp_matches))

        for otp in otp_matches:

            if otp in sent_otps:
                continue

            sent_otps.add(otp)

            current_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            telegram_message = f'''
NEW OTP RECEIVED

OTP: {otp}

Time: {current_time}
'''

            print(telegram_message)

            send_telegram(telegram_message)

    except Exception as e:
        print("Error:", e)

    time.sleep(CHECK_INTERVAL)