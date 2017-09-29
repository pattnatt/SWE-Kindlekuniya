from django.db import models

class Product(models.Model):

    quantity = models.IntegerField(default=1)
    isbn = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.IntegerField()
    weight = models.IntegerField()
    isMonocrome = models.BooleanField()
    paperType = models.CharField(max_length=30)
    coverType = models.CharField(max_length=30)
    page = models.IntegerField()
    size = models.CharField(max_length=30)
    discription = models.TextField()
    pictureUrl = models.URLField()
    
    def __str__(self):
        return self.name

    def getAmount(self):
        return self.price * self.quantity


    


        
        
