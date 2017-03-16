import os
import tempfile
from zipfile import ZipFile

from django.test import TestCase

from tsdata.utils import (
    download_and_unzip_data, flush_memcached, get_csv_path, get_datafile_path,
    get_zipfile_path, line_count, unzip_data
)


class TestUtils(TestCase):

    multi_db = True

    @staticmethod
    def make_test_zip(zip_path):
        with ZipFile(zip_path, 'w') as test_zip:
            test_zip.writestr('file1.txt', b'file1')
            test_zip.writestr('file2.txt', b'file2')
            test_zip.writestr('file3.txt', b'file3')

    def test_download_and_unzip_data(self):
        """
        create a temporary directory then create a zip in it, then
        check that it is downloaded properly
        """

        orig_destination = tempfile.TemporaryDirectory()
        zip_path = os.path.join(orig_destination.name, 'foo.zip')
        self.make_test_zip(zip_path)
        url = 'http://example.com/foo.zip'  # must have same basename that we create
        destination = download_and_unzip_data(url, orig_destination.name)
        self.assertEqual(orig_destination.name, destination)
        self.assertEqual(
            {'foo.zip', 'file1.txt', 'file2.txt', 'file3.txt'},
            set(os.listdir(orig_destination.name))
        )
        orig_destination.cleanup()

    def test_flush_memcached(self):
        """
        can only verify that it won't do anything in a test environment
        """
        self.assertFalse(flush_memcached())

    def test_get_csv_path(self):
        destination = tempfile.TemporaryDirectory()
        zip_path = os.path.join(destination.name, 'foo.zip')
        self.make_test_zip(zip_path)
        path_to_first_file_csv = get_csv_path(
            'http://example.com/foo.zip', destination.name
        )
        self.assertEqual(
            os.path.join(destination.name, 'file1-processed.csv'),
            path_to_first_file_csv
        )
        destination.cleanup()

    def test_get_datafile_path_special(self):
        with self.assertRaises(ValueError):
            get_datafile_path(None, 'anything')
        with self.assertRaises(ValueError):
            get_datafile_path('something', 'anything', zip_path='anything')

    def test_get_datafile_path_with_url(self):
        destination = tempfile.TemporaryDirectory()
        zip_path = os.path.join(destination.name, 'foo.zip')
        self.make_test_zip(zip_path)
        path_to_first_file = get_datafile_path(
            'http://example.com/foo.zip', destination.name
        )
        self.assertEqual(
            os.path.join(destination.name, 'file1.txt'),
            path_to_first_file
        )
        destination.cleanup()

    def test_get_datafile_path_with_zip_path(self):
        destination = tempfile.TemporaryDirectory()
        zip_path = os.path.join(destination.name, 'foo.zip')
        self.make_test_zip(zip_path)
        path_to_first_file = get_datafile_path(None, destination.name, zip_path=zip_path)
        self.assertEqual(
            os.path.join(destination.name, 'file1.txt'),
            path_to_first_file
        )
        destination.cleanup()

    def test_get_zipfile_path(self):
        self.assertEqual(
            '/tmp/favicon.ico',
            get_zipfile_path('https://example.com/favicon.ico', '/tmp')
        )

    def test_line_count(self):
        expected_num_lines = 2345
        with tempfile.NamedTemporaryFile(mode='w') as t:
            for i in range(expected_num_lines):
                print('line %s' % i, file=t)
            t.flush()
            self.assertEqual(expected_num_lines, line_count(t.name))

    def test_unzip_data(self):
        """
        test of download_and_unzip_data() above hits a lot of the main
        path of unzip_data(); this tests a few special scenarios
        """
        with self.assertRaises(ValueError):
            unzip_data(None)
        with self.assertRaises(ValueError):
            unzip_data('something', url=None, zip_path=None)
        with self.assertRaises(ValueError):
            unzip_data('something', url='http://example.com/foo.zip', zip_path='/tmp/foo.zip')
