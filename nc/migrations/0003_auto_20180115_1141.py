# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nc', '0002_agency_census_profile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stop',
            name='date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
