# -*- coding: utf8 -*-

import unittest
import os
import sys
import datetime
from dateutil.tz import tzlocal
from datetime import timedelta

# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sdk.api.botips import BotIps
from sdk.api.date_utils import DateUtils


class TestBotIpsAPI(unittest.TestCase):

    __TEST_TOKEN = 'test'

    def setUp(self):
        self.bot_ips = BotIps(base_url='https://api.blueliv.com',
                              token=self.__TEST_TOKEN,
                              cache_ttl=10,
                              out_of_date_time=6,
                              http_timeout=60)

    def test_token_headers(self):
        self.assertEqual(self.bot_ips.headers,
                         {"Authorization": "bearer {}".format(self.__TEST_TOKEN)})

    def test_get_query_updated(self):
        now = DateUtils.now()
        self.assertEqual("/last",
                         self.bot_ips._BotIps__get_endpoint(now,
                                                            pos=False))

    def test_get_query_out_of_date(self):
        out_date = DateUtils.now()-timedelta(minutes=10*20+1)
        self.assertEqual("/recent",
                         self.bot_ips._BotIps__get_endpoint(out_date,
                                                            pos=False))
        self.assertEqual("/recent",
                         self.bot_ips._BotIps__get_endpoint(None,
                                                            pos=False))

    def test_pos_feed(self):
      now = DateUtils.now()
      self.assertEqual("/pos/last",
                       self.bot_ips._BotIps__get_endpoint(now,
                                                          pos=True))
      self.assertEqual("/pos/recent",
                       self.bot_ips._BotIps__get_endpoint(None,
                                                          pos=True))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBotIpsAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
