from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

from .models import Product

class IndexView(generic.ListView):
    template_name = 'cart/cart.html'
    context_object_name = 'cartItem_list'

    def get_queryset(self):
        objects = Product.objects.filter()
        return objects

        

class ResultsView(generic.ListView):
    model = Product
    template_name = 'cart/results.html'
    context_object_name = 'cartItem_list'

    def get_queryset(self):
        objects = Product.objects.filter()
        return objects

def btn_sm(request):
    if request.POST['up']:
        id = request.POST.get('up')
        obj = Product.objects.get(pk=id)
        obj.quantity = object.quantity + 1
    if request.POST['down']:
        id = request.POST.get('down')
        obj = Product.objects.get(pk=id)
        obj.quantity = object.quantity - 1

        return render(request, 'cart/cart.html' ,Product.objects.filter())
        
        
