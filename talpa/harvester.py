import json
from time import sleep

from talpa import AllegroDB
from talpa.provider import AllegroProvider
from talpa.schema import AllegroQuerySchema
from talpa.utils_allegro import create_meta


class AllegroHarvester:

    def __init__(self, provider: AllegroProvider, storage: AllegroDB):
        self.provider = provider
        self.storage = storage

    def update(self, interval):
        schema = AllegroQuerySchema(strict=True)

        for query in self.storage.queries:

            query = schema.ensure_query_for_closed_items(query)
            schema.validate(query)
            allegro_query = schema.dump(query).data

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

    def _dump_query_result(self, result):
        self.storage.searches.insert(result)

    def _queue_items_to_download_from_query_result(self, result):
        pass

    # @TODO what about item bids? implement extra check or base on item check only?
    def _item_already_downloaded(self, id_):
        pass
