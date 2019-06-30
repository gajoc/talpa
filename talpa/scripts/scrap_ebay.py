import sys

from talpa.env import ensure_env
from talpa.harvester import EbayHarvester
from talpa.storage import ebay_db as edb
from talpa.utils import read_json
from talpa.webapi.ebay_client import EbayClient


env = ensure_env()

webapi_cfg = read_json('../.webapi_ebay')

MAX_QUERIES = sys.maxsize
MAX_ITEMS = sys.maxsize

c = EbayClient(webapi_cfg)
eh = EbayHarvester(client=c, storage=edb)

eh.run(query_limit=MAX_QUERIES, item_limit=MAX_ITEMS, interval=1)
