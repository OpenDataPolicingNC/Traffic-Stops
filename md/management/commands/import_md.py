from django.core.management.base import BaseCommand

from md.data import importer


class Command(BaseCommand):
    """Helper command to kickoff MD data import"""
    url = "https://s3-us-west-2.amazonaws.com/openpolicingdata/TODO.zip"

    def handle(self, *args, **options):
        dest = None
        if len(args) == 1:
            dest = args[0]
        importer.run(self.url, dest)
