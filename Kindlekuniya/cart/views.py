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
        if request.POST.get('delete_item'):
            item_id = request.POST.get('delete_item')
            for book, quantity in items.items():
                if str(book.product_id) == str(item_id):
                    del request.session[cart_prefix + str(book.product_id)]

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
    
    if request.method == 'POST' and request.session['user_id']  and items:
        if request.POST.get('update_session'):
            book_dict = request.POST.dict()
            for book_id, book_quantity in book_dict.items():                
                if len(str(book_id)) > len('update_cart_'):
                    if str(book_id)[0:len('update_cart_')] == 'update_cart_':
                        product_id=str(book_id)[len('update_cart_'):]
                        request.session[cart_prefix + str(product_id)] = int(book_quantity)                    
            items = get_product_in_cart(request)
            context = {
                'cart_item_list': items,
            }
            #return HttpResponse("ok")
            return render(request, template_name, context)
    
    return render(request, template_name, context)

def get_address(user_id):
    address_list = []
    user = User.objects.get(user_id=user_id)
    for value in Address.objects.filter(user=user):
        default = ''
        if value.address_id == user.default_address:
            default = 'disabled'
        address_list.append([value.address,value.city,value.zipcode,value.address_id,default])
    return address_list


def AddressView(request):
    template_name = 'cart/address_select.html'

    if not request.session.has_key('user_id'):
        return HttpResponseRedirect("/user/login")

    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)

    address_list = get_address(user_id)
    return render(request, template_name,{'address_list':address_list})


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
