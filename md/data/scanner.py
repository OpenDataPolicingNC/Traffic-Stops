# Implementation of scan_md command, not used for actual data import
#
# This will report some of the stranger field values in the raw data.

import csv
import logging
import os
import re

from tsdata.utils import (download_and_unzip_data, line_count, get_csv_path,
                          get_datafile_path)
from md.data.importer import xls_to_csv

logger = logging.getLogger(__name__)


def run(url, destination=None, download=True):
    """Download MD data, extract, convert to CSV, and scan for issues"""
    logger.info('*** MD Data Scan Started ***')
    destination = download_and_unzip_data(url, destination)
    # Convert to CSV
    xls_path = get_datafile_path(url, destination)
    csv_path = get_csv_path(url, destination)
    if not os.path.exists(csv_path):
        xls_to_csv(xls_path, csv_path)
    else:
        logger.info("{} exists, skipping XLS->CSV conversion".format(csv_path))
    csv_count = line_count(csv_path)
    logger.debug('Rows: {}'.format(csv_count))
    scan([csv_path])


STRAY_RE = re.compile('(^ +|`+$| +$|^[¿`])')

NA_RE = re.compile('^(NA|na|n//a|n/a)$')

# These regexes are applied after the value has been cleaned with STRAY_RE.
# "CDS" == "Controlled Dangerous Substance"
FIELD_REGEXES = {
    'STOPDATE': re.compile(r'^\d\d/\d\d/\d\d$'),
    'TIME_OF_STOP': re.compile(r'(\d\d:\d\d|\d?\d:\d\d [AP]M|\d:\d\d|\d :\d\d|:)$'),
    'LOCATION': re.compile(r'^(|[A-Za-z0-9 -^_@&/\\~`.]+)$'),
    'DURATION': re.compile(r'^(|\d\d?\d?|\d\+|\d?\.\d\d?|\d:\d\d|:\d\d|\d\d? ?M|\d H|\dHR|\+/-\d+|\d+\.|-\d+|< ?5|<10|<15|<30|\d\d? ?min|\d+MI|N/A|UNK)$'),  # noqa
    # STOP_REASON: The expression doesn't do any meaningful validation.
    #
    # STOP_REASON examples:
    #   21-1129
    #   21-201(a1)
    #   22-204F
    #   22-412.3(b)
    #   22-216
    #   21-801.1
    #   55
    #   55*
    #   64*-
    'STOP_REASON': re.compile(r'^(|[\da-zA-Z() -`.]+)$'),
    # SEARCH_REASON
    #
    # Presumably "I" is Incident to Arrest?
    'SEARCH_REASON': re.compile(
        r'^(|Incident to Arrest|I|Probable Cause|K-9|K-9 Scan|k9 alert|Drugs|Consensual|Other|Exigent Circumstances|odor of marijuana|VEH TOWED|TOWED VEH|VEH TOW|TOWED|ARREST/TOW|arrest|Other Vehicle Impound|impounded|VEH IMPOUNDED|VEH IMPOUND|IMPOUNDED INVENTORY|Other CONSENT AND TOW|Probable Cause/VEH TOWED|saw toy gun|N/A|NONE|no search)$',  # noqa
        flags=re.IGNORECASE
    ),
    'SEARCH_CONDUCTED': re.compile(r'^[NY]$'),
    'WHATSEARCHED': re.compile(
        r'^(|Property|Both|B|Person|per|vehicle|vehicle inventory|SEARCH INCIDENTAL|contraband|CDS|none|no search|N/A)$',  # noqa
        flags=re.IGNORECASE
    ),
    'SEIZED': re.compile(
        r'^(|Contraband Only|Contraband|Contraband and Property|Both|Property Only|Property|paraphernalia|impound inventory|Nothing|No CDs in vehicle|none|non|N/A|no search)$',  # noqa
        flags=re.IGNORECASE
    ),
    'STOPOUTCOME': re.compile(
        r'^(|Citation|Arrest|Citation/ARREST|RECOVERED EVIDENCE|CDS MARIJUANA|CDS ARREST|cds located|dui|Warning|Warnnig|Warning / Citation|SERO|SERO and Warning|SERO, Warning|SERO and Warning x2|nothing found|NOTHING LOCATED)$',  # noqa
        flags=re.IGNORECASE
    ),
    # CRIME_CHARGED: The expression doesn't do any meaningful validation.
    'CRIME_CHARGED': re.compile(r'^(|[\da-zA-Z() -`.]+)$'),
    'REGISTRATION_STATE': re.compile(r'^(|[A-Z][A-Z]|N/A|NONE)$'),
    'GENDER': re.compile(r'^(|[FMU]|female|male)$', flags=re.IGNORECASE),
    'DOB': re.compile(r'^(|\d\d/\d\d/\d\d)$'),
    'RESIDENCE_STATE': re.compile(r'^(|md|[A-Z][A-Z]|N/A)$'),
    # "AA" county is presumably Anne Arundel County
    # "F" county is presumably Frederick
    # "m" county is presumably Montgomery
    # "PG" county is presumably Prince George's County
    # "6"/"06" county is presumably Carroll
    'MD_COUNTY': re.compile(r"^(|F|AA|aa|m|PG|6|06|N/A|PRINCESS ANNE|[A-Z '.]+ - \d\d)$"),
    'ETHNICITY': re.compile(r'^(|BLACK|BLK|WHITE|W|ASIAN|OTHER|HISPANIC|NATIVE AMERICAN|UNKNOWN)$'),
    'OFFICERID': re.compile(r'^[1-9][0-9]*$'),
    'AGENCY': re.compile(r'^[A-Z]+$')
}

FIELDS_TO_COLUMNS = dict()
COLUMNS_TO_FIELDS = dict()


def scan(csv_fns, report=True):
    """
    :param csv_fns: A sequence of one or more names of CSV files comprising the
    data to be processed.  Only the first file should have column headings.
    :param report: Whether or not to report bad data
    """
    num_records = 0

    for file_num, csv_fn in enumerate(csv_fns):
        print('File %s...' % csv_fn)
        line_in_file = 0
        with open(csv_fn, encoding='ISO8859-1') as f:
            reader = csv.reader(f)
            if file_num == 0:  # no headings on subsequent files
                heading_row = next(reader)
                line_in_file += 1
                for col_num, heading in enumerate(heading_row):
                    FIELDS_TO_COLUMNS[heading] = col_num
                    COLUMNS_TO_FIELDS[col_num] = heading

            for row in reader:
                num_records += 1
                line_in_file += 1
                for col_num, col_val in enumerate(row):
                    field_name = COLUMNS_TO_FIELDS[col_num]
                    if field_name in FIELD_REGEXES:
                        orig_col_val = col_val
                        col_val = STRAY_RE.sub('', col_val)
                        assert not STRAY_RE.match(col_val), '"%s" not totally cleaned up' % orig_col_val  # noqa
                        col_val = NA_RE.sub('N/A', col_val)
                        if not FIELD_REGEXES[field_name].match(col_val):
                            print('%s:%s Not valid for %s: "%s"' % (
                                csv_fn,
                                line_in_file,
                                field_name,
                                col_val
                            ))
                            if report:
                                for heading, value in zip(heading_row, row):
                                    print('    %-20s: %s' % (heading, value))
                                print('')

    print('Total records: {:,}'.format(num_records))
