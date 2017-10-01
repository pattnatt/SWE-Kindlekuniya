from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import HistEntry, HistData
from .tables import HistEntryTable, HistDataTable
from user.models import User, Address

def get_user(request):
    if(request.session.has_key('userID')):
         return User.objects.get(userID = int(request.session['userID']))
    else:
         return None

def index(request):
    # TODO: change to userID
    histsTable = HistEntryTable(HistEntry.objects.filter(
        user=get_user(request)
    ))
    histsTable.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(histsTable)
    context = {
        'table': histsTable,
        'user' : get_user(request),
    }
    return render(request, 'hist_index.html', context)


def detail(request, orderId):
    histDataTable = HistDataTable(HistData.objects.filter(
        orderId=orderId
    ))
    histEntry = HistEntry.objects.get(orderId=orderId)
    histDataTable.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(histDataTable)
    context = {
        'histDataTable': histDataTable,
        'histEntry': histEntry,
        'error_message': "Specified entry is invalid or not authorised",
        'user': get_user(request),
    }
    return render(request, 'hist_details.html', context)
