from dotenv import load_dotenv
import requests
import threading
import time
import os

load_dotenv()

DUCKDNS_DOMAIN = os.getenv("DUCKDNS_DOMAIN")
DUCKDNS_TOKEN = os.getenv("DUCKDNS_TOKEN")

if not DUCKDNS_DOMAIN or not DUCKDNS_TOKEN:
    raise ValueError("DuckDNS domain or token not found in .env file")

def update_duckdns():
    while True:
        url = f"https://www.duckdns.org/update?domains={DUCKDNS_DOMAIN}&token={DUCKDNS_TOKEN}&ip="
        try:
            response = requests.get(url)
            if response.text.strip() == "OK":
                print("DuckDNS update successful.")
            else:
                print(f"DuckDNS update failed: {response.text}")
        except requests.RequestException as e:
            print(f"Error updating DuckDNS: {e}")
        time.sleep(300)

duckdns_thread = threading.Thread(target=update_duckdns, daemon=True)
duckdns_thread.start()
