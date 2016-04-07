# -*- coding: utf-8 -*-

import logging
import requests
import csv


class InvalidResource(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Response(object):

    __MESSAGES = {
        200: 'No Errors',
        401: 'Not authorized! Please check your API token',
        403: 'Forbidden! You do not have access to this resource',
        500: 'Internal Server Error',
        504: 'Server timeout'
    }

    __HEADERS = {
        'crimeservers': ['_id', 'url', 'type', 'subType', 'country', 'countryName', 'city',
                         'status', 'host', 'latitude', 'longitude', 'ip', 'updatedAt', 'asnId',
                         'asnDesc', 'firstSeenAt', 'lastSeenAt', 'confidence'],
        'botips': ['botnetFamily', 'ip', 'country', 'countryName', 'latitude', 'longitude',
                   'seenAt', 'botnetUrl', 'botnetIp', 'destinationPort', 'botnetType',
                   'operatingSystem', 'botId', 'city', 'portalUrl', 'portalDomain', 'createdAt'],
        # Key 'signatures' not printed yet in csv
        'malwares': ['filename', 'contentType', 'md5', 'sha1', 'sha256', 'analyzedAt',
                     'firstSeenAt', 'fileType', 'fileSize', 'malwareType', 'malwareFamily',
                     'confidence', 'architecture'],
        'hacktivism_country': ['name', 'iso', 'total'],
        'hacktivism_ops': ['hashTag', 'total'],
    }

    def __init__(self, status_code, items,
                 updated_at, next_update, total_size, name):
        self.status_code = status_code
        self.error_msg = self.__MESSAGES[status_code] if status_code in self.__MESSAGES else 'Could not connect'
        self.items = items
        self.updated_at = updated_at
        self.next_update = next_update
        self.total_size = total_size
        self.name = name

    def get_csv_file(self, output_file=None):
        if output_file == None:
            output_file = self.name

        with open(output_file + '.csv', 'wb') as f:
            w = csv.writer(f)
            w.writerow(self.__HEADERS[self.name])

            for item in self.items:
                row = []
                for k in self.__HEADERS[self.name]:
                    value = item.get(k, "")
                    if type(value) is list:
                        row.append(",".join(value))
                    else:
                        row.append(value)
                w.writerow([unicode(s).encode("utf-8") for s in row])

    def __str__(self):
        return "\t-> Updated At: {}\n\t-> Next Update: {}\n\t-> Number of Items: {}\nStatus Code: {}\nErrors: {}\n".format(
            self.updated_at,
            self.next_update,
            self.total_size,
            self.status_code,
            self.error_msg)


class Resource(object):
    """Generic REST resource of Blueliv's API.
    Every resource should extend this class.
    """

    __USER_AGENT = "SDK v2"
    __API_CLIENT = "6918a2e6-86e8-4be3-9800-e658dd37e760"

    __RESOURCES = {
        'crimeservers': {
            'items': 'crimeServers',
            'endpoint': '/v1/crimeserver',
            'feeds': {
                'all': {
                    'online': '/online',
                    'recent': '/recent',
                    'last': '/last'
                },
                'test': {
                    'test': '/test'
                }
            }
        },
        'botips': {
            'items': 'ips',
            'endpoint': '/v1/ip',
            'feeds': {
                'non-pos': {
                    'recent': '/recent',
                    'last': '/last'
                },
                'pos': {
                    'recent': '/pos/recent',
                    'last': '/pos/last'
                },
                'full': {
                    'recent': '/full/recent',
                    'last': '/full/last'
                },
                'test': {
                    'test': '/test'
                }
            }
        },
        'malwares': {
            'items': 'malwares',
            'endpoint': '/v1/malware',
            'feeds': {
                'all': {
                    'recent': '/recent',
                    'last': '/last',
                    'lastday': '/lastday'
                },
                'test': {
                    'test': '/test'
                }
            }
        },
        'hacktivism_country': {
            'items': 'countries',
            'endpoint': '/v1/hacktivism',
            'feeds': {
                'all': {
                    'recent': '/country/recent',
                    'last': '/country/last',
                    'lastday': '/country/lastday'
                },
                'test': {
                    'test': '/test'
                }
            }
        },
        'hacktivism_ops': {
            'items': 'hashtags',
            'endpoint': '/v1/hacktivism',
            'feeds': {
                'all': {
                    'current': '/ops/current',
                    'recent': '/ops/recent',
                    'last': '/ops/last',
                    'lastday': '/ops/lastday'
                },
                'test': {
                    'test': '/test'
                }
            }
        }
    }

    def __init__(self, base_url, name, token,
                 http_timeout=60, log_level=logging.NOTSET,
                 proxy=None):
        """Arguments:
            base_url -- the base URL of the API
            (e.g., 'https://api.blueliv.com')
            name -- name of the resource (e.g., 'crimeservers' or 'botips')
            token -- the user API token
            http_timeout -- the HTTP timeout for a given resource
            (in seconds). Default: 60 seconds (1 minute)
            log_level -- The log level that you want. Default: NOTSET
            proxy -- The proxy that you are using to access the API. Default:
            None. Format is: { "http": "http://user:pass@host:port/",
                               "https": "http://user:pass@host:port/"}
        """
        self.base_url = base_url
        self.name = name
        self.http_timeout = http_timeout
        self.headers = {"Authorization": "bearer {0}".format(token)} if token else {}
        self.headers["User-Agent"] = self.__USER_AGENT
        self.headers["X-API-CLIENT"] = self.__API_CLIENT
        self.proxy = proxy
        self.log_level = log_level

    def __call_endpoint(self, feed, feed_type):
        base_url = self.base_url + self.__RESOURCES[self.name]['endpoint']

        if feed_type in self.__RESOURCES[self.name]['feeds']:
            feed_lookup = self.__RESOURCES[self.name]['feeds'][feed_type]
        else:
            raise InvalidResource('Feed {} does not exist!'.format(feed_type))

        if feed not in feed_lookup:
            raise InvalidResource('Resource {} does not exist'.format(feed))

        updatedAt, nextUpdate, total_size, items = None, None, None, []
        status_code, response = self.get(base_url + feed_lookup[feed])
        if response is not None and self.__RESOURCES[self.name]['items'] in response:
            items = response[self.__RESOURCES[self.name]['items']]
            if "meta" in response:
                updatedAt = response["meta"]["updated"]
                nextUpdate = response["meta"]["nextUpdate"]
                total_size = response["meta"]["totalSize"]

        return Response(status_code, items, updatedAt, nextUpdate, total_size, self.name)

    def online(self, feed_type='all'):
        return self.__call_endpoint('online', feed_type)

    def recent(self, feed_type='all'):
        return self.__call_endpoint('recent', feed_type)

    def last(self, feed_type='all'):
        return self.__call_endpoint('last', feed_type)

    def lastday(self, feed_type='all'):
        return self.__call_endpoint('lastday', feed_type)

    def current(self, feed_type='all'):
        return self.__call_endpoint('current', feed_type)

    def test(self):
        return self.__call_endpoint('test', 'test')

    def get_resources(self):
        return self.__RESOURCES[self.name]['feeds']

    def get(self, url):
        """Downloads and parses to JSON a given resource. Returns
        the parsed response."""
        logger = logging.getLogger('get')
        logger.setLevel(self.log_level)
        response = None
        status_code = None
        try:
            r = requests.get("{0}?key={1}".format(url, self.__API_CLIENT), verify=True, headers=self.headers,
                             proxies=self.proxy, timeout=self.http_timeout)
            r.raise_for_status()
            status_code = r.status_code
            response = r.json()
        except Exception:
            logger.exception("Error downloading data from: {}".format(url))

        return (status_code, response)
