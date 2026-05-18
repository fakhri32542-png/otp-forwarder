import os
import re
import time
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

# ==============================================================================
# CONFIGURATION
# ==============================================================================
API_URL = "http://139.99.68.231/ints/agent/SMSCDRStats"
USERNAME = "Furqan32"
PASSWORD = "Furqan32"
BOT_TOKEN = "8705044326:AAG4HZjHJ0JThaMc0BCkqFJ1yakyus_JraQ"
CHAT_ID = "-1003824926404"
CHECK_INTERVAL = 4  # Polling interval optimized for instant delivery

# Active session token
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

def send_telegram(message):
    try:
        telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(telegram_url, data=payload, timeout=15)
        print(f"[Telegram Alert]: Status Code -> {response.status_code}")
    except Exception as e:
        print(f"[-] Telegram Delivery Error: {e}")

def solve_captcha(soup_object):
    try:
        page_text = soup_object.get_text()
        match = re.search(r'(\d+)\s*\+\s*(\d+)', page_text)
        if match:
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            result = num1 + num2
            return str(result)
    except Exception as e:
        print(f"[-] Captcha Solving Error: {e}")
    return None

def build_bulletproof_session():
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=5)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def main():
    print("[+] SMS PRODUCTION ENGINE (TOP-ROW LIVE INSTANT TRACKER) ACTIVE")
    # Sirf aakhri bheje gaye naye OTP ki state save rakhne ke liye variable
    last_processed_otp_signature = ""
    use_login_fallback = False
    
    while True:
        session = None
        try:
            session = build_bulletproof_session()
            
            if not use_login_fallback:
                print("\n[*] Connecting secure sync channel...")
                dashboard_response = session.get(API_URL, headers=HEADERS, timeout=20)
                
                if "Sign In" not in dashboard_response.text:
                    print("[+] Cookie authorized successfully. Monitoring TOP row only...")
                    
                    for loop_counter in range(250):
                        response = session.get(API_URL, headers=HEADERS, timeout=20)
                        
                        if "Sign In" in response.text:
                            print("[!] Session expired natively. Shifting to backup login...")
                            use_login_fallback = True
                            break
                            
                        dash_soup = BeautifulSoup(response.text, "html.parser")
                        rows = dash_soup.find_all("tr")
                        
                        target_row_data = None
                        
                        # Filter rows to find the actual first data row, skipping system headers
                        for row in rows:
                            cells = row.find_all("td")
                            if cells:
                                row_text_check = row.get_text(" ").strip()
                                if not any(k in row_text_check.lower() for k in ["dashboard", "sign out", "navigation", "total rows"]):
                                    # Yeh hamari sabse top wali valid data row hai
                                    target_row_data = [cell.get_text(" ").strip() for cell in cells if cell.get_text().strip()]
                                    break
                        
                        # Agar koi valid data line mili hai
                        if target_row_data and len(target_row_data) >= 2:
                            current_signature = " | ".join(target_row_data)
                            
                            # 🚨 AGAR YEH SIGNATURE LATEST VALE SE ALAG HAI TO ISKA MATLAB NAYA SMS AYA HAI
                            if current_signature != last_processed_otp_signature:
                                print(f"[+] ⚡ FRESH TOP-ROW OTP DETECTED!")
                                
                                # Beautiful layout message template for Telegram
                                formatted_message = "📩 *NEW LATEST SMS RECEIVED*\n\n"
                                for index, val in enumerate(target_row_data):
                                    formatted_message += f"🔹 *Field {index+1}:* `{val}`\n"
                                    
                                send_telegram(formatted_message)
                                # Update signature to current one to lock duplication
                                last_processed_otp_signature = current_signature
                            else:
                                print(f"[.] Sync Status: Stable | No new update on top row.")
                        else:
                            print("[-] No valid data row detected on the page template.")
                            
                        time.sleep(CHECK_INTERVAL)
                    continue
                else:
                    print("[-] Injected PHPSESSID token cookie is expired. Switching to form login...")
                    use_login_fallback = True

            # ==============================================================================
            # PLAN B: FALLBACK AUTO-LOGIN
            # ==============================================================================
            if use_login_fallback:
                print("[*] Parsing panel HTML forms framework...")
                clean_headers = HEADERS.copy()
                if "Cookie" in clean_headers:
                    del clean_headers["Cookie"]
                    
                response = session.get(API_URL, headers=clean_headers, timeout=20)
                soup = BeautifulSoup(response.text, "html.parser")
                
                captcha_val = solve_captcha(soup)
                if not captcha_val:
                    print("[-] Captcha frame unrecognized. Waiting for valid context...")
                    time.sleep(30)
                    continue
                    
                payload = {"username": USERNAME, "password": PASSWORD, "capt": captcha_val}
                login_response = session.post(API_URL, headers=clean_headers, data=payload, timeout=20)
                
                if "Sign In" in login_response.text or login_response.status_code != 200:
                    print("[-] Manual login fallback declined by application host.")
                    time.sleep(15)
                    continue
                    
                print("[+] Fallback Handshake Complete. Activating top-row monitor...")
                
                for loop_counter in range(40):
                    dashboard_response = session.get(API_URL, headers=clean_headers, timeout=20)
                    if "Sign In" in dashboard_response.text:
                        break
                        
                    dash_soup = BeautifulSoup(dashboard_response.text, "html.parser")
                    rows = dash_soup.find_all("tr")
                    
                    fallback_row = None
                    for row in rows:
                        cells = row.find_all("td")
                        if cells:
                            row_text_check = row.get_text(" ").strip()
                            if not any(k in row_text_check.lower() for k in ["dashboard", "sign out", "navigation"]):
                                fallback_row = [cell.get_text(" ").strip() for cell in cells if cell.get_text().strip()]
                                break
                                
                    if fallback_row and len(fallback_row) >= 2:
                        current_signature = " | ".join(fallback_row)
                        if current_signature != last_processed_otp_signature:
                            formatted_message = "📩 *NEW LATEST SMS RECEIVED (FALLBACK)*\n\n"
                            for index, val in enumerate(fallback_row):
                                formatted_message += f"🔹 *Field {index+1}:* `{val}`\n"
                            send_telegram(formatted_message)
                            last_processed_otp_signature = current_signature
                            
                    time.sleep(CHECK_INTERVAL)
                
                use_login_fallback = False

        except Exception as global_error:
            print(f"[!!] Production runtime loop caught error: {global_error}")
            time.sleep(10)

if __name__ == "__main__":
    main()
                
