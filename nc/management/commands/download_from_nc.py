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

    if os.path.exists(nc_data_file):
        raise CommandError('File "%s" already exists in current directory' % nc_data_file)

    # Note: NC documents show FileZilla set up to use explicit FTP over TLS
    #       if available (like FTP_TLS), but it isn't currently enabled.
    ftp = FTP(nc_data_site)
    ftp.login(nc_data_user, nc_data_password)
    ftp.cwd(nc_data_directory)
    print(ftp.retrlines('LIST'))
    with open(nc_data_file, 'wb') as f:
        ftp.retrbinary('RETR %s' % nc_data_file, f.write)
    click.secho('File written to "%s"' % nc_data_file)
