import logging
import os

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


def create_schema(format_path, schema_path):
    """
    Create in2csv-compatible schema file.

    Use MSSQL format files [1] (included in the data dump) to build
    schema files [2] for use with the in2csv command.

    [1] Non-XML Format Files (SQL Server)
        https://msdn.microsoft.com/en-us/library/ms191479.aspx#Structure
    [2] https://csvkit.readthedocs.org/en/0.9.1/scripts/in2csv.html#description
    """
    mapping = {'length': (36, 44),
               'name': (59, 86)}
    schema = ['column,start,length']
    with open(format_path, 'r') as f:
        version = f.readline().strip()  # noqa
        num_columns = int(f.readline())  # noqa
        start = 0
        for line in f:
            name = line[mapping['name'][0]:mapping['name'][1]].strip()
            length = int(line[mapping['length'][0]:mapping['length'][1]].strip())
            schema.append("%s,%s,%s" % (name, start, length))
            start += length
    with open(schema_path, 'w') as f:
        for line in schema:
            f.write("%s\n" % line)


def convert_to_csv(destination):
    """Convert each NC *.txt data file to CSV"""
    files = filter(lambda x: x.endswith('format.txt'),
                   os.listdir(destination))
    for file_name in files:
        name, _ = file_name.split('_')
        format_path = os.path.join(destination, file_name)
        data_path = os.path.join(destination, name + '.txt')
        schema_path = os.path.join(destination, name + '_schema.csv')
        csv_path = os.path.join(destination, name + '.csv')
        if os.path.exists(csv_path):
            logger.info('{} already exists, skipping csv conversion'.format(csv_path))
            continue
        create_schema(format_path, schema_path)
        logger.info("Converting {} > {}".format(data_path, csv_path))
        if hasattr(settings, 'WEBSERVER_ROOT'):
            base = os.path.join(settings.WEBSERVER_ROOT, 'env/bin/')
        else:
            base = ''
        # Convert to CSV using ISO-8859-1 encoding
        # TODO: This may be incorrect https://en.wikipedia.org/wiki/Windows-1252
        call(["{}in2csv -e iso-8859-1 -f fixed -s {} {} > {}".format(base,
                                                                     schema_path,
                                                                     data_path,
                                                                     csv_path)],
             shell=True)
        call([r"sed -i 's/\x0//g' {}".format(csv_path)], shell=True)
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
    cmd = ['psql',
           '-v', 'data_dir={}'.format(destination),
           '-v', 'nc_time_zone={}'.format(settings.NC_TIME_ZONE),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_nc']['NAME']]
    if settings.DATABASE_ETL_USER:
        cmd.append(settings.DATABASE_ETL_USER)
    call(cmd)
