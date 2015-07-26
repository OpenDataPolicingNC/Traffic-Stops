from django.core.management.base import BaseCommand

from nc import prime_cache


class Command(BaseCommand):
    """Prime cache on production server"""

    def handle(self, *args, **options):
        url = None
        if len(args) == 1:
            url = args[0]
        prime_cache.run(url)
