import os
import sys

RAW_DATA_DIR = '../raw-data'
sys.path.append(os.path.abspath('.'))

from collections import OrderedDict
from datetime import datetime

from django.conf import settings

from stops.models import Stop, Person, Search, Contraband, SearchBasis


def _date_converter(txt):
    return datetime.strptime(r'2000-01-03 20:35:00.000', '%Y-%m-%d %H:%M:%S.%f')

def _float_converter(txt):
    try:
        return float(txt)
    except:
        return 0.

class StopConverter(object):

    django_class = Stop

    def __init__(self, txt):
        self.raw = OrderedDict([("StopID", txt[0:12].strip()),
                                ("AgencyDescription", txt[12:112].strip()),
                                ("StopDate", txt[112:136].strip()),
                                ("Purpose", txt[136:141].strip()),
                                ("Action", txt[141:146].strip()),
                                ("DriverArrest", txt[146:149].strip()),
                                ("PassengerArrest", txt[149:152].strip()),
                                ("EncounterForce", txt[152:155].strip()),
                                ("EngageForce", txt[155:158].strip()),
                                ("OfficerInjury", txt[158:161].strip()),
                                ("DriverInjury", txt[161:164].strip()),
                                ("PassengerInjury", txt[164:167].strip()),
                                ("OfficerId", txt[167:177].strip()),
                                ("StopLocation", txt[177:192].strip()),
                                ("StopCity", txt[192:212].strip())])

    def get_django_object(self):
        obj = Stop(stop_id = self.raw["StopID"],
                   agency_description = self.raw["AgencyDescription"],
                   date = _date_converter(self.raw["StopDate"]),
                   purpose = self.raw["Purpose"],
                   action = self.raw["Action"],
                   driver_arrest = bool(int(self.raw["DriverArrest"])),
                   passenger_arrest = bool(int(self.raw["PassengerArrest"])),
                   encounter_force = bool(int(self.raw["EncounterForce"])),
                   engage_force = bool(int(self.raw["EngageForce"])),
                   officer_injury = bool(int(self.raw["OfficerInjury"])),
                   driver_injury = bool(int(self.raw["DriverInjury"])),
                   passenger_injury = bool(int(self.raw["PassengerInjury"])),
                   officer_id = self.raw["OfficerId"],
                   stop_location = self.raw["StopLocation"],
                   stop_city = self.raw["StopCity"])
        return obj


class PersonConverter(object):

    django_class = Person

    def __init__(self, txt):
        self.raw = OrderedDict([("PersonID", txt[0:12].strip()),
                                ("StopID", txt[12:24].strip()),
                                ("Type", txt[24:25].strip()),
                                ("Age", txt[25:30].strip()),
                                ("Gender", txt[30:31].strip()),
                                ("Ethnicity", txt[31:32].strip()),
                                ("Race", txt[32:33].strip())])

    def get_django_object(self):
        obj = Person(person_id = self.raw["PersonID"],
                     stop = Stop.objects.get(stop_id=self.raw["StopID"]),
                     type = self.raw["Type"],
                     age = self.raw["Age"],
                     gender = self.raw["Gender"],
                     ethnicity = self.raw["Ethnicity"],
                     race = self.raw["Race"])
        return obj


class SearchConverter(object):

    django_class = Search

    def __init__(self, txt):
        self.raw = OrderedDict([("SearchID", txt[0:12].strip()),
                                ("StopID", txt[12:24].strip()),
                                ("PersonID", txt[24:36].strip()),
                                ("Type", txt[36:41].strip()),
                                ("VehicleSearch", txt[41:44].strip()),
                                ("DriverSearch", txt[44:47].strip()),
                                ("PassengerSearch", txt[47:50].strip()),
                                ("PropertySearch", txt[50:53].strip()),
                                ("VehicleSeized", txt[53:56].strip()),
                                ("PersonalPropertySeized", txt[56:59].strip()),
                                ("OtherPropertySeized", txt[59:62].strip())])

    def get_django_object(self):
        obj = Search(search_id = self.raw["SearchID"],
                     stop = Stop.objects.get(stop_id=self.raw["StopID"]),
                     person = Stop.objects.get(stop_id=self.raw["PersonID"]),
                     type = self.raw["Type"],
                     vehicle_search=bool(int(self.raw["VehicleSearch"])),
                     driver_search=bool(int(self.raw["DriverSearch"])),
                     passenger_search=bool(int(self.raw["PassengerSearch"])),
                     property_search=bool(int(self.raw["PropertySearch"])),
                     vehicle_siezed=bool(int(self.raw["VehicleSeized"])),
                     personal_property_siezed=bool(int(self.raw["PersonalPropertySeized"])),
                     other_property_sized=bool(int(self.raw["OtherPropertySeized"])))
        return obj


class ContrabandConverter(object):

    django_class = Contraband

    def __init__(self, txt):
        self.raw = OrderedDict([("ContrabandID", txt[0:12].strip()),
                                ("SearchID", txt[12:24].strip()),
                                ("PersonID", txt[24:36].strip()),
                                ("StopID", txt[36:48].strip()),
                                ("Ounces", txt[48:89].strip()),
                                ("Pounds", txt[89:130].strip()),
                                ("Pints", txt[130:171].strip()),
                                ("Gallons", txt[171:212].strip()),
                                ("Dosages", txt[212:253].strip()),
                                ("Grams", txt[253:294].strip()),
                                ("Kilos", txt[294:335].strip()),
                                ("Money", txt[335:376].strip()),
                                ("Weapons", txt[376:417].strip()),
                                ("DollarAmt", txt[417:458].strip())])

    def get_django_object(self):
        obj = Contraband(contraband_id=self.raw["ContrabandID"],
                         search=Search.objects.get(search_id=self.raw["SearchID"]),
                         person=Person.objects.get(person_id=self.raw["PersonID"]),
                         stop=Stop.objects.get(stop_id=self.raw["StopID"]),
                         ounces=_float_converter(self.raw["Ounces"]),
                         pounds=_float_converter(self.raw["Pounds"]),
                         pints=_float_converter(self.raw["Pints"]),
                         gallons=_float_converter(self.raw["Gallons"]),
                         dosages=_float_converter(self.raw["Dosages"]),
                         grams=_float_converter(self.raw["Grams"]),
                         kilos=_float_converter(self.raw["Kilos"]),
                         money=_float_converter(self.raw["Money"]),
                         weapons=_float_converter(self.raw["Weapons"]),
                         dollar_amount=_float_converter(self.raw["DollarAmt"]))
        return obj


class SearchBasisConverter(object):

    django_class = SearchBasis

    def __init__(self, txt):
        self.raw = OrderedDict([("SearchBasisID", txt[0:12].strip()),
                                ("SearchID", txt[12:24].strip()),
                                ("PersonID", txt[24:36].strip()),
                                ("StopID", txt[36:48].strip()),
                                ("Basis", txt[48:58].strip())])

    def get_django_object(self):
        obj = SearchBasis(search_basis_id=self.raw["SearchBasisID"],
                          search=Search.objects.get(search_id=self.raw["SearchID"]),
                          person=Person.objects.get(person_id=self.raw["PersonID"]),
                          stop=Stop.objects.get(stop_id=self.raw["StopID"]),
                          basis=self.raw["Basis"])
        return obj


def load_files(fn, converter_class, save_interval=10000):
    with open(fn, 'rb') as txtfile:
        objects = []
        for i, line in enumerate(txtfile):
            conv = converter_class(line)
            objects.append(conv.get_django_object())
            if i%save_interval==0:
                print 'Saving rows {i}'.format(i=i)
                converter_class.django_class.objects.bulk_create(objects)
                objects = []

    # save final objects at the end of the loop
    converter_class.django_class.objects.bulk_create(objects)
    print 'Objects succesfully loaded'


def main():
    load_files(os.path.join(RAW_DATA_DIR, 'STOP.txt'), StopConverter)
    load_files(os.path.join(RAW_DATA_DIR, 'PERSON.txt'), PersonConverter)
    load_files(os.path.join(RAW_DATA_DIR, 'SEARCH.txt'), SearchConverter)
    load_files(os.path.join(RAW_DATA_DIR, 'CONTRABAND.txt'), ContrabandConverter)
    load_files(os.path.join(RAW_DATA_DIR, 'SEARCHBASIS.txt'), SearchBasisConverter)

if __name__ == "__main__":
    main()
