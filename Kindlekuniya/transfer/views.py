from django.shortcuts import render
from django.conf import settings
from .forms import TransferForm, HistoryForm
from user.models import User
from .models import TransferEntry
from history.models import HistData, HistEntry
from Catalog.models import Product

def index(request):
    title = 'Transfer Confirmation Form'
    form_id = HistoryForm(request.POST or None, request=request)
    form = TransferForm(request.POST or None)
    confirm_message = None
    detail = None
    order = None
    total_sum = 0
    shipping_price = 0
    book_title = {}

    order_id = request.session.get('order_id')
    if not order_id:
        order_id = None

    if form_id.is_valid():
        order_id = form_id.data["order_id"]
        print(order_id)
        request.session['order_id'] = order_id
        detail = HistData.objects.filter(order_id=order_id)
        order = HistEntry.objects.get(order_id=order_id)
        count = 0
        for data in detail:
            total_sum = total_sum + data.tax
            book_title[count] = Product.objects.get(product_id=data.product_id)
            count = count + 1
        shipping_price = order.shipping_price
        total_sum = total_sum + shipping_price

    if form.is_valid() and order_id:
        owner = User.objects.get(user_id=request.session['user_id'])
        value = form.cleaned_data["value"]
        transfer_datetime = form.cleaned_data["transfer_datetime"]
        histEntry = HistEntry.objects.get(order_id=order_id)
        histEntry.status = 'PROCESS'
        histEntry.save()
        new_entry = TransferEntry(
            owner=owner,
            order_id=histEntry,
            value=value,
            transfer_date=transfer_datetime,
        )
        new_entry.save()

        title = "Please stand by"
        confirm_message = "Please wait while we check on your confirmation. Once confirmed, you will be notified"
        form = None
        form_id = None

    context = {
        'title': title,
        'form': form,
        'form_id': form_id,
        'order_id': order_id,
        'confirm_message': confirm_message,
        'detail': detail,
        'total_sum': total_sum,
        'book_title': book_title,
        'shipping_price': shipping_price,
    }
    return render(request, 'transfer_confirm.html', context)
