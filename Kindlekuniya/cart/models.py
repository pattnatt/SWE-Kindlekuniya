from django.db import models

class Product(models.Model):

    isbn = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.IntegerField()
    weight = models.IntegerField()
    isMonocrome = models.BinaryField()
    paperType = models.CharField(max_length=30)
    coverType = models.CharField(max_length=30)
    page = models.IntegerField()
    size = models.CharField(max_length=30)
    discription = models.CharField(max_length=240)
    pictureUrl = models.URLField()

    def __str__(self):
        return self.name


class Stock(models.Model):

    quantity = models.IntegerField()
    product = models.OneToOneField(Product)
    
        
        
