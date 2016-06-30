from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from nc.models import Agency


class AgencyTests(APITestCase):

    def test_list_agencies(self):
        """Test Agency list"""
        Agency.objects.create(name="Durham")
        url = reverse('nc:agency-api-list')
        data = [{'id': 1, 'name': 'Durham'}]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_stops_api(self):
        """Test Agency stops API endpoint"""
        agency = Agency.objects.create(name="Durham")
        url = reverse('nc:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = Agency.objects.create(name="Durham")
        url = reverse('nc:agency-api-stops-by-reason', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
