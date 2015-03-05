# -*- coding: utf8 -*-

import logging
import sys
import os
from api.crimeservers import CrimeServers


class BluelivAPI():
    """Blueliv API SDK for Python"""

    def __init__(self, base_url="https://api.blueliv.com", token=None,
                 cache_ttl=3600000, out_of_date_time=24, http_timeout=60):
        """Arguments:
            cache_ttl -- time-to-live (TTL) of the Crime Servers cache
            (in milliseconds). Default: 3600000 (1 hour)
            out_of_date_time -- number of (sliding) `windows` of the Crime
            Servers cache. Default: 24
            http_timeout -- HTTP timeout (in seconds). Default: 60 (1 minute)
        """
        self.base_url = base_url
        self.crime_servers = CrimeServers(base_url,
                                          token,
                                          cache_ttl,
                                          out_of_date_time,
                                          http_timeout * 10)
