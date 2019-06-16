import calendar
from datetime import datetime

from zeep.exceptions import Fault


def now_unix_time():
    """
    seconds since 1.1.1970
    """
    return calendar.timegm(datetime.utcnow().utctimetuple())


def get_item_and_bids(_id, client):
    """
    :param client: allegro webapi client.
    :param _id: allegro item id.
    :type _id: int
    """

    item = None
    bids = None
    present_in_service = True
    msg = None

    try:
        item = client.get_item(_id, extra_key='vendor', extra_info='allegro.pl')
        item = client.serialize(item)
    except Fault as err:
        present_in_service = False
        msg = str(err)
        return None, None, present_in_service, msg

    except Exception as err:
        msg = str(err)
        return None, None, present_in_service, msg

    try:
        bids = client.get_bids(_id)
        bids = client.serialize(bids)
    except Fault as err:
        msg = 'bids getting error, ' + str(err)
        return item, None, present_in_service, msg

    except Exception as err:
        msg = 'bids getting error, ' + str(err)
        return None, None, present_in_service, msg

    return item, bids, present_in_service, msg
