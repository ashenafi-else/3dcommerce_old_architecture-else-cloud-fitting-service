# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 18:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0061_auto_20170508_1149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanattribute',
            name='user',
        ),
    ]
