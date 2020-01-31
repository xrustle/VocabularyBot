from pymongo import MongoClient
from bot.config import MONGO


class MongoDB:
    def __init__(self):
        client = MongoClient(**MONGO['uri'])
        self.db = client.get_database(MONGO['db'])

    def insert_word(self, user_id, word):
        collection = self.db[str(user_id)]
        collection.insert_one(word)

    def get_words(self, user_id):
        collection = self.db[str(user_id)]
        return collection.find({})

    def get_search_results(self, user_id, search_query):
        collection = self.db[str(user_id)]
        return collection.find({'word': {'$regex': search_query}})


db = MongoDB()

res = db.get_search_results(844216, 'Word')
for i in res:
    print(i['word'])
