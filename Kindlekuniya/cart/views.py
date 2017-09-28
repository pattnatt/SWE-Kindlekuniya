from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def cart(request):
    return render(request, "./templates/static/cart.html", {})
