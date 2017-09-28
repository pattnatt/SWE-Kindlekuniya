from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from .models import Product

def cart(request):
    cartItem = Product.objects.filter()
    return render(request ,'cart/cart.html',{'cartItem':cartItem})
