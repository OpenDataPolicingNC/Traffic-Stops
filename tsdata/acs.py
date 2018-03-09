# American Community Survey 5-Year Data
# https://www.census.gov/data/developers/data-sets/acs-5year.2016.html
#
# Notes:
#  - Examples: http://api.census.gov/data/2016/acs/acs5/examples.html
#  - Places: https://www.census.gov/content/dam/Census/data/developers/understandingplace.pdf
#
# Fact Finder:
#  - Home: http://factfinder.census.gov/faces/nav/jsf/pages/index.xhtml
#  - Durham city, NC: https://factfinder.census.gov/bkmk/table/1.0/en/ACS/16_5YR/DP05/1600000US3719000  # noqa

import census
import pandas as pd
from us import states

from django.conf import settings
from django.db import transaction

from tsdata.models import CensusProfile, STATE_CHOICES


# Variables: http://api.census.gov/data/2016/acs/acs5/variables.json
NC_RACE_VARS = {
    'B03002_001E': 'total',              # Estimate!!Total
    'B03002_003E': 'white',              # Estimate!!Total!!Not Hispanic or Latino!!White alone
    'B03002_004E': 'black',              # Estimate!!Total!!Not Hispanic or Latino!!Black or African American alone  # noqa
    'B03002_005E': 'native_american',    # Estimate!!Total!!Not Hispanic or Latino!!American Indian and Alaska Native alone  # noqa
    'B03002_006E': 'asian',              # Estimate!!Total!!Not Hispanic or Latino!!Asian alone
    'B03002_007E': 'native_hawaiian',    # Estimate!!Total!!Not Hispanic or Latino!!Native Hawaiian and Other Pacific Islander alone  # noqa
    'B03002_008E': 'other',              # Estimate!!Total!!Not Hispanic or Latino!!Some other race alone  # noqa
    'B03002_009E': 'two_or_more_races',  # Estimate!!Total!!Not Hispanic or Latino!!Two or more races  # noqa
    'B03002_012E': 'hispanic',           # Estimate!!Total!!Hispanic or Latino
    'B03002_002E': 'non_hispanic',       # Estimate!!Total!!Not Hispanic or Latino
}

OTHER_RACE_VARS = {
    'C02003_001E': 'total',
    'C02003_003E': 'white',
    'C02003_004E': 'black',
    'C02003_005E': 'native_american',
    'C02003_006E': 'asian',
    'C02003_007E': 'native_hawaiian',
    'C02003_008E': 'other',
    'C02003_009E': 'two_or_more_races',
    'B03002_012E': 'hispanic',
    'B03002_002E': 'non_hispanic',
}

RACE_VARIABLES = {
    settings.NC_KEY.upper(): NC_RACE_VARS,
    settings.IL_KEY.upper(): OTHER_RACE_VARS,
    settings.MD_KEY.upper(): OTHER_RACE_VARS,
}


class ACS(object):
    """Base class to call ACS API and normalize output"""

    source = "ACS 5-Year Data (2012-2016)"
    geography = None
    drop_columns = None

    def __init__(self, key, state_abbr):
        self.api = census.Census(key, year=2016)
        self.fips = getattr(states, state_abbr).fips
        self.state_abbr = state_abbr

        self.race_variables = RACE_VARIABLES[state_abbr]
        # NAME = geography/location
        # GEO_ID = combination of country, state, county
        self.variables = ['NAME', 'GEO_ID'] + list(self.race_variables.keys())

    def call_api(self):
        raise NotImplemented()

    def get(self):
        # load response (list of dicts) into pandas
        df = pd.DataFrame(self.call_api())
        # insert metadata
        df['state'] = self.state_abbr
        df['source'] = self.source
        df['geography'] = self.geography
        # rename common columns
        df.rename(columns={'NAME': 'location', 'GEO_ID': 'id'}, inplace=True)
        # replace census variable names with easier to read race labels
        df.rename(columns=self.race_variables, inplace=True)
        # convert race columns to numerics
        num_cols = list(self.race_variables.values())
        df[num_cols] = df[num_cols].apply(pd.to_numeric)
        # remove unused columns
        if self.drop_columns:
            df.drop(self.drop_columns, axis=1, inplace=True)
        return df


class ACSStateCounties(ACS):
    """
    State County Demographics
    ex: http://api.census.gov/data/2016/acs/acs5?get=NAME&for=county:*&in=state:24
    """
    geography = 'county'
    drop_columns = ['county']

    def call_api(self):
        return self.api.acs5.state_county(self.variables, self.fips, census.ALL)


class ACSStatePlaces(ACS):
    """
    State Place Demographics
    ex: http://api.census.gov/data/2016/acs/acs5?get=NAME&for=place:*&in=state:24
    """
    geography = 'place'
    drop_columns = ['place']

    def call_api(self):
        return self.api.acs5.state_place(self.variables, self.fips, census.ALL)

    def get(self):
        df = super(ACSStatePlaces, self).get()
        # ignore Census Designated Places (CDP)
        return df[~df.location.str.contains('CDP')]


def get_state_census_data(key):
    """Download several state Census endpoints into a single DataFrame"""
    profiles = []
    for state in [abbr.upper() for abbr, name in STATE_CHOICES]:
        profiles.append(ACSStateCounties(key, state).get())
        profiles.append(ACSStatePlaces(key, state).get())
    return pd.concat(profiles)


@transaction.atomic
def refresh_census_models(data):
    profiles = []
    CensusProfile.objects.all().delete()
    for row in data:
        profile = CensusProfile(
            id=row['id'],
            location=row['location'],
            geography=row['geography'],
            state=row['state'],
            source=row['source'],
            white=row['white'],
            black=row['black'],
            native_american=row['native_american'],
            asian=row['asian'],
            native_hawaiian=row['native_hawaiian'],
            other=row['other'],
            two_or_more_races=row['two_or_more_races'],
            hispanic=row['hispanic'],
            non_hispanic=row['non_hispanic'],
            total=row['total'],
        )
        profiles.append(profile)
    CensusProfile.objects.bulk_create(profiles)
