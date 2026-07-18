import telebot
import os
from flask import Flask

# Token chuẩn của bồ
TOKEN = '8859495272:AÂEsFIB3L5sTzS3AEoFublF1qjZxAIB'
UIGO
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot dang chay!"

if __name__ == "__main__":
    import threading
    def run_bot():
        bot.infinity_polling()
    
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
