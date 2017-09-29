from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, Catagory

def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def detail(request, product_id):
    product = Product.objects.get(id = int(product_id))
    quantityWarning = 20
    context = {
        'product' : product,
        'quantityWarning' : quantityWarning,
    }
    return render(request, 'detail.html', context)

def catagory(request, catagory_id):
    catagory = Catagory.objects.get(id = int(catagory_id))
    products = Product.objects.filter(catagory__id = int(catagory_id))
    context = {
        'catagory' : catagory,
        'products' : products,
    }
    return render(request, 'catagory.html', context)
