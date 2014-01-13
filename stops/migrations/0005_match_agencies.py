# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for agency in orm.Agency.objects.all():
            orm.Stop.objects.filter(agency_description=agency.name).update(agency=agency)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'stops.agency': {
            'Meta': {'object_name': 'Agency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'stops.contraband': {
            'Meta': {'object_name': 'Contraband'},
            'contraband_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'dollar_amount': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'dosages': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'gallons': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'grams': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'kilos': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'money': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'ounces': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Person']"}),
            'pints': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'pounds': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Search']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"}),
            'weapons': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'stops.person': {
            'Meta': {'object_name': 'Person'},
            'age': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'person_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'stops.search': {
            'Meta': {'object_name': 'Search'},
            'driver_search': ('django.db.models.fields.BooleanField', [], {}),
            'other_property_sized': ('django.db.models.fields.BooleanField', [], {}),
            'passenger_search': ('django.db.models.fields.BooleanField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Person']"}),
            'personal_property_siezed': ('django.db.models.fields.BooleanField', [], {}),
            'property_search': ('django.db.models.fields.BooleanField', [], {}),
            'search_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'vehicle_search': ('django.db.models.fields.BooleanField', [], {}),
            'vehicle_siezed': ('django.db.models.fields.BooleanField', [], {})
        },
        u'stops.searchbasis': {
            'Meta': {'object_name': 'SearchBasis'},
            'basis': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Person']"}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Search']"}),
            'search_basis_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"})
        },
        u'stops.stop': {
            'Meta': {'object_name': 'Stop'},
            'action': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'agency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Agency']", 'null': 'True'}),
            'agency_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'driver_arrest': ('django.db.models.fields.BooleanField', [], {}),
            'driver_injury': ('django.db.models.fields.BooleanField', [], {}),
            'encounter_force': ('django.db.models.fields.BooleanField', [], {}),
            'engage_force': ('django.db.models.fields.BooleanField', [], {}),
            'officer_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'officer_injury': ('django.db.models.fields.BooleanField', [], {}),
            'passenger_arrest': ('django.db.models.fields.BooleanField', [], {}),
            'passenger_injury': ('django.db.models.fields.BooleanField', [], {}),
            'purpose': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'stop_city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stop_id': ('django.db.models.fields.PositiveIntegerField', [], {'primary_key': 'True'}),
            'stop_location': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        }
    }

    complete_apps = ['stops']
    symmetrical = True
