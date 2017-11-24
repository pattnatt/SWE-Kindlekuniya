# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-24 15:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('history', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferEntry',
            fields=[
                ('entry_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Total Transfer')),
                ('transfer_date', models.DateTimeField(verbose_name='Transfer Date')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='history.HistEntry')),
                ('owner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
