# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0031_auto_20170420_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='last',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.Size'),
        ),
    ]
