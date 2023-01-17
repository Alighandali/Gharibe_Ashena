import os
import telebot

# initialize bot
bot = telebot.TeleBot(
    os.environ['BOT_TOKEN'], parse_mode='HTML'
)
