import logging
import os
import requests
import subprocess
import tempfile
import time
import zipfile

from collections import OrderedDict


logger = logging.getLogger(__name__)


def call(cmd, shell=False):
    """Spawn a new process and capture its output"""
    logger.debug(' '.join(cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=shell)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise IOError(stderr)
    if stderr:
        logger.error(stderr.decode('utf-8'))
    return stdout


def line_count(fname):
    """Count number of lines in specified file"""
    return int(call(['wc', '-l', fname]).strip().split()[0])


def get_zipfile_path(url, destination):
    """
    Get full path of the zipfile as if it has been downloaded to destination.
    """
    return os.path.join(destination, url.split('/')[-1])


def get_datafile_path(url, destination):
    """
    Get full path of the datafile within the downloaded zip.
    Assumptions:
    1. zip has already been downloaded to destination.
    2. the first file in the zip is the datafile
    Datafile may not have been extracted yet.
    """
    zip_filename = get_zipfile_path(url, destination)
    archive = zipfile.ZipFile(zip_filename)
    return os.path.join(destination, archive.infolist()[0].filename)


def get_csv_path(url, destination):
    """
    Get full path of the CSV form of the datafile in the downloaded zip.
    Assumptions: See assumptions of get_datafile_path()
    """
    datafile_path = get_datafile_path(url, destination)
    return os.path.splitext(datafile_path)[0] + '.csv'


def download_and_unzip_data(url, destination, prefix='state-'):
    """Download and unzip data into destination directory"""
    download = True
    # make sure destination exists or create a temporary directory
    if not destination:
        destination = tempfile.mkdtemp(prefix=prefix)
        logger.debug("Created temp directory {}".format(destination))
    else:
        if not os.path.exists(destination):
            os.makedirs(destination)
            logger.info("Created {}".format(destination))
        else:
            download = False
    # don't re-download data if directory already exists with data files
    if not download:
        logger.debug("{} exists, skipping download".format(destination))
        return destination
    zip_filename = get_zipfile_path(url, destination)
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
    return destination


class GroupedData(object):
    """Data structure to build and flatten nested dictionaries"""

    def __init__(self, by, defaults=None):
        if type(by) is str:
            by = tuple([by])
        self.group_by = by
        self.data = OrderedDict()
        self.defaults = defaults or {}

    def add(self, **kwargs):
        """Save (group, value) mapping to internal dict"""
        group = []
        for name in self.group_by:
            group.append(kwargs.pop(name))
        group = tuple(group)
        if group not in self.data:
            self.data[group] = OrderedDict(self.defaults.copy())
        self.data[group].update(kwargs)

    def flatten(self):
        """Transform (group, value) mapping into list of dicts"""
        response = []
        for group, data in self.data.items():
            group_by = zip(self.group_by, group)
            row = OrderedDict(group_by)
            row.update(data)
            response.append(row)
        return response
