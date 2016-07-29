from django.core.urlresolvers import reverse
from django.test import TestCase
from nc.models import Agency


class ViewTests(TestCase):
    multi_db = True

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

    def test_agency_list(self):
        response = self.client.get(reverse('nc:agency-list'))
        self.assertEqual(200, response.status_code)

    def test_agency_list_sorted_agencies(self):
        """
        Verify that agencies are delivered in an appropriately sorted and
        chunked form.
        """
        Agency.objects.create(name="Abc")
        Agency.objects.create(name="Def")
        Agency.objects.create(name="Ghi")
        Agency.objects.create(name="Abc_")
        Agency.objects.create(name="Def_")
        Agency.objects.create(name="Ghi_")
        Agency.objects.create(name="Abc__")
        Agency.objects.create(name="Def__")
        Agency.objects.create(name="Ghi__")
        Agency.objects.create(name="Abc___")
        Agency.objects.create(name="Def___")
        Agency.objects.create(name="Ghi___")
        Agency.objects.create(name="Abc____")
        Agency.objects.create(name="Def____")
        Agency.objects.create(name="Ghi____")

        response = self.client.get(reverse('nc:agency-list'))
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
