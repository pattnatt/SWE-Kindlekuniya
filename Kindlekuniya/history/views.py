from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import HistEntry, HistData
from .tables import HistEntryTable, HistDataTable


def index(request):
    # TODO: change to userID
    histsTable = HistEntryTable(HistEntry.objects.filter(
        orderOwner=request.user
    ))
    histsTable.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(histsTable)
    context = {
        'table': histsTable
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
        'user': str(request.user),
    }
    return render(request, 'hist_details.html', context)
