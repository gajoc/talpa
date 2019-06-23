from urllib.parse import quote_plus

from pymongo import MongoClient

from talpa.env import ensure_env
from talpa.storage import allegro_db as adb

env = ensure_env()

with env.prefixed("TALPA_"):
    MONGO_HOST = env("MONGO_HOST")
    MONGO_PORT = env("MONGO_PORT")
    MONGO_USERNAME = env("MONGO_USERNAME")
    MONGO_PASSWORD = env("MONGO_PASSWORD")
    MONGO_DB_NAME = env("MONGO_DB_NAME")

with env.prefixed("TALPA_ALLEGRO_MONGO_"):
    ITEMS_COLLECTION = env("ITEMS_COLLECTION")
    QUERIES_COLLECTION = env("QUERIES_COLLECTION")
    SEARCHES_COLLECTION = env("SEARCHES_COLLECTION")
    QUEUED_ITEMS_COLLECTION = env("QUEUED_ITEMS_COLLECTION")
    BIDS_COLLECTION = env("BIDS_COLLECTION")


uri = "mongodb://%s:%s@%s:%s" % (
    quote_plus(MONGO_USERNAME), quote_plus(MONGO_PASSWORD), MONGO_HOST, MONGO_PORT)
client = MongoClient(uri)
db = client[MONGO_DB_NAME]


def populate(collection, documents):
    result = collection.insert_many(documents)
    print(f'migration of {collection} done, inserted {len(result.inserted_ids)} documents')

# how do dump mongo data
# mongodump --out /data/backup/date like mongodump --out /data/backup/2019-06-23
# location /data/backup is binded with host folder in ~ dir (see docker-compose file)


populate(collection=db[ITEMS_COLLECTION], documents=list(adb.items))

populate(collection=db[QUERIES_COLLECTION], documents=list(adb.queries))

populate(collection=db[SEARCHES_COLLECTION], documents=list(adb.searches))

populate(collection=db[QUEUED_ITEMS_COLLECTION], documents=list(adb.queued_items))

populate(collection=db[BIDS_COLLECTION], documents=list(adb.bids))
