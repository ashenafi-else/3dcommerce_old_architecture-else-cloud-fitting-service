# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 10:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0028_auto_20170315_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Last',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=64)),
                ('attachatment', models.FileField(upload_to='')),
                ('path', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size_type', models.CharField(choices=[('CUSTOM', 'Undefined type'), ('SHOESIZE', 'Shoe size')], default='CUSTOM', max_length=64)),
                ('value', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.Sizes'),
        ),
    ]