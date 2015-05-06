# -*- coding: utf8 -*-

import unittest
import os
import sys
import logging
import mock
# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sdk.blueliv_api import BluelivAPI
from sdk.api.crimeservers import CrimeServers
from sdk.api.date_utils import DateUtils


class TestBluelivAPI(unittest.TestCase):

    __DEFAULT_API_URL = 'https://freeapi.blueliv.com'

    # This method will be used by the mock to replace requests.get
    def mocked_requests_get(*args, **kwargs):
        return MockResponse('OK', 200)

    def setUp(self):
        self.proxy = {'http': '50.60.110.152:80',
                      'https': '50.60.110.152:80'}
        self.api = BluelivAPI(token='test', proxy=self.proxy)

    def test_get_default_params(self):
        self.assertEqual(self.api.base_url, self.__DEFAULT_API_URL)

    def test_get_default_logging_level(self):
        self.assertEqual(self.api.log_level, logging.NOTSET)

    def test_has_proxy_(self):
        self.assertEqual(self.api.proxy, self.proxy)

    def test_crimeservers_api(self):
        self.assertIsNotNone(self.api.crime_servers)
        self.assertTrue(isinstance(self.api.crime_servers, CrimeServers))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_has_proxy_in_request(self, mock_get):
        response = self.api.crime_servers.download_all()
        self.assertIn(mock.call(self.api.base_url + '/v1/crimeserver/online',
                                headers={'Authorization': 'bearer test'},
                                proxies=self.proxy,
                                timeout=600, 
                                verify=True), 
                      mock_get.call_args_list)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBluelivAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
