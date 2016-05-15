# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('state', models.CharField(max_length=2, choices=[('nc', 'North Carolina'), ('md', 'Maryland')])),
                ('name', models.CharField(max_length=255, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('url', models.URLField(unique=True, verbose_name='URL')),
                ('destination', models.CharField(help_text='Optional destination abs. path', max_length=1024, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('date_finished', models.DateTimeField(null=True)),
                ('successful', models.BooleanField(default=False)),
                ('dataset', models.ForeignKey(to='tsdata.Dataset')),
            ],
        ),
    ]
