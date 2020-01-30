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

db = MongoDB()

if __name__ == "__main__":
    item = {"test": "test"}
    db.insert(item)
