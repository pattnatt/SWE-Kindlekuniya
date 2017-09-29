from django.shortcuts import get_object_or_404, render
from django.http import Http404
# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse

from django.http import HttpResponse
from django.template import loader
from .models import Order,OrderItem
from django.views import generic
from django.utils import timezone

from django.core.urlresolvers import reverse


# Create your views here.


class IndexView(generic.ListView):
    template_name = 'history/index.html'
    context_object_name = 'latest_order_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Order.objects.order_by('-date')[:5]