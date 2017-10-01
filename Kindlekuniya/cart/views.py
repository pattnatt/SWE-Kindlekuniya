from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

# Create your views here.

from .models import Product

def IndexView(request):
    template_name = 'cart/cart.html'
    items = Product.objects.filter()
    context = {
        'cartItem_list':items,
    }
    
    if request.method == 'POST':
        if request.POST.get('id_of_input'):
            item_id = request.POST.get('id_of_input')
            item_quantity = request.POST.get('quantity_of_item')
            obj = Product.objects.get(pk=item_id)
            obj.quantity = item_quantity
            obj.save()
            return render(request, template_name, context)
        else:
            return HttpResponse("fail2")
    else:
        return render(request, template_name, context )

        
class ResultsView(generic.ListView):
    template_name = 'cart/results.html'
    context_object_name = 'cartItem_list'

    def get_queryset(self):
        objects = Product.objects.filter()
        return objects

