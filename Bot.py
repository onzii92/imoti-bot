import requests
from bs4 import BeautifulSoup
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

sent = set()

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

def get_ads():
    url = "https://www.imot.bg/bg/pcgi/imot.cgi?act=3"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    ads = []
    for a in soup.find_all("a", href=True):
        link = a["href"]
        if "imot.cgi" in link:
            full = "https://www.imot.bg" + link
            ads.append(full)

    return ads[:10]

while True:
    try:
        ads = get_ads()
        for ad in ads:
            if ad not in sent:
                send(ad)
                sent.add(ad)
    except:
        pass

    time.sleep(300)
