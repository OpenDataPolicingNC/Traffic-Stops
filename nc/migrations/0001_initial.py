# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import caching.base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Agencies',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Contraband',
            fields=[
                ('contraband_id', models.IntegerField(primary_key=True, serialize=False)),
                ('ounces', models.FloatField(null=True, default=0)),
                ('pounds', models.FloatField(null=True, default=0)),
                ('pints', models.FloatField(null=True, default=0)),
                ('gallons', models.FloatField(null=True, default=0)),
                ('dosages', models.FloatField(null=True, default=0)),
                ('grams', models.FloatField(null=True, default=0)),
                ('kilos', models.FloatField(null=True, default=0)),
                ('money', models.FloatField(null=True, default=0)),
                ('weapons', models.FloatField(null=True, default=0)),
                ('dollar_amount', models.FloatField(null=True, default=0)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('D', 'Driver'), ('P', 'Passenger')], max_length=2)),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2)),
                ('ethnicity', models.CharField(choices=[('H', 'Hispanic'), ('N', 'Non-Hispanic')], max_length=2)),
                ('race', models.CharField(choices=[('A', 'Asian'), ('B', 'Black'), ('I', 'Native American'), ('U', 'Other'), ('W', 'White')], max_length=2)),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('search_id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Consent'), (2, 'Search Warrant'), (3, 'Probable Cause'), (4, 'Search Incident to Arrest'), (5, 'Protective Frisk')])),
                ('vehicle_search', models.BooleanField(default=False)),
                ('driver_search', models.BooleanField(default=False)),
                ('passenger_search', models.BooleanField(default=False)),
                ('property_search', models.BooleanField(default=False)),
                ('vehicle_siezed', models.BooleanField(default=False)),
                ('personal_property_siezed', models.BooleanField(default=False)),
                ('other_property_sized', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='nc.Person')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SearchBasis',
            fields=[
                ('search_basis_id', models.IntegerField(primary_key=True, serialize=False)),
                ('basis', models.CharField(choices=[('ER', 'Erratic/Suspicious Behavior'), ('OB', 'Observation of Suspected Contraband'), ('OI', 'Other Official Information'), ('SM', 'Suspicious Movement'), ('TIP', 'Informant Tip'), ('WTNS', 'Witness Observation')], max_length=4)),
                ('person', models.ForeignKey(to='nc.Person')),
                ('search', models.ForeignKey(to='nc.Search')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('agency_description', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('purpose', models.PositiveSmallIntegerField(choices=[(1, 'Speed Limit Violation'), (2, 'Stop Light/Sign Violation'), (3, 'Driving While Impaired'), (4, 'Safe Movement Violation'), (5, 'Vehicle Equipment Violation'), (6, 'Vehicle Regulatory Violation'), (7, 'Seat Belt Violation'), (8, 'Investigation'), (9, 'Other Motor Vehicle Violation'), (10, 'Checkpoint')])),
                ('action', models.PositiveSmallIntegerField(choices=[(1, 'Verbal Warning'), (2, 'Written Warning'), (3, 'Citation Issued'), (4, 'On-View Arrest'), (5, 'No Action Taken')])),
                ('driver_arrest', models.BooleanField(default=False)),
                ('passenger_arrest', models.BooleanField(default=False)),
                ('encounter_force', models.BooleanField(default=False)),
                ('engage_force', models.BooleanField(default=False)),
                ('officer_injury', models.BooleanField(default=False)),
                ('driver_injury', models.BooleanField(default=False)),
                ('passenger_injury', models.BooleanField(default=False)),
                ('officer_id', models.CharField(max_length=15)),
                ('stop_location', models.CharField(max_length=15)),
                ('stop_city', models.CharField(max_length=20)),
                ('agency', models.ForeignKey(null=True, to='nc.Agency', related_name='stops')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.AddField(
            model_name='searchbasis',
            name='stop',
            field=models.ForeignKey(to='nc.Stop'),
        ),
        migrations.AddField(
            model_name='search',
            name='stop',
            field=models.ForeignKey(to='nc.Stop'),
        ),
        migrations.AddField(
            model_name='person',
            name='stop',
            field=models.ForeignKey(to='nc.Stop'),
        ),
        migrations.AddField(
            model_name='contraband',
            name='person',
            field=models.ForeignKey(to='nc.Person'),
        ),
        migrations.AddField(
            model_name='contraband',
            name='search',
            field=models.ForeignKey(to='nc.Search'),
        ),
        migrations.AddField(
            model_name='contraband',
            name='stop',
            field=models.ForeignKey(to='nc.Stop'),
        ),
    ]
