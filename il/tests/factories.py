import datetime

import factory
import factory.fuzzy

from il import models


CURRENT_YEAR = datetime.datetime.now().year


class AgencyFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Agency

    name = factory.Sequence(lambda n: "Agency %03d" % n)


class StopFactory(factory.django.DjangoModelFactory):

    class Meta(object):
        model = models.Stop

    stop_id = factory.Sequence(lambda x: x)
    year = factory.fuzzy.FuzzyChoice(range(2005, CURRENT_YEAR + 1))
    purpose = factory.fuzzy.FuzzyChoice(x[0] for x in models.PURPOSE_CHOICES)
    search_conducted = factory.fuzzy.FuzzyChoice(x[0] for x in models.YN_CHOICES)
    seized = factory.fuzzy.FuzzyChoice(x[0] for x in models.YN_CHOICES)
    gender = factory.fuzzy.FuzzyChoice(x[0] for x in models.GENDER_CHOICES)
    ethnicity = factory.fuzzy.FuzzyChoice(x[0] for x in models.ETHNICITY_CHOICES)
    agency = factory.SubFactory(AgencyFactory)
