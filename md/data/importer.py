import logging
import os
import re

import pandas as pd

from django.conf import settings

from tsdata.util import (call, download_and_unzip_data, get_csv_path,
     get_datafile_path, line_count)


logger = logging.getLogger(__name__)

TIME_OF_STOP_re = re.compile(r'(\d?\d):(\d\d)( [AP]M)?$')
DEFAULT_TIME_OF_STOP = '00:00'

GENDER_MALE_re = re.compile(r'^(M|male|MALE|m +)$')
GENDER_FEMALE_re = re.compile(r'^(F|female|w|F +)$')

SEIZED_CONTRABAND_re = re.compile(r'^(Contraband.*|paraphernalia.*|Both)$')

ETHNICITY_WHITE_re = re.compile(r'^(WHITE|W|W.)$')
ETHNICITY_BLACK_re = re.compile(r'^(BLACK|BLK)$')
ETHNICITY_TO_CODE = {
    'HISPANIC': 'H',
    'ASIAN': 'A',
    'NATIVE AMERICAN': 'I',
}

STOP_REASON_re = re.compile(r'^ *(\d+) *- *(\d+) *\(.*\) *$')

MD_COLUMNS_TO_DROP = (
    'WHATSEARCHED', 'STOPOUTCOME', 'CRIME_CHARGED',
    'REGISTRATION_STATE', 'RESIDENCE_STATE', 'MD_COUNTY',
)


def fix_ETHNICITY(s):
    if ETHNICITY_WHITE_re.match(s):
        return 'W'
    elif ETHNICITY_BLACK_re.match(s):
        return 'B'
    else:
        return ETHNICITY_TO_CODE.get(s, 'U')


def fix_GENDER(s):
    if GENDER_MALE_re.match(s):
        return 'M'
    elif GENDER_FEMALE_re.match(s):
        return 'F'
    else:
        return 'U'


def fix_SEIZED(s):
    if SEIZED_CONTRABAND_re.match(s):
        return 'Y'
    else:
        return 'N'


def fix_STOP_REASON(s):
    m = STOP_REASON_re.match(s)
    if m:
        return m.group(1) + '-' + m.group(2)
    else:
        return s


def fix_TIME_OF_STOP(s):
    s = s.strip()
    m = TIME_OF_STOP_re.match(s)
    if not m:
        return DEFAULT_TIME_OF_STOP
    hour = int(m.group(1))
    minute = int(m.group(2))
    if not 0 <= hour < 24:
        return DEFAULT_TIME_OF_STOP
    if not 0 <= minute < 60:
        return DEFAULT_TIME_OF_STOP
    return s


def compute_AGE(row):
    stop_date = row['date']
    dob = row['DOB_as_dt']
    if pd.isnull(dob) or dob > stop_date:
        return 0
    else:
        delta = stop_date - dob
        return int(delta.days / 365.25)


def load_xls(xls_path):
    logger.info('Loading {} into pandas'.format(xls_path))
    num_sheets = 3
    df_dict = pd.read_excel(
        xls_path, sheetname=list(range(num_sheets)),
        keep_default_na=False, na_values=[]
    )
    for i in range(1, num_sheets):
        df_dict[i].columns = df_dict[0].columns
    stops = pd.concat(
        [df_dict[k] for k in sorted(df_dict.keys())],
        ignore_index=True
    )
    return stops


def add_date_column(stops):
    blank = pd.DataFrame({'blank': ' '}, index=range(len(stops['STOPDATE'])))
    stops['date'] = pd.to_datetime(stops['STOPDATE'].map(str) + blank['blank'].map(str) + stops['TIME_OF_STOP'].map(str))


def add_age_column(stops):
    stops['DOB_as_dt'] = pd.to_datetime(stops.DOB)
    stops['computed_AGE'] = stops.apply(compute_AGE, axis=1)
    stops.drop(['DOB_as_dt'], axis=1, inplace=True)


def process_raw_data(stops):
    # Drop some columns
    stops.drop(list(MD_COLUMNS_TO_DROP), axis=1, inplace=True)

    # Fix data
    stops['TIME_OF_STOP'] = stops['TIME_OF_STOP'].apply(fix_TIME_OF_STOP)
    stops['GENDER'] = stops['GENDER'].apply(fix_GENDER)
    stops['SEIZED'] = stops['SEIZED'].apply(fix_SEIZED)
    stops['ETHNICITY'] = stops['ETHNICITY'].apply(fix_ETHNICITY)

    # Add age, index, and date columns
    add_date_column(stops)
    add_age_column(stops)
    stops['index'] = range(1, len(stops) + 1)  # adds column at end

    # move the index column to the front
    stops = stops[stops.columns.tolist()[-1:] + stops.columns.tolist()[:-1]]
    return stops


def xls_to_csv(xls_path, csv_path):
    assert not os.path.exists(csv_path)
    stops = load_xls(xls_path)
    stops = process_raw_data(stops)
    logger.info("Converting {} > {}".format(xls_path, csv_path))
    stops.to_csv(csv_path, index=False)
    return stops


def run(url, destination=None, download=True):
    """Download MD data, extract, convert to CSV, and load into PostgreSQL"""
    logger.info('*** MD Data Import Started ***')
    destination = download_and_unzip_data(url, destination)
    # Convert to CSV
    xls_path = get_datafile_path(url, destination)
    csv_path = get_csv_path(url, destination)
    if not os.path.exists(csv_path):
        xls_to_csv(xls_path, csv_path)
    else:
        logger.info("{} exists, skipping XLS->CSV conversion".format(csv_path))
    csv_count = line_count(csv_path)
    logger.debug('Rows: {}'.format(csv_count))
    # use COPY to load CSV files as quickly as possible
    copy_from(csv_path)


def copy_from(csv_path):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    cmd = ['psql',
           '-v', 'data_file={}'.format(csv_path),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_md']['NAME']]
    if settings.DATABASES['traffic_stops_md']['USER']:
        cmd.append(settings.DATABASES['traffic_stops_md']['USER'])
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
