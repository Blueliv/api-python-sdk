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
    bot_ips, updatedAt = api.bot_ips.update(last_date)
    if updatedAt:
        print(updatedAt, bot_ips)
        try:
            # WORK WITH NON-POS BOTIPS DATA
            pass
        except:
            # DO NOT SAVE updatedAt
            pass
        else:
            # SAVE updatedAt
            pass
    else:
        logger.error("Last updated date could not be retrieved")

    pos_bot_ips, updatedAt_pos = api.bot_ips.update_pos(last_date)
    if updatedAt_pos:
        print(updatedAt_pos, pos_bot_ips)
        try:
            # WORK WITH POS BOTIPS DATA
            pass
        except:
            # DO NOT SAVE updatedAt
            pass
        else:
            # SAVE updatedAt
            pass
    else:
        logger.error("Last updated date could not be retrieved")

    full_bot_ips, updatedAt_full = api.bot_ips.update_full(last_date)
    if updatedAt_full:
        print(updatedAt_full, full_bot_ips)
        try:
            # WORK WITH FULL BOTIPS DATA
            pass
        except:
            # DO NOT SAVE updatedAt
            pass
        else:
            # SAVE updatedAt
            pass
    else:
        logger.error("Last updated date could not be retrieved")
