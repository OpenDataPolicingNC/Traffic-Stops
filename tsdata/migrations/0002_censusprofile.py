# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CensusProfile',
            fields=[
                ('id', models.CharField(serialize=False, verbose_name='ID', primary_key=True, max_length=16)),
                ('location', models.CharField(max_length=255)),
                ('geography', models.CharField(max_length=16)),
                ('state', models.CharField(max_length=2)),
                ('source', models.CharField(max_length=255)),
                ('white', models.PositiveIntegerField(default=0)),
                ('black', models.PositiveIntegerField(default=0)),
                ('native_american', models.PositiveIntegerField(default=0)),
                ('asian', models.PositiveIntegerField(default=0)),
                ('native_hawaiian', models.PositiveIntegerField(default=0)),
                ('other', models.PositiveIntegerField(default=0)),
                ('two_or_more_races', models.PositiveIntegerField(default=0)),
                ('hispanic', models.PositiveIntegerField(default=0)),
                ('non_hispanic', models.PositiveIntegerField(default=0)),
                ('total', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
