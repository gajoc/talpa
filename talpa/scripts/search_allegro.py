import argparse
import json

from talpa.env import ensure_env
from talpa.provider import AllegroProvider
from talpa.schema import SearchAllegroSchema
from talpa.utils import read_token, dumps

default_tokens_file = '../.tokens'
default_dump_file = '../data/search_result.json'


ap = argparse.ArgumentParser()
ap.add_argument('queries_file', help='path to file with allegro queries in json format',
                nargs='?',
                default='../queries.json')
args = ap.parse_args()


if __name__ == '__main__':
    env = ensure_env()
    with env.prefixed("TALPA_ALLEGRO_"):
        BASE_URL = env("BASE_URL")

    token = read_token(default_tokens_file)['token']
    search_schema = SearchAllegroSchema(strict=True, many=True)

    queries = json.load(open(args.queries_file, 'r'))
    queries_loaded = search_schema.load(queries).data
    queries_parsed = search_schema.dump(queries_loaded).data

    ap = AllegroProvider(token=token, base_url=BASE_URL)

    for query in queries_parsed:
        result = ap.search(query)
        dumps(default_dump_file, data=result, overwrite=False)