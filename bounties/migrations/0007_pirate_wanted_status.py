# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0006_pirate_crew'),
    ]

    operations = [
        migrations.AddField(
            model_name='pirate',
            name='wanted_status',
            field=models.CharField(default='DOA', choices=[('DOA', 'Dead or Alive'), ('OA', 'Only Alive')], max_length=16),
        ),
    ]
