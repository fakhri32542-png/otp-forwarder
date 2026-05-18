import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# CONFIG
# ==========================================
API_URL = "http://54.38.176.48/ints/agent/SMSTestPanel"
USERNAME = "Fakhar325"
PASSWORD = "Fakhar325"
BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"  # Real token input karein
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10

def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Status]: {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Delivery Error: {e}")

def solve_captcha_from_text(text):
    try:
        match = re.search(r'(\d+)\s*\+\s*(\d+)', text)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            print(f"[+] Captcha Solved: {num1} + {num2} = {result}")
            return str(result)
    except Exception as e:
        print(f"[-] Captcha Solving Error: {e}")
    return None

def get_real_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Railway local environment standard system discovery path lookups
    paths = ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium-browser"]
    for path in paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            print(f"[+] System Chrome Binary found at: {path}")
            break

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def main():
    print("[*] Production Real Browser Monitoring Service Triggered...")
    last_sms_data = ""
    driver = None

    while True:
        try:
            if driver is None:
                driver = get_real_browser()

            print(f"[*] Browsing target panel: {API_URL}")
            driver.get(API_URL)
            time.sleep(4)

            page_source = driver.page_source
            if "Sign In" in page_source or "username" in page_source.lower():
                print("[*] Authentication screen challenge found.")
                soup = BeautifulSoup(page_source, "html.parser")
                captcha_val = solve_captcha_from_text(soup.get_text())

                if not captcha_val:
                    print("[-] Critical target tracking sync broke. Retrying view stream...")
                    time.sleep(5)
                    continue

                user_field = driver.find_element(By.NAME, "username")
                pass_field = driver.find_element(By.NAME, "password")
                capt_field = driver.find_element(By.NAME, "capt")
                
                user_field.clear()
                user_field.send_keys(USERNAME)
                pass_field.clear()
                pass_field.send_keys(PASSWORD)
                capt_field.clear()
                capt_field.send_keys(captcha_val)

                capt_field.submit()
                print("[*] Dispatching session creation forms...")
                time.sleep(5)

            for _ in range(20):
                current_source = driver.page_source
                if "Sign In" in current_source and "username" in current_source.lower():
                    print("[!] Local container context identity token dropped.")
                    break

                dash_soup = BeautifulSoup(current_source, "html.parser")
                current_text_snapshot = dash_soup.get_text("\n").strip()

                if len(current_text_snapshot) > 50:
                    if current_text_snapshot != last_sms_data:
                        print("[+] Payload mutation captured. Transmitting text data...")
                        tele_message = f"📩 NEW SMS RECEIVED (STABLE BROWSER)\n\n{current_text_snapshot[:3500]}"
                        send_telegram(tele_message)
                        last_sms_data = current_text_snapshot
                    else:
                        print("[.] State unchanged. Synchronized loop waiting for stack updates.")
                else:
                    print("[-] Context execution layout state tracking is unreadable.")

                time.sleep(CHECK_INTERVAL)
                driver.refresh()
                time.sleep(3)

        except Exception as err:
            print(f"[!!] Production runtime loop caught error: {err}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
                driver = None
            time.sleep(10)

if __name__ == "__main__":
    main()
    
