# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20170930_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='AddrID',
            new_name='addr_id',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='userID',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='userID',
            new_name='user_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='isActivated',
        ),
        migrations.AddField(
            model_name='user',
            name='is_activated',
            field=models.CharField(choices=[('AC', 'Active'), ('CL', 'Closed'), ('WT', 'Waiting')], default='WT', max_length=2),
        ),
    ]
