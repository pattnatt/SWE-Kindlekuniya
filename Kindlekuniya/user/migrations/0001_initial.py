# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-25 04:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(default=None, max_length=512)),
                ('city', models.CharField(default=None, max_length=128)),
                ('zipcode', models.CharField(default=None, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(default=None, max_length=120, unique=True)),
                ('firstname', models.CharField(default=None, max_length=120)),
                ('lastname', models.CharField(default=None, max_length=120)),
                ('is_activated', models.CharField(choices=[('AC', 'Active'), ('CL', 'Closed'), ('WT', 'Waiting')], default='WT', max_length=2)),
                ('reset_password', models.CharField(choices=[('RS', 'Reset'), ('CL', 'Closed')], default='CL', max_length=2)),
                ('password', models.CharField(default=None, max_length=512)),
                ('phone_number', models.CharField(default=None, max_length=10)),
                ('default_address', models.IntegerField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
