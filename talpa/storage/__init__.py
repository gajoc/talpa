from talpa.storage.tinydb import tiny_db, _QueriesCollection, _SearchesCollection, _QueuedItemsCollection, \
    _ItemsCollection, _BidsCollection


class AllegroDB:

    queries = _QueriesCollection(tiny_db.table('queries'))
    searches = _SearchesCollection(tiny_db.table('searches'))
    queued_items = _QueuedItemsCollection(tiny_db.table('queued_items'))
    items = _ItemsCollection(tiny_db.table('items'))
    bids = _BidsCollection(tiny_db.table('bids'))


allegro_db = AllegroDB
