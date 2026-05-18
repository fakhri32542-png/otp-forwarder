import os
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

# ==============================================================================
# CONFIGURATION
# ==============================================================================
API_URL = "http://54.38.176.48/ints/agent/SMSTestPanel"
USERNAME = "Fakhar325"
PASSWORD = "Fakhar325"
BOT_TOKEN = "8705044326:AAG4HZjHJ0JThaMc0BCkqFJ1yakyus_JraQ"  # Aapka active token
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 10

# Active cookie for instant login bypass
SESSION_COOKIE = "c2968f7f9c1f60162e478310d0dc5318"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "http://54.38.176.48/ints/agent/SMSTestPanel",
    "Origin": "http://54.38.176.48",
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
    except Exception as e:
        print(f"[-] Captcha Solving Error: {e}")
    return None

# ==============================================================================
# RESILIENT HTTP CONNECTION BUILDER (Fixed Without urllib3 Conflict)
# ==============================================================================
def build_bulletproof_session():
    session = requests.Session()
    # Built-in Requests max_retries implementation (Zero imports conflict)
    adapter = HTTPAdapter(max_retries=5) 
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# ==============================================================================
# MAIN SYSTEM WORKER
# ==============================================================================
def main():
    print("[+] SMS SERVICE PRODUCTION ENGINE LOGGED ON")
    last_sms_snapshot = ""
    use_login_fallback = False
    
    while True:
        session = None
        try:
            session = build_bulletproof_session()
            
            # Primary Route: Direct Bypass via PHPSESSID Cookie
            if not use_login_fallback:
                print("\n[*] Initializing direct cookie channel handshake...")
                dashboard_response = session.get(API_URL, headers=HEADERS, timeout=20)
                
                if "Sign In" not in dashboard_response.text:
                    print("[+] Cookie authentication verified successfully.")
                    
                    for loop_counter in range(100):
                        response = session.get(API_URL, headers=HEADERS, timeout=20)
                        
                        if "Sign In" in response.text:
                            print("[!] Cookie context dropped natively. Shifting to backup plan...")
                            use_login_fallback = True
                            break
                            
                        dash_soup = BeautifulSoup(response.text, "html.parser")
                        current_text_layer = dash_soup.get_text("\n").strip()
                        
                        if len(current_text_layer) > 50:
                            if current_text_layer != last_sms_snapshot:
                                print("[+] State mutation discovered. Transmitting logs...")
                                formatted_message = f"📩 NEW SMS RECEIVED (STABLE PRODUCTION)\n\n{current_text_layer[:3500]}"
                                send_telegram(formatted_message)
                                last_sms_snapshot = current_text_layer
                            else:
                                print(f"[.] Sync Status: OK | Stream Count: {loop_counter+1}/100 | Sockets Stable.")
                        else:
                            print("[-] Error: Buffer string under min threshold.")
                            
                        time.sleep(CHECK_INTERVAL)
                    continue
                else:
                    print("[-] Current Cookie stream is stale. Launching fallback login routing...")
                    use_login_fallback = True

            # Plan B: Credential Handshake + Captcha Matching Engine
            if use_login_fallback:
                print("[*] Launching standard forms parsing module...")
                clean_headers = HEADERS.copy()
                if "Cookie" in clean_headers:
                    del clean_headers["Cookie"]
                    
                response = session.get(API_URL, headers=clean_headers, timeout=20)
                soup = BeautifulSoup(response.text, "html.parser")
                
                captcha_val = solve_captcha(soup)
                if not captcha_val:
                    print("[-] Captcha framework response error. Recycling main branch...")
                    time.sleep(10)
                    continue
                    
                payload = {
                    "username": USERNAME,
                    "password": PASSWORD,
                    "capt": captcha_val
                }
                
                login_response = session.post(API_URL, headers=clean_headers, data=payload, timeout=20)
                
                if "Sign In" in login_response.text or login_response.status_code != 200:
                    print("[-] Fallback routine rejected by server. Sleeping thread...")
                    time.sleep(15)
                    continue
                    
                print("[+] Fallback Login Verified. Monitoring active dashboard data stream...")
                
                for loop_counter in range(40):
                    dashboard_response = session.get(API_URL, headers=clean_headers, timeout=20)
                    
                    if "Sign In" in dashboard_response.text:
                        print("[!] Fallback identity token expired. Resetting node...")
                        break
                        
                    dash_soup = BeautifulSoup(dashboard_response.text, "html.parser")
                    current_text_layer = dash_soup.get_text("\n").strip()
                    
                    if len(current_text_layer) > 50:
                        if current_text_layer != last_sms_snapshot:
                            print("[+] Update captured via fallback layer! Transmitting...")
                            formatted_message = f"📩 NEW SMS RECEIVED (FALLBACK BACKUP)\n\n{current_text_layer[:3500]}"
                            send_telegram(formatted_message)
                            last_sms_snapshot = current_text_layer
                        else:
                            print(f"[.] Fallback Sync: OK | Count: {loop_counter+1}/40")
                    else:
                        print("[-] Content frame data empty.")
                        
                    time.sleep(CHECK_INTERVAL)
                
                use_login_fallback = False

        except Exception as global_error:
            print(f"[!!] Production runtime loop exception caught: {global_error}")
            time.sleep(10)

if __name__ == "__main__":
    main()
                        
