# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


from django.utils.text import slugify


def gen_slug(apps, schema_editor):
    Agency = apps.get_model('nc', 'Agency')
    for agency in Agency.objects.all():
        agency.slug = slugify(agency.name)
        agency.save()


class Migration(migrations.Migration):

    dependencies = [
        ('nc', '0002_agency_slug'),
    ]

    operations = [
        migrations.RunPython(gen_slug, migrations.RunPython.noop)
    ]
