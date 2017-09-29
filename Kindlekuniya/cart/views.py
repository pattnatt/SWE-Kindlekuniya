from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

from .models import Product

class IndexView(generic.ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cartItem_list'

    def get_queryset(self):
       
        return Product.objects.filter()



