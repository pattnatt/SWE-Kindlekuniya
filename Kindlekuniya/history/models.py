from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
import os
# Create your models here.

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.IntegerField(default='0')
    date = models.DateTimeField('order date')
    def __str__(self):
        return str(self.orderID)
    status = models.CharField(default="on hold",max_length=50)
    shipMethodID = models.IntegerField(default=0); #change to ForeignKey
    payMethod = models.CharField(default="credit card",max_length=50); 
    trackingNo = models.CharField(max_length=20);
    
class OrderItem(models.Model):
    ordItemsID = models.AutoField(primary_key=True);
    orderID = models.ForeignKey(Order, on_delete = models.CASCADE);
    productID = models.IntegerField(); #change to ForeignKey
    quantity = models.IntegerField(default=1);
    sumPrice = models.IntegerField();
    tax = models.IntegerField();
    def __str__(self):
        return str(self.ordItemsID)
        

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
    id = models.AutoField(primary_key=True);
    isbn = models.DecimalField(max_digits = 13, decimal_places = 0, unique = True)
    name = models.CharField(max_length = 250)
    author = models.CharField(max_length = 250)
    catagory = models.ManyToManyField(Catagory)
    publisher = models.CharField(max_length = 250)
    price = models.FloatField()
    weight = models.FloatField()
    isMonocrome = models.BooleanField(default = True)
    paperType = models.CharField(max_length = 2, choices=PAPER_TYPE)
    coverType = models.CharField(max_length = 2, choices=COVER_TYPE)
    size_height = models.FloatField()
    size_width = models.FloatField()
    size_thickness = models.FloatField()
    description = models.TextField(blank = True)
    pictureUrl = models.ImageField(upload_to = get_product_image_path, blank = True, null = True)
    quantity = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return self.name

    def getAmount(self):
        return self.price * self.quantity
    
