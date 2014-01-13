from django.db import models


PURPOSE_CHOICES = (('1', 'Speed Limit Violation'),
                   ('2', 'Stop Light/Sign Violation'),
                   ('3', 'Driving While Impaired'),
                   ('4', 'Safe Movement Violation'),
                   ('5', 'Vehicle Equipment Violation'),
                   ('6', 'Vehicle Regulatory Violation'),
                   ('7', 'Seat Belt Violation'),
                   ('8', 'Investigation'),
                   ('9', 'Other Motor Vehicle Violation'),
                   ('10', 'Checkpoint'))

ACTION_CHOICES = (('1', 'Verbal Warning'),
                  ('2', 'Written Warning'),
                  ('3', 'Citation Issued'),
                  ('4', 'On-View Arrest'),
                  ('5', 'No Action Taken'))


class Stop(models.Model):
    stop_id = models.PositiveIntegerField(primary_key=True)
    agency_description = models.CharField(max_length=100)
    agency = models.ForeignKey('Agency', null=True)
    date = models.DateTimeField()
    purpose = models.PositiveSmallIntegerField(choices=PURPOSE_CHOICES)
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    driver_arrest = models.BooleanField()
    passenger_arrest = models.BooleanField()
    encounter_force = models.BooleanField()
    engage_force = models.BooleanField()
    officer_injury = models.BooleanField()
    driver_injury = models.BooleanField()
    passenger_injury = models.BooleanField()
    officer_id = models.CharField(max_length=15) # todo: keys
    stop_location = models.CharField(max_length=15) # todo: keys
    stop_city = models.CharField(max_length=20)



PERSON_TYPE_CHOICES = (("Dr", "Driver"),
                       ("Pa", "Passenger"))

GENDER_CHOICES = (("M", "Male"),
                  ("F", "Female"))

ETHNICITY_CHOICES = (('H' , 'Hispanic'),
                     ('NH', 'Non-Hispanic'))


RACE_CHOICES = (('A', 'Asian'),
                ('B', 'Black'),
                ('I', 'Native American'),
                ('U', 'Other/Unknown'),
                ('W', 'White'))

class Person(models.Model):
    person_id = models.IntegerField(primary_key=True)
    stop = models.ForeignKey(Stop)
    type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES)
    age  = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY_CHOICES)
    race = models.CharField(max_length=2, choices=RACE_CHOICES)


SEARCH_TYPE_CHOICES = ()

class Search(models.Model):
    search_id = models.IntegerField(primary_key=True)
    stop = models.ForeignKey(Stop)
    person = models.ForeignKey(Person)
    type = models.PositiveSmallIntegerField(choices=SEARCH_TYPE_CHOICES)
    vehicle_search = models.BooleanField()
    driver_search = models.BooleanField()
    passenger_search = models.BooleanField()
    property_search = models.BooleanField()
    vehicle_siezed = models.BooleanField()
    personal_property_siezed = models.BooleanField()
    other_property_sized = models.BooleanField()


class Contraband(models.Model):
    contraband_id = models.IntegerField(primary_key=True)
    search = models.ForeignKey(Search)
    person = models.ForeignKey(Person)
    stop = models.ForeignKey(Stop)
    ounces = models.FloatField(default=0)
    pounds = models.FloatField(default=0)
    pints = models.FloatField(default=0)
    gallons = models.FloatField(default=0)
    dosages = models.FloatField(default=0)
    grams = models.FloatField(default=0)
    kilos = models.FloatField(default=0)
    money = models.FloatField(default=0)
    weapons = models.FloatField(default=0)
    dollar_amount = models.FloatField(default=0)


SEARCH_BASIS_CHOICES = (('ER',   'Erratic/Suspicious Behavior'),
                        ('OB',   'Observation of Suspected Contraband'),
                        ('OI',   'Other Official Information'),
                        ('SM',   'Suspicious Movement'),
                        ('TIP',  'Informant Tip'),
                        ('WTNS', 'Witness Observation'))


class SearchBasis(models.Model):
    search_basis_id = models.IntegerField(primary_key=True)
    search = models.ForeignKey(Search)
    person = models.ForeignKey(Person)
    stop = models.ForeignKey(Stop)
    basis = models.CharField(max_length=4, choices=SEARCH_BASIS_CHOICES)


class Agency(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
