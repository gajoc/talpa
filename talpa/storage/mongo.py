from abc import ABC
from urllib.parse import quote_plus

from pymongo import MongoClient
from pymongo.collection import Collection

from talpa.env import ensure_env
from talpa.storage.base import BaseCollection


class MongoBaseCollection(BaseCollection, ABC):
    def __iter__(self):
        return self._a_collection.find()

    def __len__(self):
        return self._a_collection.count_documents({})


class _QueriesCollection(MongoBaseCollection, ABC):
    """
    queries __iter__
    """

    def __init__(self, a_collection: Collection):
        super().__init__(a_collection)


class _SearchesCollection(MongoBaseCollection, ABC):
    """
    searches.insert(query_result) simple append to collection or table
    """

    def __init__(self, a_collection: Collection):
        super().__init__(a_collection)

    def insert(self, search_result):
        self._a_collection.insert_one(search_result)


class _QueuedItemsCollection(MongoBaseCollection, ABC):
    """
    queued_items.contains(queued_item_id) this is allegro_id
    queued_items.insert(queued_item) item object from allegro search result
    queued_items.remove(queued_item_id) this is allegro_id
    queued_items __iter__

    """

    def __init__(self, a_collection: Collection):
        super().__init__(a_collection)

    def insert(self, queued_item):
        self._a_collection.insert_one(queued_item)

    def contains(self, id_) -> bool:
        # return self._a_collection.find(Query().id == id_)
        result = self._a_collection.find_one({'id': str(id_)})
        if result:
            return True
        return False

    def remove(self, id_):
        # item = self._a_collection.get(Query().id == id_)
        # if item:
        #     self._a_collection.remove(doc_ids=[item.doc_id])
        self._a_collection.delete_many({'id': str(id_)})


class _ItemsCollection(MongoBaseCollection, ABC):
    """
    items.contains(allegro_id)
    items.insert(item) downloaded item by webapi client

    """

    def __init__(self, a_collection: Collection):
        super().__init__(a_collection)

    def insert(self, item):
        self._a_collection.insert_one(item)

    def contains(self, id_) -> bool:
        # return self._a_collection.find(Query().itemListInfoExt.itId == int(id_))
        result = self._a_collection.find_one({'itemListInfoExt.itId': int(id_)})
        if result:
            return True
        return False


class _BidsCollection(MongoBaseCollection, ABC):
    """
    bids.insert_many(bids) downloaded list of bids for particular allegro item

    """

    def __init__(self, a_collection: Collection):
        super().__init__(a_collection)

    def insert(self, bids):
        self._a_collection.insert_many(bids)


env = ensure_env()

with env.prefixed("TALPA_"):
    MONGO_HOST = env("MONGO_HOST")
    MONGO_PORT = env("MONGO_PORT")
    MONGO_USERNAME = env("MONGO_USERNAME")
    MONGO_PASSWORD = env("MONGO_PASSWORD")
    MONGO_DB_NAME = env("MONGO_DB_NAME")


uri = "mongodb://%s:%s@%s:%s" % (
    quote_plus(MONGO_USERNAME), quote_plus(MONGO_PASSWORD), MONGO_HOST, MONGO_PORT)
client = MongoClient(uri)

mongo_db = client[MONGO_DB_NAME]
