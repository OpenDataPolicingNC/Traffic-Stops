import logging
import os
import pandas as pd
import re

from django.conf import settings

from md.data import DATASET_BASENAME
from tsdata.util import call, line_count, download_and_unzip_data


logger = logging.getLogger(__name__)

TIME_OF_STOP_re = re.compile(r'((\d?\d):(\d\d)|(\d?\d):(\d\d) [AP]M)$')
TIME_OF_STOP_re = re.compile(r'(\d?\d):(\d\d)( [AP]M)?$')
DEFAULT_TIME_OF_STOP = '00:00'


def fix_TIME_OF_STOP(s):
    # print(s)
    s = s.strip()
    m = TIME_OF_STOP_re.match(s)
    if not m:
        return DEFAULT_TIME_OF_STOP
    hour = int(m.group(1))
    minute = int(m.group(2))
    if not 0 <= hour < 24:
        return DEFAULT_TIME_OF_STOP
    if not 0 <= minute < 60:
        return DEFAULT_TIME_OF_STOP
    # if m.group(3) and m.group(3) == ' PM':
    #     print(s)

    # XXX Check converted CSV to see if we need to fix up the handling
    #     of 'PM', which can be appended to times before or after 12:00 p.m.
    # IOW, does the right thing happen for both '8:53 PM' and '20:53 PM'?
    return s


def load_xls(xls_path):
    logger.info('Loading {} into pandas'.format(xls_path))
    num_sheets = 3
    df_dict = pd.read_excel(
        xls_path, sheetname=list(range(num_sheets)),
        keep_default_na=False, na_values=[]
    )
    for i in range(1, num_sheets):
        df_dict[i].columns = df_dict[0].columns
    stops = pd.concat(
        [df_dict[k] for k in sorted(df_dict.keys())],
        ignore_index=True
    )

    # Fix data
    stops['TIME_OF_STOP'] = stops['TIME_OF_STOP'].apply(fix_TIME_OF_STOP)

    # Add index and date columns
    stops['index'] = range(1, len(stops) + 1)  # adds column at end
    blank = pd.DataFrame({'blank': ' '}, index=range(len(stops['STOPDATE'])))
    stops['date'] = pd.to_datetime(stops['STOPDATE'].map(str) + blank['blank'].map(str) + stops['TIME_OF_STOP'].map(str))
    # move the new columns to the front
    stops = stops[stops.columns.tolist()[-2:] + stops.columns.tolist()[:-2]]
    return stops


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
    call(cmd)


# https://gist.github.com/mangecoeur/1fbd63d4758c2ba0c470
