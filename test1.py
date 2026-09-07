import requests
from bs4 import BeautifulSoup
import time

# ==========================================
# 基礎設定
# ==========================================
stock_list = ["1101", "2330", "1102"]

# 你的 Bot Token
bot_token = "8100636404:AAEpe-ShnrXrToqaBujhVMBI-H_nOnn04m4"

# 你的 Telegram Chat ID
chat_id = "6310091238"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ==========================================
# 爬蟲與發送訊息主程式
# ==========================================
for stockid in stock_list:
    url = f"https://tw.stock.yahoo.com/quote/{stockid}.TW"
    
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 抓取股價 (包含跌、平盤、漲等 Class)
        price_element = soup.find('span', class_=[
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-down)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c)",
            "Fz(32px) Fw(b) Lh(1) Mend(16px) D(f) Ai(c) C($c-trend-up)"
        ])
        
        if price_element:
            price = price_element.getText()
            message = f"股票 {stockid} 即時股價為 {price}"
        else:
            message = f"股票 {stockid} 暫時無法獲取即時股價"
            
    except Exception as e:
        message = f"擷取股票 {stockid} 失敗：{e}"
    
    # 發送 Telegram 訊息
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}"
    
    try:
        requests.get(telegram_url)
        print(f"[成功發送] {message}")
    except Exception as e:
        print(f"[發送失敗] {e}")
    
    time.sleep(3)
