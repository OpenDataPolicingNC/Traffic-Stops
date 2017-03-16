from django.core.management.base import BaseCommand

from nc import prime_cache


class Command(BaseCommand):
    """Prime cache on production server"""

    def add_arguments(self, parser):
        parser.add_argument(
            '--cutoff-duration-secs',
            dest='cutoff', default=None,
            help='Stop priming cache for agencies once it takes less than this'
        )

    def handle(self, *args, **options):
        cutoff = float(options['cutoff']) if options['cutoff'] else None
        prime_cache.run(cutoff_duration_secs=cutoff)
