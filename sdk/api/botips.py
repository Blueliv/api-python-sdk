# -*- coding: utf8 -*-

import logging
from resource import Resource
from date_utils import DateUtils


class BotIps(Resource):
    """Bot Ips resource API

    Four end-points are available:
        * /last - returns the last `cache_ttl`/(1000*60) minutes of updates.
        It should be used to update a local environment;
        * /pos/last - same as above but only for Bot IPs whose botnet is from
        type POS (Point-of-Sale);
        * /recent - returns the last `cache_ttl`/(1000*60) * `out_of_date_time`
        minutes of updates. This is a recovery mechanism and should be used to
        update your local environment if the user loses the last updates;
        * /pos/recent - same as above but only for Bot IPs whose botnet is from
        type POS (Point-of-Sale).
    """

    __MESSAGES = {
        'no_last_update': "There is no `lastUpdate`",
        'last_updated_at': "Last update was at `{}`",
        'outdated_db': "Bot IPs is outdated",
        'done': "Done!"
    }

    __END_POINTS = {
        'pos_last': '/pos/last',
        'pos_recent': '/pos/recent',
        'last': '/last',
        'recent': '/recent'
    }

    def __init__(self, base_url, token,
                 cache_ttl, out_of_date_time, http_timeout):
        """Arguments:
            cache_ttl -- time-to-live (TTL) of the cache (in milliseconds).
            out_of_date_time -- number of (sliding) `windows` available at
            end-point `/recent`
            http_timeout -- HTTP timeout (in seconds).
        """
        super(BotIps, self).__init__(base_url=base_url,
                                     token=token,
                                     base_end_point='/v1/ip',
                                     http_timeout=http_timeout)
        self.cache_ttl = cache_ttl
        self.out_of_date_time = out_of_date_time

    def __get_endpoint(self, last_update_date, pos):
        """Returns the end-point to call given a
        date (`/{pos}/recent` or `/{pos}/last`).
        Arguments:
            last_update_date -- the date of the last update
            the user has saved locally;
            pos -- flag to choose between Bot IPs POS feed and the normal
                one.
        """
        logger = logging.getLogger('__get_endpoint')

        pos_prefix = 'pos_' if pos else ''
        now = DateUtils.now()
        now_str = DateUtils.to_iso_date(now)
        if last_update_date is None:
            logger.info(self.__MESSAGES['no_last_update'])
            return self.__END_POINTS[pos_prefix + 'recent']
        else:
            update_time = self.cache_ttl
            n_available_updates = self.out_of_date_time
            outdated = DateUtils.is_outdated(now,
                                             last_update_date,
                                             update_time * 2)

            if outdated:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS[pos_prefix + 'recent']
            else:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS[pos_prefix + 'last']

    def update(self, last_updated_date=None, pos=False):
        """Returns a list of Bot IPs and the date when the updated occurred.

            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date or outdated
                regarding to Blueliv Bot IPs' API;
                pos -- flag to choose between Bot IPs POS feed and the normal
                one.
        """
        logger = logging.getLogger('update')
        url = self.base_url + self.__get_endpoint(
            DateUtils.to_iso_date(last_updated_date),
            pos)
        updatedAt = None
        bot_ips = None
        response = self.get(url)
        if response is not None and "ips" in response:
            bot_ips = response["ips"]
            updatedAt = response["meta"]["updated"] if "meta" in response and "updated" in response["meta"] else None

        return (bot_ips, updatedAt)

    def update_pos(self, last_updated_date=None):
        """Returns a list of Bot IPs and the date when the updated occurred.
        It is a short-hand to the method `update`, without the `pos` parameter.
            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date or outdated.
        """
        logger = logging.getLogger('update_pos')
        return self.update(last_updated_date, pos=True)

    def download(self):
        """Downloads the last hour of Bot Ips' feed. It is a short-hand to
        the method `update`, without a `last_update_date` parameter.
        """
        logger = logging.getLogger('download')
        return self.update(last_updated_date=None)

    def download_pos(self):
        """Downloads the last hour of Bot Ips' POS feed. It is a short-hand to
        the method `update`, without a `last_update_date` parameter and with
        the `pos` parameter as `True`.
        """
        logger = logging.getLogger('download_pos')
        return self.update(last_updated_date=None, pos=True)
