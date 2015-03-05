# -*- coding: utf8 -*-

import logging
from sdk.blueliv_api import BluelivAPI

if __name__ == '__main__':
    __LOG_FILE = 'blueliv.log'
    logging.basicConfig(filename=__LOG_FILE, level=logging.DEBUG)
    logger = logging.getLogger('main')
    api = BluelivAPI(base_url='https://freeapi.blueliv.com',
                     token='<INSERT YOUR TOKEN HERE>')

    # Get the last updatedAt if available from your local settings
    last_date = "2015-01-26T16:22:38+0100"
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
