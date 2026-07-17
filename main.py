import telebot
import random
import string
import json
import os
import base64
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string
import threading

# ==========================================
# CẤU HÌNH THÔNG TIN CHÍNH
# ==========================================
TOKEN = '8859495272:AAEnhxF0Jaz2GØ8qWj4YaMJf6vxvqGNjQXM'

# Nội dung file cấu hình của bồ đã được mã hóa Base64
SAFE_DATA_ENCODED = "W0dlbmVyYWxdCmRucy1zZXJ2ZXIgPSAxLjEuMS4xCltSdWxlXQpGSU5BTCxEUkVDVA=="
# ==========================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
KEY_FILE = "keys.json"

def get_clean_config():
    try:
        return base64.b64decode(SAFE_DATA_ENCODED).decode('utf-8')
    except:
        return "Error loading configuration."

def load_keys():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_keys(keys_data):
    with open(KEY_FILE, "w") as f:
        json.dump(keys_data, f, indent=4)

def generate_key():
    return f"KEY-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"

# --- TELEGRAM BOT CONTROL ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Chào mừng bồ!\n👉 Bấm /getkey để nhận mã kích hoạt (Hạn 24h).")

@bot.message_handler(commands=['getkey'])
def send_key(message):
    user_id = str(message.chat.id)
    keys_data = load_keys()
    
    # Render sẽ cung cấp một đường link web sau khi deploy thành công.
    # Bồ có thể điền link đó vào đây hoặc để người dùng tự truy cập.
    web_url = "ĐƯỜNG_LINK_WEB_RENDER_CỦA_BẠN"
    
    for key, info in keys_data.items():
        if info.get("user_id") == user_id:
            expire_time = datetime.strptime(info["expire_at"], "%Y-%m-%d %H:%M:%S")
            if datetime.now() < expire_time:
                bot.reply_to(message, f"⚠️ Bồ đã lấy key hôm nay rồi!\n🔑 Key: `{key}`\n🌐 Web nhập: {web_url}", parse_mode='Markdown')
                return

    new_key = generate_key()
    expire_at = (datetime.now() + timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
    keys_data[new_key] = {"user_id": user_id, "expire_at": expire_at}
    save_keys(keys_data)
    
    response_msg = (
        "🎉 **TẠO KEY THÀNH CÔNG!**\n\n"
        f"🔑 Key của bồ:\n`{new_key}`\n\n"
        f"🌐 **Trang kích hoạt:**\n{web_url}"
    )
    bot.send_message(message.chat.id, response_msg, parse_mode='Markdown')

# --- WEB PANEL CONTROL (FLASK) ---
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Verification System</title>
        <style>
            body { font-family: -apple-system, sans-serif; background: #0a0a0a; color: #fff; text-align: center; padding: 50px 20px; }
            input { padding: 14px; width: 80%; max-width: 300px; border-radius: 10px; border: 1px solid #333; margin-bottom: 15px; font-size: 16px; background: #1a1a1a; color: #fff; outline: none; }
            button { padding: 14px 25px; background: #2f80ed; color: #fff; border: none; border-radius: 10px; font-weight: bold; font-size: 16px; cursor: pointer; width: 85%; max-width: 326px; }
            .box { background: #121212; padding: 40px 20px; border-radius: 16px; display: inline-block; border: 1px solid #222; width: 90%; max-width: 400px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>🔑 Xác thực hệ thống</h2>
            <p style="color: #888; font-size: 14px; margin-bottom: 25px;">Nhập Key từ Bot Telegram để nhận file cấu hình</p>
            <form action="/verify" method="POST">
                <input type="text" name="key_code" placeholder="KEY-XXXXXX" required autocomplete="off"><br>
                <button type="submit">XÁC THỰC NGAY</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/verify', methods=['POST'])
def verify():
    user_key = request.form.get('key_code', '').strip()
    keys_data = load_keys()
    is_valid = False
    
    if user_key in keys_data:
        expire_time = datetime.strptime(keys_data[user_key]["expire_at"], "%Y-%m-%d %H:%M:%S")
        if datetime.now() < expire_time:
            is_valid = True
            
    if is_valid:
        config_content = get_clean_config()
        return render_template_string(f"""
        <html>
        <body style="background: #0a0a0a; color: #27ae60; font-family: -apple-system, sans-serif; padding: 20px; text-align: center;">
            <h2>🟢 Xác thực thành công!</h2>
            <p style="color: #888;">Copy nội dung bên dưới dán vào ứng dụng của bạn:</p>
            <textarea style="width: 90%; max-width: 500px; height: 250px; background: #121212; color: #fff; padding: 15px; border-radius: 12px; border: 1px solid #222; font-family: monospace; font-size: 13px;" readonly>{config_content}</textarea>
            <br><br><a href="/" style="color: #2f80ed; text-decoration: none;">Quay lại</a>
        </body>
        </html>
        """)
    else:
        return render_template_string("""
        <html>
        <body style="background: #0a0a0a; color: #eb5757; font-family: -apple-system, sans-serif; padding: 50px; text-align: center;">
            <h2>❌ Key không hợp lệ hoặc đã hết hạn!</h2>
            <p style="color: #888;">Vui lòng quay lại Bot Telegram để lấy key mới.</p>
            <a href="/" style="color: #2f80ed; text-decoration: none; font-weight: bold;">THỬ LẠI</a>
        </body>
        </html>
        """)

def run_web():
    # Render sẽ tự cấp cổng qua biến môi trường PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # Chạy Web Flask ở luồng phụ
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()
    
    # Chạy Bot Telegram ở luồng chính
    print("Hệ thống đang khởi động...")
    bot.infinity_polling()
