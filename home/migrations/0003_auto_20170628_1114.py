# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-28 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20170627_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.Company'),
        ),
    ]