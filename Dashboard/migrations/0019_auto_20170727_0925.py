# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-27 13:25
from __future__ import unicode_literals

import Dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0018_auto_20170717_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='quote',
            field=models.FileField(null=True, upload_to=Dashboard.models.user_directory_path),
        ),
    ]
