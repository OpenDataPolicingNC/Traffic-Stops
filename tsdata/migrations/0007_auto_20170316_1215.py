# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0006_create_statefacts'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='report_email_1',
            field=models.EmailField(max_length=254, blank=True),
        ),
        migrations.AddField(
            model_name='dataset',
            name='report_email_2',
            field=models.EmailField(max_length=254, blank=True),
        ),
    ]
