from django.db import models
from django.forms import ModelForm
from passlib.hash import pbkdf2_sha256
import uuid


class User(models.Model):
    ACTIVE_TYPE = (
        ('AC', 'Active'),
        ('CL', 'Closed'),
        ('WT', 'Waiting'),
    )
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    email = models.EmailField(max_length=120, default=None, unique=True)
    firstname = models.CharField(max_length=120, default=None)
    lastname = models.CharField(max_length=120, default=None)
    is_activated = models.CharField(
        max_length=2,
        choices=ACTIVE_TYPE,
        default='WT'
    )
    reset_password = models.BooleanField(default=False)
    password = models.CharField(max_length=512, default=None)
    phone_number = models.CharField(max_length=10, default=None)

    def __str__(self):
        return self.email

class Address(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    addr = models.CharField(max_length=512, default=None)
    city = models.CharField(max_length=128, default=None)
    zipcode = models.CharField(max_length=5, default=None)

    def __str__(self):
        return self.user.email


class AddressModelForm(ModelForm):
    class Meta:
        model = Address
        fields = ['addr', 'city', 'zipcode','user']


class SignupModelForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'firstname', 'lastname', 'password', 'phone_number']
