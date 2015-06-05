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
    print(api.crime_servers.get_resources())
    # Get online crime servers
    response = api.crime_servers.online()
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        #print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')

    """
    # Get recent crime servers
    response = api.crime_servers.recent()
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        #print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')

    # Get last crime servers
    response = api.crime_servers.last()
    print(response)
    try:
        # WORK WITH BOT IPS DATA
        # Get all the items returned
        print(response.updated_at)
        print(response.total_size)
        #print(response.items)  # botips
        print(response.next_update)
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')
    """
