# -*- coding: utf-8 -*-

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


    try:
        # Call to desired endpoint
        response = api.crime_servers.last()
        # Generate CSV Format file (by default filename = resourcename.csv)
        response.get_csv_file()
        # Generate CSV Format file with desired filename (csv_example.csv)
        response.get_csv_file(output_file='csv_example')
    except Exception as e:
        logger.error('{}'.format(e))
    else:
        print('Success!')
    


