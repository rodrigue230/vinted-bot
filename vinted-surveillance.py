from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import smtplib
import requests
from email.mime.text import MIMEText

URL = "https://www.vinted.fr/catalog?search_text=bosch+carlotta"
CHECK_FILE = "seen_items.json"
TELEGRAM_TOKEN="7802981919:AAHV5-ptPsNkEK2zLgmxokqmyaZjIz1XR3g"
TELEGRAM_CHAT_ID="2049467518"
EMAIL_SENDER = "rody.nalinnes@gmail.com"
EMAIL_PASSWORD = "Glafira-10508404v"
EMAIL_RECEIVER = "rody.nalinnes@gmail.com"

try:
    with open(CHECK_FILE, "r") as f:
        seen_items = json.load(f)
except:
    seen_items = []

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(URL)
time.sleep(5)

items = []
ads = driver.find_elements(By.CSS_SELECTOR, "a[data-testid='item-box']")

for ad in ads:
    title = ad.text
    link = ad.get_attribute("href")
    items.append({"title": title, "link": link})

driver.quit()

new_items = [item for item in items if item not in seen_items]

if new_items:
    message_body = "Nouvelle pièce détectée sur Vinted :\n\n"
    for item in new_items:
        message_body += f"{item['title']}\n{item['link']}\n\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_body
    }

    requests.post(url, data=data)

with open(CHECK_FILE, "w") as f:
    json.dump(items, f)

url = "https://api.telegram.org/bot7802981919:AAHV5-ptPsNkEK2zLgmxokqmyaZjIz1XR3g/sendMessage"

data = {
    "chat_id": "2049467518",
    "text": "TEST TELEGRAM OK"
}

requests.post(url, data=data)