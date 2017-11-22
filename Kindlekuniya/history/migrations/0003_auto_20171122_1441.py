# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-22 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0002_auto_20171120_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histentry',
            name='order_id',
            field=models.UUIDField(default=uuid.UUID('86e9160a-527e-4363-82f6-8117650babe0'), editable=False, primary_key=True, serialize=False, verbose_name='Order ID'),
        ),
    ]
