# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0004_auto_20161004_0743'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateFacts',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('state_key', models.CharField(max_length=2, unique=True, choices=[('nc', 'North Carolina'), ('md', 'Maryland'), ('il', 'Illinois')])),
                ('total_stops', models.PositiveIntegerField(default=0)),
                ('total_stops_millions', models.PositiveIntegerField(default=0)),
                ('total_searches', models.PositiveIntegerField(default=0)),
                ('total_agencies', models.PositiveIntegerField(default=0)),
                ('start_date', models.CharField(max_length=20, default='')),
                ('end_date', models.CharField(max_length=20, default='')),
            ],
            options={
                'verbose_name_plural': 'state facts',
            },
        ),
        migrations.CreateModel(
            name='TopAgencyFacts',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('rank', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('agency_id', models.PositiveIntegerField(default=0)),
                ('stops', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255, default='')),
                ('state_facts', models.ForeignKey(to='tsdata.StateFacts')),
            ],
            options={
                'ordering': ['state_facts__state_key', 'rank'],
                'verbose_name_plural': 'top agency facts',
            },
        ),
        migrations.AlterUniqueTogether(
            name='topagencyfacts',
            unique_together=set([('state_facts', 'rank')]),
        ),
    ]
