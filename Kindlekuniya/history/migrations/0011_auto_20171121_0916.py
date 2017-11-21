# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-21 02:16
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0010_auto_20171121_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histentry',
            name='order_id',
            field=models.UUIDField(default=uuid.UUID('e2a061e4-99ef-4193-b216-93c32d77c00c'), editable=False, primary_key=True, serialize=False, verbose_name='Order ID'),
        ),
    ]