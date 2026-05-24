import cloudscraper
from bs4 import BeautifulSoup
import os

URL = "https://flexagift.com/id-en/pertamina/e-voucher-pertamina-rp-30000"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'mobile': False
    }
)

def send(msg):
    scraper.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=30
    )

r = scraper.get(URL, timeout=30)

print("STATUS:", r.status_code)

html = r.text.lower()

if "just a moment" in html:
    print("Cloudflare masih aktif")
    exit()

soup = BeautifulSoup(r.text, "html.parser")

product = soup.find(id="product-detail")

if not product:
    print("product-detail tidak ditemukan")
    exit()

btn_buy = str(product.get("data-btn-buy", "")).lower()
btn_cart = str(product.get("data-btn-add-to-cart8", "")).lower()

max_qty = int(product.get("data-max-qty", 0))

print("BUY:", btn_buy)
print("CART:", btn_cart)
print("MAX_QTY:", max_qty)

available = (
    btn_buy != "disabled"
    and btn_cart != "disabled"
    and max_qty > 0
)

if available:
    send(
        f"🔥 FLEXAGIFT STOCK AVAILABLE\n\n"
        f"Qty: {max_qty}\n"
        f"{URL}"
    )

    print("NOTIFICATION SENT")

else:
    print("Stock unavailable")
