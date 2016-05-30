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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('state', models.CharField(choices=[('nc', 'North Carolina'), ('md', 'Maryland')], max_length=2)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_received', models.DateField()),
                ('url', models.URLField(unique=True, verbose_name='URL')),
                ('destination', models.CharField(blank=True, max_length=1024, help_text='Absolute path to destination directory (helpful for testing)')),
            ],
        ),
        migrations.CreateModel(
            name='Import',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
                ('date_finished', models.DateTimeField(null=True)),
                ('successful', models.BooleanField(default=False)),
                ('dataset', models.ForeignKey(to='tsdata.Dataset')),
            ],
        ),
    ]
