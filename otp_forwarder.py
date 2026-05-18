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
CHECK_INTERVAL = 10

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
        payload = {"chat_id": CHAT_ID, "text": message}
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
            print(f"[+] Backup Captcha Solved: {num1} + {num2} = {result}")
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
    print("[+] SMS PRODUCTION ENGINE (REAL-TIME FILTER MODE) ACTIVE")
    # Store sent messages to prevent duplicates
    sent_messages_pool = set()
    use_login_fallback = False
    
    while True:
        session = None
        try:
            session = build_bulletproof_session()
            
            if not use_login_fallback:
                print("\n[*] Handshaking fresh session via target cookie...")
                dashboard_response = session.get(API_URL, headers=HEADERS, timeout=20)
                
                if "Sign In" not in dashboard_response.text:
                    print("[+] Cookie authorized successfully. Streaming live data...")
                    
                    for loop_counter in range(100):
                        response = session.get(API_URL, headers=HEADERS, timeout=20)
                        
                        if "Sign In" in response.text:
                            print("[!] Cookie context dropped on host. Moving to login matrix...")
                            use_login_fallback = True
                            break
                            
                        dash_soup = BeautifulSoup(response.text, "html.parser")
                        
                        # Target Table Rows (Tr) ya text segments dhoondna
                        table_rows = dash_soup.find_all("tr")
                        
                        if table_rows:
                            # Table structure se data nikalna
                            for row in table_rows:
                                row_text = row.get_text(" ").strip()
                                # Filter logs, headers and empty spaces
                                if len(row_text) > 15 and "username" not in row_text.lower() and row_text not in sent_messages_pool:
                                    print(f"[+] New SMS detected in row parsing pool!")
                                    formatted_message = f"📩 NEW SMS RECEIVED\n\n{row_text[:3500]}"
                                    send_telegram(formatted_message)
                                    sent_messages_pool.add(row_text)
                        else:
                            # Fallback text blocking system agar website list elements standard na hon
                            current_text_layer = dash_soup.get_text("\n").strip()
                            if len(current_text_layer) > 30 and current_text_layer not in sent_messages_pool:
                                print("[+] New update found via fallback text layer!")
                                formatted_message = f"📩 NEW SMS RECEIVED (SNAPSHOT)\n\n{current_text_layer[:3500]}"
                                send_telegram(formatted_message)
                                sent_messages_pool.add(current_text_layer)
                        
                        # Pool size limit to maintain low RAM footprints
                        if len(sent_messages_pool) > 200:
                            sent_messages_pool.clear()
                            
                        print(f"[.] Sync Status: OK | Count: {loop_counter+1}/100 | Pool Size: {len(sent_messages_pool)}")
                        time.sleep(CHECK_INTERVAL)
                    continue
                else:
                    print("[-] Injected Cookie stream is stale/expired. Activating login routing...")
                    use_login_fallback = True

            if use_login_fallback:
                print("[*] Parsing panel HTML fields structure...")
                clean_headers = HEADERS.copy()
                if "Cookie" in clean_headers:
                    del clean_headers["Cookie"]
                    
                response = session.get(API_URL, headers=clean_headers, timeout=20)
                soup = BeautifulSoup(response.text, "html.parser")
                
                captcha_val = solve_captcha(soup)
                if not captcha_val:
                    print("[-] HTML Text Captcha missing. Sleeping thread...")
                    time.sleep(30)
                    continue
                    
                payload = {"username": USERNAME, "password": PASSWORD, "capt": captcha_val}
                login_response = session.post(API_URL, headers=clean_headers, data=payload, timeout=20)
                
                if "Sign In" in login_response.text or login_response.status_code != 200:
                    print("[-] Manual login fallback declined by host application.")
                    time.sleep(15)
                    continue
                    
                print("[+] Fallback Login Verified. Tracking active dashboard data stream...")
                
                for loop_counter in range(40):
                    dashboard_response = session.get(API_URL, headers=clean_headers, timeout=20)
                    if "Sign In" in dashboard_response.text:
                        break
                        
                    dash_soup = BeautifulSoup(dashboard_response.text, "html.parser")
                    table_rows = dash_soup.find_all("tr")
                    
                    if table_rows:
                        for row in table_rows:
                            row_text = row.get_text(" ").strip()
                            if len(row_text) > 15 and "username" not in row_text.lower() and row_text not in sent_messages_pool:
                                formatted_message = f"📩 NEW SMS RECEIVED (FALLBACK)\n\n{row_text[:3500]}"
                                send_telegram(formatted_message)
                                sent_messages_pool.add(row_text)
                    time.sleep(CHECK_INTERVAL)
                
                use_login_fallback = False

        except Exception as global_error:
            print(f"[!!] Production runtime loop caught error: {global_error}")
            time.sleep(10)

if __name__ == "__main__":
    main()
                    
