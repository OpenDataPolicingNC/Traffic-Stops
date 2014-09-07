# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_agencies(apps, schema_editor):
    "Select distinct agencies from Stop table and populate Agency table"
    Agency = apps.get_model("stops", "Agency")
    Stop = apps.get_model("stops", "Stop")
    agencies = Stop.objects.values_list("agency_description", flat=True).order_by('agency_description').distinct()
    for agency in agencies:
        Agency.objects.create(name=agency)
    # match up agencies
    for agency in Agency.objects.all():
        Stop.objects.filter(agency_description=agency.name).update(agency=agency)


def backwards(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('stops', '0002_stop_agency'),
    ]

    operations = [
        migrations.RunPython(add_agencies, backwards),
    ]
