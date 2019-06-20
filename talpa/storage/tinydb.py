from abc import ABC

from tinydb import Query
from tinydb.database import Table, TinyDB

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
        self._a_collection.remove(doc_ids=[id_])


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
        return self._a_collection.contains(Query().itemListInfoExt.itId == id_)


class _BidsCollection(BaseCollection, ABC):
    """
    bids.insert_many(bids) downloaded list of bids for particular allegro item

    """

    def __init__(self, a_collection: Table):
        super().__init__(a_collection)

    def insert(self, bids):
        self._a_collection.insert_multiple(bids)


class AllegroDB:
    _allegro_db = TinyDB('../db/allegro_db.json')

    queries = _QueriesCollection(_allegro_db.table('queries'))
    searches = _SearchesCollection(_allegro_db.table('searches'))
    queued_items = _QueuedItemsCollection(_allegro_db.table('queued_items'))
    items = _ItemsCollection(_allegro_db.table('items'))
    bids = _BidsCollection(_allegro_db.table('bids'))


allegro_db = AllegroDB
