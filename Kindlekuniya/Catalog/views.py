from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Product, Catagory
from django.conf import settings
from .forms import ProductToCartForm

cart_prefix = 'CART_PRODUCT_'


def get_product_in_cart(request):
    cart_product = {}
    if request.session.keys():
        for key in request.session.keys():
            if len(str(key)) > len(cart_prefix):
                if str(key)[0:len(cart_prefix)] == cart_prefix:
                    product = Product.objects.get(
                        product_id=str(key)[len(cart_prefix):]
                    )
                    if product:
                        cart_product[product] = request.session[key]
    return cart_product


def index(request):
    products = Product.objects.all().order_by('-created_at')[0:12]
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


def detail(request, product_id):
    product = Product.objects.get(product_id=product_id)
    quantity_warning = 20
    confirm_message = None
    form = None

    if product.quantity > 0:
        form = ProductToCartForm(
            request.POST or None,
            max_order=min(quantity_warning, product.quantity)
        )
        if form.is_valid():
            product_id = product.product_id
            quantity = int(form.cleaned_data['quantity'])
            confirm_message = "Added to cart."
            request.session[cart_prefix + str(product_id)] = quantity

    context = {
        'product': product,
        'quantity_warning': quantity_warning,
        'form': form,
        'confirm_message': confirm_message,
    }
    return render(request, 'detail.html', context)


def catagory(request, catagory_id):
    catagory = Catagory.objects.get(product_id=int(catagory_id))
    products = Product.objects.filter(catagory__id=int(catagory_id))
    context = {
        'catagory': catagory,
        'products': products,
    }
    return render(request, 'catagory.html', context)


def view_cart(request):
    context = {
        'cart_product': get_product_in_cart(request),
    }

    return render(request, 'view_cart.html', context)
