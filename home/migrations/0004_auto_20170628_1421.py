# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-28 18:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170628_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.Company'),
        ),
    ]
