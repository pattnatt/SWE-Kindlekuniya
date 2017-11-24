from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import Product, Catagory, IndexGroup
from django.conf import settings
from .forms import ProductToCartForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

cart_prefix = 'CART_PRODUCT_'
confirm_message_stock = None

def product_search(request, key_word):
    key_words = key_word.split(' ')
    sqs = SearchQuerySet().all().exclude(content='thisshouldnotmatchanythingintheindex')
    for word in key_words :
        sqs = sqs.filter(content = word)

    context = {
        'key_word' : key_word,
        'sqs': sqs,
    }
    return render(request, 'search/search.html', context)

def product_search_blank(request):
    context = {
    }
    return render(request, 'search/search.html', context)

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

def delete_product_in_cart(request):
    cart_product = []
    if request.session.keys():
        for key in request.session.keys():
            if len(str(key)) > len(cart_prefix):
                if str(key)[0:len(cart_prefix)] == cart_prefix:
                    cart_product.append(key)
        for key in cart_product :
            del request.session[key]

def get_product_count_in_cart(request):
    product_count = 0
    if request.session.keys():
        for key in request.session.keys():
            if len(str(key)) > len(cart_prefix):
                if str(key)[0:len(cart_prefix)] == cart_prefix:
                    product = Product.objects.get(
                        product_id=str(key)[len(cart_prefix):]
                    )
                    if product:
                        product_count += int(request.session[key])
    return product_count

def get_product_weight(request):
    product_weight = 0
    if request.session.keys():
        for key in request.session.keys():
            if len(str(key)) > len(cart_prefix):
                if str(key)[0:len(cart_prefix)] == cart_prefix:
                    product = Product.objects.get(
                        product_id=str(key)[len(cart_prefix):]
                    )
                    if product:
                        product_weight += (float(product.weight) *  float(request.session[key]))
    return product_weight

def get_shipping_price(request):
    product_weight = get_product_weight(request)

    if product_weight < 20 :
        return 45.0 / 1.0
    elif product_weight < 100 :
        return 50.0 / 1.0
    elif product_weight < 250 :
        return 55.0 / 1.0
    elif product_weight < 500 :
        return 65.0 / 1.0
    elif product_weight < 1000 :
        return 80.0 / 1.0
    elif product_weight < 1500 :
        return 95.0 / 1.0
    elif product_weight < 2000 :
        return 110.0 / 1.0
    elif product_weight < 2500 :
        return 140.0 / 1.0
    elif product_weight < 3000 :
        return 155.0 / 1.0
    elif product_weight < 3500 :
        return 180.0 / 1.0
    elif product_weight < 4000 :
        return 200.0 / 1.0
    elif product_weight < 4500 :
        return 220.0 / 1.0
    elif product_weight < 5000 :
        return 240.0 / 1.0
    elif product_weight < 5500 :
        return 265.0 / 1.0
    elif product_weight < 6000 :
        return 280.0 / 1.0
    elif product_weight < 6500 :
        return 305.0 / 1.0
    elif product_weight < 7000 :
        return 330.0 / 1.0
    elif product_weight < 7500 :
        return 355.0 / 1.0
    elif product_weight < 8000 :
        return 380.0 / 1.0
    elif product_weight < 8500 :
        return 410.0 / 1.0
    elif product_weight < 9000 :
        return 440.0 / 1.0
    elif product_weight < 9500 :
        return 470.0 / 1.0
    else :
        return 500.0 / 1.0

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
    key = cart_prefix + product_id
    if key in request.session:
        current_quantity = request.session[key]

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
            request.session[key] = quantity + current_quantity

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
