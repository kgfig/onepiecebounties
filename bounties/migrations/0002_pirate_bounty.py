# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pirate',
            name='bounty',
            field=models.IntegerField(default=None, max_length=50),
        ),
    ]
