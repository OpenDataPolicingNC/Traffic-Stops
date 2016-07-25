import json
import requests

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from tsdata import acs


ACS_JSON_URL = "https://s3-us-west-2.amazonaws.com/openpolicingdata/acs.json"


class Command(BaseCommand):
    """
    Import or download Census data

    - Import saved JSON from S3 (deafult behavior and requires no API key):
        python manage.py import_census
    - Download and output saved JSON from S3 (requires no API key):
        python manage.py import_census --output --indent=4
    - Save JSON file (for uploading to S3):
        python manage.py import_census --use-api --output > acs.json
    """

    help = "Import County and Place Census data"

    def add_arguments(self, parser):
        parser.add_argument('--use-api',
                            action='store_true',
                            dest='api',
                            default=False,
                            help='Download data from Census API (requires key)')
        parser.add_argument('--output',
                            action='store_true',
                            dest='output',
                            default=False,
                            help='Output JSON to stdout rather than importing')
        parser.add_argument('--indent', default=None, type=int)
        parser.add_argument('--url',
                            default=ACS_JSON_URL,
                            help='URL for Census data in JSON format')

    def handle(self, *args, **options):
        if options['api']:
            # make sure you've set settings.CENSUS_API_KEY
            data = acs.get_state_census_data(key=settings.CENSUS_API_KEY)
            # normalize to json so it can be dump'd or loaded below
            data = json.loads(data.to_json(orient='records'))
        else:
            r = requests.get(options['url'])
            if r.status_code != 200:
                raise CommandError("Failed to access {}".format(options['url']))
            data = r.json()
        if options['output']:
            print(json.dumps(data, indent=options['indent']))
        else:
            acs.refresh_census_models(data)
