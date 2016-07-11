from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from nc.tests import factories
from nc.api import GROUPS


class AgencyTests(APITestCase):

    def test_list_agencies(self):
        """Test Agency list"""
        agency = factories.AgencyFactory()
        url = reverse('agency-api-list')
        data = [{'id': agency.pk, 'name': agency.name}]
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_stops_api(self):
        """Test Agency stops API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stops_count(self):
        """Test Agency stop counts"""
        agency = factories.AgencyFactory()
        factories.PersonFactory(race='B', stop__agency=agency,
                                ethnicity='N', stop__year=2010)
        factories.PersonFactory(race='B', stop__agency=agency,
                                ethnicity='N', stop__year=2010)
        factories.PersonFactory(race='W', stop__agency=agency,
                                ethnicity='N', stop__year=2012)
        url = reverse('agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.data[0]['year'], 2010)
        self.assertEqual(response.data[0]['black'], 2)
        self.assertEqual(response.data[1]['year'], 2012)
        self.assertEqual(response.data[1]['white'], 1)

    def test_officer_stops_count(self):
        """Test officer (within an agency) stop counts"""
        p = factories.PersonFactory()
        url = reverse('agency-api-stops', args=[p.stop.agency.pk])
        url = "{}?officer={}".format(url, p.stop.officer_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data[0]['year'], p.stop.date.year)
        self.assertEqual(response.data[0][GROUPS[p.race]], 1)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('agency-api-stops-by-reason', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_searches(self):
        """Test Agency search counts"""
        agency = factories.AgencyFactory()
        p1 = factories.PersonFactory(stop__agency=agency)
        s1 = factories.SearchFactory(person=p1, stop=p1.stop)
        url = reverse('agency-api-searches', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], s1.stop.date.year)
        self.assertEqual(response.data[0][GROUPS.get(s1.person.race)], 1)
