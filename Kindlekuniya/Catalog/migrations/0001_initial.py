# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-24 15:12
from __future__ import unicode_literals

import Catalog.models
import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='IndexGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('priority', models.CharField(choices=[('5', '5 (Highest)'), ('4', '4'), ('3', '3'), ('2', '2'), ('1', '1 (Lowest)')], default='1', max_length=1)),
                ('is_showing', models.CharField(choices=[('1', 'Yes'), ('0', 'No')], default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('isbn', models.DecimalField(decimal_places=0, max_digits=13, unique=True)),
                ('name', models.CharField(max_length=250)),
                ('author', models.CharField(max_length=250)),
                ('publisher', models.CharField(max_length=250)),
                ('price', models.FloatField()),
                ('weight', models.FloatField()),
                ('printing_type', models.CharField(choices=[('MN', 'Monochrome'), ('CL', 'Full CMY'), ('SN', 'Single Tone'), ('TT', 'Two Tone')], default='MN', max_length=2)),
                ('paper_type', models.CharField(choices=[('NS', 'Newsprint'), ('CP', 'Coated Paper'), ('UP', 'Uncoated Paper'), ('BP', 'Bond Paper'), ('GR', 'Green Read Paper')], default='CP', max_length=2)),
                ('cover_type', models.CharField(choices=[('PD', 'Paperback'), ('HC', 'Hardcover')], default='PD', max_length=2)),
                ('size_height', models.FloatField()),
                ('size_width', models.FloatField()),
                ('size_thickness', models.FloatField()),
                ('description', models.TextField(blank=True)),
                ('picture_url', models.ImageField(blank=True, null=True, upload_to=Catalog.models.get_product_image_path)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('catagory', models.ManyToManyField(to='Catalog.Catagory')),
            ],
        ),
        migrations.AddField(
            model_name='indexgroup',
            name='product',
            field=models.ManyToManyField(to='Catalog.Product'),
        ),
    ]
