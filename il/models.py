from django.db import models

from caching.base import CachingManager, CachingMixin

from tsdata.models import CensusProfile

YN_CHOICES = (
    ("Y", "Yes"),
    ("N", "No")
)

UNKNOWN_PURPOSE = 11
PURPOSE_CHOICES = (
    (1, 'Moving Violation'),
    (2, 'Equipment'),
    (3, 'Registration'),
    (UNKNOWN_PURPOSE, 'Unknown')
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("U", "Unknown")
)

ETHNICITY_CHOICES = (
    ('W', 'White'),
    ('B', 'Black'),
    ('H', 'Hispanic'),
    ('U', 'Unknown'),  # unknown includes "Other"
)

SEARCH_CONDUCTED_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('U', 'Unknown'),
)

SEIZED_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
    ('U', 'Unknown'),
)


class Stop(CachingMixin, models.Model):
    stop_id = models.IntegerField(primary_key=True, default=1)
    year = models.PositiveSmallIntegerField()
    purpose = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES, default=UNKNOWN_PURPOSE)
    search_conducted = models.CharField(max_length=1, choices=SEARCH_CONDUCTED_CHOICES)
    seized = models.CharField(max_length=1, choices=SEIZED_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=20, choices=ETHNICITY_CHOICES)
    agency = models.ForeignKey('Agency', null=True, related_name='stops')
    agency_description = models.CharField(max_length=100)

    objects = CachingManager()

    def __str__(self):
        return 'Stop %d agency %s in %s' % (
            self.stop_id, self.agency_description, self.year,
        )


class Agency(CachingMixin, models.Model):
    name = models.CharField(max_length=255)
    # link to CensusProfile (no cross-database foreign key)
    census_profile_id = models.CharField(max_length=16, blank=True, default='')

    objects = CachingManager()

    class Meta(object):
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name

    @property
    def census_profile(self):
        if self.census_profile_id:
            profile = CensusProfile.objects.get(id=self.census_profile_id)
            return profile.get_census_dict()
        else:
            return dict()
