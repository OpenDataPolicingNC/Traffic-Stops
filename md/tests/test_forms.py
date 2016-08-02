import datetime
import factory
import factory.fuzzy

from django.test import TestCase

from . import factories

from .. import forms, models


class TestSearchForm(TestCase):
    def test_agency_required(self):
        search_form = forms.SearchForm(data={})
        self.assertFalse(search_form.is_valid())
        error_keys = search_form.errors.keys()
        self.assertEqual(len(error_keys), 1)
        self.assertTrue('agency' in error_keys)

    def test_clean_no_start_date(self):
        search_form = forms.SearchForm(data={
            'end_date': '1/1/2013',
            'start_date': '12/31/2013'})
        self.assertFalse(search_form.is_valid())
        error_keys = search_form.errors.keys()
        self.assertTrue('end_date' in error_keys)

    def test_clean_more_than_one_year(self):
        search_form = forms.SearchForm(data={
            'agency': 'Maryland State Police',
            'start_date': '1/1/2013',
            'end_date': '1/3/2014'})
        self.assertFalse(search_form.is_valid())
        error_keys = search_form.errors.keys()
        self.assertTrue('end_date' in error_keys)

    def test_form_generates_valid_query(self):
        # agency = factory.SubFactory(factories.AgencyFactory)
        # officer = factory.fuzzy.FuzzyInteger(0)
        # start_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2013, 1, 1, 0, 0,
        #                                          tzinfo=datetime.timezone.utc))
        # end_date = factory.fuzzy.FuzzyDateTime(datetime.datetime(2013, 1, 1, 0, 0,
        #                                        tzinfo=datetime.timezone.utc))
        # age = factory.fuzzy.FuzzyInteger(0, 100)
        # gender = factory.fuzzy.FuzzyChoice(x[0] for x in models.GENDER_CHOICES)
        # ethnicity = factory.fuzzy.FuzzyChoice(
        #     x[0] for x in models.ETHNICITY_CHOICES)
        # purpose = factory.fuzzy.FuzzyChoice(
        #     x[0] for x in models.PURPOSE_CHOICES)
     search_form = forms.SearchForm(data={
            'agency': 'Montgomery County Police Department',
            'officer': '1',
            'start_date': '1/1/2014',
            'end_date': '1/31/2014',
            'age': '20',
            'gender': 'F',
            'ethnicity': 'A',
            'purpose': [0]
        })
        self.assertTrue(search_form.is_valid())

