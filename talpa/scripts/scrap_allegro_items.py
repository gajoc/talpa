from talpa.env import ensure_env
from talpa.harvester import AllegroHarvester
from talpa.provider import AllegroProvider
from talpa.scripts.search_allegro import default_tokens_file
from talpa.storage import allegro_db as adb
from talpa.utils import read_json, read_token
from talpa.webapi.client import AllegroClient

env = ensure_env()

webapi_cfg = read_json('../.webapi')
with env.prefixed("TALPA_ALLEGRO_"):
    BASE_URL = env("BASE_URL")

if __name__ == '__main__':
    ap = AllegroProvider(token=
                         read_token(default_tokens_file)['token'],
                         base_url=BASE_URL)

    c = AllegroClient(url=webapi_cfg['URL'],
                      web_key=webapi_cfg['KEY'],
                      country_id=webapi_cfg['COUNTRY_ID'],
                      user=webapi_cfg['USER'])

    ah = AllegroHarvester(provider=ap, storage=adb)

    ah.run(client=c, limit=3, interval=1)
