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

    # Get the last updatedAt if available from your local settings
    last_date = "2015-05-06T10:40:00+0000"
    crimeservers, updatedAt = api.crime_servers.update(last_date)
    if updatedAt:
        print(updatedAt, crimeservers)
        try:
            # WORK WITH CRIMESERVERS DATA
            pass
        except:
            # DO NOT SAVE updatedAt
            pass
        else:
            # SAVE updatedAt
            pass
    else:
        logger.error("Last updated date could not be retrieved")
