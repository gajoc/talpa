from datetime import datetime
from urllib.parse import quote_plus

from pymongo import MongoClient

from env import ensure_env

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
print(client)
db = client[MONGO_DB_NAME]
talpa_allegro_collection = db['posts-test']

post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.utcnow()}


post_id = talpa_allegro_collection.insert_one(post).inserted_id

print(f'inserted document got id {post_id}')
