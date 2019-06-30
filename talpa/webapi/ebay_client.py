"""
Created on May 24, 2017

@author: pawel
"""

import time
import calendar
import logging

from ebaysdk.finding import Connection
from ebaysdk.response import ResponseDataObject


class EbayClient(object):

    def __init__(self, config):
        self._config = config
        self._client = Connection(domain=self._config['domain'], debug=False,
                                  appid=self._config['appid'],
                                  config_file=None,
                                  siteid=self._config['siteid'])
        self._logger = logging.getLogger(__name__)

    def search(self, query, add_download_time=True):
        """
        Query ebay for items and return results.

        :param add_download_time:
        :param query: user query values.
        :type query: dict

        :returns: items (see ebay FindingAPI docs)
        :rtype: list

        .. note::
            Search is provided only in completed items. For more info see
            findCompletedItems function in ebay FindingAPI.
        """

        '''
        # query for each page result based on paginationOutput
        <paginationOutput> PaginationOutput
            <entriesPerPage> int </entriesPerPage>
            <pageNumber> int </pageNumber>
            <totalEntries> int </totalEntries>
            <totalPages> int </totalPages>
        </paginationOutput>
        sample responses:
        {'totalPages': '4', 'pageNumber': '1', 'totalEntries': '369', 'entriesPerPage': '100'}
        {'pageNumber': '0', 'totalPages': '0', 'entriesPerPage': '100', 'totalEntries': '0'}
        '''

        ebay_pages_per_query_limit = 100
        results = []
        response = self._client.execute('findCompletedItems', query)

        total_pages = int(response.reply.paginationOutput.totalPages)
        total_entries = int(response.reply.paginationOutput.totalEntries)

        self._logger.info('found total results %d (%d pages)' % (total_entries, total_pages))
        if not total_pages:
            return results

        # page no. starts with 1 (first page already got)
        page_no = 1
        while True:
            if add_download_time:
                # utc datetime from ebay to timestamp
                download_time = calendar.timegm( \
                    response.reply.timestamp.utctimetuple())
                for item_ in response.reply.searchResult.item:
                    item_.download_unixtime = download_time

            results.extend(response.reply.searchResult.item)
            self._logger.info('fetching results, page %d/%d' % (page_no, total_pages))
            page_no += 1
            if page_no > total_pages: break
            if page_no >= ebay_pages_per_query_limit:
                self._logger.warning('request reached ebay limit. Only first %d pages will be fetched' %
                                     ebay_pages_per_query_limit)
                break
            time.sleep(2)
            # set specific page no to query
            query['paginationInput'] = {'pageNumber': page_no}
            response = self._client.execute('findCompletedItems', query)

        return results

    @classmethod
    def deserialize(cls, item):
        """
        Deserialize item to python native data structures.

        :param item: object in collection returned by search method.
        :type item: see ebay FindingAPI docs.

        :returns: serialized item.
        """

        t_bool = {'false': False, 'true': True}

        def detect_numbers(val):
            """
            Try to convert int and float strings to numbers
            """
            try:
                return int(val)
            except (ValueError, TypeError):
                try:
                    return float(val)
                except (ValueError, TypeError):
                    return val

        if isinstance(item, ResponseDataObject):
            s_item = {}
            for name in [att for att in dir(item) if not att.startswith('__')]:
                value = getattr(item, name)
                if hasattr(value, '__call__'): continue
                s_item[name] = cls.deserialize(value)
            return s_item
        if isinstance(item, (tuple, list)):
            return [cls.deserialize(elem) for elem in item]

        # warning, order of calls does matter !!
        item = detect_numbers(item)
        item = t_bool.get(item, item)
        return item
