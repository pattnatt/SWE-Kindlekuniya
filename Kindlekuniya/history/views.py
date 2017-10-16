from django.shortcuts import render
from django_tables2 import RequestConfig
from .models import HistEntry, HistData
from .tables import HistEntryTable, HistDataTable
from user.models import User, Address


def get_user(request):
    if(request.session.has_key('user_id')):
        return User.objects.get(user_id=request.session['user_id'])
    else:
        return None


def index(request):
    hists_table = HistEntryTable(HistEntry.objects.filter(
        user=get_user(request)
    ))
    hists_table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(hists_table)
    context = {
        'table': hists_table,
        'user': get_user(request),
    }
    return render(request, 'hist_index.html', context)


def detail(request, order_id):
    hist_data_table = HistDataTable(HistData.objects.filter(
        order_id=order_id
    ))
    hist_entry = HistEntry.objects.get(order_id=order_id)
    hist_data_table.paginate(page=request.GET.get('page', 1), per_page=25)
    RequestConfig(request).configure(hist_data_table)
    context = {
        'hist_data_table': hist_data_table,
        'hist_entry': hist_entry,
        'error_message': "Specified entry is invalid or not authorised for " + str(get_user(request)),
        'user': get_user(request),
        'check': str(hist_entry.user)
    }
    return render(request, 'hist_details.html', context)
