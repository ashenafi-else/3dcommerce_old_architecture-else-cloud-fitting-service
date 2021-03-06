# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0006_auto_20170203_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.AlterField(
            model_name='scan',
            name='original_left_foot_path',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='scan',
            name='original_right_foot_path',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='scan',
            name='path_left_foot_in_fitting_service',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='scan',
            name='path_right_foot_in_fitting_service',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='path',
            field=models.CharField(max_length=1000, unique=True),
        ),
        migrations.AlterField(
            model_name='shoe',
            name='path_in_fitting_service',
            field=models.CharField(max_length=1000),
        ),
    ]
