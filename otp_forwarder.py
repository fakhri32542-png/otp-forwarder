import os
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

# ==============================================================================
# CONFIGURATION (UPDATED WITH NEW NEW TARGET NODE)
# ==============================================================================
API_URL = "http://139.99.68.231/ints/agent/SMSCDRStats"
USERNAME = "Furqan32"
PASSWORD = "Furqan32" # Agar password alag hai to yahan exact string replace kar sakte hain
BOT_TOKEN = "8705044326:AAG4HZjHJ0JThaMc0BCkqFJ1yakyus_JraQ"
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10

# 🔴 APNI FRESH ACTIVE COOKIE INTEGRATED
SESSION_COOKIE = "6a4afd6d965a8124fa5499bde286a673"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "http://139.99.68.231/ints/agent/SMSCDRStats",
    "Origin": "http://139.99.68.231",
    "Connection": "keep-alive",
    "Cookie": f"PHPSESSID={SESSION_COOKIE}"
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
# BACKUP CAPTCHA SOLVER (Fallback Mode)
# ==============================================================================
def solve_captcha(soup_object):
    try:
        page_text = soup_object.get_text()
        match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            print(f"[+] Backup Captcha Solved: {num1} + {num2} = {result}")
            return str(result)
            
        inputs = soup_object.find_all("input")
        for i in inputs:
            placeholder = i.get("placeholder", "")
            if "+" in placeholder:
                match = re.search(r'(\d+)\s*\+\s*(\d+)', placeholder)
                if match:
                    result = int(match.group(1)) + int(match.group(2))
                    print(f"[+] Captcha Solved From Placeholder: {result}")
                    return str(result)
    except Exception as e:
        print(f"[-] Captcha Solving Error: {e}")
    return None

# ==============================================================================
# RESILIENT HTTP CONNECTION BUILDER
# ==============================================================================
def build_bulletproof_session():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=5)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ==============================================================================
# MAIN SYSTEM WORKER
# ==============================================================================
def main():
    print("[+] SMS SERVICE RUNNING ON NEW NODE PIPELINE")
    last_sms_snapshot = ""
    use_login_fallback = False
    
    while True:
        session = None
        try:
            session = build_bulletproof_session()
            
            # Route 1: Cookie Direct Access Mode
            if not use_login_fallback:
                print("\n[*] Handshaking fresh session via target cookie...")
                dashboard_response = session.get(API_URL, headers=HEADERS, timeout=20)
                
                if "Sign In" not in dashboard_response.text:
                    print("[+] Cookie authorized successfully. Streaming data logs...")
                    
                    for loop_counter in range(100):
                        response = session.get(API_URL, headers=HEADERS, timeout=20)
                        
                        if "Sign In" in response.text:
                            print("[!] Cookie context dropped on host. Moving to login matrix...")
                            use_login_fallback = True
                            break
                            
                        dash_soup = BeautifulSoup(response.text, "html.parser")
                        current_text_layer = dash_soup.get_text("\n").strip()
                        
                        if len(current_text_layer) > 50:
                            if current_text_layer != last_sms_snapshot:
                                print("[+] Data stream update found! Transmitting to telegram...")
                                formatted_message = f"📩 NEW SMS RECEIVED (STABLE PRODUCTION)\n\n{current_text_layer[:3500]}"
                                send_telegram(formatted_message)
                                last_sms_snapshot = current_text_layer
                            else:
                                print(f"[.] Sync Status: OK | Count: {loop_counter+1}/100 | Node Active.")
                        else:
                            print("[-] Warning: Buffer string length under threshold.")
                            
                        time.sleep(CHECK_INTERVAL)
                    continue
                else:
                    print("[-] Injected Cookie stream is stale/expired. Activating login routing...")
                    use_login_fallback = True

            # Route 2: Fallback Login Protocol
            if use_login_fallback:
                print("[*] Parsing panel HTML fields structure...")
                clean_headers = HEADERS.copy()
                if "Cookie" in clean_headers:
                    del clean_headers["Cookie"]
                    
                response = session.get(API_URL, headers=clean_headers, timeout=20)
                soup = BeautifulSoup(response.text, "html.parser")
                
                captcha_val = solve_captcha(soup)
                if not captcha_val:
                    print("[-] HTML Text Captcha missing. Node using dynamic Image context.")
                    print("[*] Please update 'SESSION_COOKIE' parameter with a fresh string from your active browser.")
                    time.sleep(30)
                    continue
                    
                payload = {
                    "username": USERNAME,
                    "password": PASSWORD,
                    "capt": captcha_val
                }
                
                login_response = session.post(API_URL, headers=clean_headers, data=payload, timeout=20)
                
                if "Sign In" in login_response.text or login_response.status_code != 200:
                    print("[-] Manual login fallback declined by host application.")
                    time.sleep(15)
                    continue
                    
                print("[+] Fallback Login Verified. Tracking continuous active stream...")
                
                for loop_counter in range(40):
                    dashboard_response = session.get(API_URL, headers=clean_headers, timeout=20)
                    if "Sign In" in dashboard_response.text:
                        break
                        
                    dash_soup = BeautifulSoup(dashboard_response.text, "html.parser")
                    current_text_layer = dash_soup.get_text("\n").strip()
                    
                    if len(current_text_layer) > 50:
                        if current_text_layer != last_sms_snapshot:
                            formatted_message = f"📩 NEW SMS RECEIVED (FALLBACK MODE)\n\n{current_text_layer[:3500]}"
                            send_telegram(formatted_message)
                            last_sms_snapshot = current_text_layer
                    time.sleep(CHECK_INTERVAL)
                
                use_login_fallback = False

        except Exception as global_error:
            print(f"[!!] Production runtime loop caught error: {global_error}")
            time.sleep(10)

if __name__ == "__main__":
    main()
    
