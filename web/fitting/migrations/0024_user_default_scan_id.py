# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0023_auto_20170301_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='default_scan_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
