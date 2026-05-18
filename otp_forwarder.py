import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==========================================
# CONFIG
# ==========================================
API_URL = "http://54.38.176.48/ints/agent/SMSTestPanel"
USERNAME = "Fakhar325"
PASSWORD = "Fakhar325"
BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"  # Apna Token yahan lagayein
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10

# ==========================================
# TELEGRAM NOTIFIER
# ==========================================
def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Status]: {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Delivery Error: {e}")

# ==========================================
# CAPTCHA ENGINE (Math Solver)
# ==========================================
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

# ==========================================
# BROWSER INITIALIZATION
# ==========================================
def get_real_browser():
    """Background mein anti-bot parameters ke sath Chrome setup karta ha."""
    chrome_options = Options()
    
    # Cloud (Railway) par browser bina window ke background mein chalane ke liye
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Real user mimic karne ke liye headers aur settings
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Chrome Driver automatically download aur configure karega
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # WebDriver detection ko mazeed bypass karne ke liye JavaScript script injection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver

# ==========================================
# MAIN WORKER LOOP
# ==========================================
def main():
    print("[*] Real Browser SMS Engine Started...")
    last_sms_data = ""
    driver = None

    while True:
        try:
            if driver is None:
                print("[*] Launching Real Chrome Browser Instance...")
                driver = get_real_browser()

            print(f"[*] Navigating to: {API_URL}")
            driver.get(API_URL)
            time.sleep(3) # Page load hone ka wait

            # Check karein ke kya hum login page par hain ya direct dashboard par
            page_source = driver.page_source
            if "Sign In" in page_source or "username" in page_source.lower():
                print("[*] Login page detected. Processing credentials...")
                
                # HTML parse karke captcha dhoondna
                soup = BeautifulSoup(page_source, "html.parser")
                page_text = soup.get_text()
                captcha_val = solve_captcha_from_text(page_text)

                if not captcha_val:
                    print("[-] Page text se captcha nahi mila. Reloading page...")
                    time.sleep(5)
                    continue

                # Selenium ke zariye input fields dhoondna aur values type karna
                # (Yahan inputs ke standard selectors use kiye hain, agar text elements badlein to hum badal sakte hain)
                user_field = driver.find_element(By.NAME, "username")
                pass_field = driver.find_element(By.NAME, "password")
                capt_field = driver.find_element(By.NAME, "capt")
                
                user_field.clear()
                user_field.send_keys(USERNAME)
                
                pass_field.clear()
                pass_field.send_keys(PASSWORD)
                
                capt_field.clear()
                capt_field.send_keys(captcha_val)

                # Form submit karne ke liye submit button dhoond kar click karna
                # Agar button par form structure ha to submit() kaam karega, warna enter key click hogi
                capt_field.submit()
                print("[*] Form submitted. Waiting for dashboard redirection...")
                time.sleep(5)

            # Dashboard loop (Login hone ke baad browser isi page par rahega aur refresh karega)
            for _ in range(20):
                current_source = driver.page_source
                
                # Agar kisi wajah se session out ho jaye to loop tor kar dobara login karega
                if "Sign In" in current_source and "username" in current_source.lower():
                    print("[!] Kicked out from session. Restarting login engine...")
                    break

                dash_soup = BeautifulSoup(current_source, "html.parser")
                current_text_snapshot = dash_soup.get_text("\n").strip()

                if len(current_text_snapshot) > 50:
                    if current_text_snapshot != last_sms_data:
                        print("[+] New state change in dashboard! Forwarding data...")
                        
                        tele_message = f"📩 NEW SMS RECEIVED (BROWSER MODE)\n\n{current_text_snapshot[:3500]}"
                        send_telegram(tele_message)
                        
                        last_sms_data = current_text_snapshot
                    else:
                        print("[.] Stream read synchronized. Browser waiting for new data.")
                else:
                    print("[-] Dashboard loaded but text layer is short.")

                time.sleep(CHECK_INTERVAL)
                driver.refresh() # Browser tab ko refresh karega naye SMS check karne ke liye
                time.sleep(3)

        except Exception as err:
            print(f"[!!] Browser Loop Exception: {err}")
            if driver:
                try:
                    driver.quit() # Bad state waqt browser band karein taake memory leak na ho
                except:
                    pass
                driver = None # loop agli dafa naya browser auto-create karega
            time.sleep(10)

if __name__ == "__main__":
    main()
    
