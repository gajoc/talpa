import pprint

import requests

from talpa.env import ensure_env
from talpa.utils import read_token

env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_"):
    CLIENT_ID = env("CLIENT_ID")
    API_KEY = env("API_KEY")
    CLIENT_SECRET = env("CLIENT_SECRET")
    BASE_URL = env("BASE_URL")

    data = read_token('.tokens')

    payload = {
        'category.id': '93615',
        'phrase': 'tenge',
    }

    headers = {
        'Accept': 'application/vnd.allegro.public.v1+json',
        'content-type': 'application/vnd.allegro.public.v1+json',
        'Authorization': 'Bearer %s' % data['token'],
    }

    r = requests.get(url=requests.compat.urljoin(BASE_URL, 'offers/listing'), headers=headers, params=payload)
    search_result = r.json()
    pprint.pprint(search_result)
