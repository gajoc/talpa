from talpa.env import ensure_env
from talpa.storage.mongo import mongo_db, _QueriesCollection, _SearchesCollection, _QueuedItemsCollection, \
    _ItemsCollectionAllegro, _BidsCollection

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
    items = _ItemsCollection(mongo_db[ITEMS_COLLECTION])
    bids = _BidsCollection(mongo_db[BIDS_COLLECTION])


allegro_db = AllegroMongoDB
