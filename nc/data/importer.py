import logging
import os
import tempfile

from django.conf import settings
from django.db import connections

from .util import call, line_count, download_and_unzip_data


logger = logging.getLogger(__name__)
cursor = connections['traffic_stops_nc'].cursor()


def run(url, destination=None, download=True):
    """Download NC data, extract, convert to CSV, and load into PostgreSQL"""
    logger.info('*** NC Data Import Started ***')
    # make sure destination exists or create a temporary directory
    if not destination:
        destination = tempfile.mkdtemp(prefix='nc-')
        logger.debug("Created temp directory {}".format(destination))
    else:
        if not os.path.exists(destination):
            os.makedirs(destination)
            logger.info("Created {}".format(destination))
        else:
            download = False
    # don't redownload data if directory already exists with data files
    if download:
        download_and_unzip_data(url, destination)
    else:
        logger.debug("{} exists, skipping download".format(destination))
    # convert data files to CSV for database importing
    convert_to_csv(destination)
    # inspect table constraints so we can toggle them off during import
    drop_constraints = get_constraints_sql(SELECT_DROP_CONSTRAINTS_SQL)
    add_constraints = get_constraints_sql(SELECT_ADD_CONSTRAINTS_SQL)
    # drop constraints to speed up import
    if drop_constraints:
        logger.info("Dropping table constraints")
        cursor.execute(drop_constraints)
    # use COPY to load CSV files as quickly as possible
    copy_from(destination)
    # add constraints back
    logger.info("Adding table constraints")
    cursor.execute(add_constraints)
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
        # Convert to CSV using ISO-8859-1 encoding
        # TODO: This may be incorrect https://en.wikipedia.org/wiki/Windows-1252
        call(["in2csv -e iso-8859-1 -f fixed -s {} {} > {}".format(schema_path,
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


def get_constraints_sql(select_sql):
    """
    Simple wrapper function used to execute a SQL query that returns a
    list of SQL commands to be run later.
    """
    cursor.execute(select_sql)
    sql = ''
    for row in cursor.fetchall():
        sql += row[0]
    return sql


def copy_from(destination):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    cmd = ['psql',
           '-v', 'data_dir={}'.format(destination),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_nc']['NAME']]
    if settings.DATABASES['traffic_stops_nc']['USER']:
        cmd.append(settings.DATABASES['traffic_stops_nc']['USER'])
    call(cmd)


# SQL commands to drop/create all nc_* table constraints
# Adapted from: http://blog.hagander.net/archives/131-Automatically-dropping-and-creating-constraints.html    # noqa


SELECT_DROP_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" DROP CONSTRAINT IF EXISTS "'||conname||'";'
FROM pg_constraint
INNER JOIN pg_class ON conrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE relname LIKE 'nc_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END,contype,nspname,relname,conname;
"""  # noqa

SELECT_ADD_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" ADD CONSTRAINT "'||conname||'" '||pg_get_constraintdef(pg_constraint.oid)||';'
FROM pg_constraint
INNER JOIN pg_class ON conrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE relname LIKE 'nc_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END DESC,contype DESC,nspname DESC,relname DESC,conname DESC;
"""  # noqa
