from django.core.management.base import BaseCommand

from nc.data import importer


class Command(BaseCommand):
    """Helper command to kickoff NC data import"""
    url = "https://s3-us-west-2.amazonaws.com/openpolicingdata/TS_2015_02_12T14.24.03.810.zip"

    def handle(self, *args, **options):
        dest = None
        if len(args) == 1:
            dest = args[0]
        importer.run(self.url, dest)
