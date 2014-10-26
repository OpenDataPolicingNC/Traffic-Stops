from django.test import TestCase

from stops.utils import GroupedData


class GrouperTestCase(TestCase):
    def test_single_item_group(self):
        """Verify group by with single item"""
        stops = GroupedData(by='year')
        stops.add(year=2010, race1=10)
        stops.add(year=2010, race2=10)
        stops.add(year=2011, race1=5)
        stops.add(year=2011, race2=5)
        expected = [{'year': 2010, 'race1': 10, 'race2': 10},
                    {'year': 2011, 'race1': 5, 'race2': 5}]
        self.assertEqual(stops.flatten(), expected)

    def test_pair_item_group(self):
        """Verify group by with two items"""
        stops = GroupedData(by=('purpose', 'year'))
        stops.add(purpose='Checkpoint', year=2010, race1=10)
        stops.add(purpose='Checkpoint', year=2010, race2=10)
        stops.add(purpose='Checkpoint', year=2011, race1=5)
        stops.add(purpose='Checkpoint', year=2011, race2=5)
        expected = [{'purpose': 'Checkpoint', 'year': 2010, 'race1': 10, 'race2': 10},
                    {'purpose': 'Checkpoint', 'year': 2011, 'race1': 5, 'race2': 5}]
        self.assertEqual(stops.flatten(), expected)

    def test_default_values(self):
        """Verify group by with two items"""
        stops = GroupedData('year', defaults={'race1': 0, 'race2': 0})
        stops.add(year=2010, race1=10)
        stops.add(year=2011, race2=10)
        expected = [{'year': 2010, 'race1': 10, 'race2': 0},
                    {'year': 2011, 'race1': 0, 'race2': 10}]
        self.assertEqual(stops.flatten(), expected)
