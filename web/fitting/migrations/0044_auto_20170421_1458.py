# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0043_auto_20170420_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='default_scan',
        ),
        migrations.AddField(
            model_name='user',
            name='default_scans',
            field=models.ManyToManyField(blank=True, null=True, related_name='default_scan', to='fitting.Scan'),
        ),
    ]
