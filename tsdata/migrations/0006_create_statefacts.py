# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


STATE_KEYS = (settings.IL_KEY, settings.MD_KEY, settings.NC_KEY)


def create_state_facts(apps, schema_editor):
    StateFacts = apps.get_model('tsdata', 'StateFacts')
    TopAgencyFacts = apps.get_model('tsdata', 'TopAgencyFacts')
    for state_key in STATE_KEYS:
        state_facts, _ = StateFacts.objects.get_or_create(
            state_key=state_key
        )
        for rank in range(1, 6):
            TopAgencyFacts.objects.get_or_create(
                state_facts=state_facts, rank=rank
            )


def delete_state_facts(apps, schema_editor):
    StateFacts = apps.get_model('tsdata', 'StateFacts')
    for state_key in STATE_KEYS:
        StateFacts.objects.filter(state_key=state_key).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tsdata', '0005_auto_20170314_1359'),
    ]

    operations = [
        migrations.RunPython(create_state_facts, delete_state_facts),
    ]
