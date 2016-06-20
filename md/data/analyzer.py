import logging
import os

import pandas as pd

from tsdata.util import download_and_unzip_data
from md.data import DATASET_BASENAME
from md.data.importer import load_xls

logger = logging.getLogger(__name__)

# TODO: Compute an age column and analyze that too.
COLUMNS_TO_ANALYZE = (
    'DURATION', 'STOP_REASON', 'SEARCH_CONDUCTED', 'SEARCH_REASON',
    'WHATSEARCHED', 'SEIZED', 'STOPOUTCOME', 'CRIME_CHARGED',
    'REGISTRATION_STATE', 'GENDER', 'RESIDENCE_STATE', 'MD_COUNTY',
    'ETHNICITY', 'AGENCY',
)


def run(url, report, destination=None, download=True):
    """Download MD data, extract, convert to CSV, and scan for issues"""
    logger.info('*** MD Data Analysis Started ***')
    destination = download_and_unzip_data(url, destination)
    xls_path = os.path.join(destination, DATASET_BASENAME + '.xlsx')
    stops = load_xls(xls_path)
    analyze(stops, report)


def analyze(stops, report):
    stops['datetime'] = pd.to_datetime(stops['STOPDATE'])
    years = stops['datetime'].map(lambda x: x.year)
    for col in COLUMNS_TO_ANALYZE:
        print('Column %s:' % col, file=report)
        print('', file=report)
        print('%s over entire dataset:' % col, file=report)
        print(getattr(stops, col).value_counts(), file=report)
        print('', file=report)
        print('%s by year:' % col, file=report)
        print(stops.groupby([years, getattr(stops, col)])[col].count(), file=report)
        print('', file=report)
        print('-' * 50, file=report)
