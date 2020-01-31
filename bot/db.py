from pymongo import MongoClient
from bot.config import MONGO
import re


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
        regexp = re.compile(rf'{search_query}', re.IGNORECASE)
        return collection.find({'word': {'$regex': regexp}})


db = MongoDB()
