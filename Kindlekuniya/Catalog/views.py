from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, Catagory
from django.conf import settings
from .forms import ProductToCartForm

def index(request):
    context = {
    }
    return render(request, 'index.html', context)

def detail(request, product_id):
    product = Product.objects.get(id = int(product_id))
    quantityWarning = 20
    confirm_message = None
    form = None

    if product.quantity > 0:
        form = ProductToCartForm(request.POST or None, max_order = min(quantityWarning, product.quantity))
        if form.is_valid():
            product_id = product.id
            quantity = int(form.cleaned_data['quantity'])
            confirm_message = "Order " + str(product_id) + " -> " + str(quantity)

    context = {
        'product' : product,
        'quantityWarning' : quantityWarning,
        'form' : form,
        'confirm_message' : confirm_message,
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
