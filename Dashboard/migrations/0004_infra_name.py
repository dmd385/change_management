# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-11 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_auto_20170710_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='infra',
            name='name',
            field=models.CharField(default='default', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
