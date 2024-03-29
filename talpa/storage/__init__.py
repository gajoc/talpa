from talpa.env import ensure_env
from talpa.storage.mongo import mongo_db, _QueriesCollection, _SearchesCollection, _QueuedItemsCollection, \
    _ItemsCollectionAllegro, _BidsCollection, _ItemsCollectionEbay

env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_MONGO_"):
    ITEMS_COLLECTION = env("ITEMS_COLLECTION")
    QUERIES_COLLECTION = env("QUERIES_COLLECTION")
    SEARCHES_COLLECTION = env("SEARCHES_COLLECTION")
    QUEUED_ITEMS_COLLECTION = env("QUEUED_ITEMS_COLLECTION")
    BIDS_COLLECTION = env("BIDS_COLLECTION")


class AllegroMongoDB:

    queries = _QueriesCollection(mongo_db[QUERIES_COLLECTION])
    searches = _SearchesCollection(mongo_db[SEARCHES_COLLECTION])
    queued_items = _QueuedItemsCollection(mongo_db[QUEUED_ITEMS_COLLECTION])
    items = _ItemsCollectionAllegro(mongo_db[ITEMS_COLLECTION])
    bids = _BidsCollection(mongo_db[BIDS_COLLECTION])


with env.prefixed("TALPA_EBAY_MONGO_"):
    E_ITEMS_COLLECTION = env("ITEMS_COLLECTION")
    E_QUERIES_COLLECTION = env("QUERIES_COLLECTION")


class EbayMongoDB:

    queries = _QueriesCollection(mongo_db[E_QUERIES_COLLECTION])
    items = _ItemsCollectionEbay(mongo_db[E_ITEMS_COLLECTION])


allegro_db = AllegroMongoDB
ebay_db = EbayMongoDB
