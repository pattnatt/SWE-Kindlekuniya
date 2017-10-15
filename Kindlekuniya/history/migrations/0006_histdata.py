# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-29 16:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0005_auto_20170929_0327'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderName', models.CharField(max_length=300)),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.HistEntry')),
            ],
        ),
    ]
