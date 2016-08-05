# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0002_censusprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censusprofile',
            name='geography',
            field=models.CharField(max_length=16, choices=[('county', 'County'), ('place', 'Place')]),
        ),
    ]
