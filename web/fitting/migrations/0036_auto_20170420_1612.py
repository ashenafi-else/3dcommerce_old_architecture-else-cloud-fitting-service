# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 16:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0035_auto_20170420_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='compareresult',
            name='scan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fitting.Scan'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='compareresult',
            unique_together=set([('last', 'scan')]),
        ),
    ]