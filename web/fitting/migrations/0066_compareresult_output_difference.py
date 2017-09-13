# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-13 12:50
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0065_product_brand_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='compareresult',
            name='output_difference',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
