import djclick as click

from nc.data.download_from_nc import download_latest


@click.command()
def command():
    download_latest()
