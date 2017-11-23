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
        'cart_item_list': items,
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
                'cart_item_list': items,
            }
            return render(request, template_name, context)
        elif request.POST.get('delete_item'):
            item_id = request.POST.get('delete_item')
            for book, quantity in items.items():
                if book.id == int(item_id):
                    del request.session[cart_prefix + str(book.id)]

            items = get_product_in_cart(request)
            context = {
                'cart_item_list': items,
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
        'cart_item_list': items,
    }

    if request.method == 'POST' and request.session['user_id'] and items:
        user = User.objects.get(user_id=request.session['user_id'])
        address = Address.objects.get(user_id=int(request.session['user_id']))

        new_entry = HistEntry(user=user, address=address,)
        new_entry.save()

        for product, quantity in items.items():
            new_data = HistData(
                order_id=new_entry,
                product_id=str(product.product_id),
                quantity=quantity,
                sum_price=product.price*quantity,
                tax=product.price*quantity,
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

    if request.session.has_key('user_id') and items:
        user = User.objects.get(user_id=request.session['user_id'])
        address = Address.objects.get(user_id=request.session['user_id'],address_id=user.default_address)

        new_entry = HistEntry(user=user, address=address,)
        new_entry.save()

        for product, quantity in items.items():
            new_data = HistData(
                order_id=new_entry,
                product_id=str(product.product_id),
                quantity=quantity,
                sum_price=float(product.price)*float(quantity),
                tax=float(product.price)*float(quantity),
            )
            new_data.save()
            product.quantity -= int(quantity)
            product.save()
        message = 'Checkout Success'

    context = {
        'message': message,
    }

    return render(request, template_name, context)
