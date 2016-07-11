from django.conf import settings
from django.core.management.base import BaseCommand

from tsdata import acs

import json
import pandas as pd


class Command(BaseCommand):
    """Sample command to play with Census data"""

    def handle(self, *args, **options):
        # !! Make sure you've set settings.CENSUS_API_KEY !!
        data = acs.get_state_census_data(settings.CENSUS_API_KEY, 'MD')
        data = data.to_json(orient='records')
        print(json.dumps(json.loads(data), indent=4))
