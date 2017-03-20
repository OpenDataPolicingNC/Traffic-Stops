from django.core.management.base import BaseCommand

from nc.data import DEFAULT_URL, importer


class Command(BaseCommand):
    """Helper command to kickoff NC data import"""

    def add_arguments(self, parser):
        parser.add_argument('--dest', default=None)
        parser.add_argument('--url', default=DEFAULT_URL)
        parser.add_argument('--min-stop-id', default=None)
        parser.add_argument('--max-stop-id', default=None)

    def handle(self, *args, **options):
        min_stop_id = int(options['min_stop_id']) if options['min_stop_id'] else None
        max_stop_id = int(options['max_stop_id']) if options['max_stop_id'] else None
        importer.run(
            options['url'], options['dest'],
            min_stop_id=min_stop_id,
            max_stop_id=max_stop_id,
        )
