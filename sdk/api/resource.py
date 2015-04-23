# -*- coding: utf8 -*-

import logging
import json
import requests
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

class Resource(object):
    """Generic REST resource of the Blueliv's API.
    Every resource should extend this class.
    """

    def __init__(self, base_url, token, base_end_point, http_timeout=60):
        """Arguments:
            base_url -- the base URL of the API
            (e.g., 'https://api.blueliv.com')
            token -- the user API token
            base_end_point -- the base end-point of the resource
            (e.g., '/v1/crimeservers')
            http_timeout -- the HTTP timeout for a given resource
            (in seconds). Default: 60 seconds (1 minute)
        """
        self.base_url = base_url + base_end_point
        self.http_timeout = http_timeout
        self.headers = {"Authorization": "bearer {0}".format(token)} if token else {}

    def get(self, query):
        """Downloads and parses to JSON a given resource. Returns
        the parsed response."""
        logger = logging.getLogger('get')
        response = None
        try:
            r = requests.get(query, verify=False,
                             headers=self.headers, timeout=self.http_timeout)
            r.raise_for_status
            response = r.json()
        except Exception as e:
            logger.error("Error downloading data from: {}"
                         .format(query))

        return response
