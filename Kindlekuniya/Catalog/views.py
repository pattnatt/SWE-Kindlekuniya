from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, Catagory

def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def detail(request, product_id):
    product = Product.objects.get(id = int(product_id))
    context = {
        'product' : product
    }
    return render(request, 'detail.html', context)

#def show_product_by_catagory(request, catagory_id):
