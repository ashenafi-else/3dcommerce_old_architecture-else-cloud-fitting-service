# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-21 15:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0045_auto_20170421_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_scans',
            field=models.ManyToManyField(related_name='default_scans', to='fitting.Scan'),
        ),
    ]