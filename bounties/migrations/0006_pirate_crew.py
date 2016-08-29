# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0005_crew'),
    ]

    operations = [
        migrations.AddField(
            model_name='pirate',
            name='crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='bounties.Crew'),
        ),
    ]
