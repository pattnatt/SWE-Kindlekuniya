from django.shortcuts import render
from django.conf import settings
from .forms import TransferForm
from user.models import User
from .models import TransferEntry
from history.models import HistData

def index(request):
    title = 'Transfer Confirmation Form'
    form = TransferForm(request.POST or None, request=request)
    confirm_message = None

    if form.is_valid():
        owner = User.objects.get(user_id=request.session['user_id'])
        order_id = form.cleaned_data["order_id"]
        value = form.cleaned_data["value"]
        transfer_datetime = form.cleaned_data["transfer_datetime"]
        new_entry = TransferEntry(
            owner=owner,
            order_id=order_id,
            value=value,
            transfer_date=transfer_datetime,
        )
        new_entry.save()

        title = "Please stand by"
        confirm_message = "Please wait while we check on your confirmation. Once confirmed, you will be notified"
        form = None

    context = {
        'title': title,
        'form': form,
        'confirm_message': confirm_message,
    }
    return render(request, 'transfer_confirm.html', context)
