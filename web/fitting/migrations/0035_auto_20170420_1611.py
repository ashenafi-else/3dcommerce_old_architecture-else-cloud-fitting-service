# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-20 16:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0034_auto_20170420_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='scan_id',
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='user_id',
        ),
        migrations.AddField(
            model_name='attribute',
            name='scan',
            field=models.IntegerField(default=1, verbose_name='Last'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attribute',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fitting.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='compareresult',
            name='last',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fitting.Last'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scan',
            name='attachment',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='compareresult',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='compareresult',
            name='scan_id',
        ),
        migrations.RemoveField(
            model_name='compareresult',
            name='shoe_id',
        ),
    ]