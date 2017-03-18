import csv
import os
import tempfile

from django.conf import settings
from django.core import mail
from django.test import TestCase

from nc.data.importer import update_nc_agencies


class StableAgencyTests(TestCase):
    multi_db = True

    def setUp(self):
        self.destination_td = tempfile.TemporaryDirectory()
        self.destination = self.destination_td.name
        self.agencies_in_stops = [
            'Agency 1',
            'Agency 2',
            'Agency 3',
            'Agency 4',
            'Agency 5',
        ]
        self.perm_agency_table = os.path.join(self.destination, 'Perm_NC_agencies.csv')
        self.stops_csv_file = os.path.join(self.destination, 'Stop.csv')
        self.create_dummy_stops(self.stops_csv_file, self.agencies_in_stops)

    def tearDown(self):
        self.destination_td.cleanup()

    @staticmethod
    def create_dummy_stops(stops_csv_file, agencies_in_stops):
        with open(stops_csv_file, 'w') as csvfile:
            stops_writer = csv.writer(csvfile)
            stops_writer.writerow(['column1', 'column2', 'column3'])
            for agency_id, agency_name in enumerate(agencies_in_stops):
                stops_writer.writerow([str(agency_id + 1), agency_name, 'foo'])

    @staticmethod
    def create_dummy_agency_table(agency_file, agencies_in_table):
        with open(agency_file, 'w') as csvfile:
            agency_writer = csv.writer(csvfile)
            agency_writer.writerow(['Id', 'Agency Name', 'GEOID'])
            for agency_id, agency_name in enumerate(agencies_in_table):
                agency_writer.writerow([str(agency_id + 1), agency_name, ''])

    def test_new_agency(self):
        """
        Two new agencies in Stops.csv; verify that a temporary
        agency table with those two added will be used for import.
        """
        agencies_in_table = [
            'Agency 1',
            'Agency 3',
            'Agency 5',
        ]
        self.create_dummy_agency_table(self.perm_agency_table, agencies_in_table)
        agency_file = update_nc_agencies(self.perm_agency_table, self.destination)
        self.assertNotEqual(self.perm_agency_table, agency_file)

        # verify that all the agencies in Stops are reflected in the new table
        with open(agency_file) as csvfile:
            agency_reader = csv.reader(csvfile)
            next(agency_reader)  # skip headings
            agencies_in_table = [
                row[1] for row in agency_reader
            ]
        self.assertEqual(set(self.agencies_in_stops), set(agencies_in_table))

        # an e-mail about the new agencies should have been sent
        self.assertEqual(len(mail.outbox), 1)
        received_mail = mail.outbox[0]
        self.assertEqual(len(received_mail.attachments), 1)
        self.assertIn('New NC agencies were discovered during import', received_mail.subject)
        self.assertEqual(set(received_mail.to), set(settings.NC_AUTO_IMPORT_MONITORS))
        self.assertEqual(received_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertNotIn('Agency 1', received_mail.body)
        self.assertIn('Agency 2', received_mail.body)
        self.assertNotIn('Agency 3', received_mail.body)
        self.assertIn('Agency 4', received_mail.body)
        self.assertNotIn('Agency 5', received_mail.body)

    def test_same_agencies(self):
        """
        Stops.csv has same set of agencies as table; verify that the normal
        table is used for import.
        """
        agencies_in_table = self.agencies_in_stops
        self.create_dummy_agency_table(self.perm_agency_table, agencies_in_table)
        agency_file = update_nc_agencies(self.perm_agency_table, self.destination)
        self.assertEqual(self.perm_agency_table, agency_file)
        # no e-mail about new agencies
        self.assertEqual(len(mail.outbox), 0)
