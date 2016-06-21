# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0002_auto_20160620_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stop',
            old_name='stop_date',
            new_name='date',
        ),
    ]
