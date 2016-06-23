# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stop',
            old_name='stop_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='stop',
            old_name='location_text',
            new_name='stop_location',
        ),
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
            name='registration_state',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='residence_county',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='residence_state',
        ),
        migrations.RemoveField(
            model_name='stop',
            name='search_type',
        ),
        migrations.AddField(
            model_name='stop',
            name='age',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stop',
            name='date_of_birth_text',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='duration_text',
            field=models.CharField(null=True, max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='ethnicity',
            field=models.CharField(choices=[('W', 'White'), ('B', 'Black'), ('H', 'Hispanic'), ('A', 'Asian'), ('I', 'Native American'), ('U', 'Unknown')], max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='officer_id',
            field=models.CharField(max_length=15, blank=True, default=None),
        ),
        migrations.AddField(
            model_name='stop',
            name='search_conducted',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='seized',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], max_length=1, blank=True),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_date_text',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_id',
            field=models.IntegerField(primary_key=True, serialize=False, default=1),
        ),
        migrations.AddField(
            model_name='stop',
            name='stop_time_text',
            field=models.CharField(max_length=20, blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='stop',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], max_length=1, blank=True),
        ),
        migrations.AlterField(
            model_name='stop',
            name='search_reason',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
