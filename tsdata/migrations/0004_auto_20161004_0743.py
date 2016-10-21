# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0003_auto_20160808_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='state',
            field=models.CharField(max_length=2, choices=[('nc', 'North Carolina'), ('md', 'Maryland'), ('il', 'Illinois')]),
        ),
    ]
