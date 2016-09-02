# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0007_pirate_wanted_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirate',
            name='wanted_status',
            field=models.IntegerField(default=1, choices=[(1, 'Dead or Alive'), (2, 'Only Alive')]),
        ),
    ]
