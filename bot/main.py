from bot.config import TOKEN, PROXY
from bot.msg import msg
from bot.db import db
import telebot
from telebot import apihelper

# telebot.apihelper.proxy = PROXY
bot = telebot.TeleBot(TOKEN)
users = {}


def delete_messages(chat_id, msg_list):
    for message in msg_list:
        try:
            apihelper.delete_message(TOKEN, chat_id, message)
        except apihelper.ApiException:
            pass


@bot.message_handler(commands=['start'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if db.is_user_in_db(cid):
        bot.send_message(cid, msg('ru', 'already_in'))
    else:
        db.add_update_user({'_id': cid, 'step': 0, 'messages': []})
        bot.send_message(cid, msg('ru', 'user_added'))


@bot.message_handler(commands=['add'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if not db.is_user_in_db(cid):
        command_start(m)
    message = bot.send_message(cid, msg('ru', 'insert_word'))
    db.set_user(cid, 1, message=m.message_id)
    db.set_user(cid, 1, message=message.message_id)


@bot.message_handler(func=lambda message: db.get_user(message.chat.id)['step'] == 1)
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if not m.text:
        db.set_user(cid, 1, message=m.message_id)
        message = bot.send_message(cid, msg('ru', 'waiting_for_text'))
        db.set_user(cid, 1, message=message.message_id)
        return
    message = bot.send_message(cid, msg('ru', 'insert_translate'))
    db.add_update_user({'_id': cid})
    db.set_user(cid, 2, word=m.text, message=m.message_id)
    db.set_user(cid, 2, word=m.text, message=message.message_id)


@bot.message_handler(func=lambda message: db.get_user(message.chat.id)['step'] == 2)
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if not m.text:
        db.set_user(cid, 2, message=m.message_id)
        message = bot.send_message(cid, msg('ru', 'waiting_for_text'))
        db.set_user(cid, 2, message=message.message_id)
        return
    word = db.get_user(cid)['word']
    db.insert_word(cid, {'word': word,
                         'definition': m.text})
    bot.send_message(cid, msg('ru', 'word_was_inserted'))
    db.set_user(cid, 0, message=m.message_id)
    delete_messages(cid, db.get_user(cid)['messages'])
    db.set_user(cid, message='cleanup')
    bot.send_message(cid, word + ' - ' + m.text)


@bot.message_handler(commands=['show'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    bot.send_message(cid, msg('ru', 'start'))


if __name__ == "__main__":
    print('Bot started...')
    bot.polling()
