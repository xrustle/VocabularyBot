import json

with open('msg.json', encoding='utf-8') as json_data_file:
    messages = json.load(json_data_file)


def get(lang, message):
    return messages[lang][message]


def emoji(name):
    return messages['emoji'][name]
