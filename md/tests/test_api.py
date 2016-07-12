from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from md.models import ETHNICITY_CHOICES
from md.tests import factories


class AgencyTests(APITestCase):

    def test_list_agencies(self):
        """Test Agency list"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-list')
        data = [{'id': agency.pk, 'name': agency.name}]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_stops_api(self):
        """Test Agency stops API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stops_count(self):
        """Test Agency stop counts"""
        agency = factories.AgencyFactory()

        ethnicity_1_code, ethnicity_1_label = ETHNICITY_CHOICES[1]
        ethnicity_3_code, ethnicity_3_label = ETHNICITY_CHOICES[3]

        factories.StopFactory(ethnicity=ethnicity_1_code, agency=agency, year=2010)
        factories.StopFactory(ethnicity=ethnicity_1_code, agency=agency, year=2010)
        factories.StopFactory(ethnicity=ethnicity_3_code, agency=agency, year=2012)
        url = reverse('md:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data[0]['year'], 2010)
        self.assertEqual(response.data[0][ethnicity_1_label], 2)
        self.assertEqual(response.data[1]['year'], 2012)
        self.assertEqual(response.data[1][ethnicity_3_label], 1)

    def test_officer_stops_count(self):
        """Test officer (within an agency) stop counts"""
        stop = factories.StopFactory()
        url = reverse('md:agency-api-stops', args=[stop.agency.pk])
        url = "{}?officer={}".format(url, stop.officer_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data[0]['year'], stop.date.year)
        ethnicity_label = dict(ETHNICITY_CHOICES)[stop.ethnicity]
        self.assertEqual(response.data[0][ethnicity_label], 1)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-stops-by-reason', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_searches(self):
        """Test Agency search counts"""
        agency = factories.AgencyFactory()
        stop = factories.StopFactory(agency=agency, search_conducted='Y')
        url = reverse('md:agency-api-searches', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], stop.date.year)
        self.assertEqual(response.data[0][dict(ETHNICITY_CHOICES)[stop.ethnicity]], 1)
