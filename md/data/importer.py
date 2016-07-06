import csv
import datetime
import logging
import math
import os
import re

import pandas as pd

from django.db import connections
from django.conf import settings

from md.models import PURPOSE_BY_INDEX, PURPOSE_CHOICES, UNKNOWN_PURPOSE
from tsdata.sql import drop_constraints_and_indexes
from tsdata.utils import (call, download_and_unzip_data, get_csv_path,
     get_datafile_path, line_count)


logger = logging.getLogger(__name__)

STOP_REASON_CSV = 'md/data/STOP_REASON-normalization.csv'
PURPOSE_BY_STOP_REASON = dict()

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
    'UNKNOWN': 'U',
    'OTHER': 'U'
}

STOP_REASON_cleanup_re = re.compile(r'^ *(\d+) *- *(\d+) *\(.*\) *$')  # used to remove blanks
STOP_REASON_simplify_re = re.compile(r'^(\d+)-(\d+)')  # used to ignore minor references

DOB_re = re.compile(r'^(\d\d?)/(\d\d?)/(\d\d?)$')

MD_COLUMNS_TO_DROP = (
    'WHATSEARCHED', 'STOPOUTCOME', 'CRIME_CHARGED',
    'REGISTRATION_STATE', 'RESIDENCE_STATE', 'MD_COUNTY',
)


def load_STOP_REASON_normalization_rules():
    """
    Read a CSV file that contains a column of STOP_REASON values for each of
    the md.models.PURPOSE_CHOICES.  The CSV file is from an Excel workbook
    provided by SCSJ with minimal editing.

    Sanity check that the headings in the CSV roughly match PURPOSE_CHOICES.

    Output: Fill in global dictionary PURPOSE_BY_STOP_REASON.
    """
    CELL_re = re.compile(r'^(\d\d?-\d\d\d\d?|\d\d\*|\d\d)')
    BLANK_re = re.compile(r'^ *$')

    def clean_cell(s, line_number):
        m = CELL_re.match(s)
        if not m:
            raise ValueError('Line %d of %s has bad cell value "%s"' % (
                line_number, STOP_REASON_CSV, s
            ))
        return m.group(1)

    with open(STOP_REASON_CSV, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        headings = next(reader)

        # Ensure that the headings in STOP_REASON_CSV roughly match the strings
        # in PURPOSE_CHOICES.  (Ignore case and extra trailing text in the CSV.)
        if len(headings) != len(PURPOSE_CHOICES):
            raise ValueError('PURPOSE_CHOICES out of sync with headings in %s' % STOP_REASON_CSV)
        for i, heading in enumerate(headings):
            if not heading.lower().startswith(PURPOSE_BY_INDEX[i].lower()):
                raise ValueError('PURPOSE_CHOICES[%d] out of sync with heading in %s' % (
                    i, STOP_REASON_CSV
                ))

        line_number = 2
        for row in reader:
            line_number += 1
            for i, val in enumerate(row):
                if not BLANK_re.match(val):
                    val = clean_cell(val, line_number)
                    PURPOSE_BY_STOP_REASON[val] = i


def fix_ETHNICITY(s):
    if ETHNICITY_WHITE_re.match(s):
        return 'W'
    elif ETHNICITY_BLACK_re.match(s):
        return 'B'
    else:
        code = ETHNICITY_TO_CODE.get(s)
        if code:
            return code
        logger.info('Bad ethnicity: "%s"', s)
        return 'U'


def fix_GENDER(s):
    if GENDER_MALE_re.match(s):
        return 'M'
    elif GENDER_FEMALE_re.match(s):
        return 'F'
    else:
        logger.info('Bad gender: "%s"', s)
        return 'U'


def fix_SEIZED(s):
    if SEIZED_CONTRABAND_re.match(s):
        return 'Y'
    else:
        return 'N'


def fix_STOP_REASON(s):
    m = STOP_REASON_cleanup_re.match(s)
    if m:
        return m.group(1) + '-' + m.group(2)
    else:
        return s


def purpose_from_STOP_REASON(s):
    normalized = PURPOSE_BY_STOP_REASON.get(s)
    if not normalized:
        m = STOP_REASON_simplify_re.match(s)
        if m:
            normalized = PURPOSE_BY_STOP_REASON.get('%s-%s' % (m.group(1), m.group(2)))
    if not normalized:
        logger.info('Bad STOP_REASON: "%s"', s)
        normalized = UNKNOWN_PURPOSE
    return normalized


def fix_TIME_OF_STOP(s):
    s = s.strip()
    m = TIME_OF_STOP_re.match(s)
    if not m:
        logger.info('Bad time of stop: "%s"', s)
        return DEFAULT_TIME_OF_STOP
    hour = int(m.group(1))
    minute = int(m.group(2))
    if not 0 <= hour < 24 or not 0 <= minute < 60:
        logger.info('Bad time of stop: "%s"', s)
        return DEFAULT_TIME_OF_STOP
    return s


def compute_AGE(row):
    dob = row['DOB']
    stop_date = row['date']

    m = DOB_re.match(dob)
    if not m:
        age = 0
    else:
        dob_year = int(m.group(3))
        stop_date_year = stop_date.year
        stop_date_year_of_century = stop_date_year % 100
        stop_date_century = int(math.floor(stop_date_year / 100.0)) * 100

        if dob_year >= stop_date_year_of_century:
            dob_year += (stop_date_century - 100)
        else:
            dob_year += stop_date_century

        dob = datetime.datetime(dob_year, int(m.group(1)), int(m.group(2)))
        delta = stop_date - dob
        age = int(delta.days / 365.25)

    return age


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
    stops['computed_AGE'] = stops.apply(compute_AGE, axis=1)


def add_purpose_column(stops):
    load_STOP_REASON_normalization_rules()
    stops['purpose'] = stops['STOP_REASON'].apply(purpose_from_STOP_REASON)


def process_raw_data(stops):
    # Drop some columns
    stops.drop(list(MD_COLUMNS_TO_DROP), axis=1, inplace=True)

    # Fix data
    stops['TIME_OF_STOP'] = stops['TIME_OF_STOP'].apply(fix_TIME_OF_STOP)
    stops['GENDER'] = stops['GENDER'].apply(fix_GENDER)
    stops['SEIZED'] = stops['SEIZED'].apply(fix_SEIZED)
    stops['ETHNICITY'] = stops['ETHNICITY'].apply(fix_ETHNICITY)

    # Add date, age, purpose, and index columns
    add_date_column(stops)
    add_age_column(stops)
    add_purpose_column(stops)
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
    # drop constraints/indexes
    drop_constraints_and_indexes(connections['traffic_stops_md'].cursor())
    # use COPY to load CSV files as quickly as possible
    copy_from(csv_path)


def copy_from(csv_path):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    cmd = ['psql',
           '-v', 'data_file={}'.format(csv_path),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_md']['NAME']]
    if settings.DATABASE_ETL_USER:
        cmd.append(settings.DATABASE_ETL_USER)
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
