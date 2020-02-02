import json
import os

path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(path, 'config.json'), encoding='utf-8') as json_data_file:
    conf = json.load(json_data_file)

TOKEN = conf['bot_token']
PROXY = conf['proxy']
PROXY_ON = conf['proxy_on']
MONGO = conf['mongo']
