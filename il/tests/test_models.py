from django.test import TestCase

from . import factories


class TestAgencyModel(TestCase):
    multi_db = True

    def test_str(self):
        """Smoke test for string representation."""
        agency = factories.AgencyFactory(name="hello")
        self.assertEqual(str(agency), "hello")


class TestStopModel(TestCase):
    multi_db = True

    def test_str(self):
        """Smoke test for string representation."""
        stop = factories.StopFactory(year=2013)
        self.assertEqual(str(stop), "Stop %s agency %s in 2013" % (
            stop.pk, stop.agency_description
        ))
