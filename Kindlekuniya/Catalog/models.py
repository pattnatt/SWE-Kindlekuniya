from django.db import models
from datetime import datetime
import os

def get_product_image_path(instance, filename):
    return os.path.join('product_image', str(instance.id), filename)

class Catagory(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)

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
        ('MN', 'Monocrome'),
        ('CL', 'Colorized'),
    )

    isbn = models.DecimalField(max_digits = 13, decimal_places = 0, unique = True)
    name = models.CharField(max_length = 250)
    author = models.CharField(max_length = 250)
    catagory = models.ManyToManyField(Catagory)
    publisher = models.CharField(max_length = 250)
    price = models.FloatField()
    weight = models.FloatField()
    printingType = models.CharField(max_length = 2, choices=PRINTING_TYPE)
    paperType = models.CharField(max_length = 2, choices=PAPER_TYPE)
    coverType = models.CharField(max_length = 2, choices=COVER_TYPE)
    size_height = models.FloatField()
    size_width = models.FloatField()
    size_thickness = models.FloatField()
    description = models.TextField(blank = True)
    pictureUrl = models.ImageField(upload_to = get_product_image_path, blank = True, null = True)
    quantity = models.PositiveIntegerField(default = 0)
    created_at = models.DateTimeField(default = datetime.now, blank = True)

    def __str__(self):
        return self.name
