from talpa.env import ensure_env
from talpa.harvester import AllegroHarvester
from talpa.provider import AllegroProvider
from talpa.storage import allegro_db as adb
from talpa.utils import read_token

default_tokens_file = '../.tokens'
env = ensure_env()

with env.prefixed("TALPA_ALLEGRO_"):
    BASE_URL = env("BASE_URL")


if __name__ == '__main__':
    ap = AllegroProvider(token=
                         read_token(default_tokens_file)['token'],
                         base_url=BASE_URL)

    ah = AllegroHarvester(provider=ap, storage=adb)
    ah.update(interval=1)

    print(f'processed {len(adb.queries)} queries.')
    print(f'items in queue {len(adb.queued_items)}.')
