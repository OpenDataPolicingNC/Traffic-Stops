import datetime
import math

import factory
import factory.fuzzy

from tsdata import models


class DatasetFactory(factory.django.DjangoModelFactory):
    state = factory.Iterator(models.STATE_CHOICES, getter=lambda c: c[0])
    name = factory.Sequence(lambda n: 'Dataset %d' % n)
    url = factory.LazyAttribute(lambda obj: 'https://example.com/%s' % obj.state)
    date_received = factory.fuzzy.FuzzyDateTime(datetime.datetime(
        2008, 1, 1, 0, 0, tzinfo=datetime.timezone.utc))

    class Meta:
        model = models.Dataset


class CensusProfileFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.CensusProfile

    id = factory.Sequence(lambda n: '16000US%07d' % n)
    location = factory.Sequence(lambda n: 'Location %d' % n)
    geography = 'place'
    state = 'AA'
    source = 'ACS 5-Year Data (2012-2016)'
    white = factory.fuzzy.FuzzyInteger(1, 100)
    black = factory.fuzzy.FuzzyInteger(1, 100)
    native_american = factory.fuzzy.FuzzyInteger(1, 100)
    asian = factory.fuzzy.FuzzyInteger(1, 100)
    native_hawaiian = factory.fuzzy.FuzzyInteger(1, 100)
    other = factory.fuzzy.FuzzyInteger(1, 100)
    two_or_more_races = factory.fuzzy.FuzzyInteger(1, 100)

    total = factory.LazyAttribute(
        lambda o: (
            o.white + o.black + o.native_american +
            o.asian + o.native_hawaiian + o.other +
            o.two_or_more_races
        )
    )

    hispanic = factory.LazyAttribute(
        lambda o: math.floor(0.2 * o.total)
    )

    non_hispanic = factory.LazyAttribute(
        lambda o: o.total - o.hispanic
    )
