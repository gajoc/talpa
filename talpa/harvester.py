import json
from itertools import chain
from time import sleep

from pymongo.errors import DuplicateKeyError

from talpa.provider import AllegroProvider
from talpa.schema import AllegroQuerySchema, EbayQuerySchema
from talpa.storage import AllegroMongoDB, EbayMongoDB
from talpa.utils import LimitedCounter, VerboseCounter
from talpa.utils_allegro import create_meta
from talpa.webapi.allegro_client import AllegroClient
from talpa.webapi.ebay_client import EbayClient
from talpa.webapi.utils import get_item_and_bids


class AllegroHarvester:

    def __init__(self, provider: AllegroProvider, storage: AllegroMongoDB):
        self.provider = provider
        self.storage = storage
        self.allegro_query_schema = AllegroQuerySchema()

    def update(self, limit: int, interval):
        limit_reached = LimitedCounter(limit, 'limit of queries reached')

        for query in self.storage.queries:
            if limit_reached():
                print(str(limit_reached))
                break

            query = self.allegro_query_schema.ensure_query_for_closed_items(query)
            allegro_query = self.parse_query_to_allegro_format(query)

            result = self.provider.search(allegro_query)
            if 'error' in result:
                raise ValueError(f'got error when querying {allegro_query}, \n'
                                 f'API response is\n{json.dumps(result, indent=4)}')
            print(f'queried for {allegro_query}')

            result['metadata'] = create_meta(query)
            self._dump_query_result(result)
            self._queue_items_to_download_from_query_result(result)

            sleep(interval)

    def run(self, client: AllegroClient, limit: int, interval):
        limit_reached = LimitedCounter(limit, 'limit of downloads reached')
        count_items = VerboseCounter('number of downloaded items')
        count_bids = VerboseCounter('number of downloaded bids')
        count_skipped = VerboseCounter('number of skipped items')

        def by_ending_date(q_item):
            return q_item['publication']['endingAt']

        for queued_item in sorted(self.storage.queued_items, key=by_ending_date):
            id_ = queued_item['id']

            if self.is_item_downloaded(id_):
                self.storage.queued_items.remove(id_)
                count_skipped()
                count_skipped.print('skipped item',
                                    id_,
                                    'closed at',
                                    by_ending_date(queued_item),
                                    'total skipped already')
                continue

            if limit_reached():
                print(limit_reached)
                break

            item, bids, present_in_service, msg = get_item_and_bids(_id=int(id_), client=client)
            if item:
                self._dump_downloaded_item(item)
                self.storage.queued_items.remove(id_)
                count_items()
                count_items.print('download item', id_,
                                  'ended at', by_ending_date(queued_item),
                                  'limit is', limit, 'current')
                sleep(interval)
            if bids:
                self._dump_downloaded_bids(bids)
                count_bids()
                sleep(interval)
            if not present_in_service:
                self.storage.queued_items.remove(id_)
                print('download item', id_, 'failed:', msg)

        print('\n'.join(['scrapping allegro finished:',
                         '+++++++++++++++++++++++++++', str(count_items), str(count_bids), str(count_skipped)]))

    def is_item_queued(self, allegro_id):
        if self.storage.queued_items.contains(allegro_id):
            return True
        return False

    def is_item_downloaded(self, allegro_id):
        if self.storage.items.contains(allegro_id):
            return True
        return False

    def parse_query_to_allegro_format(self, query):
        self.allegro_query_schema.validate(query)
        return self.allegro_query_schema.dump(query)

    def _dump_query_result(self, result):
        self.storage.searches.insert(result)

    def _dump_downloaded_item(self, item):
        self.storage.items.insert(item)

    def _dump_downloaded_bids(self, bids):
        self.storage.bids.insert(bids)

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


class EbayHarvester:

    def __init__(self, client: EbayClient, storage: EbayMongoDB):
        self.client = client
        self.storage = storage
        self.ebay_query_schema = EbayQuerySchema()

    def run(self, query_limit: int, item_limit: int, interval):
        query_limit_reached = LimitedCounter(query_limit, 'limit of queries reached')
        items_limit_reached = LimitedCounter(item_limit, 'limit of downloaded items reached')
        count_skipped = VerboseCounter('number of skipped items')
        count_items = VerboseCounter('number of downloaded items')

        for no, query in enumerate(self.storage.queries):

            if query_limit_reached():
                print(query_limit_reached)
                break

            self.ebay_query_schema.validate(query)
            parsed_query = self.ebay_query_schema.dump(query)
            print('query no.', no, parsed_query)
            result = self.client.search(parsed_query)
            sleep(interval)

            for item in result:
                deserialized_item = self.client.deserialize(item)
                try:
                    if items_limit_reached():
                        break
                    self.storage.items.insert(deserialized_item)
                    count_items()
                    count_items.print('download item', deserialized_item['itemId'],
                                      'ended at', deserialized_item['listingInfo']['endTime'],
                                      'limit is', item_limit, 'current')
                except DuplicateKeyError:
                    count_skipped()

            if items_limit_reached():
                print(items_limit_reached)
                break

        print('\n'.join(['scrapping ebay finished:',
                         '+++++++++++++++++++++++++++', str(count_items), str(count_skipped)]))
