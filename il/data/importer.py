import csv
import logging
import os

from django.db import connections
from django.conf import settings
import pandas as pd

from il.models import UNKNOWN_PURPOSE
from tsdata.sql import drop_constraints_and_indexes
from tsdata.utils import (call, download_and_unzip_data, get_csv_path,
                          get_datafile_path, line_count)


logger = logging.getLogger(__name__)

AGENCY_MAPPING_CSV = 'il/data/IL_agencies.csv'
AGENCY_NAME_BY_CODE = dict()

STOP_PURPOSE_TO_CODE = {
    'Moving Violation': 1,
    'Equipment': 2,
    'Registration': 3,
}


def load_IL_agency_mappings():
    """
    Read a CSV file that maps agency codes (as used in raw stop data) to
    agency names and optional census GEOID values.

    When the proper agency name hasn't been determined, it has the same value as
    the agency code.
    """
    AGENCY_NAME_BY_CODE.clear()
    with open(AGENCY_MAPPING_CSV, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip headings
        line_number = 1
        for code, name, _ in reader:
            line_number += 1
            if code in AGENCY_NAME_BY_CODE:
                raise ValueError('Line %d of %s has duplicated agency code "%s"' % (
                    line_number, AGENCY_MAPPING_CSV, code,
                ))
            AGENCY_NAME_BY_CODE[code] = name


def load_csv(csv_path):
    logger.info('Loading {} into pandas'.format(csv_path))
    stops = pd.read_csv(
        csv_path,
        keep_default_na=False, na_values=[]
    )
    return stops


def lookup_agency(s):
    name = AGENCY_NAME_BY_CODE.get(str(s))
    if not name:
        logger.error('Agency code "%s" not in %s', s, AGENCY_MAPPING_CSV)
        name = s
    return name


def add_agency_column(stops):
    load_IL_agency_mappings()
    stops['agency'] = stops['agencycode'].apply(lookup_agency)


def fixup_race(s):
    return 'U' if s == 'O' else s


def contraband_to_seized(s):
    return 'U' if s == '' else s


def search_to_search(s):
    return 'U' if s == '' else s


def stop_purpose_to_purpose(s):
    return STOP_PURPOSE_TO_CODE.get(s, UNKNOWN_PURPOSE)


def process_raw_data(stops):
    stops['Race'] = stops['Race'].apply(fixup_race)
    stops['Search'] = stops['Search'].apply(search_to_search)
    stops['Contraband'] = stops['Contraband'].apply(contraband_to_seized)
    stops['purpose'] = stops['StopPurpose'].apply(stop_purpose_to_purpose)
    add_agency_column(stops)
    stops['index'] = range(1, len(stops) + 1)  # adds column at end

    stops.drop(['agencycode', 'agencyname', 'StopPurpose'], axis=1, inplace=True)

    # move the index column to the front
    stops = stops[stops.columns.tolist()[-1:] + stops.columns.tolist()[:-1]]
    return stops


def raw_to_processed(raw_csv_path, processed_csv_path):
    assert not os.path.exists(processed_csv_path)
    stops = load_csv(raw_csv_path)
    stops = process_raw_data(stops)
    logger.info("Converting {} > {}".format(raw_csv_path, processed_csv_path))
    stops.to_csv(processed_csv_path, index=False)
    return stops


def run(url, destination=None, download=True):
    """Download IL data, extract, and load into PostgreSQL"""
    logger.info('*** IL Data Import Started ***')
    destination = download_and_unzip_data(url, destination)
    # Convert to CSV
    raw_csv_path = get_datafile_path(url, destination)
    processed_csv_path = get_csv_path(url, destination)
    if not os.path.exists(processed_csv_path):
        raw_to_processed(raw_csv_path, processed_csv_path)
    else:
        logger.info("{} exists, skipping cleanup".format(processed_csv_path))
    csv_count = line_count(processed_csv_path)
    logger.debug('Rows: {}'.format(csv_count))
    # drop constraints/indexes
    drop_constraints_and_indexes(connections['traffic_stops_il'].cursor())
    # use COPY to load CSV file as quickly as possible
    copy_from(processed_csv_path)


def copy_from(csv_path):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    il_csv_path = os.path.join(
        os.path.dirname(__file__),
        os.path.basename(AGENCY_MAPPING_CSV)
    )
    cmd = ['psql',
           '-v', 'data_file={}'.format(csv_path),
           '-v', 'il_time_zone={}'.format(settings.IL_TIME_ZONE),
           '-v', 'il_csv_table={}'.format(il_csv_path),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_il']['NAME']]
    if settings.DATABASE_ETL_USER:
        cmd.append(settings.DATABASE_ETL_USER)
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
