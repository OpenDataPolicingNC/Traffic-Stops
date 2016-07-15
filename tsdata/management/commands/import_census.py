from django.conf import settings
from django.core.management.base import BaseCommand

from tsdata import acs

import json


class Command(BaseCommand):
    """Sample command to play with Census data"""

    def handle(self, *args, **options):
        # !! Make sure you've set settings.CENSUS_API_KEY !!
        acs.refresh_census_models()
        # data = data.to_json(orient='records')
        # print(json.dumps(json.loads(data), indent=4))
