# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-17 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0014_auto_20170716_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='change',
            name='act_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='change',
            name='est_time',
            field=models.IntegerField(null=True),
        ),
    ]