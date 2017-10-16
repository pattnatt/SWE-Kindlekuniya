# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 06:05
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Catalog', '0010_product_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='pictureUrl',
            new_name='picture_url',
        ),
        migrations.RemoveField(
            model_name='product',
            name='coverType',
        ),
        migrations.RemoveField(
            model_name='product',
            name='id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='isMonocrome',
        ),
        migrations.RemoveField(
            model_name='product',
            name='paperType',
        ),
        migrations.AddField(
            model_name='product',
            name='cover_type',
            field=models.CharField(choices=[('PD', 'Paperback'), ('HC', 'Hardcover')], default='PD', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='paper_type',
            field=models.CharField(choices=[('NS', 'Newsprint'), ('CP', 'Coated Paper'), ('UP', 'Uncoated Paper'), ('BP', 'Bond Paper'), ('GR', 'Green Read Paper')], default='CP', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='printing_type',
            field=models.CharField(choices=[('MN', 'Monochrome'), ('CL', 'Full CMY'), ('SN', 'Single Tone'), ('TT', 'Two Tone')], default='MN', max_length=2),
        ),
        migrations.AddField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]