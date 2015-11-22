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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('location_text', models.CharField(max_length=1024)),
                ('agency_description', models.CharField(max_length=100)),
                ('stop_date', models.DateTimeField()),
                ('gender', models.CharField(max_length=2, choices=[('m', 'Male'), ('f', 'Female')], blank=True)),
                ('dob', models.DateField(null=True)),
                ('race', models.CharField(max_length=1, choices=[('h', 'Hispanic'), ('a', 'Asian'), ('w', 'White'), ('b', 'Black'), ('u', 'Unknown'), ('o', 'Other')], blank=True)),
                ('residence_county', models.CharField(max_length=100)),
                ('residence_state', models.CharField(max_length=1, choices=[('i', 'In'), ('o', 'Out')], blank=True)),
                ('registration_state', models.CharField(max_length=1, choices=[('i', 'In'), ('o', 'Out')], blank=True)),
                ('stop_reason', models.CharField(max_length=64)),
                ('search_type', models.CharField(max_length=4, choices=[('both', 'Both'), ('prop', 'Property'), ('pers', 'Person')], blank=True)),
                ('search_reason', models.CharField(max_length=16, choices=[('incarrest', 'incarrest'), ('cons', 'cons'), ('other', 'other'), ('prob', 'prob'), ('k9', 'k9'), ('exigent', 'exigent')], blank=True)),
                ('disposition', models.CharField(max_length=8, choices=[('contra', 'Contraband'), ('both', 'Both'), ('prop', 'Property')], blank=True)),
                ('outcome', models.CharField(max_length=8, choices=[('sero', 'sero'), ('warn', 'Warning'), ('cit', 'Citation'), ('arr', 'Arrest')], blank=True)),
                ('agency', models.ForeignKey(related_name='stops', to='md.Agency', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
