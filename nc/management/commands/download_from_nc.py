import djclick as click

from nc.data.download_from_nc import nc_download_and_unzip_data


@click.command()
def command():
    nc_download_and_unzip_data('./newncdata')
