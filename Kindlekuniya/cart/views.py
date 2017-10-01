from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from Catalog.views import get_product_in_cart, cart_prefix
from Catalog.models import Product
from history.models import HistEntry, HistData
from user.models import User, Address

def IndexView(request):
    template_name = 'cart/cart.html'
    items = get_product_in_cart(request)
    context = {
        'cartItem_list':items,
    }

    if request.method == 'POST':
        if request.POST.get('id_of_input'):
            item_id = request.POST.get('id_of_input')
            item_quantity = request.POST.get('quantity_of_item')
            for book, quantity in items.items():
                if book.id == int(item_id):
                    request.session[cart_prefix + str(book.id)] = item_quantity

            items = get_product_in_cart(request)
            context = {
                'cartItem_list':items,
            }
            return render(request, template_name, context)
        elif request.POST.get('delete_item'):
            item_id = request.POST.get('delete_item')
            for book, quantity in items.items():
                if book.id == int(item_id):
                    del request.session[cart_prefix + str(book.id)]

            items = get_product_in_cart(request)
            context = {
                'cartItem_list':items,
            }
            return render(request, template_name, context)
        else:
            return HttpResponse("fail2")
    else:
        return render(request, template_name, context)


def ResultsView(request):
    template_name = 'cart/results.html'
    items = get_product_in_cart(request)
    context = {
        'cartItem_list':items,
    }

    if request.method == 'POST' and request.session['userID'] and items:
        user = User.objects.get(userID = int(request.session['userID']))
        address = Address.objects.get(userID = int(request.session['userID']))

        new_entry = HistEntry(user=user, address=address,)
        new_entry.save()

        for product, quantity in items.items():
            new_data = HistData(orderId=new_entry, productID=product,
                quantity=quantity, sumPrice=product.price*quantity,
                tax = product.price*quantity,
            )
            new_data.save()
            product.quantity -= quantity
            product.save()
        return render(request, template_name, context)

    return render(request, template_name, context)

def PaymentView(request):
    template_name = 'cart/payment.html'
    items = get_product_in_cart(request)
    message = 'Checkout Failed'

    if request.session.has_key('userID') and items:
        user = User.objects.get(userID = int(request.session['userID']))
        address = Address.objects.get(userID = int(request.session['userID']))

        new_entry = HistEntry(user=user, address=address,)
        new_entry.save()

        for product, quantity in items.items():
            new_data = HistData(orderId=new_entry, productID=product,
                quantity=quantity, sumPrice=float(product.price)*float(quantity),
                tax = float(product.price)*float(quantity),
            )
            new_data.save()
            product.quantity -= int(quantity)
            product.save()
        message = 'Checkout Success'

    context = {
        'message':message,
    }

    return render(request, template_name, context)
