from django.db import models


class Stop(models.Model):
    stop_id = models.CharField(max_length=12)
    agency_description = models.CharField(max_length=100)
    date = models.DateTimeField()
    purpose = models.CharField(max_length=5)
    action = models.CharField(max_length=5)
    driver_arrest = models.BooleanField()
    passenger_arrest = models.BooleanField()
    encounter_force = models.BooleanField()
    engage_force = models.BooleanField()
    officer_injury = models.BooleanField()
    driver_injury = models.BooleanField()
    passenger_injury = models.BooleanField()
    officer_id = models.CharField(max_length=15) # todo: keys
    stop_location = models.CharField(max_length=15) #todo: keys
    stop_city = models.CharField(max_length=20)


PERSON_TYPE_CHOICES = (("Dr", "Driver"),
                       ("Pa", "Passenger"))

GENDER_CHOICES = (("M", "Male"),
                  ("F", "Female"))

ETHNICITY_CHOICES = ()

RACE_CHOICES = ()

class Person(models.Model):
    person_id = models.CharField(max_length=12)
    stop = models.ForeignKey(Stop)
    type = models.CharField(max_length=2, choices=PERSON_TYPE_CHOICES)
    age  = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    ethnicity = models.CharField(max_length=2, choices=ETHNICITY_CHOICES)
    race = models.CharField(max_length=2, choices=RACE_CHOICES)


SEARCH_TYPE_CHOICES = ()

class Search(models.Model):
    search_id = models.CharField(max_length=12)
    stop = models.ForeignKey(Stop)
    person = models.ForeignKey(Person)
    type = models.CharField(max_length=2, choices=SEARCH_TYPE_CHOICES)
    vehicle_search = models.BooleanField()
    driver_search = models.BooleanField()
    passenger_search = models.BooleanField()
    property_search = models.BooleanField()
    vehicle_siezed = models.BooleanField()
    personal_property_siezed = models.BooleanField()
    other_property_sized = models.BooleanField()


class Contraband(models.Model):
    contraband_id = models.CharField(max_length=12)
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


SEARCH_BASIS_CHOICES = ()

class SearchBasis(models.Model):
    search_basis_id = models.CharField(max_length=12)
    search = models.ForeignKey(Search)
    person = models.ForeignKey(Person)
    stop = models.ForeignKey(Stop)
    basis = models.CharField(max_length=2, choices=SEARCH_BASIS_CHOICES)
