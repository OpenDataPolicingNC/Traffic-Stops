from django.core.management.base import BaseCommand

from nc.data import importer


class Command(BaseCommand):
    """Helper command to kickoff NC data import"""
    url = "https://s3-us-west-2.amazonaws.com/openpolicingdata/TS_2016_04_13T13.38.34.887.zip"

    def handle(self, *args, **options):
        dest = None
        if len(args) == 1:
            dest = args[0]
        importer.run(self.url, dest)
