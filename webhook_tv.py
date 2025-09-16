# webhook_tv.py
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 تنظیمات تلگرام — حتماً جایگزین کن
TELEGRAM_BOT_TOKEN = '8124995984:AAG6XQR-Ng589jcocNACB5Rz2dJ0xY2wJGI'
TELEGRAM_CHAT_ID = '-1002590101777'

def send_telegram_message(text):
    # ✅ URL اصلاح شده — بدون هیچ فاصله‌ای بعد از /bot
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        if response.status_code != 200:
            print("❌ خطا در ارسال به تلگرام:", response.text)
        else:
            print("✅ پیام به تلگرام ارسال شد.")
    except Exception as e:
        print("❌ Exception:", e)

@app.route('/webhook-tv', methods=['POST'])
def tradingview_webhook():
    try:
        data = request.get_json()
        if not 
            return jsonify({"error": "No JSON received"}), 400

        action = data.get('action', 'UNKNOWN')
        symbol = data.get('symbol', '---')
        side = data.get('side', '')
        price = data.get('price', '')
        new_value = data.get('new_value', '')
        time_str = data.get('time', '')

        if action == "OPEN":
            msg = f"🟢 *ورود به پوزیشن*\n📌 سهم: `{symbol}`\n🧭 جهت: {side}\n💰 قیمت: {price}\n⏱ زمان: {time_str}"
        elif action == "CLOSE":
            msg = f"🔴 *خروج از پوزیشن*\n📌 سهم: `{symbol}`\n🧭 جهت: {side}\n💰 قیمت: {price}\n⏱ زمان: {time_str}"
        elif action == "MODIFY":
            modify_type = data.get('type', '---')
            msg = f"🔧 *تغییر تنظیمات*\n📌 سهم: `{symbol}`\n✏️ نوع: {modify_type}\n🆕 مقدار جدید: {new_value}\n⏱ زمان: {time_str}"
        else:
            msg = f"⚠️ *اعلان ناشناخته*\n`{data}`"

        send_telegram_message(msg)
        return jsonify({"status": "success", "message": "Alert processed"}), 200

    except Exception as e:
        print("❌ Server Error:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ ضروری برای Railway — پورت رو از متغیر محیطی می‌خونه
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
