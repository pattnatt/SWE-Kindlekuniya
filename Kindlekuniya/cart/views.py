from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

from .models import Product

def IndexView(request):
    template_name = 'cart/cart.html'
    context = Product.objects.filter()

    if request.method == 'POST':
        return HttpResponse("success")
    else:
        return render(request, template_name, {'cartItem_list':context} )

        
class ResultsView(generic.ListView):
    template_name = 'cart/results.html'
    context_object_name = 'cartItem_list'

    def get_queryset(self):
        objects = Product.objects.filter()
        return objects




        
