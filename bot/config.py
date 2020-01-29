import json

with open('config.json', encoding='utf-8') as json_data_file:
    conf = json.load(json_data_file)

TOKEN = conf['bot_token']
PROXY = conf['proxy']
MONGO = conf['mongo']
