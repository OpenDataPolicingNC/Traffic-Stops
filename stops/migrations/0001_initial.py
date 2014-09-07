# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contraband',
            fields=[
                ('contraband_id', models.IntegerField(serialize=False, primary_key=True)),
                ('ounces', models.FloatField(default=0, null=True)),
                ('pounds', models.FloatField(default=0, null=True)),
                ('pints', models.FloatField(default=0, null=True)),
                ('gallons', models.FloatField(default=0, null=True)),
                ('dosages', models.FloatField(default=0, null=True)),
                ('grams', models.FloatField(default=0, null=True)),
                ('kilos', models.FloatField(default=0, null=True)),
                ('money', models.FloatField(default=0, null=True)),
                ('weapons', models.FloatField(default=0, null=True)),
                ('dollar_amount', models.FloatField(default=0, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('person_id', models.IntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(choices=[('Dr', 'Driver'), ('Pa', 'Passenger')], max_length=2)),
                ('age', models.PositiveSmallIntegerField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=2)),
                ('ethnicity', models.CharField(choices=[('H', 'Hispanic'), ('NH', 'Non-Hispanic')], max_length=2)),
                ('race', models.CharField(choices=[('A', 'Asian'), ('B', 'Black'), ('I', 'Native American'), ('U', 'Other/Unknown'), ('W', 'White')], max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('search_id', models.IntegerField(serialize=False, primary_key=True)),
                ('type', models.PositiveSmallIntegerField()),
                ('vehicle_search', models.BooleanField(default=False)),
                ('driver_search', models.BooleanField(default=False)),
                ('passenger_search', models.BooleanField(default=False)),
                ('property_search', models.BooleanField(default=False)),
                ('vehicle_siezed', models.BooleanField(default=False)),
                ('personal_property_siezed', models.BooleanField(default=False)),
                ('other_property_sized', models.BooleanField(default=False)),
                ('person', models.ForeignKey(to='stops.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SearchBasis',
            fields=[
                ('search_basis_id', models.IntegerField(serialize=False, primary_key=True)),
                ('basis', models.CharField(choices=[('ER', 'Erratic/Suspicious Behavior'), ('OB', 'Observation of Suspected Contraband'), ('OI', 'Other Official Information'), ('SM', 'Suspicious Movement'), ('TIP', 'Informant Tip'), ('WTNS', 'Witness Observation')], max_length=4)),
                ('person', models.ForeignKey(to='stops.Person')),
                ('search', models.ForeignKey(to='stops.Search')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.PositiveIntegerField(serialize=False, primary_key=True)),
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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='searchbasis',
            name='stop',
            field=models.ForeignKey(to='stops.Stop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='search',
            name='stop',
            field=models.ForeignKey(to='stops.Stop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='stop',
            field=models.ForeignKey(to='stops.Stop'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contraband',
            name='person',
            field=models.ForeignKey(to='stops.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contraband',
            name='search',
            field=models.ForeignKey(to='stops.Search'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contraband',
            name='stop',
            field=models.ForeignKey(to='stops.Stop'),
            preserve_default=True,
        ),
    ]
