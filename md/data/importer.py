import logging
import os
import pandas as pd

from django.conf import settings
from django.db import connections

from md.data import DATASET_BASENAME
from tsdata.util import call, line_count, download_and_unzip_data


logger = logging.getLogger(__name__)
cursor = connections['traffic_stops_nc'].cursor()


def load_xls(xls_path):
    logger.info('Loading {} into pandas'.format(xls_path))
    num_sheets = 3
    df_dict = pd.read_excel(
        xls_path, sheetname=list(range(num_sheets)),
        keep_default_na=False, na_values=[]
    )
    for i in range(1, num_sheets):
        df_dict[i].columns = df_dict[0].columns
    df = pd.concat(
        [df_dict[k] for k in sorted(df_dict.keys())],
        ignore_index=True
    )
    # Add index and date columns to front
    df['index'] = range(1, len(df) + 1)  # adds column at end
    df['date'] = pd.to_datetime(df['STOPDATE'])
    df = df[df.columns.tolist()[-2:] + df.columns.tolist()[:-2]]
    return df


def xls_to_csv(xls_path, csv_path):
    assert not os.path.exists(csv_path)
    df = load_xls(xls_path)
    logger.info("Converting {} > {}".format(xls_path, csv_path))
    df.to_csv(csv_path, index=False)
    return df


def run(url, destination=None, download=True):
    """Download MD data, extract, convert to CSV, and load into PostgreSQL"""
    logger.info('*** MD Data Import Started ***')
    download_and_unzip_data(url, destination)
    # Convert to CSV
    xls_path = os.path.join(destination, DATASET_BASENAME + '.xlsx')
    csv_path = os.path.join(destination, DATASET_BASENAME + '.csv')
    if not os.path.exists(csv_path):
        xls_to_csv(xls_path, csv_path)
    else:
        logger.info("{} exists, skipping XLS->CSV conversion".format(csv_path))
    csv_count = line_count(csv_path)
    logger.debug('Rows: {}'.format(csv_count))
    # use COPY to load CSV files as quickly as possible
    copy_from(csv_path)


def copy_from(csv_path):
    """Execute copy.sql to COPY csv data files into PostgreSQL database"""
    sql_file = os.path.join(os.path.dirname(__file__), 'copy.sql')
    cmd = ['psql',
           '-v', 'data_file={}'.format(csv_path),
           '-f', sql_file,
           settings.DATABASES['traffic_stops_md']['NAME']]
    if settings.DATABASES['traffic_stops_md']['USER']:
        cmd.append(settings.DATABASES['traffic_stops_md']['USER'])
    print(cmd)
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
