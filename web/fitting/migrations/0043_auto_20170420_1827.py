# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 18:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0042_auto_20170420_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='compareresult',
            name='compare_mode',
            field=models.CharField(choices=[('3D', '3d'), ('METRICS', 'metrics')], default='3D', max_length=64),
        ),
        migrations.AddField(
            model_name='compareresult',
            name='compare_type',
            field=models.CharField(choices=[('SCAN', 'scan'), ('FITTING', 'fitting')], default='FITTING', max_length=64),
        ),
    ]
