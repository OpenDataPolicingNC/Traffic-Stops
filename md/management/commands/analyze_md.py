import datetime

from django.core.management.base import BaseCommand

from md.data import analyzer, DEFAULT_URL


class Command(BaseCommand):
    """Helper command to scan MD data"""

    def add_arguments(self, parser):
        parser.add_argument('--dest', default=None)
        parser.add_argument('--url', default=DEFAULT_URL)
        parser.add_argument('--report')

    def handle(self, *args, **options):
        start_time = datetime.datetime.now()
        if options['report']:
            print('Writing report to %s...' % options['report'], file=self.stdout)
            with open(options['report'], 'w') as report:
                analyzer.run(options['url'], report, options['dest'])
        else:
            report = self.stdout
            analyzer.run(options['url'], report, options['dest'])
        stop_time = datetime.datetime.now()
        print('Elapsed time: %s' % (stop_time - start_time))
