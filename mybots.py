import telebot

TOKEN = '8859495272:AAGCMFIQy_X60dPq0Uss_TzseyVjIRP82gQ'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot đã sẵn sàng! Gửi /getkey để nhận key.")

@bot.message_handler(commands=['getkey'])
def get_key(message):
    bot.reply_to(message, "Key của bồ là: VIETANH-VIP-2026")

print("Bot dang chay...")
bot.polling()
