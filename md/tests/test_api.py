import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from md.models import Agency, ETHNICITY_CHOICES, PURPOSE_CHOICES
from md.tests import factories
from tsdata.tests.factories import CensusProfileFactory


class AgencyTests(APITestCase):

    def test_list_agencies(self):
        """Test Agency list"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Other Agencies may have been left around from other tests
        self.assertIn((agency.pk, agency.name), [
            (a.pk, a.name) for a in Agency.objects.all()
        ])

    def test_agency_census_data(self):
        """
        Construct an agency with associated CensusProfile, check
        for inclusion
        """
        census_profile = CensusProfileFactory()
        agency = factories.AgencyFactory(census_profile_id=census_profile.id)
        url = reverse('md:agency-api-detail', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('census_profile', response.data)
        # CensusProfile tests check census data in more detail
        for attr in ('hispanic', 'non_hispanic', 'total'):
            self.assertEqual(
                response.data['census_profile'][attr], getattr(census_profile, attr)
            )

    def test_stops_api(self):
        """Test Agency stops API endpoint with no stops"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['year'], 2010)
        self.assertEqual(response.data[0][ethnicity_1_label], 2)
        self.assertEqual(response.data[1]['year'], 2012)
        self.assertEqual(response.data[1][ethnicity_3_label], 1)

    def test_grouping_by_year(self):
        """
        Create one stop right at the end of the year in Maryland and another
        stop a day later and ensure that the stops are counted in the expected
        years.
        """
        md_timezone = pytz.timezone(settings.MD_TIME_ZONE)
        year = 2015
        end_of_year = md_timezone.localize(datetime.datetime(
            year=year,
            month=12,
            day=31,
            hour=23,
            minute=59,
        ))
        agency = factories.AgencyFactory()
        ethnicity_code, ethnicity_label = ETHNICITY_CHOICES[1]
        factories.StopFactory(
            ethnicity=ethnicity_code,
            agency=agency,
            date=end_of_year
        )
        factories.StopFactory(
            ethnicity=ethnicity_code,
            agency=agency,
            date=end_of_year + datetime.timedelta(days=1)
        )
        url = reverse('md:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['year'], year)
        self.assertEqual(response.data[0][ethnicity_label], 1)
        self.assertEqual(response.data[1]['year'], year + 1)
        self.assertEqual(response.data[1][ethnicity_label], 1)

    def test_officer_stops_count(self):
        """Test officer (within an agency) stop counts"""
        stop = factories.StopFactory()
        url = reverse('md:agency-api-stops', args=[stop.agency.pk])
        url = "{}?officer={}".format(url, stop.officer_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], stop.date.year)
        ethnicity_label = dict(ETHNICITY_CHOICES)[stop.ethnicity]
        self.assertEqual(response.data[0][ethnicity_label], 1)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('md:agency-api-stops-by-reason', args=[agency.pk])

        purpose_code, purpose_label = PURPOSE_CHOICES[4]
        ethnicity_code, ethnicity_label = ETHNICITY_CHOICES[1]
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
        url = reverse('md:agency-api-searches', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], stop.date.year)
        self.assertEqual(response.data[0][dict(ETHNICITY_CHOICES)[stop.ethnicity]], 1)

    def test_contraband_hit_rate(self):
        agency = factories.AgencyFactory()
        ethnicity_code, ethnicity_label = ETHNICITY_CHOICES[1]
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
        url = reverse('md:agency-api-contraband-hit-rate', args=[agency.pk])
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
