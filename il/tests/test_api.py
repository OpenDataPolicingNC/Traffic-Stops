import random

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from il.models import Agency, ETHNICITY_CHOICES, PURPOSE_CHOICES, UNKNOWN_PURPOSE
from il.tests import factories
from tsdata.tests.factories import CensusProfileFactory


KNOWN_ETHNICITY_CHOICES = [c for c in ETHNICITY_CHOICES if c[0] != 'U']
KNOWN_PURPOSE_CHOICES = [c for c in PURPOSE_CHOICES if c[0] != UNKNOWN_PURPOSE]


class AgencyTests(APITestCase):
    multi_db = True

    def test_agency_census_data(self):
        """
        Construct an agency with associated CensusProfile, check
        for inclusion
        """
        census_profile = CensusProfileFactory()
        agency = factories.AgencyFactory(census_profile_id=census_profile.id)
        url = reverse('il:agency-api-detail', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('census_profile', response.data)
        # CensusProfile tests check census data in more detail
        for attr in ('hispanic', 'non_hispanic', 'total'):
            self.assertEqual(
                response.data['census_profile'][attr], getattr(census_profile, attr)
            )

    def test_list_agencies(self):
        """Test Agency list"""
        agency = factories.AgencyFactory()
        url = reverse('il:agency-api-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Other Agencies may have been left around from other tests
        self.assertIn((agency.pk, agency.name), [
            (a.pk, a.name) for a in Agency.objects.all()
        ])

    def test_stops_api(self):
        """Test Agency stops API endpoint with no stops"""
        agency = factories.AgencyFactory()
        url = reverse('il:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_stops_count(self):
        """Test Agency stop counts"""
        agency = factories.AgencyFactory()

        ethnicities = random.sample(KNOWN_ETHNICITY_CHOICES, 2)
        ethnicity_a_code, ethnicity_a_label = ethnicities[0]
        ethnicity_b_code, ethnicity_b_label = ethnicities[1]

        factories.StopFactory(ethnicity=ethnicity_a_code, agency=agency, year=2010)
        factories.StopFactory(ethnicity=ethnicity_a_code, agency=agency, year=2010)
        factories.StopFactory(ethnicity=ethnicity_b_code, agency=agency, year=2012)
        url = reverse('il:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['year'], 2010)
        self.assertEqual(response.data[0][ethnicity_a_label], 2)
        self.assertEqual(response.data[1]['year'], 2012)
        self.assertEqual(response.data[1][ethnicity_b_label], 1)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('il:agency-api-stops-by-reason', args=[agency.pk])

        purpose_code, purpose_label = random.choice(KNOWN_PURPOSE_CHOICES)
        ethnicity_code, ethnicity_label = random.choice(KNOWN_ETHNICITY_CHOICES)
        factories.StopFactory(
            agency=agency, year=2010, purpose=purpose_code,
            ethnicity=ethnicity_code, search_conducted='N'
        )
        factories.StopFactory(
            agency=agency, year=2010, purpose=purpose_code,
            ethnicity=ethnicity_code, search_conducted='Y'
        )
        factories.StopFactory(
            agency=agency, year=2012, purpose=purpose_code,
            ethnicity=ethnicity_code, search_conducted='Y'
        )

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.keys()), 2)

        searches = response.data['searches']
        self.assertEqual(searches[0]['year'], 2010)
        self.assertEqual(searches[0][ethnicity_label], 1)
        self.assertEqual(searches[0]['purpose'], purpose_label)
        self.assertEqual(searches[1]['year'], 2012)
        self.assertEqual(searches[1][ethnicity_label], 1)
        self.assertEqual(searches[1]['purpose'], purpose_label)

        stops = response.data['stops']
        self.assertEqual(stops[0]['year'], 2010)
        self.assertEqual(stops[0][ethnicity_label], 2)
        self.assertEqual(stops[0]['purpose'], purpose_label)
        self.assertEqual(stops[1]['year'], 2012)
        self.assertEqual(stops[1][ethnicity_label], 1)
        self.assertEqual(stops[1]['purpose'], purpose_label)

    def test_searches(self):
        """Test Agency search counts"""
        agency = factories.AgencyFactory()
        stop = factories.StopFactory(agency=agency, search_conducted='Y')
        url = reverse('il:agency-api-searches', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], stop.year)
        self.assertEqual(response.data[0][dict(ETHNICITY_CHOICES)[stop.ethnicity]], 1)

    def test_contraband_hit_rate(self):
        agency = factories.AgencyFactory()
        ethnicity_code, ethnicity_label = random.choice(KNOWN_ETHNICITY_CHOICES)
        factories.StopFactory(
            agency=agency, year=2010, ethnicity=ethnicity_code,
            search_conducted='Y', seized='Y',
        )
        factories.StopFactory(
            agency=agency, year=2010, ethnicity=ethnicity_code,
            search_conducted='Y', seized='N',
        )
        factories.StopFactory(
            agency=agency, year=2012, ethnicity=ethnicity_code,
            search_conducted='Y', seized='Y',
        )
        url = reverse('il:agency-api-contraband-hit-rate', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.keys()), 2)

        searches = response.data['searches']
        self.assertEqual(searches[0]['year'], 2010)
        self.assertEqual(searches[0][ethnicity_label], 2)
        self.assertEqual(searches[1]['year'], 2012)
        self.assertEqual(searches[1][ethnicity_label], 1)

        contraband = response.data['contraband']
        self.assertEqual(contraband[0]['year'], 2010)
        self.assertEqual(contraband[0][ethnicity_label], 1)
        self.assertEqual(contraband[1]['year'], 2012)
        self.assertEqual(contraband[1][ethnicity_label], 1)
