from pymongo import MongoClient
from bot.config import MONGO


class MongoDB:
    def __init__(self):
        client = MongoClient(**MONGO['uri'])
        self.db = client.get_database(MONGO['db'])

    def insert_user(self, record, coll_name='test'):
        collection = self.db[coll_name]
        collection.insert_one(record)

    def is_user_in_db(self, user_id):
        collection = self.db['users']
        ret = True if collection.find_one({'_id': user_id}) else False
        return ret

    def add_update_user(self, user):
        collection = self.db['users']
        collection.update_one({'_id': user['_id']},
                              {'$set': user},
                              upsert=True)

    def insert_word(self, user_id, word):
        collection = self.db[str(user_id)]
        collection.insert_one(word)

    def get_user(self, user_id):
        collection = self.db['users']
        user = collection.find_one({'_id': user_id})
        return user

    def set_user(self, user_id, step=0, word=None, message=None):
        collection = self.db['users']
        collection.update_one({'_id': user_id},
                              {'$set': {'step': step,
                                        'word': word}})
        if message == 'cleanup':
            collection.update_one({'_id': user_id},
                                  {'$set': {'messages': []}})
        elif message:
            collection.update_one({'_id': user_id},
                                  {'$push': {'messages': message}},
                                  upsert=True)


db = MongoDB()

if __name__ == "__main__":
    item = {"test": "test"}
    db.insert(item)
