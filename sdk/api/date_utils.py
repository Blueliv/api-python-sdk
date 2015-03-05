# -*- coding: utf8 -*-

import datetime

from dateutil.tz import tzlocal
from dateutil import parser
from datetime import timedelta


class DateUtils():
    """Date utilities for Blueliv API"""

    __ISO_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

    @staticmethod
    def is_outdated(date_1, date_2, delta_ms):
        """Returns True if the difference between two given
        dates is greater than a `delta`, or False otherwise

        Arguments:
            date_1 -- the higher date to test
            date_2 -- the lower date to test
            delta_ms -- the `delta`, in milliseconds
        """
        return (date_1 - date_2) > timedelta(milliseconds=delta_ms)

    @staticmethod
    def to_iso_date(str_date):
        """Converts a given date into the ISO 8601 format
        ("%Y-%m-%dT%H:%M:%S%z")
        """
        if not str_date:
            return None
        try:
            d2 = parser.parse(str_date)
            iso_date = d2.astimezone(tzlocal())
        except:
            iso_date = None

        return iso_date

    @staticmethod
    def now():
        """Returns the current date with TimeZone information"""
        return datetime.datetime.now(tzlocal())

    @staticmethod
    def now_str(date_format=None):
        """Returns the current date formatted with a given date format.
        Arguments:
            date_format -- the format of the date. Default: ISO 8601
            ("%Y-%m-%dT%H:%M:%S%z")
        """
        date_format = date_format if date_format is not None else DateUtils.__ISO_DATE_FORMAT
        now = DateUtils.now()
        return now.strftime(date_format)
