from tinydb import TinyDB


class AllegroDB(object):
    _allegro_db = TinyDB('../db/allegro_db.json')

    queries = _allegro_db.table('queries')
    items = _allegro_db.table('items')
    bids = _allegro_db.table('bids')
    searches = _allegro_db.table('searches')


allegro_db = AllegroDB
