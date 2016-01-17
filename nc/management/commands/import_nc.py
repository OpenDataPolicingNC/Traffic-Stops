from django.core.management.base import BaseCommand

from nc.data import importer


class Command(BaseCommand):
    """Helper command to kickoff NC data import"""
    url = "https://s3-us-west-2.amazonaws.com/openpolicingdata/TS_2015_12_02T10.25.28.733.zip"

    def add_arguments(self, parser):
        parser.add_argument('--dest', default=None)

    def handle(self, *args, **options):
        importer.run(self.url, options['dest'])
