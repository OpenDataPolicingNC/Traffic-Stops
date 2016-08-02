from django.test import TestCase

from tsdata.tests.factories import CensusProfileFactory


class ModelTests(TestCase):

    def test_census_dict(self):

        def sum_these_keys(d, keys):
            return sum([
                d[key] for key in keys
            ])

        cp = CensusProfileFactory()
        census_dict = cp.get_census_dict()
        race_keys = (
            'white', 'black', 'native_american', 'asian', 'other'
        )
        ethnicity_keys = (
            'hispanic', 'non_hispanic'
        )
        self.assertEqual(
            set(census_dict.keys()),
            set(race_keys + ethnicity_keys + ('total',))
        )
        self.assertEqual(
            sum_these_keys(census_dict, race_keys),
            sum_these_keys(census_dict, ('total',))
        )
        self.assertEqual(
            sum_these_keys(census_dict, ethnicity_keys),
            sum_these_keys(census_dict, ('total',))
        )
