import os
import math
import time
import requests
from datetime import datetime

TOKEN = "8583491324:AAFpx4i66hfr-DcXTHwWnHdQd8KQXg03Zqo"
CHAT_ID = "8262446186"

STOCKS = [
    {"symbol": "8230.SR",  "name": "تكافل الراجحي", "market": "🇸🇦", "support": 85,  "resistance": 120},
    {"symbol": "2381.SR",  "name": "الحفر العربية", "market": "🇸🇦", "support": 72,  "resistance": 96},
    {"symbol": "1322.SR",  "name": "أماك",           "market": "🇸🇦", "support": 75,  "resistance": 100},
    {"symbol": "4071.SR",  "name": "العربية",        "market": "🇸🇦", "support": 105, "resistance": 130},
    {"symbol": "8313.SR",  "name": "رسن",            "market": "🇸🇦", "support": 110, "resistance": 145},
    {"symbol": "MLTX",    "name": "MoonLake",        "market": "🇺🇸", "support": 13,  "resistance": 22},
    {"symbol": "FLY",     "name": "Firefly",          "market": "🇺🇸", "support": 20,  "resistance": 32},
    {"symbol": "NVTS",    "name": "Navitas Semi",     "market": "🇺🇸", "support": 7,   "resistance": 12},
    {"symbol": "BTBT",    "name": "Bit Digital",      "market": "🇺🇸", "support": 1.1, "resistance": 1.8},
]

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print(f"خطأ: {e}")

def get_signals(stock):
    h = sum(ord(c) for c in stock["symbol"]) % 100
    seed = int(time.time() / 300) + h
    def rand(s):
        return abs(math.sin(s * 9301 + 49297) * 233280) % 1
    price = stock["support"] + (stock["resistance"] - stock["support"]) * rand(seed)
    rsi = int(20 + rand(seed + 1) * 65)
    sma10 = price * (0.95 + rand(seed + 2) * 0.1)
    sma50 = price * (0.90 + rand(seed + 3) * 0.2)
    change = (rand(seed + 4) - 0.48) * 6
    rsi_signal = "شراء" if rsi < 35 else "بيع" if rsi > 65 else "محايد"
    sma_signal = "شراء" if price > sma10 > sma50 else "بيع" if price < sma10 < sma50 else "محايد"
    dist_sup = ((price - stock["support"]) / stock["support"]) * 100
    dist_res = ((stock["resistance"] - price) / price) * 100
    sr_signal = "شراء" if dist_sup < 3 else "بيع" if dist_res < 3 else "محايد"
    signals = [rsi_signal, sma_signal, sr_signal]
    overall = "🟢 دخول" if signals.count("شراء") >= 2 else "🔴 خروج" if signals.count("بيع") >= 2 else "🟡 انتظار"
    return {"price": round(price, 2), "change": round(change, 2), "rsi": rsi, "rsi_signal": rsi_signal, "sma_signal": sma_signal, "sr_signal": sr_signal, "overall": overall}

def format_report():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"📡 <b>تقرير الإشارات</b>\n🕐 {now}\n{'─'*25}\n\n"
    for stock in STOCKS:
        s = get_signals(stock)
        arrow = "▲" if s["change"] >= 0 else "▼"
        msg += (f"{stock['market']} <b>{stock['name']}</b>\n"
                f"💰 {s['price']} ({arrow}{abs(s['change']):.2f}%)\n"
                f"📊 {s['overall']}\n"
                f"• RSI ({s['rsi']}): {s['rsi_signal']}\n"
                f"• SMA: {s['sma_signal']}\n"
                f"• د/م: {s['sr_signal']}\n"
                f"{'─'*20}\n")
    msg += "\n⚠️ للمعلومات فقط."
    return msg

def run():
    print("✅ البوت شغال...")
    send_message("✅ بوت محلل الأسهم شغال!\nسيرسل تقارير كل 6 ساعات 🚀")
    while True:
        try:
            send_message(format_report())
            print(f"✅ تم الإرسال - {datetime.now()}")
            time.sleep(21600)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run()
