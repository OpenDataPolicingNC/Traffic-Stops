from django.db import models

#   1: Location
#   2: Agency
#   3: Date of Stop
#   4: Time of Stop
#   5: Gender
#   6: DOB
#   7: Age at the time of stop
#   8:
#   9: Race
#  10: State of Residence
#  11: Registration (tag)
#  12: State of Registration
#  13: County of Residence
#  14: Stop Reason (Abbreviated)
#  15: Stop Reason
#  16: Search
#  17: Search Reason
#  18: Disposition
#  19: Outcome
#  20: Arrest Reason
#  21: Arrest Made
#  22: Search Conducted
#  23: Duration of Search (in minutes)
#  24: Duration of Stop      (in minutes)
#  25: Reason for Search or Stop Article
#  26: Reason for Search  or Stop Section
#  27: Reason for Search or Stop Sub-Section
#  28: Reason for Search or Stop Paragraph
#  29: Crime Charged Article
#  30: Crime Charged Section
#  31: Crime Charged Sub-Section
#  32: Crime Charged Paragraph
#  33:

GENDER_CHOICES = (("m", "Male"),
                  ("f", "Female"))

class Stop(models.Model):
    location_text = models.CharField(max_length=1024)
    agency_description = models.CharField(max_length=100)
    stop_date = models.DateTimeField()
    stop_time = models.TimeField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)




    agency = models.ForeignKey('Agency', null=True, related_name='stops')


class Agency(models.Model):
    name = models.CharField(max_length=255)

    class Meta(object):
        verbose_name_plural = 'Agencies'

    def __str__(self):
        return self.name
