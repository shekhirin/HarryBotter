from pymongo import MongoClient


class Mongo:
    def __init__(self, collection):
        self.client = MongoClient()
        self.db = self.client.harrybotter
        self.collection = self.db[collection]

    def is_user_first_contact(self, user_id):
        return True if self.collection.find({'user_id': user_id, 'first_time': {'$exists': True}})\
                           .count() == 0 else self.collection.find_one({'user_id': user_id})['first_time']

    def is_user_location_exists(self, user_id):
        return self.collection.find({'user_id': user_id, 'location.long': {'$exists': True}}).count() > 0

    def is_user_ready(self, user_id):
        return False if self.collection.find({'user_id': user_id, 'ready': {'$exists': True}})\
                            .count() == 0 else self.collection.find_one({'user_id': user_id})['ready']

    def is_user_wants(self, user_id):
        return True if self.collection.find({'user_id': user_id, 'wants': {'$exists': True}})\
                           .count() == 0 else self.collection.find_one({'user_id': user_id})['wants']

    def is_awaiting(self, user_id):
        return False if self.collection.find({'user_id': user_id, 'awaiting': {'$exists': True}})\
                            .count() == 0 else self.collection.find_one({'user_id': user_id})['awaiting']

    def get_user_location(self, user_id):
        return self.collection.find_one({'user_id': user_id})['location']

    def get_user_lang(self, user_id):
        return self.collection.find_one({'user_id': user_id})['lang']

    def insert_user_location(self, user_id, location):
        self.collection.update({'user_id': user_id}, {'$set': {'location': location}}, upsert=True)

    def insert_user_ready(self, user_id, ready):
        self.collection.update({'user_id': user_id}, {'$set': {'ready': ready}}, upsert=True)

    def insert_user_wants(self, user_id, wants):
        self.collection.update({'user_id': user_id}, {'$set': {'wants': wants}}, upsert=True)

    def user_made_first_contact(self, user_id, status):
        self.collection.update({'user_id': user_id}, {'$set': {'first_time': not status}}, upsert=True)

    def set_awaiting(self, user_id, status):
        self.collection.update({'user_id': user_id}, {'$set': {'awaiting': status}}, upsert=True)

    def set_lang(self, user_id, lang):
        self.collection.update({'user_id': user_id}, {'$set': {'lang': lang}}, upsert=True)
