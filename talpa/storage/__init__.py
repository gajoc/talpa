from talpa.env import ensure_env
from talpa.storage.tinydb import tiny_db, _QueriesCollection, _SearchesCollection, _QueuedItemsCollection, \
    _ItemsCollection, _BidsCollection


env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_TINYDB_"):
    ITEMS_TABLE = 'items'
    QUERIES_TABLE = 'queries'
    SEARCHES_TABLE = 'searches'
    QUEUED_ITEMS_TABLE = 'queued_items'
    BIDS_TABLE = 'bids'


class AllegroDB:

    queries = _QueriesCollection(tiny_db.table(QUERIES_TABLE))
    searches = _SearchesCollection(tiny_db.table(SEARCHES_TABLE))
    queued_items = _QueuedItemsCollection(tiny_db.table(QUEUED_ITEMS_TABLE))
    items = _ItemsCollection(tiny_db.table(ITEMS_TABLE))
    bids = _BidsCollection(tiny_db.table(BIDS_TABLE))


allegro_db = AllegroDB
