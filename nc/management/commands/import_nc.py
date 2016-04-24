from django.core.management.base import BaseCommand

from nc.data import importer


class Command(BaseCommand):
    """Helper command to kickoff NC data import"""

    def add_arguments(self, parser):
        parser.add_argument('--dest', default=None)
        url = "https://s3-us-west-2.amazonaws.com/openpolicingdata/TS_2016_02_22T10.49.52.640.zip"  # noqa
        parser.add_argument('--url', default=url)

    def handle(self, *args, **options):
        importer.run(options['url'], options['dest'])
