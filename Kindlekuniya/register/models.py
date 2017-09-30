from django.db import models
from django.forms import ModelForm

# Create your models here.
class User(models.Model):
    userID = models.AutoField(primary_key=True,default=None)
    email = models.EmailField(max_length=120,default=None,unique=True)
    firstname = models.CharField(max_length=120,default=None)
    lastname = models.CharField(max_length=120,default=None)
    password = models.CharField(max_length=128,default=None)
    phone_number = models.CharField(max_length=10,default=None)
    def __str__(self):
        return self.email


class signupModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'firstname','lastname','password','phone_number']
