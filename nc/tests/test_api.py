import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from nc.models import Agency, Stop, PURPOSE_CHOICES, RACE_CHOICES
from nc.tests import factories
from nc.api import GROUPS


class AgencyTests(APITestCase):

    def tearDown(self):
        Stop.objects.all().delete()
        Agency.objects.all().delete()

    def test_list_agencies(self):
        """Test Agency list"""
        agency = factories.AgencyFactory()
        url = reverse('nc:agency-api-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Other Agencies may have been left around from other tests
        self.assertIn((agency.pk, agency.name), [
            (a.pk, a.name) for a in Agency.objects.all()
        ])

    def test_stops_api(self):
        """Test Agency stops API endpoint with no stops"""
        agency = factories.AgencyFactory()
        url = reverse('nc:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_stops_count(self):
        """Test Agency stop counts"""
        agency = factories.AgencyFactory()
        factories.PersonFactory(race='B', stop__agency=agency,
                                ethnicity='N', stop__year=2010)
        factories.PersonFactory(race='B', stop__agency=agency,
                                ethnicity='N', stop__year=2010)
        factories.PersonFactory(race='W', stop__agency=agency,
                                ethnicity='N', stop__year=2012)
        url = reverse('nc:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['year'], 2010)
        self.assertEqual(response.data[0]['black'], 2)
        self.assertEqual(response.data[1]['year'], 2012)
        self.assertEqual(response.data[1]['white'], 1)

    def test_grouping_by_year(self):
        """
        Create one stop right at the end of the year in Maryland and another
        stop a day later and ensure that the stops are counted in the expected
        years.
        """
        nc_timezone = pytz.timezone(settings.NC_TIME_ZONE)
        year = 2015
        end_of_year = nc_timezone.localize(datetime.datetime(
            year=year,
            month=12,
            day=31,
            hour=23,
            minute=59,
        ))
        agency = factories.AgencyFactory()
        race_code, _ = RACE_CHOICES[1]
        race_label = GROUPS[race_code]
        factories.PersonFactory(
            race=race_code,
            ethnicity='N',
            stop__agency=agency,
            stop__date=end_of_year
        )
        factories.PersonFactory(
            race=race_code,
            ethnicity='N',
            stop__agency=agency,
            stop__date=end_of_year + datetime.timedelta(days=1)
        )
        url = reverse('nc:agency-api-stops', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['year'], year)
        self.assertEqual(response.data[0][race_label], 1)
        self.assertEqual(response.data[1]['year'], year + 1)
        self.assertEqual(response.data[1][race_label], 1)

    def test_officer_stops_count(self):
        """Test officer (within an agency) stop counts"""
        p = factories.PersonFactory()
        url = reverse('nc:agency-api-stops', args=[p.stop.agency.pk])
        url = "{}?officer={}".format(url, p.stop.officer_id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], p.stop.date.year)
        self.assertEqual(response.data[0][GROUPS[p.race]], 1)

    def test_stops_by_reason(self):
        """Test Agency stops_by_reason API endpoint"""
        agency = factories.AgencyFactory()
        url = reverse('nc:agency-api-stops-by-reason', args=[agency.pk])

        purpose_code, purpose_label = PURPOSE_CHOICES[4]
        race_code, _ = RACE_CHOICES[1]
        race_label = GROUPS[race_code]
        factories.PersonFactory(race=race_code, stop__agency=agency,
                                ethnicity='N', stop__year=2010,
                                stop__purpose=purpose_code)
        p2 = factories.PersonFactory(race=race_code, stop__agency=agency,
                                     ethnicity='N', stop__year=2010,
                                     stop__purpose=purpose_code)
        p3 = factories.PersonFactory(race=race_code, stop__agency=agency,
                                     ethnicity='N', stop__year=2012,
                                     stop__purpose=purpose_code)
        factories.SearchFactory(stop=p2.stop)
        factories.SearchFactory(stop=p3.stop)

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.keys()), 2)

        searches = response.data['searches']
        self.assertEqual(searches[0]['year'], 2010)
        self.assertEqual(searches[0][race_label], 1)
        self.assertEqual(searches[0]['purpose'], purpose_label)
        self.assertEqual(searches[1]['year'], 2012)
        self.assertEqual(searches[1][race_label], 1)
        self.assertEqual(searches[1]['purpose'], purpose_label)

        stops = response.data['stops']
        self.assertEqual(stops[0]['year'], 2010)
        self.assertEqual(stops[0][race_label], 2)
        self.assertEqual(stops[0]['purpose'], purpose_label)
        self.assertEqual(stops[1]['year'], 2012)
        self.assertEqual(stops[1][race_label], 1)
        self.assertEqual(stops[1]['purpose'], purpose_label)

    def test_searches(self):
        """Test Agency search counts"""
        agency = factories.AgencyFactory()
        p1 = factories.PersonFactory(stop__agency=agency)
        s1 = factories.SearchFactory(person=p1, stop=p1.stop)
        url = reverse('nc:agency-api-searches', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['year'], s1.stop.date.year)
        self.assertEqual(response.data[0][GROUPS.get(s1.person.race)], 1)

    def test_contraband_hit_rate(self):
        agency = factories.AgencyFactory()
        race_code, _ = RACE_CHOICES[1]
        race_label = GROUPS[race_code]
        p1 = factories.PersonFactory(race=race_code, stop__agency=agency,
                                     ethnicity='N', stop__year=2010)
        p2 = factories.PersonFactory(race=race_code, stop__agency=agency,
                                     ethnicity='N', stop__year=2010)
        p3 = factories.PersonFactory(race=race_code, stop__agency=agency,
                                     ethnicity='N', stop__year=2012)
        s1 = factories.SearchFactory(stop=p1.stop)
        factories.SearchFactory(stop=p2.stop)
        s3 = factories.SearchFactory(stop=p3.stop)
        factories.ContrabandFactory(search=s1, person=p1, stop=p1.stop)
        factories.ContrabandFactory(search=s3, person=p3, stop=p3.stop)
        url = reverse('nc:agency-api-contraband-hit-rate', args=[agency.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.keys()), 2)

        searches = response.data['searches']
        self.assertEqual(searches[0]['year'], 2010)
        self.assertEqual(searches[0][race_label], 2)
        self.assertEqual(searches[1]['year'], 2012)
        self.assertEqual(searches[1][race_label], 1)

        contraband = response.data['contraband']
        self.assertEqual(contraband[0]['year'], 2010)
        self.assertEqual(contraband[0][race_label], 1)
        self.assertEqual(contraband[1]['year'], 2012)
        self.assertEqual(contraband[1][race_label], 1)

    def test_use_of_force(self):
        pass
