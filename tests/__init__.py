from utils.mongo import Mongo


def teardown_package():
    mongo = Mongo('users')
    mongo.collection.remove({})