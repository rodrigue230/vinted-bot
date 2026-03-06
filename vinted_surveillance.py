import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.vinted.fr/catalog?search_text=bosch+carlotta"
CHECK_FILE = "seen_items.json"

TELEGRAM_TOKEN = "TON_TOKEN"
TELEGRAM_CHAT_ID = "TON_CHAT_ID"

headers = {"User-Agent": "Mozilla/5.0"}

try:
    with open(CHECK_FILE, "r") as f:
        seen_items = json.load(f)
except:
    seen_items = []

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

items = []

for a in soup.select("a[href*='/items/']"):
    title = a.get_text(strip=True)
    link = "https://www.vinted.fr" + a.get("href")

    if title:
        items.append({"title": title, "link": link})

new_items = [i for i in items if i not in seen_items]

if new_items:
    message = "Nouvelle pièce Vinted détectée :\n\n"
    for item in new_items:
        message += f"{item['title']}\n{item['link']}\n\n"

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": message},
    )

with open(CHECK_FILE, "w") as f:
    json.dump(items, f)


