from django.test import TestCase

from md.models import Agency, Stop
from md.tests.factories import AgencyFactory, StopFactory
from tsdata.dataset_facts import compute_dataset_facts


class TestDatasetFacts(TestCase):

    multi_db = True

    def setUp(self):
        super().setUp()
        self.top_five_agencies = [
            AgencyFactory()
            for _ in range(5)
        ]
        for i, agency in enumerate(self.top_five_agencies):
            for _ in range(i + 1):
                StopFactory(agency=agency)

    def test(self):
        facts = compute_dataset_facts(Agency, Stop, 'US/Eastern')
        self.assertIn('Stops: 15', facts)
        self.assertIn('Agencies: 5', facts)
        # Verify that the top 5 (only) agencies are listed in the right order
        # at the end of the facts.
        for i in range(5):
            agency = self.top_five_agencies[4 - i]
            self.assertIn('Id %d' % agency.id, facts[len(facts) - (5 - i)])
