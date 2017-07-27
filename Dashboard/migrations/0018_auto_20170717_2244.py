# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-07-18 02:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dashboard', '0017_auto_20170717_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='change',
            name='work_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='change',
            name='work_done_stamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='change',
            name='work_done_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='work_done', to=settings.AUTH_USER_MODEL),
        ),
    ]
