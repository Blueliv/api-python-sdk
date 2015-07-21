# -*- coding: utf8 -*-

import unittest
import os
import sys
import mock

# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sdk.api.resource import *


class TestResourcesAPI(unittest.TestCase):

    __TEST_TOKEN = "test"
    __USER_AGENT = "SDK v2"
    __API_CLIENT = "6918a2e6-86e8-4be3-9800-e658dd37e760"

    __TEST_HEADERS = {
      "Authorization": "bearer {0}".format(__TEST_TOKEN),
      "User-Agent": __USER_AGENT,
      "X-API-CLIENT": __API_CLIENT
    }

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
                self.raise_for_status = None

            def json(self):
                if self.status_code != 200:
                    raise Exception
                return self.json_data

        return MockResponse({'msg': 'Not found'}, 200)

    def setUp(self):
        self.bot_ips = Resource(base_url='https://api.blueliv.com',
                                name='botips',
                                token=self.__TEST_TOKEN,
                                http_timeout=60)
        self.crimeservers = Resource(base_url='https://api.blueliv.com',
                                     name='crimeservers',
                                     token=self.__TEST_TOKEN,
                                     http_timeout=60)

        self.malwares = Resource(base_url='https://api.blueliv.com',
                                     name='malwares',
                                     token=self.__TEST_TOKEN,
                                     http_timeout=60)

        self.hacktivism_ops = Resource(base_url='https://api.blueliv.com',
                                     name='hacktivism_ops',
                                     token=self.__TEST_TOKEN,
                                     http_timeout=60)

        self.hacktivism_country = Resource(base_url='https://api.blueliv.com',
                                     name='hacktivism_country',
                                     token=self.__TEST_TOKEN,
                                     http_timeout=60)

    def test_token_headers(self):
        self.assertEqual(self.bot_ips.headers, self.__TEST_HEADERS)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_bot_ips_feed(self, mock_get):
        self.bot_ips.recent('non-pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.bot_ips.last('non-pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_crimeservers_feed(self, mock_get):
        self.crimeservers.recent()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/crimeserver/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.crimeservers.last()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/crimeserver/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.crimeservers.online()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/crimeserver/online?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_bot_ips_pos_feed(self, mock_get):
        self.bot_ips.recent(feed_type='pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/pos/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.bot_ips.last(feed_type='pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/pos/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_bot_ips_full_feed(self, mock_get):
        self.bot_ips.recent(feed_type='pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/pos/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.bot_ips.last(feed_type='pos')
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/pos/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_malwares__feed(self, mock_get):
        self.malwares.recent()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/malware/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.malwares.last()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/malware/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_hacktivism__feed(self, mock_get):
        self.hacktivism_ops.recent()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/hacktivism/ops/recent?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.hacktivism_country.last()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/hacktivism/country/last?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.hacktivism_ops.current()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/hacktivism/ops/current?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

    def test_non_existant_feed(self):
        self.assertRaises(InvalidResource, self.bot_ips.recent, ('p0s'))
        self.assertRaises(InvalidResource, self.bot_ips.last, ('p0s'))
        self.assertRaises(InvalidResource, self.crimeservers.recent, ('xx'))
        self.assertRaises(InvalidResource, self.crimeservers.last, ('xx'))


    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_debug_endpoint(self, mock_get):
        self.bot_ips.test()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/ip/test?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

        self.crimeservers.test()
        self.assertIn(mock.call(self.bot_ips.base_url + '/v1/crimeserver/test?key={0}'.format(self.__API_CLIENT),
                      headers=self.__TEST_HEADERS,
                      proxies=None,
                      timeout=60,
                      verify=True), mock_get.call_args_list)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestResourcesAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
