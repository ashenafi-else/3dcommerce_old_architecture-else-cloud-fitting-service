# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0018_auto_20170228_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='base_url',
            field=models.CharField(default='https://else:7kjfWVWcRN@avatar3d.ibv.org:8443/webdav/ELSE/', max_length=1000),
        ),
    ]
