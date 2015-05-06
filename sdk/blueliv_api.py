# -*- coding: utf8 -*-

import logging
import sys
import os
from api.crimeservers import CrimeServers
from api.botips import BotIps


class BluelivAPI():
    """Blueliv API SDK for Python"""

    def __init__(self, base_url="https://freeapi.blueliv.com", token=None,
                 cache_ttl=3600000, out_of_date_time=24, http_timeout=60,
                 log_level=logging.NOTSET, proxy=None):
        """Arguments:
            base_url -- the base url of the API. Default: https://freeapi.blueliv.com
            token -- the authentication token to access the API
            cache_ttl -- time-to-live (TTL) of the Crime Servers cache
            (in milliseconds). Default: 3600000 (1 hour)
            out_of_date_time -- number of (sliding) `windows` of the Crime
            Servers cache. Default: 24
            http_timeout -- HTTP timeout (in seconds). Default: 60 (1 minute)
            log_level -- The log level that you want. Default: NOTSET
            proxy -- The proxy that you are using to access the API. Default:
            None. Format is: { "http": "http://user:pass@host:port/",
                               "https": "http://user:pass@host:port/"}
        """
        self.base_url = base_url
        self.log_level = log_level
        self.proxy = proxy
        self.crime_servers = CrimeServers(base_url,
                                          token,
                                          cache_ttl,
                                          out_of_date_time,
                                          http_timeout * 10,
                                          log_level,
                                          proxy)
        self.bot_ips = BotIps(base_url,
                              token,
                              cache_ttl / 6,
                              out_of_date_time / 4,
                              http_timeout * 10,
                              log_level,
                              proxy)
