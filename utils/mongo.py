from pymongo import MongoClient


class Mongo:
    def __init__(self, collection):
        self.client = MongoClient()
        self.db = self.client.harrybotter
        self.collection = self.db[collection]

    def check_user_location_exists(self, user_id):
        return self.collection.find({'user_id': user_id, 'location.long': {'$exists': True}}).count() > 0

    def check_user_location_no(self, user_id):
        return self.collection.find({'user_id': user_id, 'location': False}).count() > 0

    def check_user_ready(self, user_id):
        return False if self.collection.find({'user_id': user_id}).count() == 0 else \
            self.collection.find_one({'user_id': user_id})['ready']

    def check_user_wants(self, user_id):
        return True if self.collection.find({'user_id': user_id, 'wants': {'$exists': True}}).count() == 0 else \
            self.collection.find_one({'user_id': user_id})['wants']

    def get_user_location(self, user_id):
        return self.collection.find_one({'user_id': user_id})['location']

    def insert_user_location(self, user_id, location):
        self.collection.update({'user_id': user_id}, {'$set': {'location': location}}, upsert=True)

    def insert_user_ready(self, user_id, ready):
        self.collection.update({'user_id': user_id}, {'$set': {'ready': ready}}, upsert=True)

    def insert_user_wants(self, user_id, wants):
        self.collection.update({'user_id': user_id}, {'$set': {'wants': wants}}, upsert=True)
