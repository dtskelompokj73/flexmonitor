import requests
from bs4 import BeautifulSoup
import os
import re

URL = "https://flexagift.com/id-en/pertamina/e-voucher-pertamina-rp-30000"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=30)

text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True)

match = re.search(r"Remaining Stock\s*:\s*(\d+)", text)

if match:
    stock = int(match.group(1))

    print("Stock:", stock)

    if stock > 0:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": f"🔥 STOCK TERSEDIA\n\nStock: {stock}\n{URL}"
            }
        )
else:
    print("Stock tidak ditemukan")
