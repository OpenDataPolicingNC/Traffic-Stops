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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('census_profile_id', models.CharField(max_length=16, blank=True, default='')),
            ],
            options={
                'verbose_name_plural': 'Agencies',
            },
            bases=(caching.base.CachingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('stop_id', models.IntegerField(primary_key=True, serialize=False, default=1)),
                ('year', models.SmallIntegerField()),
                ('purpose', models.PositiveSmallIntegerField(choices=[(1, 'Moving Violation'), (2, 'Equipment'), (3, 'Registration'), (11, 'Unknown')], default=11)),
                ('search_conducted', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Unknown')])),
                ('seized', models.CharField(max_length=1, choices=[('Y', 'Yes'), ('N', 'No'), ('U', 'Unknown')])),
                ('gender', models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')])),
                ('ethnicity', models.CharField(max_length=20, choices=[('W', 'White'), ('B', 'Black'), ('H', 'Hispanic'), ('U', 'Unknown')])),
                ('agency_description', models.CharField(max_length=100)),
                ('agency', models.ForeignKey(null=True, to='il.Agency', related_name='stops')),
            ],
            bases=(caching.base.CachingMixin, models.Model),
        ),
    ]
