import json
import pprint

from talpa.env import ensure_env
from talpa.provider import AllegroProvider
from talpa.schema import SearchAllegroSchema
from talpa.utils import read_token, dumps

env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_"):
    BASE_URL = env("BASE_URL")

token_data = read_token('.tokens')
search_schema = SearchAllegroSchema(strict=True, many=True)

queries = json.load(open('queries.json', 'r'))
queries_loaded = search_schema.load(queries).data
queries_parsed = search_schema.dump(queries_loaded).data

ap = AllegroProvider(token=token_data['token'], base_url=BASE_URL)

for query in queries_parsed:
    search_result = ap.search(query)
    pprint.pprint(search_result)
    dumps('data/search_result.json', data=search_result, overwrite=False)
