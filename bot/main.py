import bot.config as config
from bot.msg import get
from bot.db import db
import telebot

telebot.apihelper.proxy = config.PROXY
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    bot.send_message(cid, get('ru', 'start'))


@bot.message_handler(commands=['add'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    bot.send_message(cid, get('ru', 'start'))


@bot.message_handler(commands=['show'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    bot.send_message(cid, get('ru', 'start'))


@bot.message_handler(content_types=["text"])
def print_message(m: telebot.types.Message):
    db.insert(m.json)


if __name__ == "__main__":
    bot.polling()
