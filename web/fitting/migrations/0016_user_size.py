# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-15 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0015_auto_20170214_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='size',
            field=models.IntegerField(default=37),
        ),
    ]
