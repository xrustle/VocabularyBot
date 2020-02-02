import json
import os

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, 'msg.json'), encoding='utf-8') as json_data_file:
    messages = json.load(json_data_file)


def msg(lang, message):
    return messages[lang][message]


def emoji(name):
    return messages['emoji'][name]
