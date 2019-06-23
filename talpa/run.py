from env import ensure_env

env = ensure_env()

with env.prefixed("TALPA_"):
    MONGO_HOST = env("MONGO_HOST")
    MONGO_PORT = env("MONGO_PORT")
    MONGO_USERNAME = env("MONGO_USERNAME")
    MONGO_PASSWORD = env("MONGO_PASSWORD")
    MONGO_DB_NAME = env("MONGO_DB_NAME")
