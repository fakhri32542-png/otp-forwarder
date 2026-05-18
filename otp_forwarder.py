import os
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# ==============================================================================
# CONFIGURATION
# ==============================================================================
API_URL = "http://54.38.176.48/ints/agent/SMSTestPanel"
USERNAME = "Fakhar325"
PASSWORD = "Fakhar325"
BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"  # <-- Yahan apna naya Telegram Bot Token lagayein
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10

# Server ko real user browser mimic karne ke liye detailed unique headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "http://54.38.176.48/ints/agent/SMSTestPanel",
    "Origin": "http://54.38.176.48",
    "Connection": "keep-alive"
}

# ==============================================================================
# TELEGRAM ALERTS ENGINE
# ==============================================================================
def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Alert]: Status Code -> {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Delivery Error: {e}")

# ==============================================================================
# CAPTCHA EXTRACTION & MATH ENGINE
# ==============================================================================
def solve_captcha(soup_object):
    try:
        page_text = soup_object.get_text()
        # Pure document structure se math calculations (e.g., 5 + 3) dhoondna
        match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
        
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            print(f"[+] Captcha Found & Solved: {num1} + {num2} = {result}")
            return str(result)
    except Exception as e:
        print(f"[-] Captcha Solving Matrix Error: {e}")
    return None

# ==============================================================================
# RESILIENT HTTP CONNECTION BUILDER (SERVER CONNECTION DROP PROTECTION)
# ==============================================================================
def build_bulletproof_session():
    """Server disconnects ya aborts se bachnay ke liye network pool adapter config."""
    session = requests.Session()
    retry_strategy = Retry(
        total=5,  # Network break hone par 5 bar auto-retry karega
        backoff_factor=2,  # Har retry ke darmiyan wait double hoga (2s, 4s, 8s...)
        status_forcelist=[429, 500, 502, 503, 504],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ==============================================================================
# MAIN SYSTEM WORKER
# ==============================================================================
def main():
    print("[+] HIGH-PERFORMANCE SMS SERVICE RUNNING ON RAILWAY")
    last_sms_snapshot = ""
    
    while True:
        session = None
        try:
            session = build_bulletproof_session()
            print("\n[*] Initializing target connection handshake...")
            
            # Step 1: Open Target Page
            response = session.get(API_URL, headers=HEADERS, timeout=20)
            soup = BeautifulSoup(response.text, "html.parser")
            
            captcha_val = solve_captcha(soup)
            if not captcha_val:
                print("[-] Target dashboard did not provide captcha context. Retrying loop...")
                time.sleep(10)
                continue
                
            payload = {
                "username": USERNAME,
                "password": PASSWORD,
                "capt": captcha_val
            }
            
            # Step 2: Perform Authenticated Sign-In
            print("[*] Forwarding authentication tokens and captcha matrix...")
            login_response = session.post(API_URL, headers=HEADERS, data=payload, timeout=20)
            
            if "Sign In" in login_response.text or login_response.status_code != 200:
                print("[-] Server rejected credentials or captcha timed out.")
                time.sleep(15)
                continue
                
            print("[+] Authentication verified. Monitoring data streams...")
            
            # Step 3: Stream Tracking Loop (Single Session Execution Pool)
            for loop_counter in range(50):
                dashboard_response = session.get(API_URL, headers=HEADERS, timeout=20)
                
                # Check if session auto-dropped
                if "Sign In" in dashboard_response.text:
                    print("[!] Container token expired. Requesting re-auth configuration...")
                    break
                    
                dash_soup = BeautifulSoup(dashboard_response.text, "html.parser")
                current_text_layer = dash_soup.get_text("\n").strip()
                
                if len(current_text_layer) > 50:
                    if current_text_layer != last_sms_snapshot:
                        print("[+] Data mutation detected! Transmitting to telegram...")
                        
                        formatted_message = f"📩 NEW SMS RECEIVED (STABLE PRODUCTION ENGINE)\n\n{current_text_layer[:3500]}"
                        send_telegram(formatted_message)
                        last_sms_snapshot = current_text_layer
                    else:
                        print(f"[.] Sync: OK | State: {loop_counter+1}/50 | Pipeline stable.")
                else:
                    print("[-] Data packet truncated or interface layout unrecognizable.")
                    
                time.sleep(CHECK_INTERVAL)
                
        except Exception as global_error:
            print(f"[!!] Network pipeline error intercepted: {global_error}")
            print("[*] Recycling network sockets for cold-restart...")
            time.sleep(10)

if __name__ == "__main__":
    main()
    
