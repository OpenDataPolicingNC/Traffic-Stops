# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stop',
            name='disposition',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='id',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='outcome',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='race',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='residence_county',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='search_type',
        ),
        migrations.AddField(
            model_name='stop',
            name='county',
            field=models.CharField(max_length=25, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='crime_charged',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='date_of_birth_text',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='duration_text',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='ethnicity',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='officer_id',
            field=models.IntegerField(default=None, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='search_conducted',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='seized',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_date_text',
            field=models.CharField(default='', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_id',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_outcome',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_time_text',
            field=models.CharField(default='', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='what_searched',
            field=models.CharField(max_length=64, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=6, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='registration_state',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='stop',
            name='residence_state',
            field=models.CharField(max_length=3, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='search_reason',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
