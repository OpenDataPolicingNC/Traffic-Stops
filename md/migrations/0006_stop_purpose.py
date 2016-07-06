# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('md', '0005_auto_20160630_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='purpose',
            field=models.PositiveSmallIntegerField(default=11, choices=[(0, 'Seat Belt Violation'), (1, 'Speed Limit Violation'), (2, 'Stop Light/Sign Violation'), (3, 'Driving While Impaired'), (4, 'Safe Movement Violation'), (5, 'Vehicle Equipment Violation'), (6, 'Vehicle Regulatory Violation'), (7, 'Investigation'), (8, 'Non-motor Vehicle Violations'), (9, 'Other Motor Vehicle Violation'), (10, 'Failure to remain at scene of accident'), (11, 'Unable to find statute/other')]),
        ),
    ]
