# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-25 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_user_reg_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='reg_admin',
        ),
    ]
