# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stop'
        db.create_table(u'stops_stop', (
            ('stop_id', self.gf('django.db.models.fields.PositiveIntegerField')(primary_key=True)),
            ('agency_description', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('purpose', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('action', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('driver_arrest', self.gf('django.db.models.fields.BooleanField')()),
            ('passenger_arrest', self.gf('django.db.models.fields.BooleanField')()),
            ('encounter_force', self.gf('django.db.models.fields.BooleanField')()),
            ('engage_force', self.gf('django.db.models.fields.BooleanField')()),
            ('officer_injury', self.gf('django.db.models.fields.BooleanField')()),
            ('driver_injury', self.gf('django.db.models.fields.BooleanField')()),
            ('passenger_injury', self.gf('django.db.models.fields.BooleanField')()),
            ('officer_id', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('stop_location', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('stop_city', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'stops', ['Stop'])

        # Adding model 'Person'
        db.create_table(u'stops_person', (
            ('person_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('age', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('ethnicity', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'stops', ['Person'])

        # Adding model 'Search'
        db.create_table(u'stops_search', (
            ('search_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Person'])),
            ('type', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('vehicle_search', self.gf('django.db.models.fields.BooleanField')()),
            ('driver_search', self.gf('django.db.models.fields.BooleanField')()),
            ('passenger_search', self.gf('django.db.models.fields.BooleanField')()),
            ('property_search', self.gf('django.db.models.fields.BooleanField')()),
            ('vehicle_siezed', self.gf('django.db.models.fields.BooleanField')()),
            ('personal_property_siezed', self.gf('django.db.models.fields.BooleanField')()),
            ('other_property_sized', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'stops', ['Search'])

        # Adding model 'Contraband'
        db.create_table(u'stops_contraband', (
            ('contraband_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Search'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Person'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('ounces', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('pounds', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('pints', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('gallons', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('dosages', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('grams', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('kilos', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('money', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('weapons', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
            ('dollar_amount', self.gf('django.db.models.fields.FloatField')(default=0, null=True)),
        ))
        db.send_create_signal(u'stops', ['Contraband'])

        # Adding model 'SearchBasis'
        db.create_table(u'stops_searchbasis', (
            ('search_basis_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Search'])),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Person'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stops.Stop'])),
            ('basis', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal(u'stops', ['SearchBasis'])


    def backwards(self, orm):
        # Deleting model 'Stop'
        db.delete_table(u'stops_stop')

        # Deleting model 'Person'
        db.delete_table(u'stops_person')

        # Deleting model 'Search'
        db.delete_table(u'stops_search')

        # Deleting model 'Contraband'
        db.delete_table(u'stops_contraband')

        # Deleting model 'SearchBasis'
        db.delete_table(u'stops_searchbasis')


    models = {
        u'stops.contraband': {
            'Meta': {'object_name': 'Contraband'},
            'contraband_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'dollar_amount': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'dosages': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'gallons': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'grams': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'kilos': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'ounces': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Person']"}),
            'pints': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'pounds': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Search']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stops.Stop']"}),
            'weapons': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True'})
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