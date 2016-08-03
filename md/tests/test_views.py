from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from md.tests import factories
from .. import views


class ViewTests(TestCase):
    multi_db = True

    def test_home(self):
        response = self.client.get(reverse('md:home'))
        self.assertEqual(200, response.status_code)

    def test_agency_detail(self):
        agency = factories.AgencyFactory(name="Maryland State Police")
        response = self.client.get(reverse('md:agency-detail', args=[agency.pk]))
        self.assertEqual(200, response.status_code)

    def test_agency_list(self):
        response = self.client.get(reverse('md:agency-list'))
        self.assertEqual(200, response.status_code)

    def test_agency_list_sorted_agencies(self):
        """
        Verify that agencies are delivered in an appropriately sorted and
        chunked form.
        """
        factories.AgencyFactory(name="Abc")
        factories.AgencyFactory(name="Def")
        factories.AgencyFactory(name="Ghi")
        factories.AgencyFactory(name="Abc_")
        factories.AgencyFactory(name="Def_")
        factories.AgencyFactory(name="Ghi_")
        factories.AgencyFactory(name="Abc__")
        factories.AgencyFactory(name="Def__")
        factories.AgencyFactory(name="Ghi__")
        factories.AgencyFactory(name="Abc___")
        factories.AgencyFactory(name="Def___")
        factories.AgencyFactory(name="Ghi___")
        factories.AgencyFactory(name="Abc____")
        factories.AgencyFactory(name="Def____")
        factories.AgencyFactory(name="Ghi____")

        response = self.client.get(reverse('md:agency-list'))
        sorted_agencies = response.context['sorted_agencies']

        # Verify that there are three alphabetic categories
        self.assertEqual(3, len(sorted_agencies))

        keys = [pair[0] for pair in sorted_agencies]
        # Verify that the relevant letters are in there
        self.assertTrue("A" in keys)
        self.assertTrue("D" in keys)
        self.assertTrue("G" in keys)

        # Verify that each alphabetic category contains three chunks
        # with the appropriate number of pieces (i.e. 2, 2, 1)
        for (letter, chunks) in sorted_agencies:
            self.assertEqual(3, len(chunks))
            self.assertEqual(2, len(chunks[0]))
            self.assertEqual(2, len(chunks[1]))
            self.assertEqual(1, len(chunks[2]))


class TestSearchView(TestCase):
    def test_search_good_data(self):
        self.factory = RequestFactory()
        request = self.factory.get('/md/search', data={
            'agency': 'Montgomery County Police Department',
        })
        response = views.search(request)
        text = 'error'
        self.assertNotContains(response, text, status_code=200)

    def test_search_bad_purpose_error(self):
        self.factory = RequestFactory()
        request = self.factory.get('/md/search', data={
            'agency': 'Montgomery County Police Department',
            'purpose': [25]
        })
        response = views.search(request)
        text = 'Select a valid choice. 25 is not one of the available choices'
        self.assertContains(response, text, status_code=200)

    def test_search_bad_gender_error(self):
        self.factory = RequestFactory()
        request = self.factory.get('/md/search', data={
            'agency': 'Montgomery County Police Department',
            'gender': 'hippopotamus'
        })
        response = views.search(request)
        text = 'Stops (0 total)'
        self.assertContains(response, text, status_code=200)
