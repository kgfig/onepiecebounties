# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bounties', '0004_auto_20160829_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
    ]
