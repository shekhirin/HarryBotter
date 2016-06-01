from utils.mongo import Mongo


def connection_test():
    mongo = Mongo('users')
    mongo.collection.insert({'test': 1})
    assert mongo.collection.find_one({'test': 1}) is not None
    mongo.collection.delete_many({'test': 1})
    assert mongo.collection.find_one({'test': 1}) is None


def get_user_location_test():
    mongo = Mongo('users')
    mongo.collection.insert({'user_id': 1, 'location': {'lat': 1, 'long': 2}})
    location = mongo.get_user_location(1)
    assert location['lat'] == 1
    assert location['long'] == 2


def set_lang_test():
    mongo = Mongo('users')
    mongo.set_lang(1, 'en')
    assert mongo.get_user_lang(1) == 'en'
