from datetime import date
from ftplib import FTP
import logging
import os
import tempfile

from tsdata.utils import unzip_data


logger = logging.getLogger(__name__)


def show_ftp_listing(s):
    logger.debug(s)


def nc_download_and_unzip_data(destination, prefix='state-'):
    """Download and unzip data into destination directory"""
    # make sure destination exists or create a temporary directory
    if not destination:
        destination = tempfile.mkdtemp(prefix=prefix)
        logger.debug("Created temp directory {}".format(destination))
    else:
        if not os.path.exists(destination):
            os.makedirs(destination)
            logger.info("Created {}".format(destination))
    zip_basename = date.today().strftime('NC_STOPS_Extract_%Y_%m_%d.zip')
    zip_filename = os.path.join(destination, zip_basename)
    # don't re-download data if raw data file already exists
    if os.path.exists(zip_filename):
        logger.debug("{} exists, skipping download".format(zip_filename))
    else:
        logger.debug("Downloading data to {}".format(zip_filename))
        nc_data_site = 'sbi1.jus.state.nc.us'
        nc_data_user = os.environ.get('NC_FTP_USER')
        nc_data_password = os.environ.get('NC_FTP_PASSWORD')
        nc_data_file = 'STOPS_Extract.zip'
        nc_data_directory = '/TSTOPextract'

        # Note: NC documents show FileZilla set up to use explicit FTP over TLS
        #       if available (like FTP_TLS), but the server doesn't currently
        #       support it.
        ftp = FTP(nc_data_site)
        ftp.login(nc_data_user, nc_data_password)
        ftp.cwd(nc_data_directory)
        logger.debug('Files available at %s:', nc_data_site)
        listing = ftp.retrlines('LIST', show_ftp_listing)
        line = listing.split('\n')[0]
        if not line.startswith('226 '):  # server's "Transfer complete" message
            raise ValueError('Expected 226 response from ftp server, got %r' % listing)
        logger.info('Downloading "%s"...', nc_data_file)
        with open(zip_filename, 'wb') as f:
            ftp.retrbinary('RETR %s' % nc_data_file, f.write)
        logger.info('File written to "%s"' % zip_filename)

    unzip_data(destination, zip_path=zip_filename)
    return destination
