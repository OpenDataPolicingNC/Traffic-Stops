import logging
import os
import pandas as pd

from django.conf import settings
from django.db import connections

from tsdata.util import call, line_count, download_and_unzip_data


logger = logging.getLogger(__name__)
cursor = connections['traffic_stops_nc'].cursor()


def run(url, destination=None, download=True):
    """Download MD data, extract, convert to CSV, and load into PostgreSQL"""
    logger.info('*** MD Data Import Started ***')
    download_and_unzip_data(url, destination)
    # Convert to CSV
    xls_path = os.path.join(destination, '2013.xlsx')
    csv_path = os.path.join(destination, '2013.csv')
    if not os.path.exists(csv_path):
        logger.info('Loading {} into pandas'.format(xls_path))
        df = pd.read_excel(xls_path, parse_dates={'datetime': ['Date of Stop']})
        headers = ["Location",
                   "Agency",
                   "datetime",
                   "Gender",
                   "DOB",
                   "Race",
                   "County of Residence",
                   "State of Residence",
                   "State of Registration",
                   "Stop Reason",
                   "Search",
                   "Search Reason",
                   "Disposition",
                   "Outcome"]
        logger.info("Converting {} > {}".format(xls_path, csv_path))
        df.to_csv(csv_path, columns=headers)
    else:
        logger.info("{} exists, skipping XLS->CSV conversion".format(csv_path))
    csv_count = line_count(csv_path)
    logger.debug('Rows: {}'.format(csv_count))
    # use COPY to load CSV files as quickly as possible
    copy_from(destination)


def copy_from(destination):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    cmd = ['psql',
           '-v', 'data_dir={}'.format(os.path.abspath(destination)),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_md']['NAME']]
    if settings.DATABASES['traffic_stops_md']['USER']:
        cmd.append(settings.DATABASES['traffic_stops_md']['USER'])
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
