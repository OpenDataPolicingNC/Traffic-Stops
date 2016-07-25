# American Community Survey 5-Year Data (2005-2009 to 2010-2014)
# http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html
#
# Notes:
#  - Examples: http://api.census.gov/data/2014/acs5/examples.html
#  - Places: https://www.census.gov/content/dam/Census/data/developers/understandingplace.pdf
#
# Fact Finder:
#  - Home: http://factfinder.census.gov/faces/nav/jsf/pages/index.xhtml
#  - Baltimore: http://factfinder.census.gov/bkmk/cf/1.0/en/county/Baltimore city, Maryland/RACE_AND_HISPANIC_ORIGIN  # noqa
#  - Baltimore Races: http://factfinder.census.gov/bkmk/table/1.0/en/ACS/14_5YR/DP05/0500000US24510

import census
import pandas as pd
from us import states

from tsdata.models import CensusProfile, STATE_CHOICES
from django.db import transaction


# Variables: http://api.census.gov/data/2014/acs5/variables.html
RACE_VARIABLES = {
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
VARIABLES = ['NAME'] + list(RACE_VARIABLES.keys())  # NAME = geography/location


class ACS(object):
    """Base class to call ACS API and normalize output"""

    source = "ACS 5-Year Data (2010-2014)"
    geography = None
    unique_ids = None
    drop_columns = None

    def __init__(self, key, state_abbr):
        self.api = census.Census(key)
        self.fips = getattr(states, state_abbr).fips
        self.state_abbr = state_abbr

    def call_api(self):
        raise NotImplemented()

    def get(self):
        # load response (list of dicts) into pandas
        df = pd.DataFrame(self.call_api())
        # insert metadata
        df['state'] = self.state_abbr
        df['source'] = self.source
        df['geography'] = self.geography
        # add unique id
        df['id'] = df.apply(lambda x: ''.join([getattr(x, col) for col in self.unique_ids]),  # noqa
                            axis=1)
        # rename common columns
        df.rename(columns={'NAME': 'location'}, inplace=True)
        # replace census variable names with easier to read race labels
        df.rename(columns=RACE_VARIABLES, inplace=True)
        # convert race columns to numerics
        num_cols = list(RACE_VARIABLES.values())
        df[num_cols] = df[num_cols].apply(pd.to_numeric)
        # remove unused columns
        if self.drop_columns:
            df.drop(self.drop_columns, axis=1, inplace=True)
        return df


class ACSStateCounties(ACS):
    """
    State County Demographics
    ex: http://api.census.gov/data/2014/acs5?get=NAME&for=county:*&in=state:24
    code: https://github.com/sunlightlabs/census/blob/master/census/core.py#L181
    """
    unique_ids = ('state', 'county')
    geography = 'county'
    drop_columns = ['county']

    def call_api(self):
        return self.api.acs.state_county(VARIABLES, self.fips, census.ALL)


class ACSStatePlaces(ACS):
    """
    State Place Demographics
    ex: http://api.census.gov/data/2014/acs5?get=NAME&for=place:*&in=state:24
    code: https://github.com/sunlightlabs/census/blob/master/census/core.py#L215
    """
    unique_ids = ('state', 'place')
    geography = 'place'
    drop_columns = ['place']

    def call_api(self):
        return self.api.acs.state_place(VARIABLES, self.fips, census.ALL)

    def get(self):
        df = super(ACSStatePlaces, self).get()
        # ignore Census Designated Places (CDP)
        return df[df.location.str.contains('CDP') is False]


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
            total=row['non_hispanic'],
        )
        profiles.append(profile)
    CensusProfile.objects.bulk_create(profiles)
