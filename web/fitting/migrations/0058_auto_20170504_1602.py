# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0057_auto_20170504_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modeltype',
            name='model_type',
            field=models.CharField(default='Foot', max_length=64, unique=True),
        ),
    ]
