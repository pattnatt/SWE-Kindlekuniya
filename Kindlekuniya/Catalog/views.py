from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Product, Catagory, IndexGroup
from django.conf import settings
from .forms import ProductToCartForm

cart_prefix = 'CART_PRODUCT_'
confirm_message_stock = None


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
    index_groups = IndexGroup.objects.filter(is_showing = '1').order_by('-priority')[:]
    context = {
        'products': products,
        'index_groups': index_groups,
    }
    return render(request, 'index.html', context)


def detail(request, product_id):
    global confirm_message_stock
    product = Product.objects.get(product_id=product_id)
    quantity_warning = 20
    confirm_message = None
    warning_message_1 = None
    warning_message_2 = None
    form = None
    current_quantity = 0
    for key in request.session.keys():
        if len(str(key)) > len(cart_prefix):
            if (str(key)[0:len(cart_prefix)] == cart_prefix and
            str(key)[len(cart_prefix):] == product_id):
                current_quantity = request.session[key]
                break

    if confirm_message_stock:
        confirm_message = confirm_message_stock
        confirm_message_stock = None

    if (product.quantity > 0 and current_quantity < quantity_warning
    and current_quantity < product.quantity):
        form = ProductToCartForm(
            request.POST or None,
            max_order=min(quantity_warning - current_quantity, product.quantity
            , product.quantity - current_quantity),
            current_quantity = current_quantity,
        )
        if form.is_valid():
            product_id = product.product_id
            quantity = int(form.cleaned_data['quantity'])
            request.session[cart_prefix + str(product_id)] = quantity + current_quantity

            confirm_message_stock = str(quantity) + " " + str(product.name) + " has been added to your cart."
            return HttpResponseRedirect(reverse("Catalog:detail", args=(product_id,)))
    elif product.quantity > 0 :
        if current_quantity == quantity_warning and product.quantity > quantity_warning :
            warning_message_1 = ("You cannot add more item to your cart because you already have "
            + str(current_quantity) + " items in your cart.")
            warning_message_2 = ("If you want to purchase more than 20 items, please contact us in contact form.")
        elif current_quantity > 1 :
            warning_message_1 = ("You cannot add more item to your cart because you already have "
            + str(current_quantity) + " items in your cart.")
        else :
            warning_message_1 = ("You cannot add more item to your cart because you already have "
            + str(current_quantity) + " item in your cart.")

    context = {
        'product': product,
        'quantity_warning': quantity_warning,
        'current_quantity': current_quantity,
        'form': form,
        'confirm_message': confirm_message,
        'warning_message_1': warning_message_1,
        'warning_message_2': warning_message_2,
    }
    return render(request, 'detail.html', context)


def catagory(request, catagory_id):
    catagory = Catagory.objects.get(id=int(catagory_id))
    products = Product.objects.filter(catagory__id=catagory_id)
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
