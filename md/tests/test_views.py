from django.test import TestCase, RequestFactory

from .. import views


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
