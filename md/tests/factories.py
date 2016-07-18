import datetime

import factory
import factory.fuzzy

from md import models


class AgencyFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Agency

    name = factory.Sequence(lambda n: "Agency %03d" % n)


class StopFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Stop

    stop_id = factory.Sequence(lambda x: x)
    date = factory.fuzzy.FuzzyDate(datetime.date(2008, 1, 1))
    purpose = factory.fuzzy.FuzzyChoice(x[0] for x in models.PURPOSE_CHOICES)
    search_conducted = factory.fuzzy.FuzzyChoice(x[0] for x in models.YN_CHOICES)
    seized = factory.fuzzy.FuzzyChoice(x[0] for x in models.YN_CHOICES)
    gender = factory.fuzzy.FuzzyChoice(x[0] for x in models.GENDER_CHOICES)
    ethnicity = factory.fuzzy.FuzzyChoice(
        x[0] for x in models.ETHNICITY_CHOICES)
    officer_id = factory.fuzzy.FuzzyInteger(0)
    agency = factory.SubFactory(AgencyFactory)

    @factory.post_generation
    def year(self, create, extracted, **kwargs):
        """Wrapper to easily set stop date's year in test case"""
        if not create:
            return
        if extracted:
            self.date = self.date.replace(year=extracted)
