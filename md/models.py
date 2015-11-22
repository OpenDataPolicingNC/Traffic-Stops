from django.db import models

# 'datetime',
#  'Location',
#  'Agency',
#  'Gender',
#  'DOB',
#  'Age at the time of stop',
#  'Unnamed: 7',
#  'Race',
#  'State of Residence',
#  'Registration (tag)',
#  'State of Registration',
#  'County of Residence',
#  'Stop Reason (Abbreviated)',
#  'Stop Reason',
#  'Search',
#  'Search Reason',
#  'Disposition',
#  'Outcome',
#  'Arrest Reason',
#  'Arrest Made',
#  'Search Conducted',
#  'Duration of Search (in minutes)',
#  'Duration of Stop      (in minutes)',
#  'Reason for Search or Stop Article',
#  'Reason for Search  or Stop Section',
#  'Reason for Search or Stop Sub-Section',
#  'Reason for Search or Stop Paragraph',
#  'Crime Charged Article',
#  'Crime Charged Section',
#  'Crime Charged Sub-Section',
#  'Crime Charged Paragraph'

RESIDENCE_CHOICES = (("i", "In"),
                     ("o", "Out"))

RACE_CHOICES = (("h", "Hispanic"),
                ("a", "Asian"),
                ("w", "White"),
                ("b", "Black"),
                ("u", "Unknown"),
                ("o", "Other"))

GENDER_CHOICES = (("m", "Male"),
                  ("f", "Female"))

SEARCH_TYPE_CHOICES = (("both", "Both"),
                       ("prop", "Property"),
                       ("pers", "Person"))

SEARCH_REASON_CHOICES = (("incarrest", "incarrest"),
                         ("cons", "cons"),
                         ("other", "other"),
                         ("prob", "prob"),
                         ("k9", "k9"),
                         ("exigent", "exigent"))

DISPOSITION_CHOICES = (("contra", "Contraband"),
                       ("both", "Both"),
                       ("prop", "Property"))

OUTCOME_CHOICES = (("sero", "sero"),
                   ("warn", "Warning"),
                   ("cit", "Citation"),
                   ("arr", "Arrest"))


class Stop(models.Model):
    location_text = models.CharField(max_length=1024)
    agency_description = models.CharField(max_length=100)
    stop_date = models.DateTimeField(null=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(null=True)
    race = models.CharField(max_length=1, choices=RACE_CHOICES, blank=True)
    residence_county = models.CharField(max_length=100)
    residence_state = models.CharField(max_length=1, blank=True,
                                       choices=RESIDENCE_CHOICES)
    registration_state = models.CharField(max_length=1, blank=True,
                                          choices=RESIDENCE_CHOICES)
    stop_reason = models.CharField(max_length=64)
    search_type = models.CharField(max_length=4, choices=SEARCH_TYPE_CHOICES,
                                   blank=True)
    search_reason = models.CharField(max_length=16, blank=True,
                                     choices=SEARCH_REASON_CHOICES)
    disposition = models.CharField(max_length=8, blank=True,
                                   choices=DISPOSITION_CHOICES)
    outcome = models.CharField(max_length=8, blank=True,
                               choices=OUTCOME_CHOICES)
    agency = models.ForeignKey('Agency', null=True, related_name='stops')


class Agency(models.Model):
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name
