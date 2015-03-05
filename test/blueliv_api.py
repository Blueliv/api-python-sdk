# -*- coding: utf8 -*-

import unittest
import os
import sys

# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from sdk.blueliv_api import BluelivAPI
from sdk.api.crimeservers import CrimeServers
from sdk.api.date_utils import DateUtils


class TestBluelivAPI(unittest.TestCase):

    __DEFAULT_API_URL = 'https://api.blueliv.com'

    def setUp(self):
        self.api = BluelivAPI(token='test')

    def test_get_default_params(self):
        self.assertEqual(self.api.base_url, self.__DEFAULT_API_URL)

    def test_crimeservers_api(self):
        self.assertIsNotNone(self.api.crime_servers)
        self.assertTrue(isinstance(self.api.crime_servers, CrimeServers))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBluelivAPI)
    unittest.TextTestRunner(verbosity=2).run(suite)
