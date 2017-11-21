from django.db import models
from datetime import datetime
import os
import uuid


def get_product_image_path(instance, filename):
    return os.path.join('product_image', str(instance.product_id), filename)


class Catagory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    COVER_TYPE = (
        ('PD', 'Paperback'),
        ('HC', 'Hardcover'),
    )

    PAPER_TYPE = (
        ('NS', 'Newsprint'),
        ('CP', 'Coated Paper'),
        ('UP', 'Uncoated Paper'),
        ('BP', 'Bond Paper'),
        ('GR', 'Green Read Paper'),
    )

    PRINTING_TYPE = (
        ('MN', 'Monochrome'),
        ('CL', 'Full CMY'),
        ('SN', 'Single Tone'),
        ('TT', 'Two Tone'),
    )

    product_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    isbn = models.DecimalField(max_digits=13, decimal_places=0, unique=True)
    name = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    catagory = models.ManyToManyField(Catagory)
    publisher = models.CharField(max_length=250)
    price = models.FloatField()
    weight = models.FloatField()
    printing_type = models.CharField(
        max_length=2,
        choices=PRINTING_TYPE,
        default='MN',
    )
    paper_type = models.CharField(
        max_length=2,
        choices=PAPER_TYPE,
        default='CP',
    )
    cover_type = models.CharField(
        max_length=2,
        choices=COVER_TYPE,
        default='PD',
    )
    size_height = models.FloatField()
    size_width = models.FloatField()
    size_thickness = models.FloatField()
    description = models.TextField(blank=True)
    picture_url = models.ImageField(
        upload_to=get_product_image_path,
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name

class IndexGroup(models.Model):
    SHOWING_BOOLEAN = (
        ('1', 'Yes'),
        ('0', 'No'),
    )

    PRIORITY = (
        ('5', '5 (Highest)'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1 (Lowest)'),
    )

    name = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    product = models.ManyToManyField(Product)
    priority = models.CharField(
        max_length = 1,
        choices = PRIORITY,
        default = '1',
    )
    is_showing = models.CharField(
        max_length = 1,
        choices = SHOWING_BOOLEAN,
        default = '1',
    )
