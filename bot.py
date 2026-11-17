import os
import time
import requests

# Render Environment Variables or direct fallback
TOKEN = os.environ.get("BOT_TOKEN", "UNGA_BOT_TOKEN_INGE_PODUNGA")
CHAT_ID = os.environ.get("CHAT_ID", "UNGA_CHAT_ID_INGE_PODUNGA")

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
    check_wingo()
