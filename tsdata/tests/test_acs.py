from django.test import TestCase

from tsdata import acs


class ACSTests(TestCase):
    expected_race_variables = [
        'total', 'white', 'black', 'native_american', 'asian', 'native_hawaiian',
        'other', 'two_or_more_races', 'hispanic', 'non_hispanic'
    ]

    def test_nc_variables(self):
        acs_obj = acs.ACS('', 'NC')
        self.assertCountEqual(
            acs_obj.race_variables.values(),
            self.expected_race_variables
        )
        self.assertCountEqual(
            acs_obj.variables,
            ['NAME', 'GEO_ID', 'B03002_001E', 'B03002_003E', 'B03002_004E',
             'B03002_005E', 'B03002_006E', 'B03002_007E', 'B03002_008E',
             'B03002_009E', 'B03002_012E', 'B03002_002E']
        )

    def test_il_variables(self):
        acs_obj = acs.ACS('', 'IL')
        self.assertCountEqual(
            acs_obj.race_variables.values(),
            self.expected_race_variables
        )
        self.assertCountEqual(
            acs_obj.variables,
            ['NAME', 'GEO_ID', 'C02003_001E', 'C02003_003E', 'C02003_004E',
             'C02003_005E', 'C02003_006E', 'C02003_007E', 'C02003_008E',
             'C02003_009E', 'B03002_012E', 'B03002_002E']
        )

    def test_md_variables(self):
        acs_obj = acs.ACS('', 'MD')
        self.assertCountEqual(
            acs_obj.race_variables.values(),
            self.expected_race_variables
        )
        self.assertCountEqual(
            acs_obj.variables,
            ['NAME', 'GEO_ID', 'C02003_001E', 'C02003_003E', 'C02003_004E',
             'C02003_005E', 'C02003_006E', 'C02003_007E', 'C02003_008E',
             'C02003_009E', 'B03002_012E', 'B03002_002E']
        )

    def test_other_state(self):
        with self.assertRaises(KeyError):
            acs.ACS('', 'NY')
