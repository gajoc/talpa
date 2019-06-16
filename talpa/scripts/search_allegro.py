import json
from random import randint
from time import sleep

from talpa import allegro_db as adb
from talpa.env import ensure_env
from talpa.provider import AllegroProvider
from talpa.schema import AllegroQuerySchema
from talpa.utils import read_token
from talpa.utils_allegro import create_meta

default_tokens_file = '../.tokens'
CLOSED_ITEMS_ONLY = True


if __name__ == '__main__':
    print(f'closed items mode is set as {CLOSED_ITEMS_ONLY}')
    env = ensure_env()
    with env.prefixed("TALPA_ALLEGRO_"):
        BASE_URL = env("BASE_URL")

    token = read_token(default_tokens_file)['token']
    ap = AllegroProvider(token=token, base_url=BASE_URL)

    schema = AllegroQuerySchema(strict=True)
    for q in adb.queries:
        if CLOSED_ITEMS_ONLY:
            q['search_mode'] = 'CLOSED'

        schema.validate(q)
        allegro_q = schema.dump(q).data

        print(f'searching for {allegro_q}...')
        result = ap.search(allegro_q)
        if 'error' in result:
            raise ValueError(f'got error when querying {allegro_q}, \nAPI response is\n{json.dumps(result, indent=4)}')
        result['metadata'] = create_meta(q)
        adb.searches.insert(result)
        sleep(randint(1, 3))

    print(f'processed {len(adb.queries)} queries.')
