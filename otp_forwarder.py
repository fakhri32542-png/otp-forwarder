import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==============================================================================
# CONFIGURATION
# ==============================================================================
API_URL = "http://54.38.176.48/ints/agent/SMSTestPanel"
USERNAME = "Fakhar325"
PASSWORD = "Fakhar325"
BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"  # <-- Apna sahi Telegram Bot Token yahan dalein
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10  
ITERATIONS_BEFORE_RECYCLE = 30  

# ==============================================================================
# TELEGRAM ALERTS ENGINE
# ==============================================================================
def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Logger]: Alert Status -> {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Gateway Error: {e}")

# ==============================================================================
# CAPTCHA MATHEMATICAL SOLVER
# ==============================================================================
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
        print(f"[-] Captcha Engine Failure: {e}")
    return None

# ==============================================================================
# RAILWAY NIXPACKS PROPER CHROME SETTINGS
# ==============================================================================
def get_optimized_browser():
    chrome_options = Options()
    
    # DevToolsActivePort aur Crash errors ko end karne ke liye solid arguments
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    # Detection bypassing settings
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Nixpacks ke custom binary locations dhoondna taake DevTools crash na ho
    common_binary_paths = [
        "/usr/bin/google-chrome-stable",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium"
    ]
    
    for path in common_binary_paths:
        if os.path.exists(path):
            chrome_options.binary_location = path
            print(f"[+] Setting Chrome Binary Location Path to: {path}")
            break

    print("[*] Launching Chromium Core Interface inside container...")
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

# ==============================================================================
# MAIN CORE LOOP
# ==============================================================================
def main():
    print("[+] SMS AUTOMATION MULTI-LAYER GUARD STARTED")
    last_sms_snapshot = ""
    
    while True:
        driver = None
        try:
            driver = get_optimized_browser()
            wait = WebDriverWait(driver, 25) 

            print(f"[*] Accessing panel node: {API_URL}")
            driver.get(API_URL)
            time.sleep(4) 

            # Handle Identity Challenge
            page_source = driver.page_source
            if "username" in page_source.lower() or "Sign In" in page_source:
                print("[*] Authentication prompt active.")
                
                soup = BeautifulSoup(page_source, "html.parser")
                captcha_solution = solve_captcha_from_text(soup.get_text())

                if not captcha_solution:
                    print("[-] Captcha capture failed. Restarting stream layout...")
                    driver.quit()
                    time.sleep(5)
                    continue

                user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                pass_input = driver.find_element(By.NAME, "password")
                capt_input = driver.find_element(By.NAME, "capt")
                
                user_input.clear()
                user_input.send_keys(USERNAME)
                pass_input.clear()
                pass_input.send_keys(PASSWORD)
                capt_input.clear()
                capt_input.send_keys(captcha_solution)

                print("[*] Dispatching signed auth credentials...")
                capt_input.submit()
                time.sleep(7)  

            # Main tracking loop
            for loop_count in range(ITERATIONS_BEFORE_RECYCLE):
                current_dom_state = driver.page_source
                
                if "username" in current_dom_state.lower() and "Sign In" in current_dom_state:
                    print("[!] Session verification dropped. Breaking track loops...")
                    break

                dash_soup = BeautifulSoup(current_dom_state, "html.parser")
                clean_payload_text = dash_soup.get_text("\n").strip()

                if len(clean_payload_text) > 50:
                    if clean_payload_text != last_sms_snapshot:
                        print("[+] Data modification captured! Sending update to telegram...")
                        
                        formatted_alert = f"📩 NEW SMS RECEIVED (STABLE PRODUCTION)\n\n{clean_payload_text[:3500]}"
                        send_telegram(formatted_alert)
                        
                        last_sms_snapshot = clean_payload_text
                    else:
                        print(f"[.] Sync: OK | State: {loop_count+1}/{ITERATIONS_BEFORE_RECYCLE} | Data stream un-mutated.")
                else:
                    print("[-] Error: Stream page unreadable or data layout truncated.")

                time.sleep(CHECK_INTERVAL)
                driver.refresh()
                time.sleep(3)

            print("[*] Shutting down subprocess context safely to clear server RAM...")
            driver.quit()

        except Exception as global_runtime_error:
            print(f"[!!] Core Loop Exception caught: {global_runtime_error}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            print("[*] Reviving application container state in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()
    
