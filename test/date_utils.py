# -*- coding: utf8 -*-

import unittest
import os
import sys
from dateutil import parser

# Change path so we find sdk
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from sdk.api.date_utils import DateUtils


class DateUtilsTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_is_outdated(self):
        TEST_DATE_1 = "2015-01-21T16:00:00+0100"
        TEST_DATE_2 = "2015-01-21T16:30:00+0100"
        TEST_DELTA = 1500000  # 25 minutes
        date_1 = parser.parse(TEST_DATE_1)
        date_2 = parser.parse(TEST_DATE_2)

        self.assertEqual(DateUtils.is_outdated(date_2, date_1, TEST_DELTA),
                         True)

    def test_to_iso_date(self):
        TEST_DATE = "2015-01-21T16:22:38+0100"
        now = parser.parse(TEST_DATE)
        self.assertEqual(now, DateUtils.to_iso_date(TEST_DATE))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(DateUtilsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
