from abc import ABC

from tinydb import Query
from tinydb.database import Table, TinyDB

from talpa.env import ensure_env
from talpa.storage.base import BaseCollection


class _QueriesCollection(BaseCollection, ABC):
    """
    queries __iter__
    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)


class _SearchesCollection(BaseCollection, ABC):
    """
    searches.insert(query_result) simple append to collection or table
    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)

    def insert(self, search_result):
        self._a_collection.insert(search_result)


class _QueuedItemsCollection(BaseCollection, ABC):
    """
    queued_items.contains(queued_item_id) this is allegro_id
    queued_items.insert(queued_item) item object from allegro search result
    queued_items.remove(queued_item_id) this is allegro_id
    queued_items __iter__

    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)

    def insert(self, queued_item):
        self._a_collection.insert(queued_item)

    def contains(self, id_) -> bool:
        return self._a_collection.contains(Query().id == id_)

    def remove(self, id_):
        item = self._a_collection.get(Query().id == id_)
        if item:
            self._a_collection.remove(doc_ids=[item.doc_id])


class _ItemsCollection(BaseCollection, ABC):
    """
    items.contains(allegro_id)
    items.insert(item) downloaded item by webapi client

    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)

    def insert(self, item):
        self._a_collection.insert(item)

    def contains(self, id_) -> bool:
        return self._a_collection.contains(Query().itemListInfoExt.itId == int(id_))


class _BidsCollection(BaseCollection, ABC):
    """
    bids.insert_many(bids) downloaded list of bids for particular allegro item

    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)

    def insert(self, bids):
        self._a_collection.insert_multiple(bids)


env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_TINYDB_"):
    DB_FILE = env("DB_FILE")

tiny_db = TinyDB(DB_FILE)
