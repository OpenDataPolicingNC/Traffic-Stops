# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0004_auto_20160711_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='census_profile_id',
            field=models.CharField(blank=True, max_length=16, default=''),
        ),
    ]
