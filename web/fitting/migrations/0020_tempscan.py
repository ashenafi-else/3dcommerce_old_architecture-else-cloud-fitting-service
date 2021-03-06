# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 16:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0019_auto_20170228_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempScan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scan_id', models.CharField(max_length=256)),
                ('user_id', models.IntegerField()),
                ('original_left_foot_path', models.CharField(max_length=1000)),
                ('path_left_foot_in_fitting_service', models.CharField(max_length=1000)),
                ('original_right_foot_path', models.CharField(max_length=1000)),
                ('path_right_foot_in_fitting_service', models.CharField(max_length=1000)),
                ('scanner', models.CharField(max_length=256)),
                ('type', models.CharField(max_length=100)),
                ('created_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
