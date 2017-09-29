from django.shortcuts import get_object_or_404, render
from django.http import Http404
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from django.http import HttpResponse
from django.template import loader
from .models import Order,OrderItem,Product
from django.views import generic
from django.utils import timezone

from django.core.urlresolvers import reverse


# Create your views here.


def IndexView(request):
    latest_order_list = Order.objects.order_by('-date')[:]
    d =[]
    product = Product.objects.all()[:];
    #tmp = OrderItem.objects.filter(orderID = 1)
    for order in latest_order_list :
        tmp = OrderItem.objects.filter(orderID = order.orderID)[:]
        d.append(tmp)
    context = {'latest_order_list': latest_order_list , 'd':d , 'product':product}
    return render(request, 'history/index.html', context)