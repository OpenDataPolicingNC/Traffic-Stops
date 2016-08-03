# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='census_profile_id',
            field=models.CharField(default='', blank=True, max_length=16),
        ),
    ]
