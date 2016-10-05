from django.test import TestCase
import pandas as pd

from il.data.importer import (
    fixup_contraband, fixup_race, fixup_search, fixup_stop_purpose,
    load_IL_agency_mappings, lookup_agency, process_raw_data
)
from il.models import ETHNICITY_CHOICES, UNKNOWN_PURPOSE


class TestFieldNormalization(TestCase):
    # if db calls are added: multi_db = True

    def test_fixup_contraband(self):
        self.assertEqual(fixup_contraband('Y'), 'Y')
        self.assertEqual(fixup_contraband('N'), 'N')
        self.assertEqual(fixup_contraband(''), 'U')

    def test_fixup_race(self):
        self.assertEqual(fixup_race('O'), 'U')
        for choice in ETHNICITY_CHOICES:
            self.assertEqual(fixup_race(choice[0]), choice[0])

    def test_fixup_search(self):
        self.assertEqual(fixup_search('Y'), 'Y')
        self.assertEqual(fixup_search('N'), 'N')
        self.assertEqual(fixup_search(''), 'U')

    def test_fixup_stop_purpose(self):
        self.assertEqual(fixup_stop_purpose('Moving Violation'), 1)
        self.assertEqual(fixup_stop_purpose('xxMoving Violation'), UNKNOWN_PURPOSE)

    def test_lookup_valid_agency_id(self):
        agency_id = 10011
        load_IL_agency_mappings()
        self.assertEqual('Dolton Police', lookup_agency(agency_id))

    def test_lookup_invalid_agency_id(self):
        agency_id = 910011
        load_IL_agency_mappings()
        self.assertEqual('910011', lookup_agency(agency_id))

    def test_overall_processing(self):
        """
        Check the high-level logic in process_raw_data()

        Detailed cleanup/transformation of individual cells or columns is
        tested in other methods.
        """
        stops = pd.DataFrame({
            'agencycode': [10011, 12988],
            'agencyname': ['DOLTON POLICE DEPARTMENT', 'SOUTH HOLLAND POLICE'],
            'Gender': ['F', 'M'],
            'Race': ['B', 'W'],
            'Search': ['N', ''],
            'Contraband': ['', 'Y'],
            'StopPurpose': ['Moving Violation', 'Equipment'],
            'year': [2004, 2010],
        })
        stops = process_raw_data(stops)
        self.assertEqual(stops.columns[0], 'index')
        self.assertEqual(stops.index[0], 0)
        self.assertEqual(len(stops.index), 2)
        self.assertIn('purpose', stops.columns)
        self.assertNotIn('agencycode', stops.columns)
        self.assertNotIn('agencyname', stops.columns)
        self.assertNotIn('StopPurpose', stops.columns)
