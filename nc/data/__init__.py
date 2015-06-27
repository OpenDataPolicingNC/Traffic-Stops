import os
import logging
import requests
import subprocess
import tempfile
import time
import zipfile
from django.db import connections


logger = logging.getLogger(__name__)

mapping = {'length': (36, 44),
           'name': (59, 86)}

cursor = connections['traffic_stops_nc'].cursor()


def download_and_unzip_data(url, destination):
    """Download an unzip NC data"""
    zip_filename = os.path.join(destination, url.split('/')[-1])
    logger.debug("Downloading data to {}".format(zip_filename))
    response = requests.get(url, stream=True)
    content_length = int(response.headers.get('content-length'))
    start = time.clock()
    downloaded = 0
    with open(zip_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk: 
                downloaded += len(chunk)
                now = time.clock()
                if (now - start) >= 5:
                    logger.debug('{0:.2g}% downloaded'.format(downloaded/content_length*100))
                    start = now
                f.write(chunk)
                f.flush()
    logger.debug('100% downloaded')
    archive = zipfile.ZipFile(zip_filename)
    logger.debug("Extracting archive into {}".format(destination))
    archive.extractall(path=destination)
    logger.debug("Extraction complete".format(destination))


def line_count(fname):
    """Count number of lines in specified file"""
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def create_schema(format_path, schema_path):
    """
    Create in2csv-compatible schema file.

    Use MSSQL format files [1] (included in the data dump) to build 
    schema files [2] for use with the in2csv command.

    [1] Non-XML Format Files (SQL Server)
        https://msdn.microsoft.com/en-us/library/ms191479.aspx#Structure
    [2] https://csvkit.readthedocs.org/en/0.9.1/scripts/in2csv.html#description
    """
    schema = ['column,start,length']
    with open(format_path, 'r') as f:
        version = f.readline().strip()
        num_columns = int(f.readline())
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
        subprocess.call("in2csv -e iso-8859-1 -f fixed -s {} {} > {}".format(schema_path, data_path, csv_path), shell=True)
        subprocess.call(r"sed -i 's/\x0//g' {}".format(csv_path), shell=True)
        data_count = line_count(data_path)
        csv_count = line_count(csv_path)
        if data_count == (csv_count - 1):
            logger.debug('CSV line count matches original data file: {}'.format(data_count))
        else:
            logger.error('DAT {}'.format(data_count))
            logger.error('CSV {}'.format(csv_count))


def get_constraints_sql(selecqt_sql):
    cursor.execute(selecqt_sql)
    sql = ''
    for row in cursor.fetchall():
        sql += row[0]
    return sql




def copy_from(destination):
    """"""
    cmd = ["psql"]
    cmd += ['-v', 'data_dir={}'.format(destination)]
    sql_file = os.path.join(os.path.dirname(__file__), 'import.sql')
    cmd += ['-f', sql_file]
    cmd += ['traffic_stops_nc']
    logger.debug(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if stderr:
        logger.error(stderr.decode('utf-8'))


def load(url, destination=None, download=True):
    logger.info('*** NC Data Import Started ***')
    if not destination:
        destination = tempfile.mkdtemp(prefix='nc-')
        logger.debug("Created temp directory {}".format(destination))
    else:
        if not os.path.exists(destination):
            os.makedirs(destination)
            logger.info("Created {}".format(destination))
        else:
            download = False
    if download:
        download_and_unzip_data(url, destination)
    else:
        logger.debug("{} exists, skipping download".format(destination))
    convert_to_csv(destination)
    # save drop/create constraint statements ahead of time
    drop_constraints = get_constraints_sql(SELECT_DROP_CONSTRAINTS_SQL)
    add_constraints = get_constraints_sql(SELECT_CREATE_CONSTRAINTS_SQL)
    # drop constraints to speed up import
    cursor.execute(drop_constraints)
    # use COPY to load CSV files as quickly as possible
    copy_from(destination)
    # add constraints back
    cursor.execute(add_constraints)
    logger.info("NC Data Import Complete")


SELECT_DROP_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" DROP CONSTRAINT IF EXISTS "'||conname||'";'
FROM pg_constraint 
INNER JOIN pg_class ON conrelid=pg_class.oid 
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace 
WHERE relname LIKE 'nc_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END,contype,nspname,relname,conname;
"""

SELECT_CREATE_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" ADD CONSTRAINT "'||conname||'" '||pg_get_constraintdef(pg_constraint.oid)||';'
FROM pg_constraint
INNER JOIN pg_class ON conrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE relname LIKE 'nc_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END DESC,contype DESC,nspname DESC,relname DESC,conname DESC;
"""
