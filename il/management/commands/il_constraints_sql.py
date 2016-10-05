from django.core.management.base import BaseCommand

from django.db import connections
from tsdata.sql import get_add_constraints_and_indexes


class Command(BaseCommand):
    """Inspect and print current IL database constraints and indexes"""

    def handle(self, *args, **options):
        cursor = connections['traffic_stops_il'].cursor()
        print(get_add_constraints_and_indexes(cursor))
