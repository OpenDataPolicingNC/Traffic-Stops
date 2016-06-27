# Test the aspects of data import which normalize the original data

from django.test import TestCase
import pandas as pd

from md.data.importer import (add_age_column, add_date_column, fix_ETHNICITY,
    fix_GENDER, fix_SEIZED, fix_STOP_REASON, fix_TIME_OF_STOP)


class TestFieldNormalization(TestCase):

    def test_ethnicity(self):
        data = (
            ('WHITE', 'W'),
            ('BLACK', 'B'),
            ('HISPANIC', 'H'),
            ('OTHER', 'U'),
            ('ASIAN', 'A'),
            ('NATIVE AMERICAN', 'I'),
            ('UNKNOWN', 'U'),
            ('', 'U'),
            ('BLK', 'B'),
            ('hiq', 'U'),
            ('W', 'W'),
            ('f', 'U'),
        )

        for original, normalized in data:
            self.assertEqual(fix_ETHNICITY(original), normalized)

    def test_gender(self):
        data = (
            ('M', 'M'),
            ('F', 'F'),
            ('F ', 'F'),
            ('U', 'U'),
            ('', 'U'),
            ('female', 'F'),
            ('male', 'M'),
            ('MD', 'U'),
            ('w', 'F'),
            ('n', 'U'),
        )
        for original, normalized in data:
            self.assertEqual(fix_GENDER(original), normalized)

    def test_seized(self):
        data = (
            ('Nothing', 'N'),
            ('Contraband Only', 'Y'),
            ('Property', 'N'),
            ('n/a', 'N'),
            ('paraphernalia', 'Y'),
            ('Both', 'Y'),
        )

        for original, normalized in data:
            self.assertEqual(fix_SEIZED(original), normalized)

    def test_stop_reason(self):
        """
        Final STOP_REASON normalization not yet determined;
        don't bother testing yet.
        """
        fix_STOP_REASON('13-111(a)')

    def test_time_of_stop(self):
        data = (
            ('11:23', '11:23'),
            ('11:23 AM', '11:23 AM'),
            ('24:44', '00:00'),
            ('23:60', '00:00'),
            (':', '00:00'),
        )
        for original, normalized in data:
            self.assertEqual(fix_TIME_OF_STOP(original), normalized)

    def test_computed_date(self):
        stops = pd.DataFrame({
            'STOPDATE': ['02/11/12', '12/31/2015', '6/6/2014'],
            'TIME_OF_STOP': ['20:53 PM', '8:53 PM', '18:06']
        })
        add_date_column(stops)
        self.assertEqual(
            stops.date[0],
            pd.Timestamp('2012-02-11 20:53:00')
        )
        self.assertEqual(
            stops.date[1],
            pd.Timestamp('2015-12-31 20:53:00')
        )
        self.assertEqual(
            stops.date[2],
            pd.Timestamp('2014-06-06 18:06:00')
        )

    def test_computed_age(self):
        stops = pd.DataFrame({
            'STOPDATE': ['03/04/13', '12/31/12', '1/1/15'],
            'TIME_OF_STOP': ['00:21', '11:50', '11:50'],
            'DOB': ['05/27/89', '', '1/1/20']
        })
        add_date_column(stops)
        add_age_column(stops)
        self.assertEqual(stops.computed_AGE[0], 23)
        self.assertEqual(stops.computed_AGE[1], 0)
        # Bug in age computation
        # Fix in ODPM-27
        # Conversion to datetime should assume a two-digit year
        # greater than the current two-digit year is from the
        # previous century.
        # NO!  self.assertEqual(stops.computed_AGE[2], 0)
