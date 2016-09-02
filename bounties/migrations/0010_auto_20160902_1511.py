# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0009_auto_20160902_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirate',
            name='wanted_status',
            field=models.IntegerField(choices=[(1, 'Dead or Alive'), (2, 'Only Alive')], default=1),
        ),
    ]
