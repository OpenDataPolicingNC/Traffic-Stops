import csv
import glob
import logging
import os
import sys

from django.conf import settings
from django.db import connections

from tsdata.dataset_facts import compute_dataset_facts
from tsdata.sql import drop_constraints_and_indexes
from tsdata.utils import call, flush_memcached, line_count, download_and_unzip_data, unzip_data
from nc.models import Agency, Search, Stop
from nc.prime_cache import run as prime_cache_run
from .download_from_nc import nc_download_and_unzip_data

logger = logging.getLogger(__name__)

MAGIC_NC_FTP_URL = 'ftp://nc.us/'


def run(url, destination=None, zip_path=None, min_stop_id=None,
        max_stop_id=None, prime_cache=True):
    """
    Download NC data, extract, convert to CSV, and load into PostgreSQL

    :param url: if not None, zip will be downloaded from this URL; this can
      either be a URL supported by the requests library OR the special URL
      MAGIC_NC_FTP_URL, in which case the zip will be downloaded from the state
      of North Carolina server.
    :param destination: directory for unpacking zip and creating other
      files; pass None to create a temporary file
    :param zip_path: path to previously-downloaded zip
    :param prime_cache: whether or not to prime the query cache for "big"
      NC agencies after import
    :param max_stop_id: only process stops with ids <= this value; this is to
      save time for developers by reducing the amount of data to import
    :param min_stop_id: only process stops with ids >= this value; this is to
      save time for developers by reducing the amount of data to import
    """
    if not url and not destination:
        raise ValueError('destination must be provided when no URL is provided')

    if (min_stop_id is None) != (max_stop_id is None):
        raise ValueError('provide neither or both of min_stop_id and max_stop_id')

    if max_stop_id is not None and min_stop_id > max_stop_id:
        raise ValueError('min_stop_id cannot be larger than max_stop_id')

    logger.info('*** NC Data Import Started ***')

    if url:
        if url == MAGIC_NC_FTP_URL:
            destination = nc_download_and_unzip_data(destination)
        else:
            destination = download_and_unzip_data(url, destination)
    else:
        unzip_data(destination, zip_path=zip_path)

    if max_stop_id is not None:
        truncate_input_data(destination, min_stop_id, max_stop_id)
        override_start_date = None
    else:
        # When processing entire dataset, pretend we don't have data from
        # 2000-2001 since so few agencies reported then.
        override_start_date = 'Jan 01, 2002'

    # convert data files to CSV for database importing
    convert_to_csv(destination)
    # drop constraints/indexes
    drop_constraints_and_indexes(connections['traffic_stops_nc'].cursor())
    # use COPY to load CSV files as quickly as possible
    copy_from(destination)
    logger.info("NC Data Import Complete")

    # Clear the query cache to get rid of NC queries made on old data
    flush_memcached()

    # fix landing page data
    facts = compute_dataset_facts(
        Agency, Stop, settings.NC_KEY, Search=Search,
        override_start_date=override_start_date
    )
    logger.info('NC dataset facts: %r', facts)

    # prime the query cache for large NC agencies
    if prime_cache:
        prime_cache_run()


def truncate_input_data(destination, min_stop_id, max_stop_id):
    """
    For faster development, filter Stops.txt to include stops only in a certain
    range, then adjust the data for Person, Search, Contraband, and SearchBasis
    accordingly.  By limiting the size of the input data, most phases of the
    import flow will be much faster.

    :param destination: directory path which contains NC data files
    :param min_stop_id: omit stops with lower id
    :param max_stop_id: point in the Stops data at which to truncate
    """
    logger.info('Filtering out stops with id not in (%s, %s)', min_stop_id, max_stop_id)
    data_file_description = (
        ('Stop.txt', 0),
        ('PERSON.txt', 1),
        ('Search.txt', 1),
        ('Contraband.txt', 3),
        ('SearchBasis.txt', 3),
    )
    for in_basename, stops_field_num in data_file_description:
        data_in_path = os.path.join(destination, in_basename)
        data_out_path = data_in_path + '.new'
        with open(data_in_path, 'rb') as data_in:
            with open(data_out_path, 'wb') as data_out:
                for line in data_in:
                    fields = line.split(b'\t')
                    stop_id = int(fields[stops_field_num])
                    if min_stop_id <= stop_id <= max_stop_id:
                        data_out.write(line)
        os.replace(data_out_path, data_in_path)


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
        if os.path.basename(data_path) == 'QUERY_README.txt':  # list of years in the query
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
