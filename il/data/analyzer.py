import logging

import pandas as pd

from tsdata.utils import download_and_unzip_data, get_datafile_path
from il.data.importer import load_csv

logger = logging.getLogger(__name__)

COLUMNS_TO_ANALYZE = (
    'agencycode', 'agencyname', 'Gender', 'Race', 'Search',
    'Contraband', 'StopPurpose', 'year'
)


def stats_for_state_landing_page(stops, report):

    def get_agency_name(agency_id):
        """
        This finds the agency name used on the first occurrence of the specified
        agency code in the data, and returns the title-case form of it.

        There should be a much more efficient way to handle this with pandas, so
        don't copy this code.
        """
        name = stops.agencyname[stops.agencycode[stops.agencycode == agency_id].index].values[0]
        return name.title()

    lines = ['', 'Dataset facts']
    unique_years = stops.year.unique()
    lines.append(
        '  Time frame: {} - {}'.format(
            min(unique_years),
            max(unique_years),
        )
    )
    lines.append(
        '  Stops: {:,}'.format(len(stops))
    )
    lines.append(
        '  Searches: {:,}'.format(len(stops[(stops.Search == 'Y')]))
    )
    lines.append(
        '  Agencies: {:,}'.format(stops.agencycode.nunique())
    )
    lines.append('')
    lines.append('Top five agencies:')
    agency_values = stops.agencycode.value_counts()
    for agency_id, stop_count in zip(list(agency_values.axes[0][:5]),
                                     list(agency_values.values[:5])):
        lines.append('  {:6} {:<30} {:,}'.format(
            agency_id, get_agency_name(agency_id), stop_count
        ))
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

    years = stops['year']
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
    """Download IL data, extract, load, and compute some simple stats"""
    logger.info('*** IL Data Analysis Started ***')
    destination = download_and_unzip_data(url, destination)
    csv_path = get_datafile_path(url, destination)
    stops = load_csv(csv_path)
    analyze(stops, report)
