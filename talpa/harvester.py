import json
from itertools import chain
from time import sleep

from tinydb import Query

from talpa import AllegroDB
from talpa.provider import AllegroProvider
from talpa.schema import AllegroQuerySchema
from talpa.utils_allegro import create_meta


class AllegroHarvester:

    def __init__(self, provider: AllegroProvider, storage: AllegroDB):
        self.provider = provider
        self.storage = storage
        self.allegro_query_schema = AllegroQuerySchema(strict=True)

    def update(self, interval):

        for query in self.storage.queries:

            query = self.allegro_query_schema.ensure_query_for_closed_items(query)
            allegro_query = self.parse_query_to_allegro_format(query)

            result = self.provider.search(allegro_query)
            if 'error' in result:
                raise ValueError(f'got error when querying {allegro_query}, \n'
                                 f'API response is\n{json.dumps(result, indent=4)}')

            result['metadata'] = create_meta(query)
            self._dump_query_result(result)
            self._queue_items_to_download_from_query_result(result)

            sleep(interval)

    def run(self, limit, interval):
        pass

    def is_item_queued(self, allegro_id):
        if self.storage.queued_items.contains(Query().id == allegro_id):
            return True
        return False

    def parse_query_to_allegro_format(self, query):
        self.allegro_query_schema.validate(query)
        return self.allegro_query_schema.dump(query).data

    def _dump_query_result(self, result):
        self.storage.searches.insert(result)

    @staticmethod
    def _chain_items_from_query_result(result):
        promoted = result['items']['promoted']
        regular = result['items']['regular']
        return chain(promoted, regular)

    def _queue_items_to_download_from_query_result(self, result):
        query_result_items = self._chain_items_from_query_result(result)

        for item in query_result_items:
            if self.is_item_queued(allegro_id=item['id']):
                continue
            self.storage.queued_items.insert(item)
