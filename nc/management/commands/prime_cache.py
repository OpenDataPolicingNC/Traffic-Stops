from django.core.management.base import BaseCommand

from nc import prime_cache


class Command(BaseCommand):
    """Prime cache on production server"""

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='?', default="http://0.0.0.0:8000/")

    def handle(self, *args, **options):
        prime_cache.run(options['url'])
