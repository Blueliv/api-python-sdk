# -*- coding: utf8 -*-

import logging
from sdk.blueliv_api import BluelivAPI

if __name__ == '__main__':
    __LOG_FILE = 'blueliv.log'
    logging.basicConfig(filename=__LOG_FILE)
    logger = logging.getLogger('main')

    proxy = None
    # If you have a proxy, comment the line above and uncomment
    # these lines below:
    """
    proxy = {'http': '50.60.110.152:80',
             'https': '50.60.110.152:80'}
    """
    api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                     token='<INSERT YOUR TOKEN HERE>',
                     log_level=logging.INFO,
                     proxy=proxy)

    # Get available resources
    print(api.bot_ips.get_resources())
    # Get last non-POS bot ips
    response = api.bot_ips.last('non-pos')
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')

    # Get recent POS bot ips
    response = api.bot_ips.recent('pos')
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')

    # Get last full bot ips
    response = api.bot_ips.last('full')
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')
