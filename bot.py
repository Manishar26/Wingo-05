import os
import time
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = "9233968106:AAHnPv7OYYVTSXWxuSg1V_AfnYhuOffARA8"
CHAT_ID = "1181622773"

# Dummy HTTP Server to satisfy Render's Web Service port binding requirement for free tier
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"WinGo Bot is running 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("Telegram Send Error:", e)

def check_wingo():
    last_period = ""
    print("WinGo 30S 24/7 Bot Started...")
    send_telegram("🟢 <b>WinGo 30S Alert Bot Started!</b>\n0 or 5 vantha udane alert varum.")
    
    while True:
        try:
            url = "https://draw.ar-lottery01.com/WinGo/WinGo_30S/GetHistoryIssuePage.json?pageNo=1&pageSize=3&gameId=1"
            res = requests.get(url, timeout=10)
            if res.status_code == 200:
                data = res.json()
                latest = data['data']['list'][0]
                period = latest['issueNumber']
                num = int(latest['number'])

                if period != last_period:
                    last_period = period
                    print(f"Checked Period: {period} | Number: {num}")
                    if num == 0 or num == 5:
                        msg = f"🚨 <b>WINGO 30S ALERT!</b> 🚨\n\n🎯 <b>Number:</b> {num}\n📌 <b>Period:</b> <code>{period}</code>"
                        send_telegram(msg)
        except Exception as e:
            print("Fetch error:", e)
        
        time.sleep(3)

if __name__ == "__main__":
    # Start the HTTP server in a background thread so Render detects an open port
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run the main Wingo checker loop
    check_wingo()
    
