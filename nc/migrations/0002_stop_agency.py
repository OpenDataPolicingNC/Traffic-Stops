# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stop',
            name='agency',
            field=models.ForeignKey(to='nc.Agency', related_name='stops', null=True),
            preserve_default=True,
        ),
    ]
