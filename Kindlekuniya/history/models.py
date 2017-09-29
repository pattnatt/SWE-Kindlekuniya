from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone
# Create your models here.

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    date = models.DateTimeField('order date')
    def __str__(self):
        return self.orderID
    status = models.CharField(default="on hold",max_length=50)
    shipMethodID = models.IntegerField(default='0'); #change to ForeignKey
    payMethod = models.CharField(default="credit card",max_length=50); 
    trackingNo = models.CharField(max_length=20);
    
class OrderItem(models.Model):
    ordItemsID = models.AutoField(primary_key=True);
    orderId = models.ForeignKey(Order, on_delete = models.CASCADE);
    productID = models.IntegerField(); #change to ForeignKey
    quantity = models.IntegerField(default=1);
    sumPrice = models.IntegerField();
    tax = models.IntegerField();
    
