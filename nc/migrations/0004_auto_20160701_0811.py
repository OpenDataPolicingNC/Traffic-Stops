# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('nc', '0003_auto_20160630_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(unique=True, populate_from='name', blank=True, editable=False),
        ),
    ]
