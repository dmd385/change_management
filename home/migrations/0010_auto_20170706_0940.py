# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-06 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20170706_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='locations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Location'),
        ),
    ]
