# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0003_auto_20160829_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pirate',
            name='bounty',
            field=models.IntegerField(null=True),
        ),
    ]
