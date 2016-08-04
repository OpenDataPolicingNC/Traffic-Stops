from django.test import TestCase

from . import factories


class TestAgencyModel(TestCase):

    def test_str(self):
        """Smoke test for string representation."""
        agency = factories.AgencyFactory(name="hello")
        self.assertEqual(str(agency), "hello")


class TestStopModel(TestCase):

    def test_str(self):
        """Smoke test for string representation."""
        stop = factories.StopFactory(date='2013-01-02 01:22:00+00:00', stop_location="location")
        self.assertEqual(str(stop), "Stop %s at 2013-01-02 01:22:00+00:00 at location" % stop.pk)
