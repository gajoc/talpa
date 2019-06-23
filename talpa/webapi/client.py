"""
Created on May 14, 2017

@author: pawel
"""

import zeep
import getpass
from operator import xor
import logging

from talpa.webapi.utils import now_unix_time


def _require_login(f):
    """
    Decorate any method in *AllegroClient* that requires to be logged in
    allegro service (requires allegro session key).
    """

    def wrapped(self, *args, **kwargs):
        self.login()
        return f(self, *args, **kwargs)

    return wrapped


# TODO direct info to secific stream
class AllegroClient(object):
    """
    Allegro client to interact with Allegro API web service.
    """

    def __init__(self, url, web_key, country_id, user=None, password=None):
        '''
        :param url: allegro web api service address.
        :type url: str

        :param web_key: allegro web api key.
        :type web_key: str

        :param country_id: allegro country id (1 for pl)
        :type country_id: int
        
        :param user: allegro account name.
        :type user: str
        
        .. note::
            If *user* argument not passed system will prompt for allegro
            account name and password if needed.
        '''

        # to connect settings
        self._url = url
        self._web_key = web_key
        self._country_id = country_id
        self._user = user
        self._password = password

        # allegro response settings
        self._client = zeep.Client(wsdl=self._url)
        self._sys_status = None
        self._session = None

        self._logger = logging.getLogger(__name__)

    def _build_filter_options(self, user_conditions):
        """
        Prepare and return allegro valid filter object.

        :param user_conditions: filter values to build filter.
        :type user_conditions: dict

        :returns: valid allegro filter object.
        :rtype: ArrayOfFilteroptionstype

        """

        if not user_conditions:
            raise ValueError('User conditions are empty.')
        if not isinstance(user_conditions, dict):
            raise TypeError('User conditions must be dict. Passed %s.' % \
                            str(type(user_conditions)))

        allegro_type_factory = self._client.type_factory('ns0')
        filter_query = allegro_type_factory.ArrayOfFilteroptionstype()

        # build allegro filter object
        for filter_id, value in user_conditions.items():
            option_type = allegro_type_factory.FilterOptionsType()
            option_type.filterId = filter_id

            strings_array = allegro_type_factory.ArrayOfString()
            strings_array.item = value

            option_type.filterValueId = strings_array

            filter_query.item.append(option_type)
        return filter_query

    def search(self, query):
        """
        Query allegro for items and return results.

        :param query: user query values.
        :type query: dict

        :returns: items (see allegro API docs).

        .. note::
            *query* is transformed to allegro valid filter object. Allegro
            response structure contains only items (see allegro API docs for
            'doGetItemsList' method and all options).
        """

        filter_options = self._build_filter_options(query)
        response_ = self._client.service.doGetItemsList( \
            webapiKey=self._web_key, \
            countryId=self._country_id, \
            filterOptions=filter_options, \
            resultSize=1000,  # max items allowed by allegro
            resultScope=3)  # no filter and cat. struct in response
        return response_

    def login(self):
        """
        Login to allegro web api service. Method prompt for allegro user
        account (if not passed in init) and password.

        :returns: allegro session object (see allegro API docs).

        .. tip::
            There is no need to direct call this method. It is triggered if
            interaction with allegro requires to be logged in (if allegro
            session key is needed).

        .. note::
            Method is part of *_require_login* decorator (see docs for
            *_require_login*).
        """

        try:
            if not self._session:
                msg = 'Logging to allegro...'
                self._logger.debug(msg)
                print(msg)
                if not self._sys_status:
                    # get allegro version
                    self._sys_status = self._client.service.doQuerySysStatus( \
                        sysvar=1, countryId=self._country_id, \
                        webapiKey=self._web_key)

                if not self._user:
                    self._user = input('username: ')
                else:
                    msg = 'username: %s' % self._user
                    self._logger.debug(msg)
                    print(msg)
                if not self._password:
                    self._password = getpass.getpass('password: ')

                # login
                self._session = \
                    self._client.service.doLogin(userLogin=self._user, \
                                                 userPassword=self._password, \
                                                 countryCode=self._country_id, \
                                                 webapiKey=self._web_key, \
                                                 localVersion=self._sys_status['verKey'])
        except zeep.exceptions.Fault:
            self._user = None
            self._session = None
            raise
        finally:
            self._password = None
        return self._session

    @_require_login
    def get_item(self, item_id, add_download_time=True, extra_key=None, \
                 extra_info=None):
        """
        Query allegro for item identified by *item_id* and return it.

        :param item_id: item id in allegro service.
        :type item_id: long int

        :param add_download_time: append download time to item in unix time
            format. True by default. Time available in item under key
            'download_unixtime'.
        :type add_download_time: bool

        :param extra_key: key name for *extra_info* added to item.
        :type extra_key: hashable

        :param extra_info: extra info available in item under key *extra_key*.
        :type extra_info:

        :returns: item (see allegro API docs).

        """

        if xor(bool(extra_key), bool(extra_info)):
            raise ValueError('Method called with wrong argument combination.' + \
                             '*extra_key* and *extra_info* arguments must be passed ' + \
                             'simultaneously.')

        item = self._client.service.doShowItemInfoExt( \
            sessionHandle=self._session['sessionHandlePart'], \
            itemId=str(item_id), \
            getDesc='1', \
            getAttribs='1', \
            getImageUrl='1')
        # append download time to data in unixtime format
        if add_download_time: item['download_unixtime'] = now_unix_time()
        # add extra info
        if bool(extra_key) and bool(extra_info):
            item[extra_key] = extra_info

        return item

    @_require_login
    def get_bids(self, item_id):
        """
        Query allegro for item bids identified by *item_id* and return it.

        :param item_id: item id in allegro service.
        :type item_id: long int

        :returns: item bids (see allegro API docs).
        """
        bids = self._client.service.doGetBidItem2( \
            sessionHandle=self._session['sessionHandlePart'], \
            itemId=str(item_id))
        return bids

    def get_categories(self):
        """
        Query allegro for all allegro categories and return it.

        .. note:
            Categories depend on allegro country id (passed in init).

        :returns: all categories (see allegro API docs).
        """
        categories = self._client.service.doGetCatsData( \
            countryId=self._country_id, \
            webapiKey=self._web_key)
        return categories

    def get_filters(self):
        """
        Query allegro for accepted allegro filters and return it.

        :returns: allegro filters (see allegro API docs).
        """
        response_ = self._client.service.doGetItemsList( \
            webapiKey=self._web_key, \
            countryId=self._country_id, \
            resultScope=6)  # filters struct only
        return response_

    @classmethod
    def serialize(cls, item):
        """
        Serialize item to python native data structures.

        :param item: object returned by get_item and get_bids method.
        :type item: see allegro API docs.

        :returns: serialized item.
        """

        return zeep.helpers.serialize_object(item, dict)
