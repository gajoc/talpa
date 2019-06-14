import pprint

from talpa.env import ensure_env
from talpa.provider import AllegroProvider
from talpa.utils import read_token, dumps

env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_"):
    BASE_URL = env("BASE_URL")

token_data = read_token('.tokens')

payload = {
    'category.id': '93615',
    'phrase': 'tenge',
}

ap = AllegroProvider(token=token_data['token'], base_url=BASE_URL)
search_result = ap.search(payload)
pprint.pprint(search_result)
dumps('data/search_result.json', data=search_result, overwrite=False)
