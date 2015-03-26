# -*- coding: utf8 -*-

import logging
from resource import Resource
from date_utils import DateUtils


class CrimeServers(Resource):
    """Crime Servers resource API

    Three end-points are available:
        * /online - returns all online crimeservers. It is used to start
        or restart a local environment with Blueliv's Crime Servers feed;
        * /last - returns the last `cache_ttl`/(1000*60) minutes of updates.
        It should be used to update a local environment;
        * /recent - returns the last `cache_ttl`/(1000*60) * `out_of_date_time`
        minutes of updates. This is a recovery mechanism and should be used to
        update your local environment if the user loses the last updates.
    """

    __MESSAGES = {
        'no_last_update': "There is no `lastUpdate`",
        'last_updated_at': "Last update was at `{}`",
        'outdated_db': "Crime servers is outdated",
        'download_crime_servers': "Getting ALL online crime servers",
        'update_crime_servers': "Updating crime servers",
        'done': "Done!"
    }

    __END_POINTS = {
        'online': '/online',
        'recent': '/recent',
        'last': '/last'
    }

    def __init__(self, base_url, token,
                 cache_ttl, out_of_date_time, http_timeout):
        """Arguments:
            cache_ttl -- time-to-live (TTL) of the cache (in milliseconds).
            out_of_date_time -- number of (sliding) `windows` available at
            end-point `/recent`
            http_timeout -- HTTP timeout (in seconds).
        """
        super(CrimeServers, self).__init__(base_url=base_url,
                                           token=token,
                                           base_end_point='/v1/crimeserver',
                                           http_timeout=http_timeout)
        self.cache_ttl = cache_ttl
        self.out_of_date_time = out_of_date_time

    def __get_endpoint(self, last_update_date):
        """Returns the end-point to call given a
        date (`/online`, `/recent` or `/last`).
        Arguments:
            last_update_date -- the date of the last update
            the user has saved locally.
        """
        logger = logging.getLogger('__get_endpoint')

        now = DateUtils.now()
        now_str = DateUtils.to_iso_date(now)
        if last_update_date is None:
            logger.info(self.__MESSAGES['no_last_update'])
            return self.__END_POINTS['online']
        else:
            update_time = self.cache_ttl
            n_available_updates = self.out_of_date_time
            partially_outdated = DateUtils.is_outdated(now,
                                                       last_update_date,
                                                       update_time * 2)
            fully_outdated = DateUtils.is_outdated(now,
                                                   last_update_date,
                                                   update_time *
                                                   n_available_updates)

            if fully_outdated:
                logger.info(self.__MESSAGES['outdated_db'])
                return self.__END_POINTS['online']
            elif partially_outdated:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS['recent']
            else:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS['last']

    def update(self, last_updated_date=None):
        """Returns a list of Crime Servers (either an update to the current feed,
           or all of it) and the date when the updated occurred.

            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date, partially
                outdated or fully outdated regarding to Blueliv Crime Servers'
                API.
        """
        logger = logging.getLogger('update')
        url = self.base_url + self.__get_endpoint(
            DateUtils.to_iso_date(last_updated_date))
        updatedAt = None
        crimeservers = None
        response = self.get(url)
        if response is not None and "crimeServers" in response:
            crimeservers = response["crimeServers"]
            updatedAt = response["meta"]["updated"] if "meta" in response and "updated" in response["meta"] else None

        return (crimeservers, updatedAt)

    def download_all(self):
        """Downloads the complete Crime Servers' feed. It is a short-hand to
        the method `update`, without a `last_update_date` parameter.
        """
        logger = logging.getLogger('download_all')
        return self.update(last_updated_date=None)
