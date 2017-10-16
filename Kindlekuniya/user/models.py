from django.db import models
from django.forms import ModelForm
from passlib.hash import pbkdf2_sha256


class User(models.Model):
    ACTIVE_TYPE = (
        ('AC', 'Active'),
        ('CL', 'Closed'),
        ('WT', 'Waiting'),
    )

    user_id = models.AutoField(primary_key=True, default=None)
    email = models.EmailField(max_length=120, default=None, unique=True)
    firstname = models.CharField(max_length=120, default=None)
    lastname = models.CharField(max_length=120, default=None)
    is_activated = models.CharField(
        max_length=2,
        choices=ACTIVE_TYPE,
        default='WT',
    )
    token = models.CharField(max_length=120, default='0')
    password = models.CharField(max_length=512, default=None)
    phone_number = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.email


class Address(models.Model):
    addr_id = models.AutoField(primary_key=True, default=None)
    user_id = models.IntegerField(default=None)
    addr = models.CharField(max_length=512, default=None)
    city = models.CharField(max_length=128, default=None)
    zip = models.CharField(max_length=5, default=None)

    def __str__(self):
        return self.addr + " " + self.city + " " + self.zip


class AddressModelForm(ModelForm):
    class Meta:
        model = Address
        fields = ['addr', 'city', 'zip']


class SignupModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname', 'password', 'phone_number']
