# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitting', '0056_auto_20170504_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_type', models.CharField(choices=[('CUSTOM', 'Undefined type'), ('FOOT', 'Foot')], default='CUSTOM', max_length=64, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='scan',
            name='scan_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.ModelType'),
        ),
        migrations.AlterField(
            model_name='size',
            name='size_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitting.ModelType'),
        ),
        migrations.AddField(
            model_name='last',
            name='last_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='fitting.ModelType'),
            preserve_default=False,
        ),
    ]