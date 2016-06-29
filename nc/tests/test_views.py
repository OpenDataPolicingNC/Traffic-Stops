from django.core.urlresolvers import reverse
from django.test import TestCase
from nc.models import Agency


class ViewTests(TestCase):
    def test_home(self):
        response = self.client.get(reverse('nc:home'))
        self.assertEqual(200, response.status_code)

    def test_search(self):
        response = self.client.get(reverse('nc:stops-search'))
        self.assertEqual(200, response.status_code)

    def test_agency_detail(self):
        agency = Agency.objects.create(name="Durham")
        response = self.client.get(reverse('nc:agency-detail', args=[agency.pk]))
        self.assertEqual(200, response.status_code)
