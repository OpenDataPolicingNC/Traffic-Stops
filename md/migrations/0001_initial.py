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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Agencies',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('location_text', models.CharField(max_length=1024)),
                ('agency_description', models.CharField(max_length=100)),
                ('stop_date', models.DateTimeField()),
                ('gender', models.CharField(choices=[('m', 'Male'), ('f', 'Female')], max_length=2, blank=True)),
                ('dob', models.DateField()),
                ('race', models.CharField(choices=[('h', 'Hispanic'), ('a', 'Asian'), ('w', 'White'), ('b', 'Black'), ('u', 'Unknown'), ('o', 'Other')], max_length=1, blank=True)),
                ('residence_county', models.CharField(max_length=100)),
                ('residence_state', models.CharField(choices=[('i', 'In'), ('o', 'Out')], max_length=1, blank=True)),
                ('registration_state', models.CharField(choices=[('i', 'In'), ('o', 'Out')], max_length=1, blank=True)),
                ('stop_reason', models.CharField(max_length=64)),
                ('search_type', models.CharField(choices=[('both', 'Both'), ('prop', 'Property'), ('pers', 'Person')], max_length=4, blank=True)),
                ('search_reason', models.CharField(choices=[('incarrest', 'incarrest'), ('cons', 'cons'), ('other', 'other'), ('prob', 'prob'), ('k9', 'k9'), ('exigent', 'exigent')], max_length=16, blank=True)),
                ('disposition', models.CharField(choices=[('contra', 'Contraband'), ('both', 'Both'), ('prop', 'Property')], max_length=8, blank=True)),
                ('outcome', models.CharField(choices=[('sero', 'sero'), ('warn', 'Warning'), ('cit', 'Citation'), ('arr', 'Arrest')], max_length=8, blank=True)),
                ('agency', models.ForeignKey(to='md.Agency', null=True, related_name='stops')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
