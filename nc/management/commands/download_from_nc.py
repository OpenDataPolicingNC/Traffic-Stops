from datetime import date
from ftplib import FTP
import os

from django.core.management import CommandError
import djclick as click


@click.command()
def command():
    nc_data_site = 'sbi1.jus.state.nc.us'
    nc_data_user = os.environ.get('NC_FTP_USER')
    nc_data_password = os.environ.get('NC_FTP_PASSWORD')
    nc_data_file = 'STOPS_Extract.zip'
    nc_data_directory = '/TSTOPextract'

    target_data_file = date.today().strftime('NC_STOPS_Extract_%Y_%m_%d.zip')

    if os.path.exists(target_data_file):
        raise CommandError('File "%s" already exists in current directory' % target_data_file)

    # Note: NC documents show FileZilla set up to use explicit FTP over TLS
    #       if available (like FTP_TLS), but the server doesn't currently
    #       support it.
    ftp = FTP(nc_data_site)
    ftp.login(nc_data_user, nc_data_password)
    ftp.cwd(nc_data_directory)
    click.echo('Files available at %s:' % nc_data_site)
    listing = ftp.retrlines('LIST')
    for line in listing.split('\n'):
        if not line.startswith('226 '):  # server's "Transfer complete" message
            click.echo(line)
    click.echo('Downloading...')
    with open(target_data_file, 'wb') as f:
        ftp.retrbinary('RETR %s' % nc_data_file, f.write)
    click.echo('File written to "%s"' % target_data_file)
