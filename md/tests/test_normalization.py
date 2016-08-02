# Test the aspects of data import which normalize the original data

from django.test import TestCase
import pandas as pd

from md.data.importer import (
    add_age_column, add_date_column, add_purpose_column, fix_AGENCY_column,
    fix_ETHNICITY, fix_GENDER, fix_SEIZED, fix_STOP_REASON, fix_TIME_OF_STOP,
    MD_FIRST_YEAR_TO_KEEP, process_raw_data, process_time_of_stop,
)
from md.models import UNKNOWN_PURPOSE


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

    def test_initial_year_cutoff(self):
        # Check cutoff of initial year(s)
        #
        # The dates tested will cover the full range of the year before the
        # cutoff as well as the full range of the next two years (which are
        # kept).
        #
        # The times on those days are at the day boundary in order to find any
        # TZ issues in the cutoff logic.

        y0 = MD_FIRST_YEAR_TO_KEEP - 1
        y1 = MD_FIRST_YEAR_TO_KEEP
        y2 = MD_FIRST_YEAR_TO_KEEP + 1
        orig_stops = pd.DataFrame({
            'STOPDATE': [
                '01/01/%d' % y0,
                '12/31/%d' % y0,
                '01/01/%d' % y1,
                '12/31/%d' % y1,
                '01/01/%d' % y2,
                '12/31/%d' % y2,
            ],
            'TIME_OF_STOP': [
                '00:00',
                '23:59',
                '00:00',
                '23:59',
                '00:00',
                '23:59',
            ],
        })
        new_stops = process_time_of_stop(orig_stops)
        self.assertEqual(len(orig_stops), 6)
        self.assertEqual(len(new_stops), 4)
        self.assertTrue(all(new_stops.STOPDATE == orig_stops.STOPDATE[2:]))
        self.assertTrue(all(new_stops.TIME_OF_STOP == orig_stops.TIME_OF_STOP[2:]))

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
            'STOPDATE': [
                '03/04/13', '12/31/12', '1/1/15'
            ],
            'TIME_OF_STOP': [
                '00:21', '11:50', '11:50'
            ],
            'DOB': [
                '05/27/89', '', '01/01/20'
            ]
        })
        add_date_column(stops)
        add_age_column(stops)
        self.assertEqual(stops.computed_AGE[0], 23)
        self.assertEqual(stops.computed_AGE[1], 0)
        self.assertEqual(stops.computed_AGE[2], 95)

    def test_purpose(self):
        data = (
            # (STOP_REASON-value-from-raw-data, cleaned-STOP_REASON, corresponding-value-from-PURPOSE_CHOICES)
            #
            # Most of the purposes are never assigned explicitly in the code, so
            # "constants" like UNKNOWN_PURPOSE don't exist for most.
            ('21-202(h1)', '21-202', 2),
            (' 16-303(c)', '16-303', 9),
            ('21-901.1(b)', '21-901', 1),
            ('21-1124.1(b)', '21-1124', 9),
            ('64*', '64', 5),
            ('64*-', '64', 5),
            ('64 ', '64', 5),
            ('64-', '64', 5),
            ('64*-`', '64', 5),
            ('409-b', '409', UNKNOWN_PURPOSE),
            ('412-3', '412', UNKNOWN_PURPOSE),
            ('412.3-b', '412', UNKNOWN_PURPOSE),
            ('801.1', '801', UNKNOWN_PURPOSE),
            ('801-1', '801', UNKNOWN_PURPOSE),
            ('201-a(1)', '201', UNKNOWN_PURPOSE),
            (' 22 - 216', '22-216', 5),
            ('22-412.3(b)', '22-412', 0),
            ('22-412.3(c2)', '22-412', 0),
            ('22-412', '22-412', 0),
            ('21-201.A1', '21-201', 4),
            ('21-707A', '21-707', 2),
            ('21-707a', '21-707', 2),
            ('21-507G3I(i1)', '21-507', 4),
            ('13-936E  (2i)', '13-936', 6),
            ('13-936  E(2i)', '13-936', 6),
            ('13-936  E(2iI)', '13-936', 6),
            ('21-2091(iiT)', '21-2091', UNKNOWN_PURPOSE),
            ('21-201-a(1)', '21-201', 4),
            ('9-220', '9-220', UNKNOWN_PURPOSE),
            ('06-B1B', '06-B1B', UNKNOWN_PURPOSE),
        )
        stops = pd.DataFrame({
            'STOP_REASON': [
                x for x, _, _ in data
            ]
        })
        stops['STOP_REASON'] = stops['STOP_REASON'].apply(fix_STOP_REASON)
        add_purpose_column(stops)
        for i, e in enumerate(data):
            raw_reason, cleaned_reason, expected_purpose = e
            self.assertEqual(stops.STOP_REASON[i], cleaned_reason)
            self.assertEqual(stops.purpose[i], expected_purpose, 'Expected purpose %d for "%s", got %d' % (
                expected_purpose, raw_reason, stops.purpose[i]
            ))

    def test_agency_names(self):
        stops = pd.DataFrame({
            'AGENCY': ['!@#$', 'BACOPD', 'CECIL'],
            'expected_AGENCY': ['!@#$', 'Baltimore County Police Department', "Cecil County Sheriff's Office"]
        })
        fix_AGENCY_column(stops)
        self.assertTrue(all(stops.AGENCY == stops.expected_AGENCY))

    def test_overall_processing(self):
        """
        Check the high-level logic in process_raw_data()

        Detailed cleanup/transformation of individual cells or columns is
        tested in other methods.
        """
        stops = pd.DataFrame({
            'STOPDATE': ['01/01/13', '04/05/13'],
            'TIME_OF_STOP': ['13:45', '13:07'],
            'LOCATION': ['some address', 'some other address'],
            'STOP_REASON': ['21-202(h1)', '21-201(a1)'],
            'SEARCH_CONDUCTED': ['N', 'Y'],
            'SEIZED': ['', 'Contraband'],
            'GENDER': ['M', 'F'],
            'DOB': ['01/10/72', '06/26/79'],
            'ETHNICITY': ['BLACK', 'ASIAN'],
            'OFFICERID': ['12149', '2376'],
            'AGENCY': ['MTA', 'HURLOCK'],
            # columns which are dropped
            'WHATSEARCHED': [1, 1],
            'STOPOUTCOME': [1, 1],
            'CRIME_CHARGED': [1, 1],
            'REGISTRATION_STATE': [1, 1],
            'RESIDENCE_STATE': [1, 1],
            'MD_COUNTY': [1, 1]
        })
        stops = process_raw_data(stops)
        self.assertEqual(stops.columns[0], 'index')
        self.assertEqual(stops.index[0], 0)
        self.assertEqual(len(stops.index), 2)
        self.assertIn('date', stops.columns)
        self.assertIn('computed_AGE', stops.columns)
        self.assertIn('purpose', stops.columns)
        self.assertNotIn('CRIME_CHARGED', stops.columns)
