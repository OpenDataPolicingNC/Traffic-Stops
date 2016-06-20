import logging
import os
import requests
import subprocess
import tempfile
import time
import zipfile


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
    return destination
