# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0002_auto_20160623_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from='name', null=True, blank=True, max_length=255),
        ),
    ]
