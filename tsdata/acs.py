# American Community Survey 5-Year Data (2005-2009 to 2010-2014)
# http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html
#
# Notes:
#  - Examples: http://api.census.gov/data/2014/acs5/examples.html
#  - Places: https://www.census.gov/content/dam/Census/data/developers/understandingplace.pdf

import census
import pandas as pd
from us import states


# Variables: http://api.census.gov/data/2014/acs5/variables.html
RACE_VARIABLES = {
    'C02003_001E': 'total',
    'C02003_003E': 'white',
    'C02003_004E': 'black',
    'C02003_005E': 'native_american',
    'C02003_006E': 'asian',
    'B03002_012E': 'hispanic',  # TODO: need to verify - maybe B03002_012E?
    'C02003_008E': 'other',  # TODO: need to verify
}
VARIABLES = ['NAME'] + list(RACE_VARIABLES.keys())  # NAME = geography/location


def get_state_census_data(key, state_abbr):
    """Download several Census endpoints into a single DataFrame"""
    counties = get_county_populations(key, state_abbr)
    subdivs = get_subdivision_populations(key, state_abbr)
    df = pd.concat([counties, subdivs])
    # add state column
    df['state'] = state_abbr
    # convert race columns to numeric
    num_cols = list(RACE_VARIABLES.values())
    df[num_cols] = df[num_cols].apply(pd.to_numeric)
    return df


def get_county_populations(key, state_abbr):
    """
    Return list of state's counties.
    ex: http://api.census.gov/data/2014/acs5?get=NAME&for=county:*&in=state:24
    code: https://github.com/sunlightlabs/census/blob/master/census/core.py#L181
    """
    # request census data
    c = census.Census(key)
    fips = getattr(states, state_abbr).fips
    data = c.acs.state_county(VARIABLES, fips, census.ALL)
    # load response (list of dicts) into pandas
    df = pd.DataFrame(data)
    # rename columns to include race labels
    df.rename(columns={'NAME': 'location'}, inplace=True)
    df.rename(columns=RACE_VARIABLES, inplace=True)
    # create unique id column
    df['id'] = df.apply(lambda x: x['state'] + x['county'], axis=1)
    # add source info
    df['source'] = "ACS 5-Year Data (2010-2014)"
    df['type'] = 'County'
    # remove unused columns
    df.drop(['county', 'state'], axis=1, inplace=True)
    return df


def get_subdivision_populations(key, state_abbr):
    """
    Return list of state's county subdivisions.
    ex: http://api.census.gov/data/2014/acs5?get=NAME&for=county+subdivision:*&in=state:24
    """
    # request census data
    c = census.Census(key)
    fips = getattr(states, state_abbr).fips
    geo = {'for': 'county subdivision:{}'.format(census.ALL),
           'in': 'state:{}'.format(fips)}
    data = c.acs.get(VARIABLES, geo)
    # load response (list of dicts) into pandas
    df = pd.DataFrame(data)
    # rename columns to include race labels
    df.rename(columns={'NAME': 'location'}, inplace=True)
    df.rename(columns=RACE_VARIABLES, inplace=True)
    # create unique id column
    df['id'] = df.apply(lambda x: x['state'] + x['county'] + x['county subdivision'], axis=1)
    # add static info
    df['source'] = "ACS 5-Year Data (2010-2014)"
    df['type'] = 'County Subdivision'
    # remove unused columns
    df.drop(['county', 'state', 'county subdivision'], axis=1, inplace=True)
    return df
