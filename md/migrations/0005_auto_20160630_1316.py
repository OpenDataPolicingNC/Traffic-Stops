# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0004_auto_20160630_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(editable=False, populate_from='name', unique=True, blank=True),
        ),
    ]
