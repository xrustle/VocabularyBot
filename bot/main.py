from bot.config import TOKEN, PROXY
from bot.msg import msg
from bot.db import db
import telebot
from telebot import apihelper, types

apihelper.proxy = PROXY
bot = telebot.TeleBot(TOKEN)

users = {}

find_markup = types.InlineKeyboardMarkup(row_width=1)
find_markup.add(types.InlineKeyboardButton(text=msg('ru', 'find_button'), switch_inline_query_current_chat=''))

add_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
add_markup.add(types.KeyboardButton(text=msg('ru', 'add_button')))

clear_markup = types.ReplyKeyboardRemove(selective=False)


def step_equals(user_id, step):
    user = users.get(user_id)
    if user:
        return user['step'] == step


@bot.message_handler(commands=['start'])
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    bot.send_message(cid, text=msg('ru', 'start_instruction'), reply_markup=add_markup)
    if cid not in users:
        users[cid] = {'step': 0}


@bot.message_handler(func=lambda m: m.text == msg('ru', 'add_button'))
def command_add_ru(m: telebot.types.Message):
    command_add(m)


@bot.message_handler(commands=['add'])
def command_add(m: telebot.types.Message):
    cid = m.chat.id
    users[cid] = {'step': 1}
    bot.send_message(cid, msg('ru', 'insert_word'), reply_markup=clear_markup)


@bot.message_handler(func=lambda m: step_equals(m.chat.id, 1))
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if not m.text:
        bot.send_message(cid, msg('ru', 'waiting_for_text'))
        return
    bot.send_message(cid, msg('ru', 'insert_translate'))
    users[cid] = {'step': 2,
                  'word': m.text}


@bot.message_handler(func=lambda m: step_equals(m.chat.id, 2))
def command_start(m: telebot.types.Message):
    cid = m.chat.id
    if not m.text:
        bot.send_message(cid, msg('ru', 'waiting_for_text'))
        return
    db.insert_word(cid, {'word': users[cid]['word'],
                         'definition': m.text})
    bot.send_message(cid,
                     msg('ru', 'word_was_inserted') + '\n\n*' + users[cid]['word'] + '* - ' + m.text,
                     parse_mode='markdown',
                     reply_markup=add_markup)
    users[cid] = {'step': 0}


@bot.inline_handler(func=lambda _: True)
def query_text(query):
    # func=lambda query: len(query.query) > 0
    # https://groosha.gitbook.io/telegram-bot-lessons/chapter7

    words = db.get_words(query.from_user.id)

    answer_list = [
        types.InlineQueryResultArticle(
            id=str(i), title=word['word'], description=word['definition'],
            input_message_content=types.InputTextMessageContent(
                message_text=f'*{word["word"]}* - {word["definition"]}', parse_mode='markdown')
        )
        for i, word in enumerate(words)
    ]
    bot.answer_inline_query(query.id, answer_list, cache_time=1)


if __name__ == "__main__":
    print('Bot started...')
    bot.polling()
