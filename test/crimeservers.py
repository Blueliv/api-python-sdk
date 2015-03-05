# -*- coding: utf8 -*-

import unittest
import os
import sys
import datetime
from dateutil.tz import tzlocal
from datetime import timedelta

# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sdk.api.crimeservers import CrimeServers
from sdk.api.date_utils import DateUtils


class TestCrimeServersAPI(unittest.TestCase):

    __TEST_TOKEN = 'test'

    def setUp(self):
        self.crime_servers = CrimeServers(base_url='https://api.blueliv.com',
                                          token=self.__TEST_TOKEN,
                                          cache_ttl=3600000,
                                          out_of_date_time=24,
                                          http_timeout=60)

    def test_token_headers(self):
        self.assertEqual(self.crime_servers.headers,
                         {"Authorization": "bearer {}".format(self.__TEST_TOKEN)})

    def test_get_query_updated(self):
        now = DateUtils.now()
        self.assertEqual("/last",
                         self.crime_servers._CrimeServers__get_endpoint(now))

    def test_get_query_out_of_date(self):
        out_date = DateUtils.now()-timedelta(days=1, minutes=1)
        self.assertEqual("/online",
                         self.crime_servers._CrimeServers__get_endpoint(out_date))
        self.assertEqual("/online",
                         self.crime_servers._CrimeServers__get_endpoint(None))

    def test_get_query_not_updated(self):
        out_date = datetime.datetime.now(tzlocal())-timedelta(minutes=60*2+1)
        self.assertEqual("/recent",
                         self.crime_servers._CrimeServers__get_endpoint(out_date))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCrimeServersAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
