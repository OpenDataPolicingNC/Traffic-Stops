from django.db import models

from caching.base import CachingManager, CachingMixin

from tsdata.models import CensusProfile

YN_CHOICES = (
    ("Y", "Yes"),
    ("N", "No")
)

# The numeric values for the various purposes are the column numbers in
# STOP_REASON_CSV.  Only some purpose values are referred to specifically in
# the code.  Constants aren't provided for the others.
INVESTIGATION_PURPOSE = 7
FAILURE_TO_REMAIN_PURPOSE = 10
UNKNOWN_PURPOSE = 11
PURPOSE_CHOICES = (
    # Strings must match purpose_order in app/states/md/defaults.js
    (0, 'Seat Belt Violation'),
    (1, 'Speed Limit Violation'),
    (2, 'Stop Light/Sign Violation'),
    (3, 'Driving While Impaired'),
    (4, 'Safe Movement Violation'),
    (5, 'Vehicle Equipment Violation'),
    (6, 'Vehicle Regulatory Violation'),
    (INVESTIGATION_PURPOSE, 'Investigation'),
    (8, 'Non-motor Vehicle Violations'),
    (9, 'Other Motor Vehicle Violation'),
    (FAILURE_TO_REMAIN_PURPOSE, 'Failure to remain at scene of accident'),
    (UNKNOWN_PURPOSE, 'Other/Unknown'),
)
ENABLED_PURPOSES = (
    (0, 'Seat Belt Violation'),
    (1, 'Speed Limit Violation'),
    (2, 'Stop Light/Sign Violation'),
    (3, 'Driving While Impaired'),
    (4, 'Safe Movement Violation'),
    (5, 'Vehicle Equipment Violation'),
    (6, 'Vehicle Regulatory Violation'),
    (8, 'Non-motor Vehicle Violations'),
    (9, 'Other Motor Vehicle Violation'),
    (UNKNOWN_PURPOSE, 'Other/Unknown'),
)

PURPOSE_BY_INDEX = [
    x for _, x in PURPOSE_CHOICES
]

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("U", "Unknown")
)

ETHNICITY_CHOICES = (
    ('W', 'White'),
    ('B', 'Black'),
    ('H', 'Hispanic'),
    ('A', 'Asian'),
    ('I', 'Native American'),
    ('U', 'Unknown'),  # unknown includes "Other"
)


class Stop(CachingMixin, models.Model):
    """
    "null=True" for some fields is a temporary solution for this import
    error: "null value in column "what_searched" violates not-null constraint"
    """
    stop_id = models.IntegerField(primary_key=True, default=1)
    date = models.DateTimeField(null=True)
    purpose = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES, default=UNKNOWN_PURPOSE)
    stop_date_text = models.CharField(max_length=20, blank=True, default='')
    stop_time_text = models.CharField(max_length=20, blank=True, default='')
    stop_location = models.CharField(max_length=1024)
    duration_text = models.CharField(max_length=20, blank=True, null=True)
    stop_reason = models.CharField(max_length=64)
    search_conducted = models.CharField(max_length=1, choices=YN_CHOICES, blank=True)
    search_reason = models.CharField(max_length=64, blank=True)
    seized = models.CharField(max_length=1, choices=YN_CHOICES, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth_text = models.CharField(max_length=20, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, choices=ETHNICITY_CHOICES, blank=True)
    officer_id = models.CharField(max_length=15, blank=True, default=None)
    agency_description = models.CharField(max_length=100)
    agency = models.ForeignKey('Agency', null=True, related_name='stops')
    age = models.PositiveSmallIntegerField(default=0)

    objects = CachingManager()

    def __str__(self):
        return 'Stop %d at %s at %s' % (
            self.stop_id, self.date, self.stop_location
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
