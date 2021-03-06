# Implementation of analyze_md command, not used for actual data import
#
# This will report some statistics used to understand common field values as
# well as the dataset facts used on the Maryland landing page.

import logging

import pandas as pd

from tsdata.utils import download_and_unzip_data, get_datafile_path
from md.data.importer import load_xls, process_raw_data

logger = logging.getLogger(__name__)

COLUMNS_TO_ANALYZE = (
    'DURATION', 'STOP_REASON', 'SEARCH_CONDUCTED', 'SEARCH_REASON',
    'WHATSEARCHED', 'SEIZED', 'STOPOUTCOME', 'CRIME_CHARGED',
    'REGISTRATION_STATE', 'GENDER', 'RESIDENCE_STATE', 'MD_COUNTY',
    'ETHNICITY', 'AGENCY',
)


def stats_for_state_landing_page(stops, report):
    lines = ['', 'Dataset facts']
    lines.append(
        '  Time frame: {} - {}'.format(
            stops.date.iloc[0],
            stops.date.iloc[-1]
        )
    )
    lines.append(
        '  Stops: {:,}'.format(len(stops))
    )
    lines.append(
        '  Searches: {:,}'.format(len(stops[(stops.SEARCH_CONDUCTED == 'Y')]))
    )
    lines.append(
        '  Agencies: {:,}'.format(stops.AGENCY.nunique())
    )
    lines.append('')
    lines.append('Top five agencies:')
    agency_values = stops.AGENCY.value_counts()
    for agency_name, stop_count in zip(list(agency_values.axes[0][:5]),
                                       list(agency_values.values[:5])):
        lines.append('  {:<30} {:,}'.format(agency_name, stop_count))
    lines.append('')

    for line in lines:
        print(line, file=report)


def analyze(stops, report):
    """
    The form of the data analyzed is equivalent to what is stored in the
    CSV by the import command, except that some columns not used by the
    website haven't been thrown away.
    """
    stats_for_state_landing_page(stops, report)

    years = stops['date'].map(lambda x: x.year)
    old_max_rows = pd.options.display.max_rows
    pd.options.display.max_rows = 1500
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
    pd.options.display.max_rows = old_max_rows


def run(url, report, destination=None, download=True):
    """Download MD data, extract, load, and compute some simple stats"""
    logger.info('*** MD Data Analysis Started ***')
    destination = download_and_unzip_data(url, destination)
    xls_path = get_datafile_path(url, destination)
    stops = load_xls(xls_path)
    stops = process_raw_data(stops, to_drop=())
    analyze(stops, report)
