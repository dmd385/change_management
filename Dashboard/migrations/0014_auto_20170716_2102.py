# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-17 01:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dashboard', '0013_auto_20170716_2054'),
    ]

    operations = [
        migrations.AddField(
            model_name='change',
            name='close_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='change',
            name='close_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='change',
            name='customer_auth_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='change',
            name='internal_auth_date',
            field=models.DateTimeField(null=True),
        ),
    ]
