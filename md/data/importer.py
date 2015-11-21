import logging
import openpyxl
import os

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
        logger.info("Converting {} > {}".format(xls_path, csv_path))
        call(["in2csv {} > {}".format(xls_path, csv_path)], shell=True)
    csv_count = line_count(csv_path)
    logger.debug('2013 rows: {}'.format(csv_count))
