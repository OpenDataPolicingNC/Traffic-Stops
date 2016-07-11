import datetime
import factory
import factory.fuzzy

from nc import models


class AgencyFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Agency

    name = factory.Sequence(lambda n: "Agency %03d" % n)


class PersonFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Person

    person_id = factory.Sequence(lambda x: x)
    stop = factory.SubFactory('nc.tests.factories.StopFactory')
    age = factory.fuzzy.FuzzyInteger(16, 100)
    race = factory.fuzzy.FuzzyChoice(x[0] for x in models.RACE_CHOICES)
    ethnicity = factory.fuzzy.FuzzyChoice(
        x[0] for x in models.ETHNICITY_CHOICES)
    type = 'D'


class StopFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Stop

    stop_id = factory.Sequence(lambda x: x)
    agency = factory.SubFactory(AgencyFactory)
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    purpose = factory.fuzzy.FuzzyChoice(x[0] for x in models.PURPOSE_CHOICES)
    action = factory.fuzzy.FuzzyChoice(x[0] for x in models.ACTION_CHOICES)
    officer_id = factory.fuzzy.FuzzyInteger(0)

    @factory.post_generation
    def year(self, create, extracted, **kwargs):
        """Wrapper to easily set stop date's year in test case"""
        if not create:
            return
        if extracted:
            self.date = self.date.replace(year=extracted)


class SearchFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Search

    search_id = factory.Sequence(lambda x: x)
    stop = factory.SubFactory(StopFactory)
    person = factory.SubFactory(PersonFactory)
    type = factory.fuzzy.FuzzyChoice(x[0] for x in models.SEARCH_TYPE_CHOICES)
