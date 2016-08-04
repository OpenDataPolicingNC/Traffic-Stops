import factory
import factory.fuzzy
import math

from tsdata import models


class CensusProfileFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.CensusProfile

    id = factory.Sequence(lambda n: '16000US%07d' % n)
    location = factory.Sequence(lambda n: 'Location %d' % n)
    geography = 'place'
    state = 'AA'
    source = 'ACS 5-Year Data (2010-2014)'
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
