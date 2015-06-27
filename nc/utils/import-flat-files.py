import argparse
from collections import OrderedDict
import datetime
import os
import sys
import time

sys.path.append(os.path.abspath('.')) # require for imports below

from django.conf import settings
from django.utils.timezone import get_default_timezone, make_aware
from stops.models import Stop, Person, Search, Contraband, SearchBasis


RAW_DATA_DIR = os.path.join(settings.PROJECT_ROOT, 'raw-data')
logfn = os.path.join(RAW_DATA_DIR, 'import-log.txt')
tz = get_default_timezone()


def _date_converter(txt):
    return make_aware(datetime.datetime.strptime(txt, '%Y-%m-%d %H:%M:%S.%f'), tz)


def _float_converter(txt):
    try:
        return float(txt)
    except:
        return 0.


def log_error(class_type, row_index, txt):
    with file(logfn, 'a') as log:
        log.write('{ct} row {i} not saved: {txt}\n'.format(ct=class_type, i=row_index, txt=txt))


class StopConverter(object):

    django_class = Stop

    def __init__(self, txt, index):
        self.index = index
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
        try:
            obj = Stop(stop_id = int(self.raw["StopID"]),
                       agency_description = self.raw["AgencyDescription"],
                       date = _date_converter(self.raw["StopDate"]),
                       purpose = int(self.raw["Purpose"]),
                       action = int(self.raw["Action"]),
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
        except:
            log_error("Stop", self.index, "")
            return None


class PersonConverter(object):

    django_class = Person

    def __init__(self, txt, index):
        self.index = index
        self.raw = OrderedDict([("PersonID", txt[0:12].strip()),
                                ("StopID", txt[12:24].strip()),
                                ("Type", txt[24:25].strip()),
                                ("Age", txt[25:30].strip()),
                                ("Gender", txt[30:31].strip()),
                                ("Ethnicity", txt[31:32].strip()),
                                ("Race", txt[32:33].strip())])

    def get_django_object(self):
        try:
            obj = Person(person_id = int(self.raw["PersonID"]),
                         stop = Stop.objects.get(pk=int(self.raw["StopID"])),
                         type = self.raw["Type"],
                         age = self.raw["Age"],
                         gender = self.raw["Gender"],
                         ethnicity = self.raw["Ethnicity"],
                         race = self.raw["Race"])
            return obj
        except:
            log_error("Person", self.index,
                      "stop_id = {s}".format(s=self.raw["StopID"]))
            return None


class SearchConverter(object):

    django_class = Search

    def __init__(self, txt, index):
        self.index = index
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
        try:
            obj = Search(search_id = int(self.raw["SearchID"]),
                         stop= Stop.objects.get(pk=int(self.raw["StopID"])),
                         person= Person.objects.get(pk=int(self.raw["PersonID"])),
                         type = self.raw["Type"],
                         vehicle_search=bool(int(self.raw["VehicleSearch"])),
                         driver_search=bool(int(self.raw["DriverSearch"])),
                         passenger_search=bool(int(self.raw["PassengerSearch"])),
                         property_search=bool(int(self.raw["PropertySearch"])),
                         vehicle_siezed=bool(int(self.raw["VehicleSeized"])),
                         personal_property_siezed=bool(int(self.raw["PersonalPropertySeized"])),
                         other_property_sized=bool(int(self.raw["OtherPropertySeized"])))
            return obj
        except:
            log_error("Search", self.index,
                      "stop_id = {s}, person_id={p}".format(s=self.raw["StopID"],
                                                            p=self.raw["PersonID"]))
            return None


class ContrabandConverter(object):

    django_class = Contraband

    def __init__(self, txt, index):
        self.index = index
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
        try:
            obj = Contraband(contraband_id=self.raw["ContrabandID"],
                             search=Search.objects.get(pk=self.raw["SearchID"]),
                             person=Person.objects.get(pk=self.raw["PersonID"]),
                             stop=Stop.objects.get(pk=self.raw["StopID"]),
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
        except:
            log_error("Contraband", self.index,
                      "stop_id = {s}, search_id={se}, person_id={p}".format(s=self.raw["StopID"],
                                                                            se=self.raw["SearchID"],
                                                                            p=self.raw["PersonID"]))
            return None


class SearchBasisConverter(object):

    django_class = SearchBasis

    def __init__(self, txt, index):
        self.index = index
        self.raw = OrderedDict([("SearchBasisID", txt[0:12].strip()),
                                ("SearchID", txt[12:24].strip()),
                                ("PersonID", txt[24:36].strip()),
                                ("StopID", txt[36:48].strip()),
                                ("Basis", txt[48:58].strip())])

    def get_django_object(self):
        try:
            obj = SearchBasis(search_basis_id=self.raw["SearchBasisID"],
                              search=Search.objects.get(pk=self.raw["SearchID"]),
                              person=Person.objects.get(pk=self.raw["PersonID"]),
                              stop=Stop.objects.get(pk=self.raw["StopID"]),
                              basis=self.raw["Basis"])
            return obj
        except:
            log_error("SearchBasis", self.index,
                      "stop_id = {s}, search_id={se}, person_id={p}".format(s=self.raw["StopID"],
                                                                            se=self.raw["SearchID"],
                                                                            p=self.raw["PersonID"]))
            return None


def load_files(fn, converter_class, start_line, number_lines, save_interval=10000):
    max_line = start_line+number_lines-1 #fencepost
    with open(fn, 'rb') as txtfile:
        objects = []
        start_time = time.time()
        for i, line in enumerate(txtfile):
            if i>max_line:
                break
            if i>=start_line:
                #encoding: SQL_Latin1_General_CP1_CI_AS
                conv = converter_class(line.decode('latin-1').encode('utf-8'), i)
                obj = conv.get_django_object()
                if obj:
                    objects.append(obj)
                if i>0 and i%save_interval==0:
                    converter_class.django_class.objects.bulk_create(objects)
                    elapsed_time = time.time() - start_time
                    print "Saved rows {i} ({s:.2f} records/sec)".format(i=i, s=len(objects)/elapsed_time)
                    start_time = time.time()
                    objects = []

    # save final objects at the end of the loop
    converter_class.django_class.objects.bulk_create(objects)
    print 'Objects {s} to {e} successfully loaded'.format(s=start_line, e=i-1)


def main():

    parser = argparse.ArgumentParser(description='Import flat files into database.')
    parser.add_argument("file_type", help="st = stop, pe = person, se=search, cb = contraband, sb = search basis",
                        type=str)
    parser.add_argument("start_line", help="Start row for import", type=int)
    parser.add_argument("number_lines", help="Number of lines for import", type=int)
    parser.add_argument("-lps", help="Number of save in django", type=int, default=10000)
    args = parser.parse_args()

    if args.file_type=="st":
        fn = os.path.join(RAW_DATA_DIR, 'STOP.txt')
        conv = StopConverter
    elif args.file_type=="pe":
        fn = os.path.join(RAW_DATA_DIR, 'PERSON.txt')
        conv = PersonConverter
    elif args.file_type=="se":
        fn = os.path.join(RAW_DATA_DIR, 'SEARCH.txt')
        conv = SearchConverter
    elif args.file_type=="cb":
        fn = os.path.join(RAW_DATA_DIR, 'CONTRABAND.txt')
        conv = ContrabandConverter
    elif args.file_type=="sb":
        fn = os.path.join(RAW_DATA_DIR, 'SEARCHBASIS.txt')
        conv = SearchBasisConverter
    else:
        print 'Unknown file-type specified for import'
        return

    with file(logfn, 'a') as log:
        now = datetime.datetime.now().strftime("%A, %b %d %Y at %I:%m %p")
        log.write('Import log notes on {now}\n'.format(now=now))
        log.write('File Type: {ft} | Start Line: {sl} | Number Lines: {nl}\n'.format(ft=args.file_type,
                                                                                     sl=args.start_line,
                                                                                     nl=args.number_lines))

    load_files(fn, conv, args.start_line, args.number_lines, args.lps)


if __name__ == "__main__":
    main()
