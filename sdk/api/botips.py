# -*- coding: utf8 -*-

import logging
from resource import Resource
from date_utils import DateUtils


class BotIps(Resource):
    """Bot Ips resource API

    Four end-points are available:
        * /last - returns the last `cache_ttl`/(1000*60) minutes of updates
        for non-POS botnets.
        It should be used to update a local environment;
        * /pos/last - same as above but only for Bot IPs whose botnet is from
        type POS (Point-of-Sale);
        * /full/last - same as above but for all the botnets;
        * /recent - returns the last `cache_ttl`/(1000*60) * `out_of_date_time`
        minutes of updates for non-POS botnets. This is a recovery mechanism and 
        should be used to update your local environment if the user loses the
         last updates;
        * /pos/recent - same as above but only for Bot IPs whose botnet is from
        type POS (Point-of-Sale).
        * /full/recent - same as above but for all the botnets.
    """

    __MESSAGES = {
        'no_last_update': "There is no `lastUpdate`",
        'last_updated_at': "Last update was at `{}`",
        'outdated_db': "Bot IPs is outdated",
        'done': "Done!"
    }

    __END_POINTS = {
        'full_last': '/full/last',
        'full_recent': '/full/recent',
        'pos_last': '/pos/last',
        'pos_recent': '/pos/recent',
        'last': '/last',
        'recent': '/recent',
        'debug': '/test'
    }

    def __init__(self, base_url, token,
                 cache_ttl, out_of_date_time, http_timeout,
                 log_level=logging.NOTSET, proxy=None):
        """Arguments:
            base_url -- the base url of the API
            token -- the authentication token to access the API
            cache_ttl -- time-to-live (TTL) of the cache (in milliseconds).
            out_of_date_time -- number of (sliding) `windows` available at
            end-point `/recent`
            http_timeout -- HTTP timeout (in seconds)
            log_level -- The log level that you want. Default: NOTSET
            proxy -- The proxy that you are using to access the API. Default:
            None. Format is: { "http": "http://user:pass@host:port/",
                               "https": "http://user:pass@host:port/"}
        """
        super(BotIps, self).__init__(base_url=base_url,
                                     token=token,
                                     base_end_point='/v1/ip',
                                     http_timeout=http_timeout,
                                     log_level=log_level,
                                     proxy=proxy)
        self.cache_ttl = cache_ttl
        self.out_of_date_time = out_of_date_time
        self.log_level = log_level

    def __get_endpoint(self, last_update_date, feed, debug):
        """Returns the end-point to call given a
        date (`/{pos|full}/recent` or `/{pos|full}/last`).
        Arguments:
            last_update_date -- the date of the last update
            the user has saved locally;
            feed -- to choose between feed without POS
            botnets (''), feed with only POS ('pos') botnets or
            full ('full');
            debug -- debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('__get_endpoint')
        logger.setLevel(self.log_level)

        if debug:
            return self.__END_POINTS['debug']

        if feed is not '':
            feed += '_'

        now = DateUtils.now()
        now_str = DateUtils.to_iso_date(now)
        if last_update_date is None:
            logger.info(self.__MESSAGES['no_last_update'])
            return self.__END_POINTS[feed + 'recent']
        else:
            update_time = self.cache_ttl
            n_available_updates = self.out_of_date_time
            outdated = DateUtils.is_outdated(now,
                                             last_update_date,
                                             update_time * 2)

            if outdated:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS[feed + 'recent']
            else:
                logger.info(self.__MESSAGES['last_updated_at'].format(
                    last_update_date))
                return self.__END_POINTS[feed + 'last']

    def update(self, last_updated_date=None, feed='', debug=False):
        """Returns a list of Bot IPs and the date when the updated occurred.
            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date or outdated
                regarding to Blueliv Bot IPs' API;
                feed -- to choose between feed without POS botnets (''),
                feed with only POS ('pos') botnets or full ('full').
                debug -- debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('update')
        url = self.base_url + self.__get_endpoint(
            DateUtils.to_iso_date(last_updated_date),
            feed, debug)
        updatedAt = None
        bot_ips = None
        response = self.get(url)
        if response is not None and "ips" in response:
            bot_ips = response["ips"]
            updatedAt = response["meta"]["updated"] if "meta" in response and "updated" in response["meta"] else None

        return (bot_ips, updatedAt)

    def update_pos(self, last_updated_date=None, debug=False):
        """Returns a list of Bot IPs and the date when the updated occurred.
        It is a short-hand to the method `update`, with `feed` parameter set
        as `pos`
            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date or outdated.
                debug -- Debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('update_pos')
        return self.update(last_updated_date, feed='pos', debug=debug)

    def update_full(self, last_updated_date=None, debug=False):
        """Returns a list of Bot IPs and the date when the updated occurred.
        It is a short-hand to the method `update`, with `feed` parameter set
        as `full`.
            Arguments:
                last_updated_date -- last updated date, saved locally. It is
                used to know if the local client is up-to-date or outdated.
                debug -- Debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('update_full')
        return self.update(last_updated_date, feed='full', debug=debug)

    def download(self, debug=False):
        """Downloads the last hour of Bot Ips' non-POS feed. It is a 
        short-hand to the method `update`, without a `last_update_date`
        parameter.
            Arguments:
                debug -- Debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('download')
        return self.update(last_updated_date=None, debug=debug)

    def download_pos(self, debug=False):
        """Downloads the last hour of Bot Ips' POS feed. It is a short-hand to
        the method `update`, without a `last_update_date` parameter and with
        the `feed` parameter as `pos`.
            Arguments:
                debug -- Debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('download_pos')
        return self.update(last_updated_date=None, feed='pos', debug=debug)

    def download_full(self, debug=False):
        """Downloads the last hour of Bot Ips' full feed. It is a short-hand to
        the method `update`, without a `last_update_date` parameter and with
        the `feed` parameter as `full`.
            Arguments:
                debug -- Debug mode (call always '/test' resource)
        """
        logger = logging.getLogger('download_full')
        return self.update(last_updated_date=None, feed='full', debug=debug)
