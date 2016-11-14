import csv
import glob
import logging
import os
import sys

from django.conf import settings
from django.db import connections

from tsdata.sql import drop_constraints_and_indexes
from tsdata.utils import call, line_count, download_and_unzip_data


logger = logging.getLogger(__name__)


def run(url, destination=None, download=True):
    """Download NC data, extract, convert to CSV, and load into PostgreSQL"""
    logger.info('*** NC Data Import Started ***')
    destination = download_and_unzip_data(url, destination)
    # convert data files to CSV for database importing
    convert_to_csv(destination)
    # drop constraints/indexes
    drop_constraints_and_indexes(connections['traffic_stops_nc'].cursor())
    # use COPY to load CSV files as quickly as possible
    copy_from(destination)
    logger.info("NC Data Import Complete")


def to_standard_csv(input_path, output_path):
    csv.register_dialect(
        'nc_data_in',
        delimiter='\t',
        doublequote=False,
        escapechar=None,
        lineterminator='\r\n',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        skipinitialspace=False,
    )
    csv.register_dialect(
        'nc_data_out',
        delimiter=',',
        doublequote=False,
        escapechar=None,
        lineterminator='\n',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
        skipinitialspace=False,
    )
    with open(input_path, 'rt') as input:
        with open(output_path, 'wt') as output:
            reader = csv.reader(input, dialect='nc_data_in')
            writer = csv.writer(output, dialect='nc_data_out')
            headings_written = False
            num_columns = sys.maxsize  # keep all of first row, however many
            for row in reader:
                columns = [column.strip() for i, column in enumerate(row) if i < num_columns]
                if not headings_written:
                    # Some records in Stops.csv have extra columns; drop any
                    # columns beyond those in the first record.
                    num_columns = len(columns)
                    headings = ['column%d' % (i + 1) for i in range(len(columns))]
                    writer.writerow(headings)
                    headings_written = True
                writer.writerow(columns)


def convert_to_csv(destination):
    """Convert each NC *.txt data file to CSV"""
    files = glob.iglob(os.path.join(destination, '*.txt'))
    for data_path in files:
        if data_path.endswith('QUERY_README.txt'):  # list of years in the query
            continue
        csv_path = data_path.replace('.txt', '.csv')
        if os.path.exists(csv_path):
            logger.info('{} already exists, skipping csv conversion'.format(csv_path))
            continue
        logger.info("Converting {} > {}".format(data_path, csv_path))
        # Edit source data .txt file in-place to remove NUL bytes
        # (only seen in Stop.txt)
        call([r"sed -i 's/\x0//g' {}".format(data_path)], shell=True)
        to_standard_csv(data_path, csv_path)
        data_count = line_count(data_path)
        csv_count = line_count(csv_path)
        if data_count == (csv_count - 1):
            logger.debug('CSV line count matches original data file: {}'.format(data_count))
        else:
            logger.error('DAT {}'.format(data_count))
            logger.error('CSV {}'.format(csv_count))


def copy_from(destination):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    nc_csv_path = os.path.join(os.path.dirname(__file__), 'NC_agencies.csv')
    cmd = ['psql',
           '-v', 'data_dir={}'.format(destination),
           '-v', 'nc_time_zone={}'.format(settings.NC_TIME_ZONE),
           '-v', 'nc_csv_table={}'.format(nc_csv_path),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_nc']['NAME']]
    if settings.DATABASE_ETL_USER:
        cmd.append(settings.DATABASE_ETL_USER)
    call(cmd)
