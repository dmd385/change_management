# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-17 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0015_auto_20170717_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='work_date',
            field=models.DateTimeField(null=True),
        ),
    ]
