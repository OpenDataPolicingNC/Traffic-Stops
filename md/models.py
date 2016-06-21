from django.db import models

# Columns in CSV:
#
# index
# date
# STOPDATE
# TIME_OF_STOP
# LOCATION
# DURATION
# STOP_REASON
# SEARCH_CONDUCTED
# SEARCH_REASON
# WHATSEARCHED
# SEIZED
# STOPOUTCOME
# CRIME_CHARGED
# REGISTRATION_STATE
# GENDER
# DOB
# RESIDENCE_STATE
# MD_COUNTY
# ETHNICITY
# OFFICERID
# AGENCY


YN_CHOICES = (
    ("Y", "Yes"),
    ("N", "No")
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female")
)


class Stop(models.Model):
    """
    "null=True" for some fields is a temporary solution for this import
    error: "null value in column "what_searched" violates not-null constraint"
    """
    stop_id = models.IntegerField(primary_key=True, default=1)
    date = models.DateTimeField(null=True)
    stop_date_text = models.CharField(max_length=20, blank=True, default='')
    stop_time_text = models.CharField(max_length=20, blank=True, default='')
    location_text = models.CharField(max_length=1024)
    duration_text = models.CharField(max_length=20, blank=True, null=True)
    stop_reason = models.CharField(max_length=64)
    search_conducted = models.CharField(max_length=1, choices=YN_CHOICES, blank=True)
    search_reason = models.CharField(max_length=64, blank=True)
    what_searched = models.CharField(max_length=64, blank=True, null=True)
    seized = models.CharField(max_length=64, blank=True)
    stop_outcome = models.CharField(max_length=20, blank=True)
    crime_charged = models.CharField(max_length=20, blank=True, null=True)
    registration_state = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)  # "female" "MALE" are in error
    date_of_birth_text = models.CharField(max_length=20, blank=True, null=True)
    residence_state = models.CharField(max_length=3, blank=True)  # "mfd" is in error
    county = models.CharField(max_length=25, blank=True)
    ethnicity = models.CharField(max_length=20, blank=True)
    officer_id = models.IntegerField(blank=True, default=None)
    agency_description = models.CharField(max_length=100)
    agency = models.ForeignKey('Agency', null=True, related_name='stops')


class Agency(models.Model):
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name
