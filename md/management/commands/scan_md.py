from django.core.management.base import BaseCommand

from md.data import DEFAULT_URL, scanner


class Command(BaseCommand):
    """Helper command to scan MD data"""

    def add_arguments(self, parser):
        parser.add_argument('--dest', default=None)
        parser.add_argument('--url', default=DEFAULT_URL)

    def handle(self, *args, **options):
        scanner.run(options['url'], options['dest'])
