import telebot
import os

TOKEN = '8859495272:AAENaN6dYnV7oGgmtlG7Ygv2DRg9AQlelbw'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Bot đã sẵn sàng! Gửi /getkey để nhận key nhé.")

@bot.message_handler(commands=['getkey'])
def get_key(message):
    bot.reply_to(message, "Key của bồ là: VIETANH-VIP-2026")

print("Bot đang chạy ngon lành...")
bot.polling()
