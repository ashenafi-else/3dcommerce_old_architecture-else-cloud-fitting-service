# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-08 11:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0059_auto_20170504_1634'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.RemoveField(
            model_name='last',
            name='size',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sizes',
        ),
    ]