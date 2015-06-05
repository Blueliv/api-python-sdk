# -*- coding: utf8 -*-

import logging
import sys
import os

from sdk.api.resource import *


class BluelivAPI():
    """Blueliv API SDK for Python"""

    def __init__(self, base_url="https://freeapi.blueliv.com", token=None,
                 http_timeout=60, log_level=logging.NOTSET, proxy=None):
        """Arguments:
            base_url -- the base url of the API. Default: https://freeapi.blueliv.com
            token -- the authentication token to access the API
            http_timeout -- HTTP timeout (in seconds). Default: 60 (1 minute)
            log_level -- The log level that you want. Default: NOTSET
            proxy -- The proxy that you are using to access the API. Default:
            None. Format is: { "http": "http://user:pass@host:port/",
                               "https": "http://user:pass@host:port/"}
        """
        self.base_url = base_url
        self.log_level = log_level
        self.proxy = proxy
        self.crime_servers = Resource(base_url,
                                      'crimeservers',
                                      token,
                                      http_timeout * 10,
                                      log_level,
                                      proxy)
        self.bot_ips = Resource(base_url,
                                'botips',
                                token,
                                http_timeout * 10,
                                log_level,
                                proxy)
