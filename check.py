import requests
from bs4 import BeautifulSoup
import os
import re
import sys

URL = "https://flexagift.com/id-en/miniso/e-voucher-miniso-rp-250000"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9"
}

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=30
    )

try:
    r = requests.get(
        URL,
        headers=headers,
        timeout=30
    )

    print("STATUS:", r.status_code)

    if r.status_code != 200:
        print("HTTP ERROR")
        sys.exit()

    html = r.text

    if "cloudflare" in html.lower():
        print("Cloudflare detected")
        sys.exit()

    soup = BeautifulSoup(html, "html.parser")

    product = soup.find(id="product-detail")

    if not product:
        print("product-detail not found")
        sys.exit()

    btn_buy = str(product.get("data-btn-buy", "")).strip().lower()
    btn_cart = str(product.get("data-btn-add-to-cart8", "")).strip().lower()

    max_qty_raw = product.get("data-max-qty", "0")

    try:
        max_qty = int(max_qty_raw)
    except:
        max_qty = 0

    text = soup.get_text(" ", strip=True).lower()

    out_of_stock_keywords = [
        "out of stock",
        "stok habis",
        "sold out",
        "unavailable"
    ]

    has_out_of_stock_text = any(
        x in text for x in out_of_stock_keywords
    )

    available_checks = {
        "btn_buy_enabled": btn_buy != "disabled",
        "btn_cart_enabled": btn_cart != "disabled",
        "max_qty_positive": max_qty > 0,
        "no_out_of_stock_text": not has_out_of_stock_text
    }

    print("DEBUG:")
    print(available_checks)
    print("BTN_BUY:", btn_buy)
    print("BTN_CART:", btn_cart)
    print("MAX_QTY:", max_qty)

    score = sum(available_checks.values())

    print("AVAILABLE SCORE:", score)

    # minimal 3 indikator valid
    available = score >= 3

    if available:
        msg = (
            "🔥 FLEXAGIFT STOCK AVAILABLE\n\n"
            f"Max Qty: {max_qty}\n"
            f"{URL}"
        )

        send_telegram(msg)

        print("NOTIFICATION SENT")

    else:
        print("Stock unavailable")

except Exception as e:
    print("ERROR:", e)
