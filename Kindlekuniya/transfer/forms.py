from django import forms
from history.models import HistEntry
from user.models import User


def get_user(request):
    if(request.session.has_key('user_id')):
        return User.objects.get(user_id=request.session['user_id'])
    else:
        return None


class HistoryForm(forms.Form):
    order_id = forms.ModelChoiceField(
        required=True,
        queryset=HistEntry.objects.none(),
        widget=forms.Select(attrs={"onChange": 'this.form.submit()'})
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(HistoryForm, self).__init__(*args, **kwargs)
        self.fields["order_id"].queryset = HistEntry.objects.filter(
            user=get_user(self.request),
            status='WAITING',
            pay_method='CASH',
        )


class TransferForm(forms.Form):
    value = forms.DecimalField(
        required=True,
        max_digits=10
    )
    transfer_datetime = forms.DateTimeField(help_text = "Format : YYYY-MM-DD HH:MM")
