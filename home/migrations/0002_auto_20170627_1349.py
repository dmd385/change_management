# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2017-06-27 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('town', models.CharField(max_length=30)),
                ('zipCode', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=2)),
                ('phone', models.CharField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='company',
            name='state',
        ),
        migrations.RemoveField(
            model_name='company',
            name='street',
        ),
        migrations.RemoveField(
            model_name='company',
            name='town',
        ),
        migrations.RemoveField(
            model_name='company',
            name='zipCode',
        ),
        migrations.AddField(
            model_name='company',
            name='locations',
            field=models.ForeignKey(default=14586, on_delete=django.db.models.deletion.CASCADE, to='home.Location'),
            preserve_default=False,
        ),
    ]
