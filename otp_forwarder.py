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
CHECK_INTERVAL = 10  # Har check ke darmiyan seconds ka gap
ITERATIONS_BEFORE_RECYCLE = 30  # RAM bachanay ke liye itni bar check ke baad browser restart hoga

# ==============================================================================
# TELEGRAM ALERTS ENGINE
# ==============================================================================
def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Logger]: Packet transmission status -> {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Gateway Error: {e}")

# ==============================================================================
# CAPTCHA MATHEMATICAL SOLVER
# ==============================================================================
def solve_captcha_from_text(text):
    try:
        # Poore HTML text layer se 'X + Y' pattern detect karna
        match = re.search(r'(\d+)\s*\+\s*(\d+)', text)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            print(f"[+] Captcha Solved Natively: {num1} + {num2} = {result}")
            return str(result)
    except Exception as e:
        print(f"[-] Captcha Engine Failure: {e}")
    return None

# ==============================================================================
# NIXPACKS OPTIMIZED BROWSER INITIALIZATION
# ==============================================================================
def get_optimized_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    # Automation footprints ko conceal karna taake panel block na kare
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    print("[*] Spawning a clean system integrated Chrome instance...")
    driver = webdriver.Chrome(options=chrome_options)
    
    # anti-bot bypass javascript variable tweak
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

# ==============================================================================
# MAIN SYSTEM EXECUTION LOOP
# ==============================================================================
def main():
    print("[+] SMS GATEWAY AUTOMATION DEPLOYED ON PRODUCTION")
    last_sms_snapshot = ""
    
    while True:
        driver = None
        try:
            # Step 1: Initialize browser context
            driver = get_optimized_browser()
            wait = WebDriverWait(driver, 20)  # Explicit wait pool config (Max 20 seconds)

            print(f"[*] Connecting to network target: {API_URL}")
            driver.get(API_URL)
            time.sleep(3)  # Initial buffer for handshake

            # Step 2: Handle Identity Challenge / Login Page
            page_source = driver.page_source
            if "username" in page_source.lower() or "Sign In" in page_source:
                print("[*] Authentication screen challenge encountered.")
                
                soup = BeautifulSoup(page_source, "html.parser")
                captcha_solution = solve_captcha_from_text(soup.get_text())

                if not captcha_solution:
                    print("[-] Failed to scan captcha numbers. Recycling stream pipeline...")
                    driver.quit()
                    time.sleep(5)
                    continue

                # Fields visibility ka wait karna (Slow connection handling)
                user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
                pass_input = driver.find_element(By.NAME, "password")
                capt_input = driver.find_element(By.NAME, "capt")
                
                user_input.clear()
                user_input.send_keys(USERNAME)
                pass_input.clear()
                pass_input.send_keys(PASSWORD)
                capt_input.clear()
                capt_input.send_keys(captcha_solution)

                print("[*] Submitting credentials array...")
                capt_input.submit()
                time.sleep(6)  # Wait for secure redirection token generation

            # Step 3: Stream Monitoring Pool (RAM Guard Loop)
            for loop_count in range(ITERATIONS_BEFORE_RECYCLE):
                current_dom_state = driver.page_source
                
                # Check if session expired or kicked to home
                if "username" in current_dom_state.lower() and "Sign In" in current_dom_state:
                    print("[!] Session invalidated by target host. Re-routing execution path...")
                    break

                # Parse data layers
                dash_soup = BeautifulSoup(current_dom_state, "html.parser")
                clean_payload_text = dash_soup.get_text("\n").strip()

                if len(clean_payload_text) > 50:
                    if clean_payload_text != last_sms_snapshot:
                        print("[+] Mutation captured! Parsing payload packet...")
                        
                        formatted_alert = f"📩 NEW SMS RECEIVED (STABLE PRODUCTION ENGINE)\n\n{clean_payload_text[:3500]}"
                        send_telegram(formatted_alert)
                        
                        last_sms_snapshot = clean_payload_text
                    else:
                        print(f"[.] Sync status: OK | Iteration: {loop_count+1}/{ITERATIONS_BEFORE_RECYCLE} | Data stream stable.")
                else:
                    print("[-] Warning: Dom data buffer size is under minimum thresholds.")

                time.sleep(CHECK_INTERVAL)
                driver.refresh()
                time.sleep(3)  # Wait for refresh lifecycle

            # Step 4: Clear RAM memory leakage footprints
            print("[*] Releasing active container RAM blocks. Recycling browser subprocess...")
            driver.quit()

        except Exception as global_runtime_error:
            print(f"[!!] Critical Exception Intercepted: {global_runtime_error}")
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            print("[*] Re-spinning thread in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()
